---
tags:
  - domain/ml
  - component/server
  - ml
  - search
---
# ML Commons Tutorials and Blueprints

## Summary

This release adds new tutorials and connector blueprints to ML Commons, including documentation for ColPali multimodal embedding, Ollama local LLM integration, agentic search with LLM-generated queries, and agentic memory with Strands agents. It also includes minor fixes to existing tutorials and additional unit tests.

## Details

### What's New in v3.3.0

This release focuses on expanding ML Commons documentation with new tutorials and blueprints for emerging AI capabilities:

1. **ColPali Blueprint**: A new connector blueprint for multimodal document retrieval using the ColPali model on SageMaker
2. **Ollama Connector Blueprint**: Support for local/self-hosted LLMs using Ollama or any OpenAI-compatible endpoint
3. **Agentic Search Tutorial**: Guide for using QueryPlanningTool with llmGenerated query type
4. **Agentic Memory Tutorial**: Integration guide for OpenSearch agentic memory with Strands agents
5. **Tutorial Improvements**: Updated instance type recommendations and additional unit tests

### Technical Changes

#### New Blueprints

| Blueprint | File | Description |
|-----------|------|-------------|
| ColPali | `sagemaker_connector_copali_blueprint.md` | Multimodal embedding for visual document retrieval |
| Ollama | `ollama_connector_chat_blueprint.md` | Local LLM integration via OpenAI-compatible API |

#### New Tutorials

| Tutorial | File | Description |
|----------|------|-------------|
| Agentic Search | `agentic_search_llm_generated_type.md` | Natural language to DSL query translation |
| Agentic Memory | `agentic_memory_with_strands_agent.md` | Persistent memory for AI agents |
| Conversational Search with Ollama | `conversational_search_with_Ollama.md` | RAG using local LLMs |

### ColPali Blueprint

ColPali is a multimodal embedding model for visual document retrieval. The blueprint enables:

- Text-based predictions with query embeddings
- Image-based predictions with base64-encoded images
- Combined text-and-image predictions with similarity scores

```json
POST /_plugins/_ml/models/_register?deploy=true
{
    "name": "copali model",
    "function_name": "remote",
    "connector": {
        "name": "Amazon SageMaker connector",
        "protocol": "aws_sigv4",
        "parameters": {
            "region": "us-east-1",
            "service_name": "sagemaker"
        },
        "actions": [
            {
                "action_type": "predict",
                "method": "POST",
                "url": "https://runtime.sagemaker.us-east-1.amazonaws.com/endpoints/{{endpoint_name}}/invocations",
                "request_body": "${parameters.inputs}"
            }
        ]
    }
}
```

### Ollama Connector Blueprint

Enables integration with local LLMs running on Ollama or any OpenAI-compatible endpoint:

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "Ollama Connector",
  "protocol": "http",
  "parameters": {
    "endpoint": "127.0.0.1:11434",
    "model": "qwen3:4b"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://${parameters.endpoint}/v1/chat/completions",
      "request_body": "{ \"model\": \"${parameters.model}\", \"messages\": ${parameters.messages} }"
    }
  ]
}
```

### Agentic Search Tutorial

Demonstrates using the `QueryPlanningTool` to convert natural language questions into OpenSearch Query DSL:

```json
GET shipment/_search?search_pipeline=agentic-pipeline
{
    "query": {
        "agentic": {
            "query_text": "How many orders were placed by Diane Goodwin?",
            "query_fields": "customer_full_name"
        }
    }
}
```

### Agentic Memory Tutorial

Shows how to build context-aware AI agents using OpenSearch agentic memory APIs with the Strands Agents framework:

- Store memory across conversations
- Retrieve relevant context via semantic search
- Extract and summarize key facts
- Update or delete memory when information changes

### Tutorial Fixes

| Change | Description |
|--------|-------------|
| Instance type update | Changed suggested instance type from `ml.m5.xlarge` to `ml.m7g.xlarge` in language identification tutorial |

## Limitations

- ColPali requires images in Base64 format
- Ollama connector requires enabling private IP addresses in cluster settings
- Agentic search is an experimental feature
- Agentic memory requires OpenSearch 3.2.0+

## References

### Documentation
- [Connector Blueprints Documentation](https://docs.opensearch.org/3.3/ml-commons-plugin/remote-models/blueprints/)
- [Agentic Memory APIs](https://docs.opensearch.org/latest/ml-commons-plugin/api/agentic-memory-apis/index/)
- [Strands Agents](https://strandsagents.com/latest/): Agent framework documentation
- [ColPali Model](https://huggingface.co/vidore/colpali-v1.3-hf): HuggingFace model page

### Pull Requests
| PR | Description |
|----|-------------|
| [#4130](https://github.com/opensearch-project/ml-commons/pull/4130) | Add ColPali blueprint |
| [#4160](https://github.com/opensearch-project/ml-commons/pull/4160) | Ollama connector blueprint |
| [#4127](https://github.com/opensearch-project/ml-commons/pull/4127) | Add tutorial for agentic search |
| [#4125](https://github.com/opensearch-project/ml-commons/pull/4125) | Tutorial on agentic memory with Strands agents |
| [#4145](https://github.com/opensearch-project/ml-commons/pull/4145) | Change suggested instance type in tutorial |
| [#4124](https://github.com/opensearch-project/ml-commons/pull/4124) | Adding more unit tests |
| [#4126](https://github.com/opensearch-project/ml-commons/pull/4126) | Adding more unit tests |

### Issues (Design / RFC)
- [Issue #4146](https://github.com/opensearch-project/ml-commons/issues/4146): Ollama connector request

## Related Feature Report

- Full feature documentation
