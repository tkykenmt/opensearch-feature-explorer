---
tags:
  - ml-commons
---
# ML Inference Processors

## Summary

OpenSearch v2.16.0 introduces ML Inference Search Request and Search Response Processors, extending the ML inference capabilities from ingest pipelines to search pipelines. These processors enable ML model predictions to be applied during search operations, supporting use cases like query embedding for semantic search and search result enrichment.

## Details

### What's New in v2.16.0

#### ML Inference Search Request Processor
A new search request processor that transforms search queries using ML models before execution. Key capabilities:
- Converts text queries to vector embeddings for semantic search
- Supports query template transformation with model predictions
- Works with both remote and local ML models

#### ML Inference Search Response Processor
A new search response processor that enriches search results with ML model predictions. Key capabilities:
- Adds ML-generated fields to search hits (e.g., embeddings, classifications)
- Supports many-to-one prediction mode (batch processing multiple documents)
- Configurable input/output field mappings

#### Model Input Validation for Local Models
Added validation for model input when using local models in ML processors, ensuring proper configuration and preventing runtime errors.

### Technical Changes

#### New Classes
- `MLInferenceSearchRequestProcessor`: Implements `SearchRequestProcessor` interface
- `MLInferenceSearchResponseProcessor`: Implements `SearchResponseProcessor` interface
- `MapUtils`: Utility class for counter management in batch processing
- `SearchResponseUtil`: Utility for replacing search hits in responses

#### Configuration Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `model_id` | ID of the ML model to invoke | Required |
| `function_name` | Function name (`remote`, `text_embedding`, etc.) | `remote` |
| `input_map` | Maps query/document fields to model input | Optional |
| `output_map` | Maps model output to new fields | Optional |
| `model_config` | Additional model configuration | Optional |
| `model_input` | Template for model input format | Auto-generated for remote |
| `full_response_path` | Use JSON path for output extraction | `false` (remote) |
| `ignore_missing` | Skip documents with missing input fields | `false` |
| `ignore_failure` | Continue on prediction failures | `false` |
| `max_prediction_tasks` | Maximum concurrent model invocations | `10` |
| `one_to_one` | Invoke model per document (response only) | `false` |

### Usage Examples

#### Search Request Pipeline - Query Embedding

```json
PUT /_search/pipeline/semantic_search_pipeline
{
  "request_processors": [
    {
      "ml_inference": {
        "model_id": "<embedding_model_id>",
        "query_template": "{\"query\":{\"knn\":{\"embedding\":{\"vector\":${modelPredictionOutcome},\"k\":10}}}}",
        "input_map": [
          {
            "inputText": "query.match.text.query"
          }
        ],
        "output_map": [
          {
            "modelPredictionOutcome": "embedding"
          }
        ]
      }
    }
  ]
}
```

#### Search Response Pipeline - Result Enrichment

```json
PUT /_search/pipeline/enrichment_pipeline
{
  "response_processors": [
    {
      "ml_inference": {
        "model_id": "<embedding_model_id>",
        "input_map": [
          {
            "input": "text_field"
          }
        ],
        "output_map": [
          {
            "text_embedding": "data[*].embedding"
          }
        ],
        "ignore_missing": false,
        "ignore_failure": false
      }
    }
  ]
}
```

## Limitations

- `one_to_one` mode for per-document inference in search response processor is not yet supported (throws exception)
- Local models require explicit `function_name` and `model_input` configuration
- Model must be deployed and accessible before pipeline execution
- Complex nested field mappings require JSON path syntax

## References

### Documentation
- [ML Inference Search Request Processor](https://docs.opensearch.org/2.16/search-plugins/search-pipelines/ml-inference-search-request/)
- [ML Inference Search Response Processor](https://docs.opensearch.org/2.16/search-plugins/search-pipelines/ml-inference-search-response/)

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#2688](https://github.com/opensearch-project/ml-commons/pull/2688) | Add initial MLInferenceSearchResponseProcessor | [#2173](https://github.com/opensearch-project/ml-commons/issues/2173), [#2444](https://github.com/opensearch-project/ml-commons/issues/2444) |
| [#2616](https://github.com/opensearch-project/ml-commons/pull/2616) | Add initial search request inference processor | [#2173](https://github.com/opensearch-project/ml-commons/issues/2173), [#2444](https://github.com/opensearch-project/ml-commons/issues/2444) |
| [#2731](https://github.com/opensearch-project/ml-commons/pull/2731) | Backport search request processor to 2.16 | - |
| [#2610](https://github.com/opensearch-project/ml-commons/pull/2610) | Add model input validation for local models in ml processor | [#2601](https://github.com/opensearch-project/ml-commons/issues/2601) |
