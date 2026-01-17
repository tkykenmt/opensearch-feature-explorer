---
tags:
  - k-nn
---
# Lucene Scalar Quantizer

## Summary

OpenSearch 2.16.0 introduces built-in scalar quantization for the Lucene engine in the k-NN plugin. This feature automatically quantizes 32-bit floating-point vectors to 7-bit integers during ingestion, reducing memory footprint by approximately 75% while maintaining search quality.

## Details

### What's New in v2.16.0

The Lucene scalar quantizer provides automatic vector compression without requiring pre-quantization before ingestion:

- **Automatic quantization**: Converts fp32 vectors to 7-bit integers during document indexing
- **Dynamic quantile computation**: Calculates min/max quantiles per segment based on `confidence_interval`
- **Query-time dequantization**: Quantizes query vectors using segment-specific quantiles for distance computation
- **Consistent API**: Uses the `sq` encoder under `parameters` field, similar to Faiss

### Configuration

The `sq` encoder for Lucene supports the following parameters:

| Parameter | Description | Default | Valid Values |
|-----------|-------------|---------|--------------|
| `bits` | Number of bits for quantization | `7` | `7` only (8-bit not supported due to recall issues) |
| `confidence_interval` | Controls quantile computation for min/max values | Computed as `1 - 1/(1 + dimension)` | `0` (dynamic), or `0.9` to `1.0` |

### Usage Example

```json
PUT /test-index
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "knn_vector",
        "dimension": 128,
        "method": {
          "name": "hnsw",
          "space_type": "l2",
          "engine": "lucene",
          "parameters": {
            "encoder": {
              "name": "sq",
              "parameters": {
                "bits": 7,
                "confidence_interval": 1.0
              }
            },
            "ef_construction": 128,
            "m": 24
          }
        }
      }
    }
  }
}
```

### Confidence Interval Behavior

- `0.9` to `1.0`: Static quantile calculation (e.g., `0.9` uses middle 90% of values)
- `0`: Dynamic computation with oversampling
- Not set: Computed from dimension as `max(0.9, 1 - 1/(1 + d))`

### Technical Changes

Key implementation components:

| Component | Description |
|-----------|-------------|
| `KNNScalarQuantizedVectorsFormatParams` | New class for SQ encoder parameters |
| `KNNVectorsFormatParams` | Base class for vector format parameters |
| `KNN990PerFieldKnnVectorsFormat` | Updated to support `Lucene99HnswScalarQuantizedVectorsFormat` |
| `Lucene.java` | Added `sq` encoder definition with parameter validation |
| `Parameter.DoubleParameter` | New parameter type for confidence_interval validation |

### Memory Estimation

HNSW memory with scalar quantization: `1.1 * (dimension + 8 * M)` bytes/vector

Example: 1M vectors, dimension=256, M=16:
```
1.1 * (256 + 8 * 16) * 1,000,000 ≈ 0.4 GB
```

Compared to fp32 vectors (~1.6 GB), this represents ~75% memory reduction.

## Limitations

- Only 7-bit quantization is supported (8-bit disabled due to recall issues)
- Only works with `float` data type vectors (not `byte` or `binary`)
- Slightly increases disk usage (stores both raw and quantized vectors)
- Some recall loss compared to unquantized vectors

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1848](https://github.com/opensearch-project/k-NN/pull/1848) | Add support for Lucene inbuilt Scalar Quantizer | [#1277](https://github.com/opensearch-project/k-NN/issues/1277) |

### Documentation

- [k-NN vector quantization](https://docs.opensearch.org/2.16/search-plugins/knn/knn-vector-quantization/)
