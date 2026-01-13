---
tags:
  - domain/ml
  - component/server
  - indexing
  - ml
  - search
---
# ML Commons Test Fixes

## Summary

This release includes two improvements to the ML Commons plugin: a fix for the Search Index Tool integration tests to support multi-node clusters, and a new tutorial for integrating Amazon Bedrock Guardrails with OpenSearch ML models.

## Details

### What's New in v2.17.0

#### 1. Multi-Node Cluster Test Fix

The Search Index Tool integration tests were previously excluded from multi-node cluster test runs due to issues with exception message handling. This fix removes the exclusion, enabling the tests to run successfully in both single-node and multi-node cluster configurations.

**Problem**: The `RestSearchIndexToolIT` tests failed when running with multiple nodes (`-PnumNodes=3`) because concrete exception messages could not be reliably retrieved in a distributed environment.

**Solution**: The test exclusion logic was removed from `plugin/build.gradle`, allowing the tests to run in multi-node clusters.

#### 2. Bedrock Guardrails Tutorial

A comprehensive tutorial was added demonstrating two methods to integrate Amazon Bedrock Guardrails with OpenSearch ML models:

**Method 1: Bedrock Guardrails Independent API**
- Create a dedicated connector for the Bedrock Guardrails endpoint
- Register a guardrail model that validates input before processing
- Configure the main model to use the guardrail model for input validation

**Method 2: Embedded Guardrails via Model Inference API**
- Configure guardrail headers directly in the Bedrock model connector
- Use `post_process_function` to handle guardrail intervention responses
- Simpler setup with guardrails embedded in the model invocation

### Technical Changes

#### Build Configuration Change

```groovy
// Removed from plugin/build.gradle
if (_numNodes > 1) {
    filter {
        excludeTestsMatching "org.opensearch.ml.rest.RestSearchIndexToolIT.*"
    }
}
```

#### New Tutorial File

Added `docs/tutorials/guardrails/use_bedrock_guardrails.md` with:
- Step-by-step connector configuration
- Model registration with guardrails
- Example requests and responses
- Both independent API and embedded approaches

### Usage Example

**Bedrock Guardrails Connector:**
```json
POST _plugins/_ml/connectors/_create
{
  "name": "BedRock Guardrail Connector",
  "protocol": "aws_sigv4",
  "parameters": {
    "region": "us-east-1",
    "service_name": "bedrock",
    "source": "INPUT"
  },
  "actions": [{
    "action_type": "predict",
    "method": "POST",
    "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/guardrail/<guardrailId>/version/1/apply"
  }]
}
```

**Model with Input Guardrail:**
```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "Bedrock Claude V2 model",
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

- The Bedrock Guardrails tutorial requires AWS credentials with appropriate permissions
- Guardrail configuration requires creating and managing guardrails in Amazon Bedrock console first

## References

### Documentation
- [OpenSearch Guardrails Documentation](https://opensearch.org/docs/latest/ml-commons-plugin/remote-models/guardrails/): Official guardrails documentation
- [AWS Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-create.html): Creating guardrails in Amazon Bedrock

### Pull Requests
| PR | Description |
|----|-------------|
| [#2407](https://github.com/opensearch-project/ml-commons/pull/2407) | Test: recover search index tool IT in multi node cluster |
| [#2695](https://github.com/opensearch-project/ml-commons/pull/2695) | Add tutorial for Bedrock Guardrails |

### Issues (Design / RFC)
- [Issue #2362](https://github.com/opensearch-project/ml-commons/issues/2362): Bug report for multi-node cluster test failure

## Related Feature Report

- [Full feature documentation](../../../../features/ml-commons/ml-commons-test-fixes.md)
