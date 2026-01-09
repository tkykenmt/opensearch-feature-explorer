# ML Commons Test Fixes

## Summary

This feature tracks test infrastructure improvements and documentation additions for the ML Commons plugin, including fixes for multi-node cluster integration tests and tutorials for integrating external services like Amazon Bedrock Guardrails.

## Details

### Architecture

```mermaid
graph TB
    subgraph "ML Commons Testing"
        IT[Integration Tests]
        SIT[Search Index Tool IT]
        MN[Multi-Node Support]
    end
    
    subgraph "Guardrails Integration"
        GR[Guardrails Model]
        BR[Bedrock Runtime]
        CM[Claude Model]
    end
    
    IT --> SIT
    SIT --> MN
    GR --> BR
    CM --> GR
```

### Components

| Component | Description |
|-----------|-------------|
| Search Index Tool IT | Integration tests for the Search Index Tool functionality |
| Multi-Node Test Support | Enables running integration tests across distributed clusters |
| Bedrock Guardrails Tutorial | Documentation for integrating Amazon Bedrock Guardrails |

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `numNodes` | Number of nodes for integration test cluster | 1 |
| `guardrails.input_guardrail.model_id` | Model ID for input validation | - |
| `guardrails.input_guardrail.response_filter` | JSONPath to extract guardrail action | - |
| `guardrails.input_guardrail.response_validation_regex` | Regex to validate allowed responses | - |

### Usage Example

**Running Multi-Node Integration Tests:**
```bash
./gradlew opensearch-ml-plugin:integTest \
  --tests "org.opensearch.ml.rest.RestSearchIndexToolIT" \
  -PnumNodes=3
```

**Configuring Bedrock Guardrails:**
```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "Model with Guardrails",
  "function_name": "remote",
  "connector_id": "<connector_id>",
  "guardrails": {
    "input_guardrail": {
      "model_id": "<guardrail_model_id>",
      "response_filter": "$.action",
      "response_validation_regex": "^\"NONE\"$"
    },
    "type": "model"
  }
}
```

## Limitations

- Bedrock Guardrails require AWS credentials and pre-configured guardrails in AWS console
- Multi-node test execution requires additional system resources

## Related PRs

| Version | PR | Description |
|---------|-----|-------------|
| v2.17.0 | [#2407](https://github.com/opensearch-project/ml-commons/pull/2407) | Test: recover search index tool IT in multi node cluster |
| v2.17.0 | [#2695](https://github.com/opensearch-project/ml-commons/pull/2695) | Add tutorial for Bedrock Guardrails |

## References

- [Issue #2362](https://github.com/opensearch-project/ml-commons/issues/2362): Original bug report for multi-node test failure
- [OpenSearch Guardrails Documentation](https://opensearch.org/docs/latest/ml-commons-plugin/remote-models/guardrails/)
- [AWS Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-create.html)

## Change History

- **v2.17.0** (2024-09-17): Added multi-node cluster test support and Bedrock Guardrails tutorial
