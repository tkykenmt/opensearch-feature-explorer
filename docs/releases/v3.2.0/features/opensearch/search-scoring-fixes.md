# Search Scoring Fixes

## Summary

This release fixes two bugs related to search result scoring in OpenSearch. The first fix ensures that `max_score` is properly populated in search results when `_score` is used as the primary sort field with additional secondary sort fields. The second fix improves code correctness by using `ScoreDoc` instead of `FieldDoc` when creating `TopScoreDocCollectorManager`, avoiding unnecessary type conversions.

## Details

### What's New in v3.2.0

#### Fix: max_score is null when sorting on score firstly

Prior to this fix, when using `_score` as the primary sort field combined with other secondary sort fields (e.g., `@timestamp`), the `max_score` field in search results would incorrectly return `null`. This was inconsistent with the behavior when sorting only by `_score`, which correctly returned the maximum score.

**Before the fix:**
```json
GET /logs/_search
{
  "query": { "match": { "request": "english/images" } },
  "sort": [
    { "_score": { "order": "desc" } },
    { "@timestamp": { "order": "desc" } }
  ]
}

// Response had max_score: null (incorrect)
{
  "hits": {
    "total": { "value": 10000, "relation": "gte" },
    "max_score": null,
    "hits": [...]
  }
}
```

**After the fix:**
```json
// Response now correctly shows max_score
{
  "hits": {
    "total": { "value": 10000, "relation": "gte" },
    "max_score": 0.47368687,
    "hits": [...]
  }
}
```

#### Fix: Use ScoreDoc instead of FieldDoc for TopScoreDocCollectorManager

When sorting by `_score` with `search_after` pagination, the code was incorrectly using `FieldDoc` when constructing `TopScoreDocCollectorManager`. This has been corrected to use `ScoreDoc` directly, aligning with the Lucene API changes from [apache/lucene#450](https://github.com/apache/lucene/pull/450).

### Technical Changes

#### Modified Components

| Component | Description |
|-----------|-------------|
| `TopDocsCollectorContext` | Core class handling top docs collection and max_score calculation |

#### Code Changes

The fix modifies `TopDocsCollectorContext.java` in two key areas:

1. **SimpleTopDocsCollectorContext constructor**: Added logic to extract `max_score` from the first `FieldDoc` when `_score` is the primary sort field:

```java
} else if (SortField.FIELD_SCORE.equals(sortAndFormats.sort.getSort()[0])) {
    maxScoreSupplier = () -> {
        TopDocs topDocs = topDocsSupplier.get();
        if (topDocs.scoreDocs.length == 0) {
            return Float.NaN;
        } else {
            FieldDoc fieldDoc = (FieldDoc) topDocs.scoreDocs[0];
            return (float) fieldDoc.fields[0];
        }
    };
}
```

2. **newTopDocs method**: Updated to handle `max_score` extraction when sorting by score:

```java
if (Float.isNaN(maxScore) && newTopDocs.scoreDocs.length > 0) {
    float maxScoreFromDoc = maxScore;
    if (sortAndFormats == null) {
        maxScoreFromDoc = newTopDocs.scoreDocs[0].score;
    } else if (SortField.FIELD_SCORE.equals(sortAndFormats.sort.getSort()[0])) {
        maxScoreFromDoc = (float) ((FieldDoc) newTopDocs.scoreDocs[0]).fields[0];
    }
    return new TopDocsAndMaxScore(newTopDocs, maxScoreFromDoc);
}
```

3. **TopScoreDocCollectorManager creation**: Simplified to use `ScoreDoc` directly:

```java
if (searchAfter != null) {
    return new TopScoreDocCollectorManager(numHits, searchAfter, hitCountThreshold);
}
```

### Usage Example

```json
// Search with _score as primary sort and secondary sort field
GET /my-index/_search
{
  "query": {
    "match": {
      "content": "opensearch"
    }
  },
  "sort": [
    { "_score": { "order": "desc" } },
    { "timestamp": { "order": "desc" } }
  ]
}

// Response now correctly includes max_score
{
  "took": 10,
  "hits": {
    "total": { "value": 100, "relation": "eq" },
    "max_score": 5.234,
    "hits": [
      {
        "_index": "my-index",
        "_id": "1",
        "_score": 5.234,
        "sort": [5.234, 1704067200000]
      }
    ]
  }
}
```

### Behavior Notes

- `max_score` is only populated when `_score` is the **primary** (first) sort field in **descending** order
- When `_score` is sorted in ascending order, `max_score` remains `null` (expected behavior)
- The fix works correctly with both standard and concurrent segment search modes

## Limitations

- `max_score` is only computed when `_score` is the first sort field with descending order
- Ascending score sort (`"order": "asc"`) will still return `max_score: null`

## References

### Documentation
- [Search API Documentation](https://docs.opensearch.org/3.2/api-reference/search-apis/search/): Official search API docs
- [Sort Results Documentation](https://docs.opensearch.org/3.2/search-plugins/searching-data/sort/): Sorting documentation
- [Lucene PR #450](https://github.com/apache/lucene/pull/450): Related Lucene API change

### Pull Requests
| PR | Description |
|----|-------------|
| [#18715](https://github.com/opensearch-project/OpenSearch/pull/18715) | Fix max_score is null when sorting on score firstly |
| [#18802](https://github.com/opensearch-project/OpenSearch/pull/18802) | Use ScoreDoc instead of FieldDoc when creating TopScoreDocCollectorManager |

### Issues (Design / RFC)
- [Issue #18714](https://github.com/opensearch-project/OpenSearch/issues/18714): Bug report for max_score null issue

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/search-scoring.md)
