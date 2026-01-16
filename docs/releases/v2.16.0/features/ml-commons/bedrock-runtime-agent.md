---
tags:
  - ml-commons
---
# Bedrock Runtime Agent

## Summary

OpenSearch v2.16.0 adds support for Amazon Bedrock Runtime Agent, enabling integration with Amazon Bedrock Knowledge Base. This enhancement also improves agent tool execution by passing all parameters including chat history to tools.

## Details

### What's New in v2.16.0

1. **Bedrock Agent Runtime URL Support**: Added `bedrock-agent-runtime` to the allowed connector URL patterns, enabling connections to Amazon Bedrock Knowledge Base service.

2. **Enhanced Tool Parameter Passing**: Modified `MLChatAgentRunner` to pass all parameters (including `chat_history`) to tools during execution, enabling tools to access full conversation context.

### Technical Changes

**Connector URL Allowlist Update**

The `plugins.ml_commons.trusted_connector_endpoints_regex` setting now includes:
```
^https://bedrock-agent-runtime\..*[a-z0-9-]\.amazonaws\.com/.*$
```

This allows connectors to call Amazon Bedrock Agent Runtime APIs for knowledge base retrieval.

**Tool Parameter Enhancement**

In `MLChatAgentRunner.runTool()`, tool execution now receives merged parameters:
```java
Map<String, String> parameters = new HashMap<>();
parameters.putAll(tmpParameters);  // Includes chat_history
parameters.putAll(toolParams);
tools.get(action).run(parameters, toolListener);
```

### Usage Example

**Create a Bedrock Knowledge Base Connector:**
```json
POST /_plugins/_ml/connectors/_create
{
  "name": "Amazon Bedrock Connector: knowledge",
  "description": "The connector to the Bedrock knowledge base",
  "version": 1,
  "protocol": "aws_sigv4",
  "parameters": {
    "region": "<YOUR_AWS_REGION>",
    "service_name": "bedrock"
  },
  "credential": {
    "access_key": "<YOUR_ACCESS_KEY>",
    "secret_key": "<YOUR_SECRET_KEY>"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://bedrock-agent-runtime.<region>.amazonaws.com/knowledgebases/<kb_id>/retrieve",
      "headers": {
        "content-type": "application/json",
        "x-amz-content-sha256": "required"
      },
      "request_body": "{\"retrievalQuery\": {\"text\": \"${parameters.text}\"}}"
    }
  ]
}
```

**Register a model using the connector:**
```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "bedrock: knowledge base",
  "function_name": "remote",
  "description": "Connector for bedrock knowledge base",
  "connector_id": "<connector_id>"
}
```

**Query the knowledge base:**
```json
POST /_plugins/_ml/models/<model_id>/_predict
{
  "parameters": {
    "text": "your search query"
  }
}
```

## Limitations

- Requires valid AWS credentials with appropriate Bedrock permissions
- Knowledge base must be pre-configured in Amazon Bedrock
- AWS SigV4 authentication is required for Bedrock Agent Runtime APIs

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#2651](https://github.com/opensearch-project/ml-commons/pull/2651) | Add bedrock runtime agent for knowledge base | - |
| [#2714](https://github.com/opensearch-project/ml-commons/pull/2714) | Pass all parameters including chat_history to run tools | - |

### Documentation
- [Connectors](https://docs.opensearch.org/2.16/ml-commons-plugin/remote-models/connectors/)
- [Connector Blueprints](https://docs.opensearch.org/2.16/ml-commons-plugin/remote-models/blueprints/)
