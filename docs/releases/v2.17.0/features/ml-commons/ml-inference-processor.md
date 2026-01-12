---
tags:
  - ml
  - search
---

# ML Inference Processor - One-to-One Support

## Summary

OpenSearch v2.17.0 adds `one_to_one` inference mode to the ML Inference Search Response Processor. This enhancement enables per-document model predictions, where each document in search results triggers an individual model invocation rather than batching all documents into a single prediction call.

## Details

### What's New in v2.17.0

The ML Inference Search Response Processor now supports a new `one_to_one` parameter that changes how documents are processed during inference:

- **Default behavior (`one_to_one: false`)**: All documents from search hits are collected and sent to the model in a single prediction call (many-to-one)
- **New behavior (`one_to_one: true`)**: Each document triggers a separate prediction call, with results mapped back to individual documents

### Technical Changes

#### Processing Flow

```mermaid
graph TB
    subgraph "one_to_one: false (Default)"
        A1[Search Response<br/>N documents] --> B1[Collect all inputs]
        B1 --> C1[Single Predict API call]
        C1 --> D1[Map outputs to documents]
    end
    
    subgraph "one_to_one: true (New)"
        A2[Search Response<br/>N documents] --> B2[Split into N responses]
        B2 --> C2[N Predict API calls]
        C2 --> D2[Combine responses]
    end
```

#### New Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `one_to_one` | When `true`, invokes the model once per document. When `false`, batches all documents into a single prediction. | `false` |

#### Implementation Details

The processor introduces:
- `GroupedActionListener` to handle parallel predictions and combine results
- `SearchResponseUtil.replaceHits()` to split/combine search responses
- Atomic failure tracking to stop remaining predictions on first error
- Enhanced error handling for `OpenSearchStatusException` and `MLResourceNotFoundException`

### Usage Example

```json
PUT /_search/pipeline/rerank_pipeline
{
  "response_processors": [
    {
      "ml_inference": {
        "model_id": "<rerank_model_id>",
        "input_map": [
          {
            "text": "passage_text"
          }
        ],
        "output_map": [
          {
            "score": "response"
          }
        ],
        "one_to_one": true
      }
    }
  ]
}
```

### Use Cases

The `one_to_one` mode is particularly useful for:

1. **Reranking with XGBoost models**: Models that compare a single document against the search query and return a relevance score
2. **Bedrock embedding models**: Models that accept a single string input rather than a list
3. **Per-document classification**: When each document needs individual classification or scoring

### Migration Notes

Existing pipelines using the ML Inference Search Response Processor continue to work unchanged. To enable per-document inference:

1. Add `"one_to_one": true` to your processor configuration
2. Ensure your model accepts single-document input format
3. Consider the increased number of API calls (N documents = N predictions)

## Limitations

- Increased latency due to multiple prediction calls (N documents = N API calls)
- Higher resource consumption for large result sets
- Error in any single prediction can fail the entire response (unless `ignore_failure: true`)

## References

### Documentation
- [Documentation](https://docs.opensearch.org/2.17/search-plugins/search-pipelines/ml-inference-search-response/): ML inference search response processor

### Blog Posts
- [Blog](https://opensearch.org/blog/introduction-to-ml-inference-processors-in-opensearch-review-summarization-and-semantic-search/): Introduction to ML inference processors

### Pull Requests
| PR | Description |
|----|-------------|
| [#2801](https://github.com/opensearch-project/ml-commons/pull/2801) | Support one_to_one in ML Inference Search Response Processor |

### Issues (Design / RFC)
- [Issue #2173](https://github.com/opensearch-project/ml-commons/issues/2173): RFC - ML Inference Processors
- [Issue #2444](https://github.com/opensearch-project/ml-commons/issues/2444): Related feature request

## Related Feature Report

- [Full feature documentation](../../../../features/ml-commons/ml-inference-processor.md)
