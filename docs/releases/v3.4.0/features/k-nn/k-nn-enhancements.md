---
tags:
  - indexing
  - k-nn
  - performance
  - search
---

# k-NN Enhancements

## Summary

OpenSearch v3.4.0 introduces several k-NN plugin enhancements focused on performance optimization and code quality improvements. The key changes include native SIMD-accelerated scoring for FP16 vectors, memory optimization for the `NativeEngines990KnnVectorsReader`, and a refactoring of the MMR rerank processor to avoid thread pool issues.

## Details

### What's New in v3.4.0

#### Native SIMD Scoring for FP16 (PR #2922)

This release introduces native SIMD-accelerated similarity scoring for FP16 (16-bit floating-point) vectors in the Lucene-on-Faiss memory-optimized search path. Previously, FP16 vector scoring required copying bytes to Java heap and converting to FP32 before distance computation, which was significantly slower than native FAISS C++.

The new implementation:
- Extracts memory-mapped pointers from `MemorySegmentIndexInput` and passes them directly to C++
- Leverages Faiss's SIMD-optimized distance calculation functions
- Supports AVX2, AVX512, AVX512-SPR (Sapphire Rapids), and ARM NEON with FP16

```mermaid
graph TB
    subgraph "Previous FP16 Scoring"
        A1[IndexInput] --> B1[Copy to byte array]
        B1 --> C1[Convert FP16 to FP32]
        C1 --> D1[Java Distance Calculation]
    end
    
    subgraph "New Native SIMD Scoring"
        A2[MemorySegmentIndexInput] --> B2[Extract mmap pointer]
        B2 --> C2[Pass to JNI]
        C2 --> D2[Faiss SIMD Distance]
    end
```

#### New Components

| Component | Description |
|-----------|-------------|
| `SimdVectorComputeService` | JNI service for native SIMD similarity computation |
| `NativeRandomVectorScorer` | `RandomVectorScorer` implementation that offloads scoring to native code |
| `MMapVectorValues` | Interface for memory-mapped vector data access |
| `MMapFloatVectorValues` | Float vector values with mmap pointer access |
| `AbstractMemorySegmentAddressExtractor` | Base class for extracting memory segment addresses |
| `opensearchknn_simd` | New native library for SIMD computation |

#### New Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `knn.faiss.avx2.disabled` | Disable AVX2 SIMD optimization | `false` |
| `knn.faiss.avx512.disabled` | Disable AVX512 SIMD optimization | `false` |
| `knn.faiss.avx512_spr.disabled` | Disable AVX512-SPR optimization | `false` |

#### VectorSearcherHolder Optimization (PR #2948)

Removed the per-field `VectorSearcherHolder` map from `NativeEngines990KnnVectorsReader`. The previous implementation incorrectly assumed one reader per segment for all fields, but Lucene creates one `KnnVectorsReader` per field per segment. This caused unnecessary heap usage when multiple vector fields existed.

The fix:
- Changed from `Map<String, VectorSearcherHolder>` to a single `VectorSearcherHolder`
- Reduced memory overhead for indexes with multiple vector fields
- Simplified lazy initialization logic

#### MMR Rerank Refactoring (PR #2968)

Refactored the Maximal Marginal Relevance (MMR) rerank processor to avoid using `parallelStream()`. The common ForkJoinPool used by parallel streams doesn't auto-shutdown, which caused test failures when OpenSearch core started detecting threads not shut down after tests.

Changes:
- Replaced `parallelStream()` with sequential iteration in `extractVectors()`
- Replaced parallel max-finding with sequential loop in `selectHitsWithMMR()`
- Changed `ConcurrentHashMap` to `HashMap` for similarity cache

### Usage Example

Native SIMD scoring is automatically enabled when using memory-optimized search with FP16 vectors:

```json
PUT /my-fp16-index
{
  "settings": {
    "index.knn": true,
    "index.knn.memory_optimized_search": true
  },
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "knn_vector",
        "dimension": 768,
        "method": {
          "name": "hnsw",
          "engine": "faiss",
          "space_type": "l2",
          "parameters": {
            "encoder": {
              "name": "sq",
              "parameters": {
                "type": "fp16"
              }
            }
          }
        }
      }
    }
  }
}
```

### Migration Notes

- Native SIMD scoring is automatically used when conditions are met (FP16 + memory-optimized search + MMapDirectory)
- No configuration changes required for existing FP16 indexes
- SIMD optimization is not supported on Windows

## Limitations

- Native SIMD scoring only supports FP16 vectors (not FP32 or other quantization types yet)
- Only L2 and INNER_PRODUCT space types are supported for native scoring
- Windows is not supported for SIMD optimization
- The V1 implementation uses Faiss's built-in SIMD; bulk SIMD optimization (V2) is planned for future releases

## References

### Documentation
- [Documentation: Faiss 16-bit scalar quantization](https://docs.opensearch.org/3.0/vector-search/optimizing-storage/faiss-16-bit-quantization/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#2922](https://github.com/opensearch-project/k-NN/pull/2922) | Native scoring for FP16 V1 implementation |
| [#2948](https://github.com/opensearch-project/k-NN/pull/2948) | Removed VectorSearchHolders map from NativeEngines990KnnVectorsReader |
| [#2968](https://github.com/opensearch-project/k-NN/pull/2968) | Refactor to not use parallel for MMR rerank |

### Issues (Design / RFC)
- [Issue #2938](https://github.com/opensearch-project/k-NN/issues/2938): Unnecessary heap usage in NativeEngines990KnnVectorsReader
- [RFC Issue #2875](https://github.com/opensearch-project/k-NN/issues/2875): Use SIMD for FP16 in LuceneOnFaiss

## Related Feature Report

- [Full feature documentation](../../../../features/k-nn/lucene-on-faiss.md)
