---
tags:
  - k-nn
---
# k-NN Vector Search

## Summary

OpenSearch v3.5.0 brings significant improvements to the k-NN plugin including new features for efficient filtering, SIMD performance optimizations, codec architecture enhancements, and numerous bug fixes for nested queries, memory-optimized search, and warmup operations.

## Details

### What's New in v3.5.0

#### New Features

**Index Setting to Disable Exact Search After ANN with Faiss Efficient Filters**

A new dynamic index setting `index.knn.faiss.efficient_filter.disable_exact_search` allows users to disable the fallback mechanism to exact search after ANN search when using Faiss efficient filters. This provides more control over search behavior and can improve performance in scenarios where exact search fallback is not desired.

**Bulk SIMD V2 Implementation**

A major performance optimization for FP16 vector distance computation using SIMD instructions. The new implementation combines prefetching with a multi-register strategy, calculating distances between a query and multiple vectors simultaneously (4-8 vectors at a time depending on the chip).

Performance improvements:
- 15-31% throughput improvement
- 11-25% latency improvement
- 31-44% reduction in p99 tail latency

#### Enhancements

**Lucene Engine ef_search Parameter Correction**

Fixed recall degradation issues in k-NN search (especially with small k values) by implementing dynamic ef_search resolution for the Lucene engine:
1. Use ef_search from method parameters if specified in query
2. Fall back to index setting (`knn.algo_param.ef_search`)
3. Use default ef_search value based on index version
4. Calculate effective Lucene k as `max(k, luceneK)`
5. Override `mergeLeafResults` to return top K results

**Nested k-NN Query Filter Improvements**

Fixed parent document efficient filtering for nested k-NN queries by ensuring the efficient filter query always operates in parent context and joins down to children. This resolves issues where filter clauses were not correctly scoped to root-parent level.

**Derived Source Enhancements**

- Added regex support for derived source transformer exclusion
- Improved field exclusion handling in source indexing - fields excluded from source now skip derived source logic
- Better handling of non-included fields

**Validation for k Greater Than Total Results**

Updated validation to handle scenarios where a segment has fewer results than k. The system now finds the minimum score from available results rather than failing.

**AdditionalCodecs Integration**

Integrated `AdditionalCodecs` and `EnginePlugin::getAdditionalCodecs` hook to allow additional Codec registration, enabling custom codecs to be used with k-NN, neural-search, and other plugins.

#### Bug Fixes

**Memory-Optimized Search (MOS) Reentrant Search Bug**

Fixed reentrant search when memory-optimized search is enabled for byte index. The fix ensures byte[] query is passed correctly and ByteVectorValues are created properly.

**Warmup Integer Overflow**

Fixed an integer overflow bug in the memory-optimized search warmup functionality that prevented proper warmup of large index files (>2GB). Changed warmup seek to use `long` instead of `int`.

**Warmup Exception Handling**

Added new exception type `WarmupExpectedException` to signify expected warmup behavior, improving error handling and debugging.

**Nested Docs Query with Missing Vector Fields**

Fixed nested docs query when some child documents have no vector field present. The fix creates an Intersection Iterator using VectorValuesIterator and MatchedDocsDISI to ensure only docs with vectors are scored. This resolves EOF exceptions on `.vec` files during:
- expand_nested_docs = true scenarios
- on_disk mode with rescoring
- Filtering cases with exact search fallback

**BinaryCagra Score Conversion**

Fixed a bug in the HNSW Cagra binary path where float-typed Hamming distances were incorrectly interpreted as integers. The patch now correctly converts float values back to integers after search, fixing score calculation while preserving correct ranking.

#### Build and Testing Improvements

**Gradle Build Enhancements**

- Added `validateLibraryUsage` task to prevent `System.loadLibrary` calls outside of `KNNLibraryLoader`
- Added task to generate Gradle task dependency graph for better build visualization

**Integration and BWC Tests**

Added comprehensive tests for indices containing both vector and non-vector documents:
- Tests for deleted doc segments in mixed-field indices
- Tests for segments that never had vector data
- Tests for documents updated to remove vector fields

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `index.knn.faiss.efficient_filter.disable_exact_search` | Disable exact search fallback after ANN with efficient filters | `false` |

## Limitations

- Bulk SIMD V2 ARM Neon L2 implementation has ~2% score error (under investigation)
- BinaryCagra score bug affected score values but not ranking (fixed in this release)

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#3022](https://github.com/opensearch-project/k-NN/pull/3022) | Index setting to disable exact search after ANN Search with Faiss efficient filters | [#2936](https://github.com/opensearch-project/k-NN/issues/2936) |
| [#3075](https://github.com/opensearch-project/k-NN/pull/3075) | Bulk SIMD V2 Implementation | [#2875](https://github.com/opensearch-project/k-NN/issues/2875) |
| [#3037](https://github.com/opensearch-project/k-NN/pull/3037) | Correct ef_search parameter for Lucene engine and reduce to top K | [#2940](https://github.com/opensearch-project/k-NN/issues/2940) |
| [#3049](https://github.com/opensearch-project/k-NN/pull/3049) | Field exclusion in source indexing handling | [#3034](https://github.com/opensearch-project/k-NN/issues/3034) |
| [#2990](https://github.com/opensearch-project/k-NN/pull/2990) | Join filter clauses of nested k-NN queries to root-parent scope | [#2222](https://github.com/opensearch-project/k-NN/issues/2222) |
| [#3031](https://github.com/opensearch-project/k-NN/pull/3031) | Regex for derived source support | [#3029](https://github.com/opensearch-project/k-NN/issues/3029) |
| [#3038](https://github.com/opensearch-project/k-NN/pull/3038) | Update validation for cases when k is greater than total results | [#3017](https://github.com/opensearch-project/k-NN/issues/3017) |
| [#3085](https://github.com/opensearch-project/k-NN/pull/3085) | Include AdditionalCodecs and EnginePlugin::getAdditionalCodecs hook | [OpenSearch#20411](https://github.com/opensearch-project/OpenSearch/pull/20411) |
| [#3067](https://github.com/opensearch-project/k-NN/pull/3067) | Changed warmup seek to use long instead of int to avoid overflow | [#3066](https://github.com/opensearch-project/k-NN/issues/3066) |
| [#3071](https://github.com/opensearch-project/k-NN/pull/3071) | Fix MOS reentrant search bug in byte index | [#3069](https://github.com/opensearch-project/k-NN/issues/3069) |
| [#3051](https://github.com/opensearch-project/k-NN/pull/3051) | Fix nested docs query when some child docs has no vector field present | [#3026](https://github.com/opensearch-project/k-NN/issues/3026) |
| [#2983](https://github.com/opensearch-project/k-NN/pull/2983) | Fix patch to have a valid score conversion for BinaryCagra | - |
| [#3064](https://github.com/opensearch-project/k-NN/pull/3064) | Add IT and bwc test with indices containing both vector and non-vector docs | [#2284](https://github.com/opensearch-project/k-NN/issues/2284) |
| [#3033](https://github.com/opensearch-project/k-NN/pull/3033) | Gradle ban System.loadLibrary | [#3005](https://github.com/opensearch-project/k-NN/issues/3005) |
| [#3032](https://github.com/opensearch-project/k-NN/pull/3032) | Create build graph | - |
| [#3070](https://github.com/opensearch-project/k-NN/pull/3070) | Added new exception type to signify expected warmup behavior | - |
