---
tags:
  - opensearch
---
# Terms Aggregation Performance

## Summary

Fixed a performance regression in terms aggregation on high-cardinality fields. The `tryCollectFromTermFrequencies` optimization in `GlobalOrdinalsStringTermsAggregator`, originally introduced in PR #11643, caused severe slowdowns on fields with millions of unique values (e.g., ClickBench URL field with 10M+ unique terms). Two fixes were applied: a cardinality threshold guard via a new cluster setting, and a replacement of the inefficient leap-frogging algorithm with direct segment-to-global ordinal mapping.

## Details

### What's New in v3.6.0

#### Problem

The `tryCollectFromTermFrequencies` method used a leap-frogging algorithm that iterated through all global ordinals to match them with segment terms. For high-cardinality fields (e.g., 10M unique values across 10 segments), this resulted in 100M+ global ordinal iterations with expensive `BytesRef` fetching and comparison per segment.

#### Fix 1: Max Cardinality Setting (PR #20623)

Introduced a new dynamic cluster setting `search.aggregations.terms.max_precompute_cardinality` that guards the `tryCollectFromTermFrequencies` optimization. When a segment's term count exceeds this threshold, the optimization is skipped and standard document collection is used instead.

| Setting | Description | Default |
|---------|-------------|---------|
| `search.aggregations.terms.max_precompute_cardinality` | Maximum segment cardinality for term frequency precomputation | `30000` |

The setting also affects the streaming aggregation planner: match-all queries with cardinality above the threshold are no longer forced into the traditional (non-streaming) aggregator path, allowing the streaming aggregator to handle high-cardinality cases.

#### Fix 2: Segment-to-Global Ordinal Mapping (PR #20683)

Replaced the leap-frogging algorithm with direct segment-to-global ordinal mapping using `valuesSource.globalOrdinalsMapping(ctx)`. Instead of iterating both segment and global ordinal term enums and comparing `BytesRef` values, the new approach:

1. Iterates only over segment ordinals (0 to `termCount`)
2. Maps each segment ordinal to its global ordinal via `LongUnaryOperator`
3. Checks acceptance and increments bucket count

This reduces the iteration from O(globalTerms) to O(segmentTerms) per segment, eliminating unnecessary `BytesRef` comparisons entirely.

The `LowCardinality` inner class was also updated to use global ordinals directly in the callback rather than maintaining a separate mapping state.

### Technical Changes

Key files modified:

- `GlobalOrdinalsStringTermsAggregator.java` — Replaced leap-frogging with `globalOrdinalsMapping`, updated `LowCardinality` precomputation
- `SearchService.java` — Added `TERMS_AGGREGATION_MAX_PRECOMPUTE_CARDINALITY` setting
- `SearchContext.java` / `DefaultSearchContext.java` — Added `termsAggregationMaxPrecomputeCardinality()` accessor
- `ClusterSettings.java` — Registered the new setting
- `TermsAggregatorFactory.java` — Updated streaming aggregation planner to respect cardinality threshold

## Limitations

- The default threshold of 30,000 is based on empirical testing with the big5 benchmark (26K cardinality field). Workloads with different characteristics may benefit from tuning this value.
- The setting is cluster-scoped (`NodeScope`, `Dynamic`), not per-index.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#20623](https://github.com/opensearch-project/OpenSearch/pull/20623) | Fix terms aggregation performance regression with max cardinality setting | |
| [#20683](https://github.com/opensearch-project/OpenSearch/pull/20683) | Fix terms aggregation using segment-to-global ordinals mapping | [#20626](https://github.com/opensearch-project/OpenSearch/issues/20626) |

### Issues
- [#20626](https://github.com/opensearch-project/OpenSearch/issues/20626): Performance regression in terms aggregation with match_all queries
