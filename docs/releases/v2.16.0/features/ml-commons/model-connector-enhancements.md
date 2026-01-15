---
tags:
  - ml-commons
---
# ML Commons Model & Connector Enhancements

## Summary

OpenSearch v2.16.0 introduces several enhancements to ML Commons model and connector functionality, including automated model interface generation for AWS LLMs, increased execute thread pool size for better agent performance, multi-modal default preprocess function support, and configurable disk circuit breaker settings.

## Details

### What's New in v2.16.0

#### Automated Model Interface Generation for AWS LLMs

When registering a remote model connected to AWS services (Bedrock, Comprehend, Textract), ML Commons now automatically generates the model interface based on the connector configuration. This eliminates the need to manually specify input/output schemas for supported models.

Supported models include:
- Amazon Bedrock: AI21 Labs Jurassic-2, Anthropic Claude v2/v3, Cohere Embed, Titan Embed Text/Multi-Modal
- Amazon Comprehend: DetectDominantLanguage API
- Amazon Textract: DetectDocumentText API

The interface is automatically set during model registration if:
1. The connector specifies `service_name` parameter (e.g., `bedrock`, `comprehend`, `textract`)
2. The connector specifies the model name or API name
3. No custom interface is already provided

#### Execute Thread Pool Size Increase

The execute thread pool size has been increased to improve agent execution performance:

| Setting | Before | After |
|---------|--------|-------|
| Pool Size | `max(1, allocatedProcessors - 1)` | `allocatedProcessors * 4` |
| Queue Size | `10` | `10000` |

This change addresses bottlenecks when running ML agents that use the execute thread pool.

#### Multi-Modal Default Preprocess Function

A new built-in preprocess function `connector.pre_process.multimodal.embedding` simplifies multi-modal embedding workflows. Previously, users needed to write custom painless scripts to handle text and image inputs.

The function:
- Accepts `TextDocsInputDataSet` with text in the first position and optional image (base64) in the second
- Automatically maps to `inputText` and `inputImage` parameters
- Returns `RemoteInferenceInputDataSet` directly if already in that format

#### Disk Circuit Breaker Cluster Settings

The disk circuit breaker threshold is now configurable via cluster settings instead of being hardcoded.

| Setting | Description | Default |
|---------|-------------|---------|
| `plugins.ml_commons.disk_free_space_threshold` | Minimum free disk space before circuit breaker opens | `5gb` |

### Technical Changes

#### ModelInterfaceUtils

New utility class that provides preset model interfaces for AWS services:

```java
// Automatically applied during model registration
ModelInterfaceUtils.updateRegisterModelInputModelInterfaceFieldsByConnector(
    registerModelInput, 
    connector
);
```

#### MultiModalConnectorPreProcessFunction

```java
// Usage in connector configuration
{
  "pre_process_function": "connector.pre_process.multimodal.embedding"
}
```

Input format:
```json
{
  "text_docs": ["input text", "base64_encoded_image"]
}
```

Output format:
```json
{
  "parameters": {
    "inputText": "input text",
    "inputImage": "base64_encoded_image"
  }
}
```

## Limitations

- Automated model interface generation only supports specific AWS models listed above
- Multi-modal preprocess function requires text in the first position; image-only input is not supported
- Disk circuit breaker setting requires cluster restart to take effect initially (dynamic updates work after)

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#2689](https://github.com/opensearch-project/ml-commons/pull/2689) | Automated model interface generation on AWS LLMs | - |
| [#2691](https://github.com/opensearch-project/ml-commons/pull/2691) | Increase execute thread pool size | - |
| [#2500](https://github.com/opensearch-project/ml-commons/pull/2500) | Add multi-modal default preprocess function | [#2364](https://github.com/opensearch-project/ml-commons/issues/2364) |
| [#2634](https://github.com/opensearch-project/ml-commons/pull/2634) | Change disk circuit breaker to cluster settings | [#2639](https://github.com/opensearch-project/ml-commons/issues/2639) |

### Issues
- [#2364](https://github.com/opensearch-project/ml-commons/issues/2364): Add default multi-modal process function in ml-commons
- [#2639](https://github.com/opensearch-project/ml-commons/issues/2639): Tests failing due to disk circuit breaker open
