# Concurrent Segment Search Performance Optimization

## Summary

This release improves concurrent segment search performance by omitting the `MaxScoreCollector` in `SimpleTopDocsCollectorContext` when sorting by score. This optimization reduces search latency by approximately 10% for queries that use score-based sorting with concurrent segment search enabled.

## Details

### What's New in v3.4.0

The optimization extends the existing `MaxScoreCollector` omission logic (previously applied to `CollapsingTopDocsCollectorContext` in v3.3.0) to `SimpleTopDocsCollectorContext`. When concurrent segment search is enabled and the primary sort is by score, the `MaxScoreCollector` is now skipped because the maximum score can be derived directly from the top-scoring document.

### Technical Changes

#### Code Changes

The change introduces a `sortByScore` field in `SimpleTopDocsCollectorContext` to track whether the query sorts by score as the primary sort field:

```java
private final boolean sortByScore;

// In constructor:
this.sortByScore = sortAndFormats == null || SortField.FIELD_SCORE.equals(sortAndFormats.sort.getSort()[0]);
```

This field is then used in three locations to conditionally skip the `MaxScoreCollector`:

1. **Collector creation** - When creating the collector manager, skip `MaxScoreCollector` if sorting by score
2. **newCollector()** - In the concurrent search path, only create `MaxScoreCollector` when `!sortByScore && trackMaxScore`
3. **newTopDocs()** - Use the same condition for determining total hits handling

#### Performance Impact

Benchmark results show approximately 10% improvement in search latency:

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| 50th percentile | 286ms | 257ms | ~10% |
| 90th percentile | 345ms | 282ms | ~18% |
| 99th percentile | 421ms | 331ms | ~21% |

### Usage Example

The optimization is automatic when using concurrent segment search with score-based sorting:

```json
GET my-index/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "message": "search term" } }
      ]
    }
  },
  "sort": [
    { "_score": { "order": "desc" } },
    { "_doc": { "order": "asc" } }
  ]
}
```

With concurrent segment search enabled (`search.concurrent_segment_search.mode: all`), this query will now skip the redundant `MaxScoreCollector`.

## Limitations

- The optimization only applies when `_score` is the primary sort field
- Queries with custom sort orders that don't use score as primary sort will not benefit from this optimization

## References

### Documentation
- [Concurrent Segment Search Documentation](https://docs.opensearch.org/3.0/search-plugins/concurrent-segment-search/): Official documentation

### Blog Posts
- [Introducing concurrent segment search in OpenSearch](https://opensearch.org/blog/concurrent_segment_search/): Introduction blog post
- [Exploring concurrent segment search performance](https://opensearch.org/blog/concurrent-search-follow-up/): Performance analysis blog

### Pull Requests
| PR | Description |
|----|-------------|
| [#19584](https://github.com/opensearch-project/OpenSearch/pull/19584) | Omit maxScoreCollector in SimpleTopDocsCollectorContext when concurrent segment search enabled |
| [#19181](https://github.com/opensearch-project/OpenSearch/pull/19181) | Related: Omit maxScoreCollector for field collapsing when sort by score descending |

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/concurrent-segment-search.md)
