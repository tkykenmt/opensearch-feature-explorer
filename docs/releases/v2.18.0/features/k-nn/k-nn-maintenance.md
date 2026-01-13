---
tags:
  - domain/search
  - component/server
  - indexing
  - k-nn
  - observability
  - performance
---
# k-NN Maintenance

## Summary

This release includes maintenance updates for the k-NN plugin: Lucene 9.12 codec compatibility, force merge performance optimization, benchmark folder removal, and code refactoring improvements.

## Details

### What's New in v2.18.0

Four maintenance changes improve the k-NN plugin's compatibility, performance, and code quality.

### Technical Changes

#### Lucene 9.12 Codec Update

When Lucene releases new versions, codec imports move to the `backward_codec` package path. This PR updates the k-NN plugin to work with Lucene 9.12:

| Change | Description |
|--------|-------------|
| New `KNN9120Codec` class | Supports Lucene 9.12 vector formats |
| `NativeEngineFieldVectorsWriter` update | Passes `FlatFieldVectorsWriter` to comply with Lucene 9.12 API changes |
| Scalar quantization compress flag | Set to `false` for SQ bits > 4 per Lucene 9.12 requirements |

The Lucene 9.12 API change requires `VectorFieldWriters` using `FlatFieldVectorsWriter` to call the `addValue` function explicitly.

#### Force Merge Performance Optimization

Addressed a ~20% regression in force merge latency for large datasets (cohere-10m) after switching to `NativeEngines990KnnVectorsWriter`.

| Metric | Before (2.17) | After (2.18) |
|--------|---------------|--------------|
| Index segments | 75 | 92 |
| Force merge time | 15.68 min | 12.51 min |
| Force merge segments | 3 | 3 |

The optimization skips unnecessary `KNNVectorValues` recreation when quantization is not needed.

#### Benchmark Folder Removal

Removed the deprecated `benchmarks` folder from the k-NN repository:

- Workloads migrated to [opensearch-benchmark-workloads/vectorsearch](https://github.com/opensearch-project/opensearch-benchmark-workloads/tree/main/vectorsearch)
- Eliminates CVE risks from outdated Python dependencies
- Reduces maintenance burden for unused tooling

#### Code Refactoring

Minor improvements to code quality:

- Updated unit tests to include empty field in multi-field scenarios
- Replaced `IntStream` with collection stream for iterators (index not used)
- Reduced if/else nesting through refactoring

## Limitations

- Lucene codec changes require index rebuild for existing indices to use new codec features
- Force merge optimization only applies to non-quantization scenarios

## References

### Documentation
- [k-NN Documentation](https://docs.opensearch.org/2.18/search-plugins/knn/index/): Official k-NN plugin docs
- [Lucene PR #13538](https://github.com/apache/lucene/pull/13538): FlatFieldVectorsWriter API change

### Pull Requests
| PR | Description |
|----|-------------|
| [#2195](https://github.com/opensearch-project/k-NN/pull/2195) | Fix lucene codec after lucene version bumped to 9.12 |
| [#2133](https://github.com/opensearch-project/k-NN/pull/2133) | Optimize KNNVectorValues creation for non-quantization cases |
| [#2127](https://github.com/opensearch-project/k-NN/pull/2127) | Remove benchmarks folder from k-NN repo |
| [#2167](https://github.com/opensearch-project/k-NN/pull/2167) | Minor refactoring and refactored some unit test |

### Issues (Design / RFC)
- [Issue #2193](https://github.com/opensearch-project/k-NN/issues/2193): Fix k-NN build due to lucene upgrade
- [Issue #2134](https://github.com/opensearch-project/k-NN/issues/2134): Regression in cohere-10m force merge latency

## Related Feature Report

- Full feature documentation
