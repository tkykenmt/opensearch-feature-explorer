---
tags:
  - k-nn
---
# k-NN Binary Vector Support

## Summary

OpenSearch 2.16.0 introduces binary vector support for the k-NN plugin, enabling significant memory and storage savings for large-scale vector search applications. Binary vectors use Hamming distance for similarity calculations and can reduce memory requirements by a factor of 32 compared to float32 vectors.

## Details

### What's New in v2.16.0

Binary vector support adds a new `data_type: binary` option for k-NN vector fields, allowing vectors to be stored as packed bytes instead of floating-point numbers. This feature is available exclusively with the Faiss engine.

### Supported Methods

| Method | Engine | Space Type | Description |
|--------|--------|------------|-------------|
| HNSW | Faiss | hamming | Approximate nearest neighbor search using HNSW algorithm |
| IVF | Faiss | hamming | Inverted file index with training-based approach |

### Configuration

Binary vectors require:
- `data_type`: Must be set to `binary`
- `space_type`: Must be set to `hamming`
- `dimension`: Must be a multiple of 8

### Index Mapping Example

```json
PUT /test-binary-hnsw
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
        "dimension": 8,
        "data_type": "binary",
        "method": {
          "name": "hnsw",
          "space_type": "hamming",
          "engine": "faiss",
          "parameters": {
            "ef_construction": 128,
            "m": 24
          }
        }
      }
    }
  }
}
```

### Data Format

Binary data must be converted to 8-bit signed integers (int8) in the [-128, 127] range. Each byte represents 8 binary bits packed together.

Example conversion:
- Binary: `0, 1, 1, 0, 1, 1, 0, 0` → Byte: `108`
- Binary: `1, 0, 0, 0, 1, 1, 0, 0` → Byte: `-116`

### Search Types Supported

1. **Approximate k-NN**: Using HNSW or IVF algorithms with Faiss engine
2. **Script Score k-NN**: Using `hammingbit` space type for exact search
3. **Painless Extensions**: Hamming distance calculations in custom scripts

### Script Scoring Example

```json
POST /my-knn-index/_search
{
  "query": {
    "script_score": {
      "query": { "match_all": {} },
      "script": {
        "source": "knn_score",
        "lang": "knn",
        "params": {
          "field": "my_vector",
          "query_value": [13],
          "space_type": "hammingbit"
        }
      }
    }
  }
}
```

### Performance Benefits

Based on benchmarking with 100 million 768-dimensional vectors:
- Memory reduction: ~92%
- Storage reduction: ~97%
- Comparable indexing speeds and query times on 8x smaller hardware

## Limitations

- Only supported with Faiss engine (not Nmslib or Lucene)
- Only Hamming distance space type is supported
- Dimension must be a multiple of 8
- Converting float vectors to binary may result in some recall loss (depends on quantization technique)

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1781](https://github.com/opensearch-project/k-NN/pull/1781) | Add binary format support with HNSW method in Faiss Engine | [#1767](https://github.com/opensearch-project/k-NN/issues/1767) |
| [#1784](https://github.com/opensearch-project/k-NN/pull/1784) | Add binary format support with IVF method in Faiss Engine | [#1767](https://github.com/opensearch-project/k-NN/issues/1767) |
| [#1826](https://github.com/opensearch-project/k-NN/pull/1826) | Add script scoring support for knn field with binary data type | - |
| [#1839](https://github.com/opensearch-project/k-NN/pull/1839) | Add painless script support for hamming with binary vector data type | - |

### Documentation

- [Binary k-NN vectors](https://docs.opensearch.org/2.16/field-types/supported-field-types/knn-vector/#binary-k-nn-vectors)
- [Exact k-NN with scoring script](https://docs.opensearch.org/2.16/search-plugins/knn/knn-score-script/)

### Blog Posts

- [Optimize your OpenSearch costs using binary vectors](https://opensearch.org/blog/lower-your-cost-on-opensearch-using-binary-vectors/)
