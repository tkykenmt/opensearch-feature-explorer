---
tags:
  - ml
  - search
---

# ML Commons Model & Inference

## Summary

OpenSearch v2.18.0 introduces several enhancements to the ML Commons plugin's model and inference capabilities. Key improvements include filtering out remote model auto-redeployment, making `llmQuestion` optional when `llmMessages` is used in RAG pipelines, supporting ML inference search processor writing to search extensions, enabling query string passing to `input_map` in ML inference search response processor, adding a `config` field in `MLToolSpec` for static parameters, and adding AWS Textract and Comprehend URLs to trusted endpoints.

## Details

### What's New in v2.18.0

#### Remote Model Auto-Redeployment Filtering

The `MLModelAutoRedeployer` now filters out remote models from auto-redeployment. Since ML Commons supports remote model auto-deployment when the first prediction request arrives, explicit auto-redeployment is unnecessary for remote models, reducing redundant operations.

#### Optional llmQuestion for RAG Pipelines

When using `llmMessages` in RAG (Retrieval-Augmented Generation) request parameters, the `llmQuestion` field is now optional. This provides more flexibility when constructing conversational AI pipelines where the question context is already embedded in the message history.

#### ML Inference Search Processor Writing to Search Extension

The ML inference search response processor now supports writing prediction results to the search extension (`ext`) field when using many-to-one inference mode. Previously, results were only written to individual document hits. This enables use cases like LLM summarization of search results where a single aggregated response is more appropriate.

```json
"output_map": [
  {
    "ext.ml_inference.llm_response": "response"
  }
]
```

Note: This feature is not supported for one-to-one inference because the order of inference matters and other processors might rerank results, disrupting the mapping between inputs and outputs.

#### Query String Passing to input_map

The ML inference search response processor now supports passing query string values to the `input_map`. This enables use cases like cross-encoder reranking where the original query text needs to be compared against document content.

```json
"input_map": [
  {
    "text_docs": "dairy",
    "query_text": "$.query.term.dairy.value"
  }
]
```

#### Static Parameters in MLToolSpec

A new `config` field has been added to `MLToolSpec` to support static parameters in tool execution. This allows pre-configuring tool parameters at agent registration time rather than requiring them at execution time.

```json
{
  "tools": [
    {
      "type": "SearchIndexTool",
      "config": {
        "input": "{\"index\": \"sample-index\", \"query\": {\"query\": { \"match_all\": {}}} }"
      }
    }
  ]
}
```

#### AWS Textract and Comprehend Trusted Endpoints

AWS Textract and Comprehend service URLs have been added to the trusted endpoints list, enabling integration with these AWS AI services through ML Commons connectors.

### Technical Changes

#### New Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `config` field in MLToolSpec | Static parameters for tool execution | N/A |

#### API Changes

| Change | Description |
|--------|-------------|
| `llmQuestion` optional | No longer required when `llmMessages` is provided |
| `ext` output path | ML inference processor can write to search extension |
| Query path in input_map | Supports `$.query.*` JSON path for query values |

### Usage Example

#### LLM Summarization with Search Extension Output

```json
PUT /_search/pipeline/summarize_pipeline
{
  "response_processors": [
    {
      "ml_inference": {
        "model_id": "<llm_model_id>",
        "function_name": "REMOTE",
        "input_map": [
          {
            "context": "review"
          }
        ],
        "output_map": [
          {
            "ext.ml_inference.llm_response": "response"
          }
        ],
        "model_config": {
          "prompt": "Summarize the following documents: ${parameters.context.toString()}"
        },
        "one_to_one": false
      }
    }
  ]
}
```

#### Cross-Encoder Reranking with Query Text

```json
PUT /_search/pipeline/rerank_pipeline
{
  "response_processors": [
    {
      "ml_inference": {
        "model_id": "<cross_encoder_model_id>",
        "function_name": "TEXT_SIMILARITY",
        "input_map": [
          {
            "text_docs": "content",
            "query_text": "$.query.term.content.value"
          }
        ],
        "output_map": [
          {
            "rank_score": "$.inference_results[*].output[*].data"
          }
        ],
        "one_to_one": true
      }
    }
  ]
}
```

## Limitations

- Writing to search extension (`ext`) is only supported for many-to-one inference (`one_to_one: false`)
- One-to-one inference cannot write to search extension due to ordering concerns with reranking processors

## References

### Documentation
- [ML inference search response processor documentation](https://docs.opensearch.org/2.18/search-plugins/search-pipelines/ml-inference-search-response/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#2976](https://github.com/opensearch-project/ml-commons/pull/2976) | Filter out remote model auto redeployment |
| [#3072](https://github.com/opensearch-project/ml-commons/pull/3072) | Allow llmQuestion to be optional when llmMessages is used |
| [#3061](https://github.com/opensearch-project/ml-commons/pull/3061) | Support ML Inference Search Processor Writing to Search Extension |
| [#2899](https://github.com/opensearch-project/ml-commons/pull/2899) | Enable pass query string to input_map in ml inference search response processor |
| [#2977](https://github.com/opensearch-project/ml-commons/pull/2977) | Add config field in MLToolSpec for static parameters |
| [#3154](https://github.com/opensearch-project/ml-commons/pull/3154) | Add textract and comprehend url to trusted endpoints |

### Issues (Design / RFC)
- [Issue #2897](https://github.com/opensearch-project/ml-commons/issues/2897): Query text in input_map feature request
- [Issue #2878](https://github.com/opensearch-project/ml-commons/issues/2878): Search extension output feature request
- [Issue #3067](https://github.com/opensearch-project/ml-commons/issues/3067): Optional llmQuestion feature request
- [Issue #2836](https://github.com/opensearch-project/ml-commons/issues/2836): Static tool parameters feature request
- [Issue #2918](https://github.com/opensearch-project/ml-commons/issues/2918): MLToolSpec config field feature request

## Related Feature Report

- [Full feature documentation](../../../features/ml-commons/ml-commons-model-inference.md)
