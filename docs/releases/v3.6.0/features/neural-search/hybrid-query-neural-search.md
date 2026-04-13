---
tags:
  - neural-search
---
# Hybrid Query (Neural Search)

## Summary

OpenSearch v3.6.0 delivers a comprehensive set of bug fixes for the hybrid query in the neural-search plugin, addressing critical issues in three areas: field collapse correctness, profiler support, and compound query nesting. These fixes resolve score/ranking inconsistencies when using collapse, empty profiler output with sort/collapse, crashes when hybrid queries are nested inside `function_score`/`constant_score`/`script_score`, and a compilation error from an upstream Lucene API change.

## Details

### What's New in v3.6.0

#### Hybrid Query Collapse Fixes (PRs #1753, #1763, #1787)

The collapse feature for hybrid queries had multiple relevancy and correctness bugs:

- **Score comparison using total score instead of sub-query score**: `HybridSubQueryScorer.score()` returned the sum of all sub-query scores, causing the per-sub-query priority queues in `HybridCollapsingTopDocsCollector` to maintain incorrect ordering. Fixed by introducing `HybridLeafFieldComparator` that wraps the current sub-query score for comparisons.
- **Missing bottom value in priority queue**: After the queue was marked full in `addNewEntry`, the comparator bottom value was not set, preventing correct comparison in `updateExistingEntry`. Fixed by setting the bottom value after adding the bottom entry.
- **Incorrect `GroupPriorityQueue` less-than logic**: The `lessThan` method in `GroupPriorityQueue` produced wrong top-N group selection. Fixed with corrected comparison logic.
- **Unsorted field docs in `getTopDocs`**: Field docs from groups were added to an unsorted list, disrupting normalization. Fixed by introducing a `TreeMap` with sort-criteria-based comparator.
- **Zero-score documents included in results**: Documents with score 0 (not matching a sub-query) were added to the result list, disrupting normalization. Fixed by adding a score==0 check in the collect method.
- **HashMap disrupting document order**: `collapseValueToTopDocMap` used `HashMap` which does not preserve insertion order. Switched to `LinkedHashMap`.
- **Per-group queue architecture replaced with flat queue** (PR #1787): The per-group `FieldValueHitQueue` maps were replaced with a flat per-sub-query `FieldValueHitQueue` of size `numHits`, matching the pattern used by `HybridTopScoreDocCollector`. Collapse deduplication now happens downstream in `CollapseDataCollector`. This also added `minScore` threshold feedback for early document skipping.

#### Profiler Support Fix (PR #1754)

Hybrid query did not work with the OpenSearch profiler (`"profile": true`). The `ProfileScorer` wrapper prevented access to `HybridSubQueryScorer`, causing a `ClassCastException`. Fixed by using reflection to unwrap `ProfileScorer` (and `ProfileScorable`) to build the scorers array from sub-query scorers. This is an isolated code path that does not affect normal (non-profiler) query flow. The profiler now reports `HybridQuery` breakdown with child query timing.

#### Profiler with Sort/Collapse Fix (PR #1794)

When the profiler flag was set for hybrid queries with sort and/or collapse, results were empty. The `HybridLeafCollector` for sort/collapse collectors was missing the explicit call to `populateScoresFromHybridQueryScorer()`, which is required when profiling is enabled. Fixed by adding the call in the sort and collapse collector leaf collectors.

#### Compound Query Nesting Block (PR #1791)

Hybrid query nested inside `function_score`, `constant_score`, or `script_score` caused `index_out_of_bounds_exception` (doc ID = `Integer.MAX_VALUE`) because `FunctionScoreQuery` uses `DefaultBulkScorer` instead of `HybridBulkScorer`, causing DISI/TPI desync. Fixed by adding validation that blocks hybrid queries nested inside these compound query types, including multi-level nesting detection.

#### HybridQueryDocIdStream Upstream Compatibility (PRs #1780, #1786)

Upstream Lucene added an abstract `intoArray(int, int[])` method to `DocIdStream` (via `apache/lucene#15173`), causing a compilation error. PR #1780 added the required override. PR #1786 optimized the `intoArray` implementation to stop iterating when there are more matching docs than `docIds.length`, removed dead code, and added unit tests. Relevancy benchmarks confirmed no regression (NDCG@10 delta within ±0.0006).

## Limitations

- Hybrid query with collapse may still produce slightly different results compared to hybrid query without collapse due to architectural differences in how documents are collected and sent for normalization.
- The profiler fix uses reflection to unwrap `ProfileScorer`, which may need updates if the profiler internals change in future OpenSearch versions.
- Hybrid queries remain blocked from nesting inside `function_score`, `constant_score`, and `script_score` — this is by design, not a temporary limitation.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1753](https://github.com/opensearch-project/neural-search/pull/1753) | Fix hybrid search with collapse relevancy bugs (zero-score filtering, LinkedHashMap, strategy optimization) |  |
| [#1754](https://github.com/opensearch-project/neural-search/pull/1754) | Fix profiler support for hybrid query by unwrapping ProfileScorer | [#1255](https://github.com/opensearch-project/neural-search/issues/1255) |
| [#1763](https://github.com/opensearch-project/neural-search/pull/1763) | Fix missing results and ranking in hybrid query collapse (HybridLeafFieldComparator, bottom value, GroupPriorityQueue, TreeMap sorting) |  |
| [#1780](https://github.com/opensearch-project/neural-search/pull/1780) | Fix HybridQueryDocIdStream by adding intoArray override from upstream Lucene | [#1781](https://github.com/opensearch-project/neural-search/issues/1781) |
| [#1786](https://github.com/opensearch-project/neural-search/pull/1786) | Optimize HybridQueryDocIdStream.intoArray, clean up dead code, add tests | [#1784](https://github.com/opensearch-project/neural-search/issues/1784) |
| [#1787](https://github.com/opensearch-project/neural-search/pull/1787) | Replace per-group collection with flat queue in hybrid query collapse | [#1773](https://github.com/opensearch-project/neural-search/issues/1773), [#1772](https://github.com/opensearch-project/neural-search/issues/1772) |
| [#1791](https://github.com/opensearch-project/neural-search/pull/1791) | Block hybrid query nested inside function_score, constant_score, script_score | [#1788](https://github.com/opensearch-project/neural-search/issues/1788), [#1125](https://github.com/opensearch-project/neural-search/issues/1125) |
| [#1794](https://github.com/opensearch-project/neural-search/pull/1794) | Fix empty profiler data for hybrid query with sort and/or collapse | [#1793](https://github.com/opensearch-project/neural-search/issues/1793) |

### Related Documentation
- [Documentation change request for compound query blocking](https://github.com/opensearch-project/documentation-website/issues/12079)
