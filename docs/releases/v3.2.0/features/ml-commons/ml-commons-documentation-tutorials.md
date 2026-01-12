# ML Commons Documentation & Tutorials

## Summary

This release item adds comprehensive documentation and tutorials to the ML Commons repository, covering multi-modal search, neural sparse models, semantic highlighting, language identification, agentic RAG, and e-commerce demos. These additions help users understand and implement ML-powered features in OpenSearch.

## Details

### What's New in v3.2.0

Seven documentation and tutorial PRs were merged to enhance the ML Commons repository:

1. **Multi-Modal Search Tutorial** - Step-by-step guide for using ML inference processor with Bedrock Titan multi-modal embedding model
2. **Semantic Highlighter Blueprint** - AWS SageMaker blueprint for deploying semantic highlighter models
3. **Neural Sparse Remote Model Documentation** - Guide for creating neural sparse models on SageMaker
4. **Language Identification Tutorial** - Using ML inference ingest processor for automatic language detection
5. **Agentic RAG Tutorial** - Building retrieval-augmented generation with conversational agents
6. **E-commerce Demo Notebook** - Jupyter notebook demonstrating multi-modal search for e-commerce
7. **Aleph Alpha Blueprint Fix** - Updated broken link in the Aleph Alpha blueprint

### Technical Changes

#### New Tutorials Added

| Tutorial | Location | Description |
|----------|----------|-------------|
| Multi-Modal Search | `docs/tutorials/ml_inference/semantic_search/bedrock_titan_multi-modal_embedding_model.md` | Bedrock Titan multi-modal embedding with ML inference processors |
| Language Identification | `docs/tutorials/ml_inference/language_identification/ml_inference_with_language_identification_ingest.md` | Automatic language detection during ingest |
| Agentic RAG | `docs/tutorials/agent_framework/Agentic_RAG.md` | Building RAG with conversational agents |
| E-commerce Demo | `docs/tutorials/ml_inference/ecommerce_demo.ipynb` | Multi-modal search notebook |

#### New Blueprints Added

| Blueprint | Location | Description |
|-----------|----------|-------------|
| Semantic Highlighter | `docs/remote_inference_blueprints/standard_blueprints/sagemaker_semantic_highlighter_standard_blueprint.md` | SageMaker semantic highlighter model |
| Neural Sparse | `docs/model_serving_framework/deploy_sparse_model_to_SageMaker.ipynb` | Neural sparse model deployment |

### Usage Examples

#### Multi-Modal Search with Bedrock Titan

```json
POST _plugins/_ml/connectors/_create
{
  "name": "Amazon Bedrock Connector: bedrock Titan multi-modal embedding model",
  "protocol": "aws_sigv4",
  "parameters": {
    "region": "us-east-1",
    "service_name": "bedrock",
    "model": "amazon.titan-embed-image-v1"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/model/${parameters.model}/invoke",
      "request_body": "{\"inputText\": \"${parameters.inputText:-null}\", \"inputImage\": \"${parameters.inputImage:-null}\"}"
    }
  ]
}
```

#### Language Identification Pipeline

```json
PUT _ingest/pipeline/language_identification_pipeline
{
  "processors": [
    {
      "ml_inference": {
        "model_id": "your_model_id",
        "input_map": [
          { "inputs": "name" },
          { "inputs": "notes" }
        ],
        "output_map": [
          { "predicted_name_language": "response[0].label" },
          { "predicted_notes_language": "response[0].label" }
        ]
      }
    },
    {
      "copy": {
        "source_field": "name",
        "target_field": "name_{{predicted_name_language}}"
      }
    }
  ]
}
```

#### Agentic RAG Agent

```json
POST _plugins/_ml/agents/_register
{
  "name": "RAG Agent",
  "type": "conversational",
  "llm": {
    "model_id": "your_llm_id",
    "parameters": {
      "system_prompt": "You are a helpful assistant..."
    }
  },
  "tools": [
    {
      "type": "SearchIndexTool",
      "name": "retrieve_population_data",
      "parameters": {
        "query": {
          "query": {
            "neural": {
              "embedding_field": {
                "query_text": "${parameters.question}",
                "model_id": "your_embedding_model_id"
              }
            }
          }
        }
      }
    }
  ]
}
```

## Limitations

- Tutorials require specific AWS services (Bedrock, SageMaker) with appropriate permissions
- Multi-modal embedding requires images in Base64 format
- Language identification model supports limited languages based on the underlying model

## References

### Documentation
- [ML Commons Connector Blueprints](https://docs.opensearch.org/3.0/ml-commons-plugin/remote-models/blueprints/)
- [ML Inference Processor](https://docs.opensearch.org/3.0/ingest-pipelines/processors/ml-inference/)
- [OpenSearch Tutorials](https://docs.opensearch.org/3.0/tutorials/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#3576](https://github.com/opensearch-project/ml-commons/pull/3576) | Add multi modal tutorial using ml inference processor |
| [#3879](https://github.com/opensearch-project/ml-commons/pull/3879) | Add blueprint for semantic highlighter model on AWS Sagemaker |
| [#3857](https://github.com/opensearch-project/ml-commons/pull/3857) | Add Documentation for creating Neural Sparse Remote Model |
| [#3966](https://github.com/opensearch-project/ml-commons/pull/3966) | Add tutorials for language_identification during ingest |
| [#3980](https://github.com/opensearch-project/ml-commons/pull/3980) | Update link to the model in the aleph alpha blueprint |
| [#4045](https://github.com/opensearch-project/ml-commons/pull/4045) | Add agentic rag tutorial |
| [#3944](https://github.com/opensearch-project/ml-commons/pull/3944) | Notebook for step by step in multi-modal search in ml-inference processor |

## Related Feature Report

- [Full feature documentation](../../../features/ml-commons/ml-commons-documentation-tutorials.md)
