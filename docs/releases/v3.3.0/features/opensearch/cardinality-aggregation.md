---
tags:
  - performance
  - search
---

# Cardinality Aggregation Pruning Fix

## Summary

This release fixes a performance regression in the cardinality aggregation pruning optimization that was introduced after merging Lucene 10.3.0. The fix replaces the use of `BulkScorer` with a custom self-collecting approach to avoid incorrect document matching caused by Lucene's `DenseConjunctionBulkCollector` `scoreWindow` logic.

## Details

### What's New in v3.3.0

The cardinality aggregation's dynamic pruning optimization experienced a severe performance regression (from ~5ms to ~5s on the big5 benchmark's `cardinality-low` query) after the Lucene 10.3.0 upgrade. This fix restores the expected performance by implementing self-collection instead of relying on Lucene's `BulkScorer`.

### Technical Changes

#### Problem

The `DenseConjunctionBulkCollector` in Lucene 10.3.0 was matching too many documents due to its `scoreWindow` logic, causing the pruning optimization to process far more documents than necessary.

#### Solution

The fix replaces `BulkScorer` with a custom `bulkCollect` method that:
1. Uses `Scorer` directly instead of `BulkScorer`
2. Implements manual iteration with `DocIdSetIterator`
3. Properly handles the competitive iterator for pruning

```java
// Before (problematic)
BulkScorer scorer = weight.bulkScorer(ctx);
scorer.score(pruningCollector, liveDocs, 0, DocIdSetIterator.NO_MORE_DOCS);

// After (fixed)
Scorer scorer = weight.scorer(ctx);
pruningCollector.setScorer(scorer);
DocIdSetIterator iterator = scorer.iterator();
bulkCollect(ctx.reader().getLiveDocs(), iterator, pruningCollector);
```

#### New bulkCollect Method

```java
private void bulkCollect(Bits acceptDocs, DocIdSetIterator iterator, 
                         Collector pruningCollector) throws IOException {
    DocIdSetIterator competitiveIterator = pruningCollector.competitiveIterator();
    int doc = iterator.nextDoc();
    while (doc < DocIdSetIterator.NO_MORE_DOCS) {
        if (competitiveIterator.docID() < doc) {
            int competitiveNext = competitiveIterator.advance(doc);
            if (competitiveNext != doc) {
                doc = iterator.advance(competitiveNext);
                continue;
            }
        }
        if ((acceptDocs == null || acceptDocs.get(doc))) {
            pruningCollector.collect(doc);
        }
        doc = iterator.nextDoc();
    }
}
```

### Scope

This optimization only applies when:
- Running a cardinality aggregation without sub-aggregations
- The pruning optimization is enabled (controlled by `search.aggregations.cardinality.pruning_threshold`)
- The field's term count is below the pruning threshold

### Fallback Option

If issues persist, the pruning optimization can be disabled via index setting:
```json
PUT /_cluster/settings
{
  "persistent": {
    "search.aggregations.cardinality.pruning_threshold": 0
  }
}
```

## Limitations

- The fix is specific to the interaction between cardinality aggregation pruning and Lucene 10.3.0's `BulkScorer` behavior
- A Lucene issue will be raised to track the underlying `DenseConjunctionBulkCollector` behavior

## References

### Documentation
- [Cardinality Aggregation Documentation](https://docs.opensearch.org/3.0/aggregations/metric/cardinality/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#19473](https://github.com/opensearch-project/OpenSearch/pull/19473) | Fix cardinality agg pruning optimization by self collecting |

### Issues (Design / RFC)
- [Issue #19367](https://github.com/opensearch-project/OpenSearch/issues/19367): big5.cardinality-low aggs regression after merging Lucene 10.3.0

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/cardinality-aggregation.md)
