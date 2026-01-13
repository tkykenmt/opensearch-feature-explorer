---
tags:
  - flow-framework
---
# Flow Framework

## Summary

OpenSearch v2.19.0 introduces significant enhancements to the Flow Framework plugin, including multi-tenancy support with remote metadata storage, synchronous workflow provisioning with configurable timeouts, and RBAC bug fixes for workflow state management.

## Details

### What's New in v2.19.0

#### Multi-tenancy Support

Flow Framework now supports multi-tenancy using the remote metadata SDK client, enabling stateless plugin operation with external data stores. This allows cloud providers to offer tenant-isolated workflow management.

**Configuration:**
```yaml
plugins.flow_framework.multi_tenancy_enabled: true
plugins.flow_framework.remote_metadata_type: AWSDynamoDB
plugins.flow_framework.remote_metadata_endpoint: <REMOTE_ENDPOINT>
plugins.flow_framework.remote_metadata_region: <AWS_REGION>
plugins.flow_framework.remote_metadata_service_name: <SERVICE_NAME>
```

**Supported Storage Backends:**
- Remote OpenSearch clusters
- Amazon DynamoDB

#### Synchronous Provisioning

A new `wait_for_completion_timeout` parameter enables synchronous workflow provisioning, eliminating the need to poll the status API.

**Usage:**
```bash
# Provision with timeout
POST /_plugins/_flow_framework/workflow/<id>/_provision?wait_for_completion_timeout=60s

# Reprovision with timeout
POST /_plugins/_flow_framework/workflow/<id>/_reprovision?wait_for_completion_timeout=30s
```

**Response (on completion):**
```json
{
    "workflow_id": "K13IR5QBEpCfUu_-AQdU",
    "state": "COMPLETED",
    "resources_created": [
        {
            "workflow_step_name": "create_connector",
            "workflow_step_id": "create_connector_1",
            "resource_id": "LF3IR5QBEpCfUu_-Awd_",
            "resource_type": "connector_id"
        }
    ]
}
```

**Response (on timeout):**
```json
{
    "workflow_id": "SmACR5QBdrR0lYdqgHa9",
    "state": "PROVISIONING",
    "resources_created": [...]
}
```

#### RBAC Bug Fix for Workflow State

Fixed an issue where users couldn't access workflow state after deleting the template when backend role filtering was enabled. The fix reads user information from the workflow state index as a fallback when the template is not present.

**Affected Operations:**
- Delete workflow with `clear_status=true`
- Deprovision workflow
- Get workflow state

### Technical Changes

| Change | Description |
|--------|-------------|
| Multi-tenancy client | Uses remote metadata SDK client from ML Commons for tenant-aware storage |
| Synchronous provisioning | Added `wait_for_completion_timeout` parameter to provision and reprovision APIs |
| RBAC fallback | User info now stored in workflow state for access control when template is deleted |
| Log4j improvements | Replaced string concatenation with ParameterizedMessage for better readability |

## Limitations

- Multi-tenancy requires external storage backend configuration
- Synchronous provisioning timeout may return partial results if exceeded
- Remote storage backends may introduce additional latency

## References

### Documentation
- [Provision Workflow API](https://docs.opensearch.org/2.19/automating-configurations/api/provision-workflow/)
- [Plugin as a Service](https://docs.opensearch.org/2.19/developer-documentation/plugin-as-a-service/index/)
- [Workflow Settings](https://docs.opensearch.org/2.19/automating-configurations/workflow-settings/)

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#980](https://github.com/opensearch-project/flow-framework/pull/980) | Implement multi-tenancy in Flow Framework | - |
| [#990](https://github.com/opensearch-project/flow-framework/pull/990) | Add synchronous execution option to workflow provisioning | [#967](https://github.com/opensearch-project/flow-framework/issues/967) |
| [#998](https://github.com/opensearch-project/flow-framework/pull/998) | Fix RBAC fetching from workflow state when template is not present | [#986](https://github.com/opensearch-project/flow-framework/issues/986) |
| [#943](https://github.com/opensearch-project/flow-framework/pull/943) | Replace String concatenation with Log4j ParameterizedMessage | [#905](https://github.com/opensearch-project/flow-framework/issues/905) |
