---
tags:
  - neural-search
---
# Neural Search

## Summary

OpenSearch v3.5.0 brings several enhancements to the neural-search plugin including support for asymmetric embedding models, GRPC-based hybrid query execution, `min_score` parameter support in hybrid search, sparse_vector field ingest metrics, and additional codec registration support. The release also includes backward compatibility (BWC) test fixes for Gradle 9 upgrade and version compatibility between 3.5.0 and 2.19.0.

## Details

### What's New in v3.5.0

#### Asymmetric Embedding Models Support

Asymmetric embedding models use different prefixes for queries and passages to improve retrieval quality. This feature adds support for both local and remote asymmetric models.

Key additions to `InferenceRequest`:
- `mlAlgoParams`: ML algorithm parameters for asymmetric models
- `embeddingContentType`: Content type indicator (`QUERY` or `PASSAGE`) for prefix selection

**Model Configuration Example:**
```json
{
  "model_config": {
    "model_type": "bert",
    "embedding_dimension": 768,
    "framework_type": "sentence_transformers",
    "passage_prefix": "passage: ",
    "query_prefix": "query: "
  }
}
```

**Ingest Pipeline with Asymmetric Model:**
```json
PUT /_ingest/pipeline/asymmetric_embedding_ingest_pipeline
{
  "processors": [
    {
      "ml_inference": {
        "model_input": "{\"text_docs\":[\"${input_map.text_docs}\"],\"target_response\":[\"sentence_embedding\"],\"parameters\":{\"content_type\":\"passage\"}}",
        "function_name": "text_embedding",
        "model_id": "${MODEL_ID}",
        "input_map": [{ "text_docs": "description" }],
        "output_map": [{ "fact_embedding": "$.inference_results[0].output[0].data" }]
      }
    }
  ]
}
```

**Neural Search Query with Asymmetric Model:**
```json
GET /my-index/_search
{
  "query": {
    "neural": {
      "fact_embedding": {
        "query_text": "What are some places for sports in NYC?",
        "model_id": "${MODEL_ID}",
        "boost": 1
      }
    }
  }
}
```

#### GRPC Hybrid Query

Implements hybrid query support over GRPC transport protocol, enabling high-performance hybrid search via gRPC.

**Sample GRPC Hybrid Query:**
```json
{
  "search_request_body": {
    "query": {
      "hybrid": {
        "queries": [
          {
            "match": {
              "field": "test",
              "query": { "string": "hi" }
            }
          },
          { "match_all": {} }
        ]
      }
    }
  }
}
```

#### min_score Support in Hybrid Search

Adds support for the `min_score` parameter in hybrid queries, allowing users to filter results based on the final normalized/combined score.

**Usage:**
```json
GET /my-index/_search?search_pipeline=hybrid-pipeline
{
  "min_score": 0.5,
  "query": {
    "hybrid": {
      "queries": [
        { "match": { "text_field": "search terms" } },
        { "neural": { "embedding_field": { "query_text": "semantic query", "model_id": "model-id", "k": 10 } } }
      ]
    }
  }
}
```

#### Sparse Vector Ingest Metrics

Adds ingest metrics for `sparse_vector` field type, enabling observability for sparse vector ingestion operations through the neural search stats API.

#### Additional Codec Registration

Includes `AdditionalCodecs` argument support to allow additional codec registration, following the OpenSearch core codec extensibility changes.

### Technical Changes

| Change | Description |
|--------|-------------|
| Asymmetric Models | New `embeddingContentType` and `mlAlgoParams` fields in `InferenceRequest` |
| GRPC Hybrid Query | Hybrid query builder support for GRPC transport |
| min_score | Score filtering applied to final hybrid query results |
| Sparse Vector Metrics | Ingest metrics for sparse_vector field operations |
| Codec Registration | `AdditionalCodecs` argument for codec extensibility |

### BWC Test Fixes

- Fixed BWC tests after Gradle 9 upgrade
- Corrected BWC tests between 3.5.0 and 2.19.0
- Added BWC tests for nested field support in Sparse ANN (Seismic)

## Limitations

- Asymmetric model support requires model configuration with `query_prefix` and `passage_prefix`
- GRPC hybrid query requires OpenSearch core GRPC transport support (PR #20103)
- min_score filtering is applied after score normalization/combination

## References

### Pull Requests
| PR | Title | Category |
|----|-------|----------|
| [#1605](https://github.com/opensearch-project/neural-search/pull/1605) | Add support for asymmetric embedding models | feature |
| [#1665](https://github.com/opensearch-project/neural-search/pull/1665) | Implement GRPC Hybrid Query | feature |
| [#1726](https://github.com/opensearch-project/neural-search/pull/1726) | Add support for min_score param in hybrid search | feature |
| [#1715](https://github.com/opensearch-project/neural-search/pull/1715) | Add ingest through sparse_vector field metrics | enhancement |
| [#1741](https://github.com/opensearch-project/neural-search/pull/1741) | Include AdditionalCodecs argument to allow additional Codec registration | enhancement |
| [#1729](https://github.com/opensearch-project/neural-search/pull/1729) | Enable BWC tests after upgrading to Gradle 9 | bugfix |
| [#1737](https://github.com/opensearch-project/neural-search/pull/1737) | Correct BWC tests between 3.5 and 2.19 | bugfix |
| [#1725](https://github.com/opensearch-project/neural-search/pull/1725) | Introduce BWC tests for nested field support with Sparse ANN | bugfix |

### Related Issues
- [#1495](https://github.com/opensearch-project/neural-search/issues/1495): GRPC Hybrid Query tracking
- [#1164](https://github.com/opensearch-project/neural-search/issues/1164): min_score support in hybrid search
- [#1731](https://github.com/opensearch-project/neural-search/issues/1731): BWC test CI workflow fix
- [#1728](https://github.com/opensearch-project/neural-search/issues/1728): BWC tests after Gradle 9 upgrade
- [#620](https://github.com/opensearch-project/neural-search/issues/620): Asymmetric model support
