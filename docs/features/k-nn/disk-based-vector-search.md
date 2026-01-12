# Disk-Based Vector Search

## Summary

Disk-based vector search is a k-NN feature that enables efficient vector search in low-memory environments by using binary quantization to compress vectors and storing full-precision vectors on disk. The feature uses a two-phase search approach: first searching a compressed in-memory index, then rescoring results using full-precision vectors loaded from disk. This provides significant memory savings (up to 32x compression) while maintaining high recall through automatic rescoring.

## Details

### Architecture

```mermaid
graph TB
    subgraph "Index Creation"
        User[User] --> |"mode: on_disk"| Resolver[ModeBasedResolver]
        Resolver --> |"Selects defaults"| Config[Index Configuration]
        Config --> |"engine: faiss<br/>method: hnsw<br/>compression: 32x"| Index[k-NN Index]
    end
    
    subgraph "Ingestion Flow"
        Vectors[Input Vectors<br/>float32] --> Quantizer[Binary Quantizer]
        Quantizer --> QIndex[Quantized Index<br/>In Memory]
        Vectors --> FPStore[Full Precision Store<br/>On Disk]
    end
    
    subgraph "Two-Phase Search"
        Query[Query Vector] --> Phase1["Phase 1: ANN Search<br/>(Quantized Index)"]
        Phase1 --> |"k × oversample_factor"| Candidates[Candidates]
        Candidates --> Phase2["Phase 2: Rescore<br/>(Full Precision)"]
        FPStore --> Phase2
        Phase2 --> |"Top k"| Results[Results]
    end
```

### Data Flow

```mermaid
flowchart TB
    subgraph Ingestion
        V[Vectors] --> BQ[Binary Quantization]
        BQ --> |"1 bit per dimension"| QI[Quantized Index]
        V --> |"Full precision"| Disk[(Disk Storage)]
    end
    
    subgraph Search
        Q[Query] --> ANN[ANN Search]
        QI --> ANN
        ANN --> |"Oversampled results"| RS[Rescore]
        Disk --> RS
        RS --> R[Final Results]
    end
```

### Components

| Component | Description |
|-----------|-------------|
| `ModeBasedResolver` | Resolves KNN method context based on Mode and CompressionLevel, selecting appropriate engine, method, and parameters |
| `Mode` | Enum defining workload modes: `ON_DISK`, `IN_MEMORY`, `NOT_CONFIGURED` |
| `CompressionLevel` | Enum defining compression levels with associated encoders and rescore contexts |
| `RescoreContext` | Contains oversample factor and manages rescoring behavior |
| `KNNVectorFieldMapper` | Extended to support mode and compression_level parameters |
| `KNNQueryBuilder` | Integrated with rescore context resolution for automatic rescoring |

### Configuration

| Setting | Description | Default |
|---------|-------------|--------|
| `mode` | Workload mode for the vector field | Not configured |
| `compression_level` | Compression ratio (x1, x2, x4, x8, x16, x32) | `32x` for on_disk mode |
| `space_type` | Distance function (l2, innerproduct, cosine) | l2 |
| `rescore.oversample_factor` | Multiplier for candidate retrieval during search | Based on compression level |

#### Compression Level Details

| Level | Encoder | Memory Reduction | Default Oversample Factor |
|-------|---------|------------------|---------------------------|
| x1 | None | 1x | 1.0 |
| x2 | FP16 Scalar Quantization | 2x | 1.0 |
| x4 | Lucene SQ | 4x | 1.0 |
| x8 | QFrame bit encoder | 8x | 1.5 |
| x16 | QFrame bit encoder | 16x | 2.0 |
| x32 | Binary Quantization | 32x | 3.0 |

### Usage Example

#### Basic On-Disk Index

```json
PUT my-vector-index
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "my_vector_field": {
        "type": "knn_vector",
        "dimension": 768,
        "space_type": "innerproduct",
        "mode": "on_disk"
      }
    }
  }
}
```

#### Fine-Tuned Configuration

```json
PUT my-vector-index
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "my_vector_field": {
        "type": "knn_vector",
        "dimension": 768,
        "space_type": "innerproduct",
        "mode": "on_disk",
        "compression_level": "16x",
        "method": {
          "params": {
            "ef_construction": 512
          }
        }
      }
    }
  }
}
```

#### Search with Custom Rescore

```json
GET my-vector-index/_search
{
  "query": {
    "knn": {
      "my_vector_field": {
        "vector": [1.5, 2.5, 3.5, ...],
        "k": 10,
        "method_parameters": {
          "ef_search": 512
        },
        "rescore": {
          "oversample_factor": 10.0
        }
      }
    }
  }
}
```

### Binary Quantization Algorithm

The online binary quantization works as follows:

1. **Calculate mean per dimension**: For each dimension j, compute the mean across all vectors
2. **Quantize vectors**: For each dimension, if the value exceeds the mean, set to 1; otherwise set to 0
3. **Store as bits**: Pack 8 dimensions into 1 byte, achieving 32x compression for float32 vectors

This approach requires no pretraining and can begin ingestion immediately.

## Limitations

- Only works with `float` data type
- Radial search is not supported
- Performance varies by dataset (text embeddings generally perform better than image embeddings)
- Higher compression levels may require tuning oversample_factor for optimal recall
- Training support for mode/compression has limitations with the quantization framework

## Change History

- **v2.19.0**: Added method parameter override support for training-based indices
- **v2.18.0**: Bug fixes for segments without vector fields
- **v2.17.0**: Initial implementation with mode/compression parameters, binary quantization, and two-phase rescoring

## References

### Documentation
- [Documentation: Disk-based vector search](https://docs.opensearch.org/latest/search-plugins/knn/disk-based-vector-search/)
- [Documentation: k-NN vector quantization](https://docs.opensearch.org/latest/search-plugins/knn/knn-vector-quantization/)

### Blog Posts
- [Blog: Reduce costs with disk-based vector search](https://opensearch.org/blog/reduce-cost-with-disk-based-vector-search/)

### Pull Requests
| Version | PR | Description |
|---------|-----|-------------|
| v2.17.0 | [#2034](https://github.com/opensearch-project/k-NN/pull/2034) | Introduce mode and compression param resolution |
| v2.17.0 | [#1984](https://github.com/opensearch-project/k-NN/pull/1984) | k-NN query rescore support for native engines |
| v2.17.0 | [#2044](https://github.com/opensearch-project/k-NN/pull/2044) | Add spaceType as top level parameter |
| v2.17.0 | [#2200](https://github.com/opensearch-project/k-NN/pull/2200) | Add CompressionLevel calculation for PQ |
| v2.18.0 | [#2281](https://github.com/opensearch-project/k-NN/pull/2281) | Fix bug when segment has no vector field for disk-based search |
| v2.19.0 | [#2290](https://github.com/opensearch-project/k-NN/pull/2290) | Allow method parameter override for training based indices |

### Issues (Design / RFC)
- [RFC: Disk-based Mode Design (#1949)](https://github.com/opensearch-project/k-NN/issues/1949): Design document for mode parameter
- [RFC: Optimized Disk-Based Vector Search (#1779)](https://github.com/opensearch-project/k-NN/issues/1779): Original feature proposal with benchmarks
- [RFC: Two-phased Search Re-score Design (#1861)](https://github.com/opensearch-project/k-NN/issues/1861): Rescoring implementation design
