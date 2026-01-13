---
tags:
  - domain/ml
  - component/server
  - dashboards
  - indexing
  - ml
  - security
---
# ML Commons Enhancements

## Summary

OpenSearch v3.4.0 introduces several enhancements to ML Commons focused on security, scalability, and multi-resource support. Key improvements include marking sensitive connector parameters for filtering, updating resource sharing client to use resource types instead of indexes, and significantly increasing batch inference/ingestion task limits.

## Details

### What's New in v3.4.0

#### Sensitive Parameter Filtering in Connector APIs

The connector and model registration APIs now implement `RestRequestFilter` to mark sensitive parameters that should be filtered from logs and audit trails. This prevents accidental exposure of credentials and authorization tokens.

**Filtered Fields:**
- `credential` - API keys and secrets in connector configurations
- `*.Authorization` - Authorization headers in connector actions
- `connector.credential` - Nested credentials in model registration

**Affected APIs:**
- Create Connector (`POST /_plugins/_ml/connectors/_create`)
- Update Connector (`PUT /_plugins/_ml/connectors/{connector_id}`)
- Register Model (`POST /_plugins/_ml/models/_register`)
- Update Model (`PUT /_plugins/_ml/models/{model_id}`)

#### Resource Sharing Client Enhancement

The resource sharing client now accepts resource type instead of resource index name. This change supports the security plugin's ability to handle multiple resource types within the same index (similar to Dashboards saved objects).

**Technical Change:**
```java
// Before
rsc.getAccessibleResourceIds(ML_MODEL_GROUP_INDEX, listener);
rsc.verifyAccess(modelGroupId, ML_MODEL_GROUP_INDEX, action, listener);

// After  
rsc.getAccessibleResourceIds(ML_MODEL_GROUP_RESOURCE_TYPE, listener);
rsc.verifyAccess(modelGroupId, ML_MODEL_GROUP_RESOURCE_TYPE, action, listener);
```

This enables future support for more granular resource-level access control.

#### Increased Batch Task Limits

Based on customer feedback, the maximum limits for batch inference and batch ingestion tasks have been significantly increased to support larger workloads.

| Setting | Previous Default | New Default | Previous Max | New Max |
|---------|------------------|-------------|--------------|---------|
| `plugins.ml_commons.max_batch_inference_tasks` | 10 | 100 | 500 | 10,000 |
| `plugins.ml_commons.max_batch_ingestion_tasks` | 10 | 100 | 500 | 10,000 |

### Configuration

#### Batch Task Settings

```yaml
# opensearch.yml
plugins.ml_commons.max_batch_inference_tasks: 100   # Default: 100, Range: [0, 10000]
plugins.ml_commons.max_batch_ingestion_tasks: 100   # Default: 100, Range: [0, 10000]
```

These settings are dynamic and can be updated at runtime:

```json
PUT _cluster/settings
{
  "persistent": {
    "plugins.ml_commons.max_batch_inference_tasks": 500,
    "plugins.ml_commons.max_batch_ingestion_tasks": 500
  }
}
```

### Usage Example

#### Creating a Connector with Sensitive Credentials

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "OpenAI Connector",
  "description": "Connector for OpenAI GPT models",
  "version": 1,
  "protocol": "http",
  "parameters": {
    "endpoint": "api.openai.com",
    "model": "gpt-4"
  },
  "credential": {
    "openAI_key": "sk-..."
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://api.openai.com/v1/chat/completions",
      "headers": {
        "Authorization": "Bearer ${credential.openAI_key}"
      }
    }
  ]
}
```

The `credential` and `Authorization` fields are now automatically filtered from request logging.

### Migration Notes

- **No breaking changes** - Existing connectors and models continue to work
- **Security improvement** - Sensitive parameters are now filtered by default
- **Capacity planning** - Review batch task limits if running large-scale inference workloads

## Limitations

- Sensitive parameter filtering only applies to REST API request logging; stored credentials remain encrypted in the connector index
- Resource type changes require corresponding security plugin updates (v3.4.0+)

## References

### Documentation
- [ML Commons Cluster Settings](https://docs.opensearch.org/3.0/ml-commons-plugin/cluster-settings/): Configuration options
- [Create Connector API](https://docs.opensearch.org/3.0/ml-commons-plugin/api/connector-apis/create-connector/): Connector creation documentation
- [Batch Predict API](https://docs.opensearch.org/3.0/ml-commons-plugin/api/model-apis/batch-predict/): Batch inference documentation
- [Security PR #5713](https://github.com/opensearch-project/security/pull/5713): Related security plugin changes for resource type support

### Pull Requests
| PR | Description |
|----|-------------|
| [#4308](https://github.com/opensearch-project/ml-commons/pull/4308) | Declare credential and *.Authorization as sensitive param in create connector API |
| [#4333](https://github.com/opensearch-project/ml-commons/pull/4333) | Pass resourceType instead of resourceIndex to resourceSharingClient |
| [#4474](https://github.com/opensearch-project/ml-commons/pull/4474) | Allow higher maximum number of batch inference job tasks |

## Related Feature Report

- [Full feature documentation](../../../features/ml-commons/ml-commons-enhancements.md)
