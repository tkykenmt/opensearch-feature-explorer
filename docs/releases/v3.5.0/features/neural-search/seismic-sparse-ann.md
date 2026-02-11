---
tags:
  - neural-search
---
# SEISMIC (Sparse ANN) Enhancements

## Summary

OpenSearch v3.5.0 brings two significant enhancements to the SEISMIC Sparse ANN algorithm: query explanation support for debugging and understanding search results, and improved multi-threaded query performance through optimized cache implementation.

## Details

### What's New in v3.5.0

#### 1. Query Explanation Support

The `explain` API now works with Sparse ANN queries, providing detailed breakdowns of the SEISMIC scoring process. This helps users understand why certain documents rank higher than others.

**Explanation Structure:**
```
sparse_ann score for doc X in field 'Y'
├── Query token pruning: kept top N of M tokens
├── Raw dot product score (quantized): SCORE
│   ├── token 'A' contribution: query_weight=X * doc_weight=Y
│   └── ... (contributing tokens)
├── Quantization rescaling: boost * ceiling_ingest * ceiling_search / 255 / 255
│   ├── original boost
│   ├── ceiling_ingest (quantization parameter)
│   ├── ceiling_search (quantization parameter)
│   └── MAX_UNSIGNED_BYTE_VALUE: 255
└── Filter explanation (when applicable)
    └── filter criteria and search mode (exact vs approximate)
```

**Key Explanation Components:**

| Component | Description |
|-----------|-------------|
| Query Token Pruning | Shows how many tokens were kept after top-N pruning |
| Raw Dot Product Score | Quantized integer score with per-token contributions |
| Quantization Rescaling | Formula converting raw score back to float scale |
| Filter Explanation | Indicates exact vs approximate search mode based on P vs k |

**Filter Search Modes:**
- **Exact Search Mode**: When filtered document count (P) ≤ k, all filtered documents are scored exactly
- **Approximate Search Mode**: When P > k, ANN search runs first, then filter is applied

**Example Query with Explanation:**
```json
POST /my-seismic-index/_search?explain=true
{
  "query": {
    "neural_sparse": {
      "sparse_embedding": {
        "query_text": "beach resort",
        "method_parameters": {
          "k": 5,
          "filter": {
            "bool": {
              "must": [
                { "range": { "rating": { "gte": 8, "lte": 10 } } }
              ]
            }
          }
        }
      }
    }
  }
}
```

**Example Explanation Response:**
```json
{
  "_explanation": {
    "value": 70.55404,
    "description": "sparse_ann score for doc 7 in field 'name_embedding'",
    "details": [
      {
        "value": 2,
        "description": "query token pruning: kept all 2 tokens (no pruning occurred)"
      },
      {
        "value": 17921,
        "description": "raw dot product score (quantized): 17921",
        "details": [
          {
            "value": 10000,
            "description": "token '7001' contribution: query_weight=100 * doc_weight=100"
          },
          {
            "value": 7921,
            "description": "token '3509' contribution: query_weight=89 * doc_weight=89"
          }
        ]
      },
      {
        "value": 0.003936948,
        "description": "quantization rescaling: 1.0000 * 16.00 * 16.00 / 255 / 255 = 0.003937",
        "details": [...]
      },
      {
        "value": 1,
        "description": "document passed filter with exact search mode (filter matched 4 documents <= k=5, all filtered documents scored exactly)",
        "details": [...]
      }
    ]
  }
}
```

#### 2. Multi-Threaded Query Performance Improvement

The LRU cache implementation was optimized to eliminate lock contention under high concurrency workloads.

**Problem Solved:**
The previous implementation used `Collections.synchronizedMap(LinkedHashMap)` which required acquiring a global lock on every cache access, causing severe performance degradation under concurrent load.

**Solution:**
Replaced with `ConcurrentLinkedHashMap` from the `concurrentlinkedhashmap-lru` library, providing:
- Lock-free concurrent access operations
- Exact LRU eviction behavior
- Bounded memory usage

**Performance Improvement:**

| Metric | Before (50 threads) | After (50 threads) |
|--------|---------------------|-------------------|
| Average latency | 36.81 ms | ~2-3 ms |
| P95 latency | 79 ms | Significantly reduced |
| P99 latency | 107 ms | Significantly reduced |

### Technical Changes

**New Class:**
- `SparseExplanationBuilder`: Builder class for constructing detailed SEISMIC query explanations

**Modified Classes:**
- `SparseQueryWeight.explain()`: Now delegates to `SparseExplanationBuilder` instead of returning null
- `AbstractLruCache`: Replaced `Collections.synchronizedMap(LinkedHashMap)` with `ConcurrentLinkedHashMap`

**New Dependency:**
```gradle
implementation 'com.googlecode.concurrentlinkedhashmap:concurrentlinkedhashmap-lru:1.4.2'
```

## Limitations

- Explanation adds minimal latency overhead (~0.06 ms per query on 100K documents)
- Explanation is only generated when `?explain=true` is specified

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1694](https://github.com/opensearch-project/neural-search/pull/1694) | Enable explain function within Sparse ANN query | [#1690](https://github.com/opensearch-project/neural-search/issues/1690) |
| [#1712](https://github.com/opensearch-project/neural-search/pull/1712) | Boost multi threads query efficiency | [#1684](https://github.com/opensearch-project/neural-search/issues/1684), [#1691](https://github.com/opensearch-project/neural-search/issues/1691) |

### Issues
- [#1690](https://github.com/opensearch-project/neural-search/issues/1690): Design - Sparse ANN Query Explanation Support
- [#1684](https://github.com/opensearch-project/neural-search/issues/1684): Feature - Sparse ANN Concurrent Query Throughput Improvement
- [#1691](https://github.com/opensearch-project/neural-search/issues/1691): Design - Sparse ANN Concurrent Query Throughput Improvement
