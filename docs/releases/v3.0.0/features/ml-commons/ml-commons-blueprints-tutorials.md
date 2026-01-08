# ML Commons Blueprints & Tutorials

## Summary

This release item adds new connector blueprints and tutorials to ML Commons for v3.0.0. The changes include standard blueprints for vector search (without pre/post processing functions), a blueprint for Claude 3.7 on Bedrock, Azure OpenAI embedding blueprint, and RAG tutorials for OpenAI and Bedrock.

## Details

### What's New in v3.0.0

This release introduces several documentation and blueprint improvements:

1. **Standard Blueprints for Vector Search** - New simplified blueprints that work with ML inference processor for input/output mapping (recommended for OpenSearch 2.14+)
2. **Claude 3.7 Blueprint** - Support for Anthropic's first hybrid reasoning model on Amazon Bedrock
3. **Azure OpenAI Embedding Blueprint** - Standard blueprint for text-embedding-ada-002 on Azure
4. **RAG Tutorials** - Comprehensive tutorials for conversational search with OpenAI and Bedrock Claude

### Technical Changes

#### New Standard Blueprints

Standard blueprints are designed for connectors that pass input directly to the model without requiring pre/post processing functions. These are recommended for OpenSearch 2.14+.

| Blueprint | Provider | Model |
|-----------|----------|-------|
| Bedrock Titan Embedding | AWS | amazon.titan-embed-text-v1/v2 |
| Bedrock Titan Multimodal | AWS | amazon.titan-embed-image-v1 |
| Bedrock Cohere English | AWS | cohere.embed-english-v3 |
| Bedrock Cohere Multilingual | AWS | cohere.embed-multilingual-v3 |
| Cohere Text Embedding | Cohere | embed-english-v3.0/v2.0 |
| Cohere Image Embedding | Cohere | embed-multimodal-v3.0/v2.0 |
| OpenAI Embedding | OpenAI | text-embedding-ada-002 |
| Azure OpenAI Embedding | Azure | text-embedding-ada-002 |

#### Claude 3.7 Blueprint Features

Claude 3.7 Sonnet supports two modes:
- **Standard mode**: Regular inference with configurable temperature and max tokens
- **Extended thinking mode**: Enables deeper reasoning with `budget_tokens` parameter

```json
// Extended thinking mode connector
{
  "parameters": {
    "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    "budget_tokens": 1024
  },
  "request_body": "{ \"thinking\": {\"type\": \"enabled\", \"budget_tokens\": ${parameters.budget_tokens} } }"
}
```

#### RAG Tutorial Highlights

The new tutorials demonstrate:
- Conversational search with memory persistence
- Search pipeline configuration with RAG processor
- Both Bedrock Converse API and Invoke API approaches
- OpenAI GPT-4o integration for conversational search

### Usage Example

Creating a standard blueprint connector (no pre/post processing):

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "Cohere Embed Model",
  "description": "Standard connector for Cohere embedding",
  "version": "1",
  "protocol": "http",
  "credential": {
    "cohere_key": "<API_KEY>"
  },
  "parameters": {
    "model": "embed-english-v3.0",
    "input_type": "search_document",
    "truncate": "END"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://api.cohere.ai/v1/embed",
      "headers": {
        "Authorization": "Bearer ${credential.cohere_key}"
      },
      "request_body": "{ \"texts\": ${parameters.texts}, \"model\": \"${parameters.model}\" }"
    }
  ]
}
```

### Migration Notes

- Standard blueprints are recommended for new implementations on OpenSearch 2.14+
- Legacy blueprints with pre/post processing functions remain available for existing implementations
- Claude 3.7 requires inference profile ID (e.g., `us.anthropic.claude-3-7-sonnet-20250219-v1:0`)

## Limitations

- Claude 3.7 extended thinking mode requires additional token budget configuration
- Standard blueprints require ML inference processor for input/output mapping
- Azure OpenAI requires proper endpoint and deployment name configuration

## Related PRs

| PR | Description |
|----|-------------|
| [#3659](https://github.com/opensearch-project/ml-commons/pull/3659) | Add standard blueprint for vector search |
| [#3584](https://github.com/opensearch-project/ml-commons/pull/3584) | Add blueprint for Claude 3.7 on Bedrock |
| [#3725](https://github.com/opensearch-project/ml-commons/pull/3725) | Add standard blueprint for Azure embedding ada2 |
| [#3612](https://github.com/opensearch-project/ml-commons/pull/3612) | Fix template query link |
| [#2975](https://github.com/opensearch-project/ml-commons/pull/2975) | Add tutorial for RAG of OpenAI and Bedrock |

## References

- [Issue #3619](https://github.com/opensearch-project/ml-commons/issues/3619): Standard blueprints feature request
- [Connector Blueprints Documentation](https://docs.opensearch.org/3.0/ml-commons-plugin/remote-models/blueprints/)
- [Supported Connectors](https://docs.opensearch.org/3.0/ml-commons-plugin/remote-models/supported-connectors/)
- [AWS Blog: Claude 3.7 on Bedrock](https://aws.amazon.com/blogs/aws/anthropics-claude-3-7-sonnet-the-first-hybrid-reasoning-model-is-now-available-in-amazon-bedrock/)

## Related Feature Report

- [Full feature documentation](../../../features/ml-commons/ml-commons-blueprints.md)
