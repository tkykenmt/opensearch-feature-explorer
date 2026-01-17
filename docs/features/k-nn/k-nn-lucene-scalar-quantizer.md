---
tags:
  - k-nn
---
# Lucene Scalar Quantizer

## Summary

The Lucene Scalar Quantizer is a built-in vector quantization feature in the k-NN plugin that automatically compresses 32-bit floating-point vectors to 7-bit integers during ingestion. This reduces memory footprint by approximately 75% while maintaining acceptable search recall, without requiring pre-quantization of vectors before indexing.

## Details

### Architecture

```mermaid
flowchart TB
    subgraph Ingestion
        A[fp32 Vector] --> B[Lucene SQ Encoder]
        B --> C[Compute Quantiles]
        C --> D[7-bit Quantized Vector]
        D --> E[Store in Segment]
    end
    
    subgraph Search
        F[Query Vector] --> G[Load Segment Quantiles]
        G --> H[Quantize Query]
        H --> I[Distance Computation]
        I --> J[Results]
    end
```

### How It Works

1. **Ingestion**: Input fp32 vectors are quantized to 7-bit integers using min/max quantiles computed from the data
2. **Per-segment quantization**: Each Lucene segment maintains its own quantile values
3. **Search**: Query vectors are quantized using segment-specific quantiles for distance computation
4. **Storage**: Both raw vectors and quantized vectors are stored (slight disk overhead)

### Configuration

| Parameter | Description | Default | Valid Values |
|-----------|-------------|---------|--------------|
| `bits` | Quantization bit depth | `7` | `7` only |
| `confidence_interval` | Controls quantile computation | Dimension-based | `0` or `0.9`-`1.0` |

### Confidence Interval

The `confidence_interval` parameter determines how min/max quantiles are computed:

| Value | Behavior |
|-------|----------|
| `0.9` - `1.0` | Static: Uses middle N% of vector values |
| `0` | Dynamic: Oversampling with additional computation |
| Not set | Computed as `max(0.9, 1 - 1/(1 + dimension))` |

### Usage Example

```json
PUT /my-index
{
  "settings": {
    "index": { "knn": true }
  },
  "mappings": {
    "properties": {
      "embedding": {
        "type": "knn_vector",
        "dimension": 768,
        "method": {
          "name": "hnsw",
          "engine": "lucene",
          "space_type": "l2",
          "parameters": {
            "encoder": {
              "name": "sq",
              "parameters": {
                "confidence_interval": 0.95
              }
            },
            "m": 16,
            "ef_construction": 100
          }
        }
      }
    }
  }
}
```

### Memory Estimation

HNSW with scalar quantization: `1.1 * (dimension + 8 * M)` bytes/vector

| Vectors | Dimension | M | Memory (SQ) | Memory (fp32) | Savings |
|---------|-----------|---|-------------|---------------|---------|
| 1M | 256 | 16 | ~0.4 GB | ~1.6 GB | 75% |
| 1M | 768 | 16 | ~1.0 GB | ~3.5 GB | 71% |
| 10M | 256 | 16 | ~4.0 GB | ~16 GB | 75% |

### Comparison with Other Quantization Methods

| Method | Engine | Compression | Pre-quantization Required | Recall Impact |
|--------|--------|-------------|---------------------------|---------------|
| Lucene SQ | Lucene | ~75% | No | Low |
| Lucene Byte Vector | Lucene | 75% | Yes | Low |
| Faiss SQfp16 | Faiss | 50% | No | Minimal |
| Faiss PQ | Faiss | Configurable | Training required | Variable |

## Limitations

- Only 7-bit quantization supported (8-bit disabled due to recall degradation)
- Requires `float` data type (incompatible with `byte` or `binary` vectors)
- Increases disk usage (stores both raw and quantized vectors)
- Some recall loss compared to unquantized vectors
- Only available with Lucene engine

## Change History

- **v2.16.0** (2024-08-06): Initial implementation with 7-bit quantization and confidence_interval parameter

## References

### Documentation

- [k-NN vector quantization](https://docs.opensearch.org/latest/search-plugins/knn/knn-vector-quantization/)

### Pull Requests

| Version | PR | Description |
|---------|-----|-------------|
| v2.16.0 | [#1848](https://github.com/opensearch-project/k-NN/pull/1848) | Add support for Lucene inbuilt Scalar Quantizer |

### Issues

- [#1277](https://github.com/opensearch-project/k-NN/issues/1277) - Feature request for Lucene inbuilt scalar quantizer
