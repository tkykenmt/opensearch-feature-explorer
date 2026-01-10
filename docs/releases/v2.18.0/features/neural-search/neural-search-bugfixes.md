# Neural Search Bugfixes

## Summary

This release fixes a bug in hybrid query where nested aggregations returned incorrect document order. The issue affected hybrid queries combined with deeply nested aggregations since v2.15, causing aggregation results to not correspond to the provided aggregation rules.

## Details

### What's New in v2.18.0

Fixed incorrect document order for nested aggregations in hybrid query. The bug was caused by the `HybridQueryScorer` getting document IDs and scorers from a pre-sorted collection of doc iterators, which did not work correctly for deeply nested aggregations because the order could change dynamically.

### Technical Changes

#### Root Cause

The `HybridQueryScorer.score()` method was iterating over `subScorersPQ` (a priority queue) directly, which maintained a pre-sorted order. However, for nested aggregations, the document order can change dynamically during aggregation processing, causing incorrect results.

#### Fix Implementation

The fix modifies the `score()` method in `HybridQueryScorer` to use `getSubMatches()` which returns the correct list of matching scorers for the current document:

```java
@Override
public float score() throws IOException {
    return score(getSubMatches());
}

private float score(DisiWrapper topList) throws IOException {
    float totalScore = 0.0f;
    for (DisiWrapper disiWrapper = topList; disiWrapper != null; disiWrapper = disiWrapper.next) {
        // check if this doc has match in the subQuery. If not, add score as 0.0 and continue
        if (disiWrapper.scorer.docID() == DocIdSetIterator.NO_MORE_DOCS) {
            continue;
        }
        // ... score calculation
    }
    return totalScore;
}
```

#### Changed Files

| File | Change |
|------|--------|
| `HybridQueryScorer.java` | Modified `score()` to use `getSubMatches()` for correct document ordering |
| `HybridQueryAggregationsIT.java` | Added integration tests for nested aggregations with hybrid query |
| `BaseNeuralSearchIT.java` | Added `bulkIngest()` helper and extended `buildIndexConfiguration()` |
| `TestUtils.java` | Added overloaded `assertHitResultsFromQuery()` for total count validation |
| `ingest_bulk.json` | Test data for nested aggregation scenarios |

### Usage Example

Hybrid query with nested aggregations now returns correct results:

```json
GET /my-nlp-index/_search?search_pipeline=nlp-search-pipeline
{
  "aggs": {
    "unique_names": {
      "terms": {
        "field": "actor",
        "size": 10,
        "order": { "max_score": "desc" }
      },
      "aggs": {
        "top_doc": {
          "top_hits": {
            "size": 1,
            "sort": [{ "_score": { "order": "desc" } }]
          }
        },
        "max_score": {
          "max": { "script": { "source": "_score" } }
        }
      }
    }
  },
  "query": {
    "hybrid": {
      "queries": [
        { "match": { "actor": "anil" } },
        { "range": { "imdb": { "gte": 1.0, "lte": 10.0 } } }
      ]
    }
  }
}
```

### Migration Notes

No migration required. This is a bug fix that restores correct behavior for hybrid queries with nested aggregations.

## Limitations

- Aggregation scores in the response are not normalized (expected behavior)
- The fix applies to all nested aggregation scenarios with hybrid query

## Related PRs

| PR | Description |
|----|-------------|
| [#956](https://github.com/opensearch-project/neural-search/pull/956) | Fixed incorrect document order for nested aggregations in hybrid query |

## References

- [Issue #955](https://github.com/opensearch-project/neural-search/issues/955): Bug report for incorrect nested aggregation results
- [Hybrid Search Documentation](https://docs.opensearch.org/2.18/search-plugins/hybrid-search/)
- [Nested Aggregations](https://docs.opensearch.org/2.18/aggregations/bucket/nested/)

## Related Feature Report

- [Full feature documentation](../../../../features/neural-search/hybrid-query.md)
