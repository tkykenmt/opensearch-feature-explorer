---
tags:
  - ml-commons
---
# ML Commons Tutorials

## Summary

OpenSearch v2.19.0 adds new tutorials and connector blueprints for ML Commons, including support for DeepSeek chat models, Amazon Bedrock cross-encoder reranking models, Cohere multi-modal embeddings, asymmetric embedding models, and ML inference with Cohere rerank. A bug fix for the BGE-rerank-m3-v2 SageMaker tutorial is also included.

## Details

### What's New in v2.19.0

#### New Connector Blueprints

| Blueprint | Description |
|-----------|-------------|
| DeepSeek Chat | Connector blueprint for DeepSeek Chat model integration |
| Cohere Multi-Modal | Blueprint for Cohere multi-modal embedding model (backport) |

#### New Tutorials

| Tutorial | Description |
|----------|-------------|
| Amazon Bedrock Cross-Encoder | Tutorials for Amazon Rerank 1.0 and Cohere Rerank 3.5 models on Bedrock |
| Asymmetric Embedding Models | Tutorial for using asymmetric models like multilingual-e5-small with Docker |
| ML Inference with Cohere Rerank | Tutorial using ML inference processor with by_field rerank type |
| BGE-reranker-m3-v2 on SageMaker | Tutorial for multilingual cross-encoder model on SageMaker |

### Technical Changes

#### DeepSeek Connector Blueprint

The DeepSeek connector blueprint enables integration with DeepSeek Chat API for question-answering capabilities:

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "DeepSeek Chat",
  "protocol": "http",
  "parameters": {
    "endpoint": "api.deepseek.com",
    "model": "deepseek-chat",
    "stream": false
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://${parameters.endpoint}/v1/chat/completions",
      "request_body": "{ \"model\": \"${parameters.model}\", \"messages\": ${parameters.messages}, \"stream\":${parameters.stream} }"
    }
  ]
}
```

#### Amazon Bedrock Cross-Encoder Tutorials

Two new tutorials for reranking pipelines using Amazon Bedrock:

- **Amazon Rerank 1.0**: Native Amazon reranking model with `amazon.rerank-v1:0`
- **Cohere Rerank 3.5**: Cohere model via Bedrock with `cohere.rerank-v3-5:0`

Both tutorials demonstrate:
- Creating connectors with AWS SigV4 authentication
- Pre/post processing functions for reranking pipeline compatibility
- Search pipeline configuration with rerank processor

#### Asymmetric Embedding Model Tutorial

Tutorial for running semantic search with asymmetric embedding models:

- Uses `intfloat/multilingual-e5-small` model from Hugging Face
- Demonstrates model preparation, registration, and deployment
- Shows ML inference processor configuration for ingest and search pipelines
- Includes query and passage prefix handling (`query: ` and `passage: `)

#### ML Inference with Cohere Rerank

Tutorial demonstrating the `by_field` rerank type (introduced in v2.18) with Cohere Rerank model:

- Uses ML inference processor to invoke Cohere rerank API
- Combines with by_field rerank processor to reorder results
- Alternative approach to the traditional reranking pipeline

#### Bug Fix

- Fixed `post_process_function` in the BGE-rerank-m3-v2 SageMaker tutorial

## Limitations

- DeepSeek connector requires API key from DeepSeek
- Amazon Bedrock tutorials require appropriate IAM permissions and model access
- Asymmetric model tutorial requires local model file hosting during registration
- Cohere rerank tutorial requires Cohere API key

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#3436](https://github.com/opensearch-project/ml-commons/pull/3436) | Add DeepSeek connector blueprint |  |
| [#3278](https://github.com/opensearch-project/ml-commons/pull/3278) | Add tutorials for cross encoder models on Amazon Bedrock | [#3245](https://github.com/opensearch-project/ml-commons/issues/3245) |
| [#3258](https://github.com/opensearch-project/ml-commons/pull/3258) | Tutorial for using Asymmetric models | [#3255](https://github.com/opensearch-project/ml-commons/issues/3255) |
| [#3398](https://github.com/opensearch-project/ml-commons/pull/3398) | Tutorial for ml inference with cohere rerank model |  |
| [#3232](https://github.com/opensearch-project/ml-commons/pull/3232) | Backport: adding blueprint doc for cohere multi-modal model |  |
| [#2848](https://github.com/opensearch-project/ml-commons/pull/2848) | Add tutorial for bge-reranker-m3-v2 on SageMaker |  |
| [#3296](https://github.com/opensearch-project/ml-commons/pull/3296) | Fix post_process_function on bge-rerank-m3-v2 tutorial | [#3247](https://github.com/opensearch-project/ml-commons/issues/3247) |
