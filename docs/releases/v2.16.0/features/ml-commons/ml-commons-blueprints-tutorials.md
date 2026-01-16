---
tags:
  - ml-commons
---
# ML Commons Blueprints & Tutorials

## Summary

OpenSearch v2.16.0 adds new connector blueprints and tutorials for ML Commons, including Amazon Textract integration, Cohere embedding models on Bedrock, offline batch inference connectors, cross-encoder reranking on SageMaker, and improved documentation for secrets caching with non-AWS models.

## Details

### What's New in v2.16.0

#### New Connector Blueprints

| Blueprint | Description |
|-----------|-------------|
| Amazon Textract | Connector blueprint for document text extraction using Amazon Textract |
| Cohere Embedding on Bedrock | Blueprints for Cohere embedding models (embed-english-v3, embed-multilingual-v3) via Amazon Bedrock |
| Offline Batch Inference | Connector blueprints for batch inference against SageMaker and OpenAI |

#### New Tutorials

| Tutorial | Description |
|----------|-------------|
| Cross-Encoder Reranking on SageMaker | Guide for deploying and using cross-encoder models on SageMaker for reranking |
| Secrets Caching for Non-AWS Models | Updated tutorials for caching secrets from client side to reduce API calls to secret manager |

#### Blueprint Format Improvements

- Standardized format for all Bedrock model blueprints to enable automated model interface creation
- Tidier format for Amazon managed LLM blueprints to support automated model interface

### Technical Changes

#### Secrets Caching Updates
New IAM permissions required for caching secrets from client side:
- Reduces API calls to secret manager in Amazon OpenSearch Service
- Validated with OpenAI and Cohere integrations

#### Offline Batch Inference
Connector blueprints support batch inference workflows:
- SageMaker batch transform jobs
- OpenAI batch API integration

## Limitations

- Secrets caching requires additional IAM permissions for secret manager access
- Offline batch inference connectors are designed for asynchronous processing, not real-time inference

## References

### Pull Requests
| PR | Description |
|----|-------------|
| [#2562](https://github.com/opensearch-project/ml-commons/pull/2562) | Add Amazon Textract blueprint |
| [#2607](https://github.com/opensearch-project/ml-commons/pull/2607) | Add tutorial for cross-encoder model on SageMaker |
| [#2637](https://github.com/opensearch-project/ml-commons/pull/2637) | Update tutorials for caching secrets for non-AWS models |
| [#2642](https://github.com/opensearch-project/ml-commons/pull/2642) | Make all Bedrock model blueprints in a tidier format |
| [#2667](https://github.com/opensearch-project/ml-commons/pull/2667) | Add connector blueprint for Cohere embedding models in Bedrock |
| [#2692](https://github.com/opensearch-project/ml-commons/pull/2692) | Make all Amazon managed LLM blueprints in a tidier format |
| [#2768](https://github.com/opensearch-project/ml-commons/pull/2768) | Add offline batch inference connector blueprints |

### Related Issues
- [#2488](https://github.com/opensearch-project/ml-commons/issues/2488) - Offline batch inference feature request
