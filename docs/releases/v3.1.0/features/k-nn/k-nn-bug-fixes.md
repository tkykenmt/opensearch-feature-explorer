# k-NN Bug Fixes

## Summary

OpenSearch v3.1.0 includes 9 bug fixes for the k-NN plugin addressing critical issues in quantization caching, rescoring for high-dimensional vectors, concurrent search thread safety, nested vector queries with efficient filters, memory cache race conditions, and backward compatibility for mode/compression settings.

## Details

### What's New in v3.1.0

This release focuses on stability and correctness improvements across multiple k-NN subsystems:

1. **Quantization State Cache Fixes** - Corrected cache size calculation and thread safety
2. **High-Dimensional Rescoring** - Fixed rescoring for vectors with dimensions > 1000
3. **Concurrent Search Thread Safety** - Fixed IndexInput thread safety in LuceneOnFaiss
4. **Nested Query Filter Handling** - Corrected efficient filter behavior with nested vectors
5. **Memory Cache Race Conditions** - Fixed deadlock and reference counting issues
6. **Backward Compatibility** - Blocked mode/compression for pre-2.17.0 indices
7. **Graph Loading Performance** - Avoided redundant file operations for loaded graphs
8. **Slice Count Handling** - Honored slice counts for non-quantization cases

### Technical Changes

#### Quantization State Cache Bug Fix (PR #2666)

Two bugs were fixed in the quantization state cache:

| Issue | Description | Impact |
|-------|-------------|--------|
| Scale mismatch | Cache limit used KB but objects were weighted in bytes | Frequent cache eviction (0.005% instead of 5% of JVM) |
| Thread safety | Check-then-update logic not properly guarded | Multiple threads loading meta info from disk unnecessarily |

The fix ensures proper byte-to-KB conversion and adds thread-safe cache updates.

#### Rescoring for High-Dimensional Vectors (PR #2671)

For disk-based vector search with dimensions > 1000, rescoring was not being enabled when not explicitly specified in the query. The default `rescore_enabled` was set to `false` for 32x, 16x, and 8x compression levels, but this default was only applied when dimension > 1000.

**Impact**: Recall improved significantly after the fix:
- Before: recall@k = 0.69, recall@1 = 0.66
- After: recall@k = 0.92, recall@1 = 0.99

#### Concurrent Search Thread Safety (PR #2739)

`IndexInput` in LuceneOnFaiss was being shared across multiple search threads during concurrent search. Since `IndexInput` is not thread-safe, this caused potential data corruption. The fix uses sliced index inputs instead.

#### Nested Vector Query with Efficient Filter (PR #2641)

When using nested vector queries with nested efficient filters, the `parentFilter` was incorrectly set due to double nesting in `NestedQueryBuilder#doToQuery`. The fix preserves the `nestedLevelStack` when parsing efficient nested queries.

**Affected Query Pattern**:
```json
{
  "query": {
    "nested": {
      "path": "test_nested",
      "query": {
        "knn": {
          "test_nested.test_vector": {
            "vector": [5],
            "k": 24,
            "filter": {
              "nested": {
                "path": "test_nested",
                "query": { "term": { "test_nested.parking": "false" } }
              }
            }
          }
        }
      }
    }
  }
}
```

#### Memory Cache Race Condition Fix (PR #2728)

Fixed a race condition between search threads and cache clear operations that could cause:
1. `IndexAllocation-Reference is already closed` exceptions
2. Deadlocks due to unreleased read locks

The race condition sequence:
1. Search thread gets indexAllocation from cache
2. Clear thread triggers async cache eviction
3. Clear thread checks refCount as zero, prepares to close
4. Search thread acquires readLock, tries incRef but fails (already closed)
5. Search thread throws exception without releasing readLock
6. Clear thread waits for writeLock indefinitely (deadlock)

The fix catches the exception and properly releases the lock.

#### Mode/Compression Backward Compatibility (PR #2722)

Blocked usage of `mode` and `compression` parameters on indices created before version 2.17.0. This prevents errors when trying to add new knn_vector fields with these parameters to upgraded indices.

**Error before fix**:
```
Error in std::unique_ptr<faiss::Index> faiss::{anonymous}::index_factory_sub: 
could not parse index string BHNSW16,Flat
```

#### Graph Loading Performance (PR #2719)

Avoided opening graph files when the graph is already loaded in memory. This eliminates unnecessary file operations with locks that were blocking search threads and limiting CPU utilization to ~50% even with 100 search clients.

#### Slice Count for Non-Quantization (PR #2692)

With shard-level query execution, slice count wasn't honored for the core search part in non-quantized cases. The fix reverts to using `KNNQuery` for non-quantized cases.

## Limitations

- Mode and compression parameters cannot be used on indices created before v2.17.0
- Nested efficient filters require specific query structure (filter inside knn, not double-nested)

## Related PRs

| PR | Description |
|----|-------------|
| [#2666](https://github.com/opensearch-project/k-NN/pull/2666) | Fix quantization cache scale and thread safety |
| [#2671](https://github.com/opensearch-project/k-NN/pull/2671) | Fix rescoring for dimensions > 1000 |
| [#2692](https://github.com/opensearch-project/k-NN/pull/2692) | Honor slice count for non-quantization cases |
| [#2702](https://github.com/opensearch-project/k-NN/pull/2702) | Block derived source if index.knn is false |
| [#2719](https://github.com/opensearch-project/k-NN/pull/2719) | Avoid opening graph file if already loaded |
| [#2722](https://github.com/opensearch-project/k-NN/pull/2722) | Block mode/compression for pre-2.17.0 indices |
| [#2728](https://github.com/opensearch-project/k-NN/pull/2728) | Fix RefCount and ClearCache race conditions |
| [#2739](https://github.com/opensearch-project/k-NN/pull/2739) | Fix LuceneOnFaiss to use sliced IndexInput |
| [#2641](https://github.com/opensearch-project/k-NN/pull/2641) | Fix nested vector query with efficient filter |

## References

- [Issue #2665](https://github.com/opensearch-project/k-NN/issues/2665): Quantization cache limit bug
- [Issue #2619](https://github.com/opensearch-project/k-NN/issues/2619): NativeMemoryCacheManager race condition
- [Issue #2708](https://github.com/opensearch-project/k-NN/issues/2708): Faiss 16x on_disk vectors issue
- [Issue #2511](https://github.com/opensearch-project/k-NN/issues/2511): Nested knn query with efficient filter bug
- [k-NN Documentation](https://docs.opensearch.org/3.0/vector-search/api/knn/): k-NN API reference

## Related Feature Report

- [Full k-NN documentation](../../../features/k-nn/k-nn.md)
