---
tags:
  - indexing
  - k-nn
  - performance
  - search
---

# k-NN Bugfixes

## Summary

OpenSearch 2.17.0 includes several important bugfixes for the k-NN plugin, addressing issues related to memory management, search behavior, field validation, binary vector handling, and build infrastructure. These fixes improve stability, prevent node crashes, and enhance the overall reliability of vector search operations.

## Details

### What's New in v2.17.0

This release addresses 8 bugfixes across different areas of the k-NN plugin:

### Technical Changes

#### Memory Management Improvements

**Cache Memory Overflow Fix** ([#2015](https://github.com/opensearch-project/k-NN/pull/2015))

A critical fix that prevents memory overflow caused by cache behavior. The issue stemmed from the Guava cache not immediately cleaning up evictable entries, which could cause native memory to overflow and lead to node failures.

The solution introduces a force evict mechanism that:
- Maintains an additional recency list within the cache manager
- On cache miss with potential overflow, triggers eviction before loading new items
- Works in tandem with `jemalloc` for optimal memory management

| Scenario | Without Fix | With Fix |
|----------|-------------|----------|
| Heavy query load (3 parallel indexes) | Node crashes | Increased latency, no crashes |
| Normal workload | N/A | No performance degradation |

#### Search Behavior Fixes

**Non-Existent Field Filter Handling** ([#1874](https://github.com/opensearch-project/k-NN/pull/1874))

Fixed k-NN query behavior when filters reference non-existent fields:
- Previously returned cryptic "Rewrite first" error (400 status)
- Now returns empty results (0 hits) for filters with only non-existent fields
- Properly handles complex boolean filters with mixed existing/non-existing fields

```json
// Before: Error response
{
  "error": {
    "type": "query_shard_exception",
    "reason": "failed to create query: Rewrite first"
  },
  "status": 400
}

// After: Empty results (graceful handling)
{
  "hits": {
    "total": { "value": 0 },
    "hits": []
  }
}
```

**Script Fields Context Support** ([#1917](https://github.com/opensearch-project/k-NN/pull/1917))

Added `script_fields` context to KNNAllowlist, enabling:
- Use of `cosineSimilarity` function in `script_fields` painless scripts
- Retrieval of k-NN vector values in script field evaluations
- Consistent behavior between `script_score` and `script_fields` contexts

#### Field Validation

**Invalid Character Validation** ([#1936](https://github.com/opensearch-project/k-NN/pull/1936))

Added validation to prevent invalid characters in vector field names that would cause snapshot failures:
- Vector field names are used in physical file names (e.g., `_0_2011_my vector.hnswc`)
- Spaces and other invalid filename characters now throw validation errors at index creation time
- Prevents subsequent snapshot operations from failing with "missing or invalid physical file name" errors

#### Stats and Metrics

**Graph Merge Stats Size Calculation** ([#1844](https://github.com/opensearch-project/k-NN/pull/1844))

Fixed incorrect byte size calculations in the KNNStats API for graph merge statistics:
- Corrected rounding logic for memory usage calculations
- Properly accounts for Java object alignment (8-byte boundaries)
- Ensures accurate reporting of native memory consumption

#### Binary Vector Support

**IVF Training Type Fix** ([#2086](https://github.com/opensearch-project/k-NN/pull/2086))

Fixed incorrect type usage for binary vectors during IVF (Inverted File) training, ensuring proper handling of binary vector data in quantization workflows.

#### Build Infrastructure

**MINGW64 Switch** ([#2090](https://github.com/opensearch-project/k-NN/pull/2090))

Switched from MINGW32 to MINGW64 for Windows builds:
- Fixes incorrect hamming distance calculations on Windows
- Improves recall accuracy for binary vector searches on Windows platform

**Parallel Build** ([#2006](https://github.com/opensearch-project/k-NN/pull/2006))

Parallelized `make` operations to reduce build time when building the plugin or JNI libraries for the first time.

## Limitations

- The cache memory overflow fix works optimally with `jemalloc` enabled; default `malloc` may still experience delays in memory free-up operations
- Field name validation is applied at index creation time; existing indexes with invalid field names are not automatically fixed

## References

### Documentation
- [k-NN Documentation](https://docs.opensearch.org/2.17/search-plugins/knn/index/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#1874](https://github.com/opensearch-project/k-NN/pull/1874) | Corrected search logic for non-existent fields in filter |
| [#1917](https://github.com/opensearch-project/k-NN/pull/1917) | Add script_fields context to KNNAllowlist |
| [#1844](https://github.com/opensearch-project/k-NN/pull/1844) | Fix graph merge stats size calculation |
| [#1936](https://github.com/opensearch-project/k-NN/pull/1936) | Disallow invalid characters in vector field names |
| [#2015](https://github.com/opensearch-project/k-NN/pull/2015) | Fix memory overflow caused by cache behavior |
| [#2086](https://github.com/opensearch-project/k-NN/pull/2086) | Use correct type for binary vector in IVF training |
| [#2090](https://github.com/opensearch-project/k-NN/pull/2090) | Switch MINGW32 to MINGW64 |
| [#2006](https://github.com/opensearch-project/k-NN/pull/2006) | Parallelize make to reduce build time |

### Issues (Design / RFC)
- [Issue #1286](https://github.com/opensearch-project/k-NN/issues/1286): Non-existent field filter error
- [Issue #1789](https://github.com/opensearch-project/k-NN/issues/1789): Graph merge stats calculation bug
- [Issue #1859](https://github.com/opensearch-project/k-NN/issues/1859): Space in field name prevents snapshots
- [Issue #1878](https://github.com/opensearch-project/k-NN/issues/1878): script_fields painless script limitation
- [Issue #1582](https://github.com/opensearch-project/k-NN/issues/1582): Native memory circuit breaker rearchitecture

## Related Feature Report

- [Full feature documentation](../../../features/k-nn/vector-search-k-nn.md)
