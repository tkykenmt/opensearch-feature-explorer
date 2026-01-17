---
tags:
  - k-nn
---
# k-NN Dynamic Query Parameters

## Summary

OpenSearch 2.16.0 introduces the ability to specify `ef_search` and `nprobes` parameters at query time in k-NN searches. Previously, these parameters could only be set at index level. This feature allows users to dynamically tune search accuracy and latency trade-offs per query without modifying index settings.

## Details

### What's New in v2.16.0

The `method_parameters` field is now supported in k-NN queries, enabling query-time configuration of search parameters:

```json
GET my-knn-index/_search
{
  "size": 2,
  "query": {
    "knn": {
      "target-field": {
        "vector": [2, 3, 5, 6],
        "k": 2,
        "method_parameters": {
          "ef_search": 100
        }
      }
    }
  }
}
```

### Supported Parameters

| Parameter | Method | Description |
|-----------|--------|-------------|
| `ef_search` | HNSW | Number of vectors to examine for finding top k neighbors |
| `nprobes` | IVF | Number of buckets to examine for finding top k neighbors |

### Engine Support

| Engine | ef_search | nprobes | Radial Query Support |
|--------|-----------|---------|---------------------|
| Lucene | ✓ | - | No |
| FAISS | ✓ | ✓ | Yes |
| NMSLIB | ✓ | - | No |

### Behavior by Engine

- **FAISS/NMSLIB**: Query-time `ef_search` overrides the `index.knn.algo_param.ef_search` index setting
- **Lucene**: Uses the larger of `k` and `ef_search` as the effective ef_search value. Use `size` parameter to limit final results if `ef_search > k`
- **FAISS (IVF)**: Query-time `nprobes` overrides the value set during index creation

### Neural Search Integration

The neural-search plugin also supports these parameters via the `method_parameters` field, enabling the same query-time tuning for neural search queries.

## Limitations

- Parameters are method-specific: `ef_search` only works with HNSW, `nprobes` only with IVF
- Radial search with `ef_search` is only supported on FAISS engine
- Higher values improve recall but increase search latency

## References

### Pull Requests

| PR | Repository | Description |
|----|------------|-------------|
| [#1783](https://github.com/opensearch-project/k-NN/pull/1783) | k-NN | Adds ef_search as query parameter for Lucene, FAISS, and NMSLIB |
| [#1790](https://github.com/opensearch-project/k-NN/pull/1790) | k-NN | Support ef_search parameter in radial search FAISS engine |
| [#1792](https://github.com/opensearch-project/k-NN/pull/1792) | k-NN | Adds nprobes as query parameter |
| [#814](https://github.com/opensearch-project/neural-search/pull/814) | neural-search | Adds method_parameters in neural search query |

### Related Issues

| Issue | Description |
|-------|-------------|
| [#1537](https://github.com/opensearch-project/k-NN/issues/1537) | Feature request: Enable setting ef_search parameter as part of k-NN Query |

### Documentation

- [Approximate k-NN search](https://docs.opensearch.org/2.16/search-plugins/knn/approximate-knn/)
