---
tags:
  - indexing
  - neural-search
  - search
---

# SEISMIC Bugfixes

## Summary

OpenSearch v3.4.0 includes several bug fixes for the SEISMIC (Sparse ANN) feature in the neural-search plugin. These fixes address integration test failures in multi-node environments, query handling when method_parameters is not specified, and disk space recovery issues when deleting sparse ANN indices.

## Details

### What's New in v3.4.0

This release focuses on stability and reliability improvements for the SEISMIC sparse ANN feature introduced in v3.3.0.

### Technical Changes

#### Integration Test Fixes for Multi-Node Environments

The `NeuralSparseCacheOperationIT` tests were failing in environments with dedicated master and data nodes. The tests expected memory usage changes on all nodes after calling warmup and clearcache APIs, but master nodes don't run SEISMIC and therefore don't show memory changes.

**Fix**: Modified tests to count only data nodes when verifying memory usage changes:
- Added `SparseTestCommon.getDataNodeCount()` helper method
- Changed assertions from per-node checks to data-node-only checks

#### Sparse ANN Query Method Parameters Handling

When `method_parameters` was not specified in a sparse ANN query, an `unsupported_operation_exception` was thrown. The query worked correctly when `method_parameters` was provided as an empty map `{}`.

**Root Cause**: The `NeuralSparseQueryBuilder` did not initialize a default `SparseAnnQueryBuilder` when method_parameters was omitted.

**Fix**: 
- Initialize `SparseAnnQueryBuilder` with defaults when SEISMIC is supported but method_parameters is not specified
- Handle stream deserialization to create default builder when none is present

```java
// Before: Query without method_parameters failed
GET my-index/_search
{
  "query": {
    "neural_sparse": {
      "sparse_embedding": {
        "query_tokens": { "1012": 1 }
      }
    }
  }
}

// After: Query works with default parameters
```

#### Disk Space Recovery Fix

Disk space was not being recovered after deleting a sparse ANN index. The root cause was improper resource closing in `SparseIndexEventListener`.

**Root Cause**: 
- `SegmentInfos` was not properly closed via `GatedCloseable`
- Closing `MapperService` could negatively impact `indexAnalyzers`

**Fix**: Changed resource management in `beforeIndexRemoved()`:
- Use `GatedCloseable<SegmentInfos>` for proper segment info cleanup
- Remove `MapperService` closing to avoid analyzer side effects

```java
// Before
try (MapperService mapperService = shard.mapperService()) {
    SegmentInfos segmentInfos = shard.getSegmentInfosSnapshot().get();
    // ...
}

// After
try (GatedCloseable<SegmentInfos> snapshot = shard.getSegmentInfosSnapshot()) {
    MapperService mapperService = shard.mapperService();
    SegmentInfos segmentInfos = snapshot.get();
    // ...
}
```

### Usage Example

Sparse ANN queries now work without explicitly specifying method_parameters:

```json
GET my-seismic-index/_search
{
  "query": {
    "neural_sparse": {
      "sparse_embedding": {
        "query_tokens": {
          "1000": 0.1,
          "2000": 0.2
        }
      }
    }
  }
}
```

## Limitations

- The fixes are specific to SEISMIC sparse ANN indices (requires `index.sparse: true`)
- Force merge is still recommended for optimal SEISMIC performance

## References

### Blog Posts
- [SEISMIC Blog](https://opensearch.org/blog/scaling-neural-sparse-search-to-billions-of-vectors-with-approximate-search/): Scaling neural sparse search to billions of vectors

### Pull Requests
| PR | Description |
|----|-------------|
| [#1655](https://github.com/opensearch-project/neural-search/pull/1655) | Fix IT failures in multi-node environments with dedicated master/data nodes |
| [#1674](https://github.com/opensearch-project/neural-search/pull/1674) | Handle non-specified method_parameters in sparse ANN queries |
| [#1683](https://github.com/opensearch-project/neural-search/pull/1683) | Fix disk space recovery when deleting sparse ANN indices |

### Issues (Design / RFC)
- [Issue #1653](https://github.com/opensearch-project/neural-search/issues/1653): IT failures with dedicated master/data nodes
- [Issue #1673](https://github.com/opensearch-project/neural-search/issues/1673): Query error when method_parameters not specified

## Related Feature Report

- [SEISMIC Sparse ANN](../../../features/neural-search/neural-search-seismic-sparse-ann.md)
