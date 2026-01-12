---
tags:
  - indexing
  - k-nn
  - performance
  - search
---

# Lucene On Faiss (Memory Optimized Search)

## Summary

Lucene-on-Faiss is a hybrid vector search approach that enables OpenSearch to perform vector searches on FAISS HNSW indexes without loading the entire index into memory. By combining Lucene's efficient HNSW search algorithm with FAISS's high-performance index format, this feature allows vector search operations in memory-constrained environments while maintaining strong recall performance.

The feature addresses a fundamental limitation of FAISS: the requirement to load entire vector indexes into memory. With Lucene-on-Faiss, users can run vector searches on large FAISS indexes even when available memory is less than the index size.

## Details

### Architecture

```mermaid
graph TB
    subgraph "Query Processing"
        Query[Search Query] --> KNNQueryBuilder
        KNNQueryBuilder --> |Check Settings| MemoryOptCheck{memory_optimized_search?}
    end
    
    subgraph "Memory Optimized Path"
        MemoryOptCheck --> |true| LuceneSearcher[Lucene HnswGraphSearcher]
        LuceneSearcher --> FaissHnswGraph[FaissHnswGraph Adapter]
        FaissHnswGraph --> FaissHNSW[FaissHNSW Structure]
        FaissHNSW --> IndexInput[Lucene IndexInput]
        IndexInput --> |On-demand read| FaissFile[(FAISS Index File)]
    end
    
    subgraph "Traditional Path"
        MemoryOptCheck --> |false| FaissJNI[FAISS JNI Layer]
        FaissJNI --> NativeMemory[Native Memory]
        NativeMemory --> FaissFile
    end
    
    subgraph "Vector Values"
        FaissHnswGraph --> VectorValues[FloatVectorValues / ByteVectorValues]
        VectorValues --> IndexInput
    end
```

### Data Flow

```mermaid
flowchart TB
    subgraph "Index Loading"
        A[Open Index] --> B[Parse FAISS Header]
        B --> C[Mark Section Offsets]
        C --> D[Skip to Next Section]
        D --> E[Store FaissIndex Structure]
    end
    
    subgraph "Search Execution"
        F[Query Vector] --> G[Create VectorSearcher]
        G --> H[Build FaissHnswGraph]
        H --> I[Navigate HNSW Levels]
        I --> J[Fetch Neighbors On-Demand]
        J --> K[Compute Distances]
        K --> L[Collect Top-K Results]
    end
    
    E --> G
```

### Components

| Component | Description |
|-----------|-------------|
| `FaissIndex` | Abstract base class for FAISS index types with partial loading support |
| `FaissIdMapIndex` | Handles ID mapping between internal vector IDs and Lucene document IDs |
| `FaissHNSWIndex` | Represents FAISS HNSW index with flat vector storage |
| `FaissHNSW` | HNSW graph structure with neighbor lists and level information |
| `FaissHnswGraph` | Lucene `HnswGraph` adapter that wraps `FaissHNSW` |
| `FaissMemoryOptimizedSearcher` | `VectorSearcher` implementation for FAISS indexes |
| `FaissMemoryOptimizedSearcherFactory` | Factory for creating memory-optimized searchers |
| `FaissIndexFloatFlat` | Float vector storage (L2 and Inner Product) |
| `FaissIndexScalarQuantizedFlat` | Scalar quantized vector storage (8-bit, FP16) |
| `FaissSection` | Represents a section in FAISS index file with offset and size |
| `MemoryOptimizedSearchSupportSpec` | Determines if a field configuration supports memory-optimized search |
| `VectorSearcher` | Interface for vector search compatible with Lucene's search API |
| `VectorSearcherFactory` | Factory interface for creating `VectorSearcher` instances |
| `SimdVectorComputeService` | JNI service for native SIMD similarity computation (v3.4.0+) |
| `NativeRandomVectorScorer` | `RandomVectorScorer` that offloads scoring to native SIMD code (v3.4.0+) |
| `MMapVectorValues` | Interface for memory-mapped vector data access (v3.4.0+) |
| `MMapFloatVectorValues` | Float vector values with mmap pointer access (v3.4.0+) |

### Configuration

| Setting | Description | Default | Scope |
|---------|-------------|---------|-------|
| `index.knn.memory_optimized_search` | Enable memory-optimized search for FAISS indexes | `false` | Index |

### Supported Configurations

| Engine | Method | Space Types | Vector Types | Encoders |
|--------|--------|-------------|--------------|----------|
| FAISS | HNSW | L2, INNER_PRODUCT | FLOAT, BYTE | flat, sq |

### Usage Example

#### Enable via Index Setting

```json
PUT /my-vector-index
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
            "ef_construction": 128,
            "m": 16
          }
        }
      }
    }
  }
}
```

#### Enable via On-Disk Mode

```json
PUT /my-vector-index
{
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "knn_vector",
        "dimension": 768,
        "mode": "on_disk",
        "compression_level": "1x"
      }
    }
  }
}
```

#### Search Query

```json
GET /my-vector-index/_search
{
  "query": {
    "knn": {
      "my_vector": {
        "vector": [0.1, 0.2, ...],
        "k": 10
      }
    }
  }
}
```

### Performance Characteristics

Based on benchmarks with Cohere-10M dataset:

| Configuration | QPS Change vs FAISS C++ | Recall Change |
|---------------|-------------------------|---------------|
| FP32 (k=30) | -9.56% | +0.14% |
| FP16 (k=30) | -40.43% | +0.31% |
| 8x quantization (k=30) | +76.85% | -2.76% |
| 16x quantization (k=30) | +85.10% | -3.48% |
| 32x quantization (k=30) | +51.52% | -4.52% |
| 32x quantization (k=100) | +107.27% | -1.72% |

Key observations:
- For quantized indexes, Lucene-on-Faiss can achieve up to 2x throughput improvement
- Slight recall reduction (up to 4.5%) due to Lucene's early termination logic
- Enables running large indexes (e.g., 30GB) on memory-constrained instances (e.g., 8GB RAM)

### Asymmetric Distance Computation (ADC) Support

Starting in v3.2.0, Lucene-on-Faiss supports Asymmetric Distance Computation (ADC) for binary-quantized indexes. ADC improves recall by preserving query vectors in full precision while comparing against binary-quantized document vectors.

#### How ADC Works

1. **Document Quantization**: Documents are binary-quantized (32x compression) during indexing
2. **Centroid Computation**: Per-dimension means are computed for values quantized to 0 and 1
3. **Query Transformation**: At search time, query vectors are rescaled using the centroids but kept in full precision
4. **Asymmetric Distance**: Distance is computed between the full-precision query and binary document vectors

The rescaling formula transforms each query dimension `q_d` to:
```
q'_d = (q_d - below_mean_d) / (above_mean_d - below_mean_d)
```

#### ADC Configuration Example

```json
PUT /my-vector-index
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
              "name": "binary",
              "parameters": {
                "bits": 1,
                "enable_adc": true
              }
            }
          }
        }
      }
    }
  }
}
```

#### ADC Components

| Component | Description |
|-----------|-------------|
| `ADCFlatVectorsScorer` | Scorer for asymmetric distance computation between float queries and byte vectors |
| `FlatVectorsScorerProvider` | Extended factory to return ADC-aware scorers based on space type |

## Limitations

- **Engine Support**: Only FAISS engine is supported
- **Method Support**: Only HNSW algorithm is supported; IVF and PQ are not yet supported
- **Vector Types**: Only FLOAT and BYTE data types are supported
- **Space Types**: Only L2, INNER_PRODUCT, and COSINESIMIL are supported
- **ADC Limitations**: ADC only supports 1-bit binary quantization; byte vector queries are not supported with ADC
- **Result Consistency**: Results may differ slightly from full-memory FAISS search due to differences in loop termination conditions between Lucene and FAISS

## Change History

- **v3.4.0** (2026-01-14): Added native SIMD scoring for FP16 vectors, VectorSearcherHolder memory optimization
- **v3.2.0** (2026-01-14): Added ADC support for binary-quantized indexes
- **v3.0.0** (2025-05-06): Initial implementation with HNSW support for FAISS engine

## Related Features
- [Neural Search](../neural-search/agentic-search.md)
- [Search Relevance](../search-relevance/ci-tests.md)

## References

### Documentation
- [Documentation: Memory-optimized vectors](https://docs.opensearch.org/3.0/field-types/supported-field-types/knn-memory-optimized/)
- [Documentation: Faiss 16-bit scalar quantization](https://docs.opensearch.org/3.0/vector-search/optimizing-storage/faiss-16-bit-quantization/)

### Blog Posts
- [Blog: Lucene-on-Faiss](https://opensearch.org/blog/lucene-on-faiss-powering-opensearchs-high-performance-memory-efficient-vector-search/)
- [Blog: Asymmetric Distance Computation](https://opensearch.org/blog/asymmetric-distance-computation-for-binary-quantization/)

### Pull Requests
| Version | PR | Description | Related Issue |
|---------|-----|-------------|---------------|
| v3.4.0 | [#2922](https://github.com/opensearch-project/k-NN/pull/2922) | Native SIMD scoring for FP16 | [#2875](https://github.com/opensearch-project/k-NN/issues/2875) |
| v3.4.0 | [#2948](https://github.com/opensearch-project/k-NN/pull/2948) | VectorSearcherHolder memory optimization | [#2938](https://github.com/opensearch-project/k-NN/issues/2938) |
| v3.2.0 | [#2781](https://github.com/opensearch-project/k-NN/pull/2781) | ADC support for Lucene-on-Faiss | [#2714](https://github.com/opensearch-project/k-NN/issues/2714) |
| v3.0.0 | [#2630](https://github.com/opensearch-project/k-NN/pull/2630) | Main implementation (10 sub-PRs combined) | [#2401](https://github.com/opensearch-project/k-NN/issues/2401) |
| v3.0.0 | [#2581](https://github.com/opensearch-project/k-NN/pull/2581) | Building blocks for memory optimized search | [#2401](https://github.com/opensearch-project/k-NN/issues/2401) |
| v3.0.0 | [#2590](https://github.com/opensearch-project/k-NN/pull/2590) | IxMp section loading logic | [#2401](https://github.com/opensearch-project/k-NN/issues/2401) |
| v3.0.0 | [#2594](https://github.com/opensearch-project/k-NN/pull/2594) | FaissHNSW graph implementation | [#2401](https://github.com/opensearch-project/k-NN/issues/2401) |
| v3.0.0 | [#2598](https://github.com/opensearch-project/k-NN/pull/2598) | FAISS float flat index | [#2401](https://github.com/opensearch-project/k-NN/issues/2401) |
| v3.0.0 | [#2604](https://github.com/opensearch-project/k-NN/pull/2604) | FaissIndexScalarQuantizedFlat | [#2401](https://github.com/opensearch-project/k-NN/issues/2401) |
| v3.0.0 | [#2618](https://github.com/opensearch-project/k-NN/pull/2618) | Byte index, FP16 index decoding | [#2401](https://github.com/opensearch-project/k-NN/issues/2401) |
| v3.0.0 | [#2608](https://github.com/opensearch-project/k-NN/pull/2608) | VectorReader integration | [#2401](https://github.com/opensearch-project/k-NN/issues/2401) |
| v3.0.0 | [#2616](https://github.com/opensearch-project/k-NN/pull/2616) | Index setting implementation | [#2401](https://github.com/opensearch-project/k-NN/issues/2401) |
| v3.0.0 | [#2621](https://github.com/opensearch-project/k-NN/pull/2621) | CAGRA index partial loading | [#2401](https://github.com/opensearch-project/k-NN/issues/2401) |
| v3.0.0 | [#2609](https://github.com/opensearch-project/k-NN/pull/2609) | Monotonic integer encoding for HNSW | [#2401](https://github.com/opensearch-project/k-NN/issues/2401) |

### Issues (Design / RFC)
- [RFC Issue #2401](https://github.com/opensearch-project/k-NN/issues/2401): Partial loading with FAISS engine - detailed design document
- [RFC Issue #2714](https://github.com/opensearch-project/k-NN/issues/2714): ADC and Random Rotation for binary quantization
- [RFC Issue #2875](https://github.com/opensearch-project/k-NN/issues/2875): Use SIMD for FP16 in LuceneOnFaiss
- [Issue #2938](https://github.com/opensearch-project/k-NN/issues/2938): VectorSearcherHolder memory optimization
