---
tags:
  - flow-framework
---
# Flow Framework Bugfixes

## Summary

OpenSearch 2.16.0 includes three bug fixes for the Flow Framework plugin that improve error handling during deprovisioning and index creation operations.

## Details

### What's New in v2.16.0

#### NOT_FOUND Exception Handling for Deprovision

When deprovisioning workflows, the `DeleteModelStep` and `DeleteAgentStep` now handle `NOT_FOUND` exceptions as successful deletions. Previously, if a model or agent was manually deleted before deprovisioning, the workflow would fail because ML Commons throws an exception when the resource doesn't exist. This fix treats missing resources as already deleted, allowing deprovisioning to complete successfully.

#### Index Mapping _doc Wrapper Fix

The `FlowFrameworkIndicesHandler` now correctly wraps index mappings in the required `_doc` key when creating system indices. This aligns with the `CreateIndexRequest` javadoc requirements and ensures proper index initialization with the specified mapping rather than inferring mappings from documents.

#### FlowFrameworkException Status Code Fix

The `FlowFrameworkException` class now properly extends `OpenSearchException` and overrides the `status()` method. This ensures that `ExceptionsHelper.status()` returns the correct HTTP status code instead of defaulting to 500 (INTERNAL_SERVER_ERROR). For example, a workflow ID not found error now correctly returns a 404 status.

## Limitations

- These fixes are specific to error handling scenarios and do not change normal workflow behavior

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#805](https://github.com/opensearch-project/flow-framework/pull/805) | Handle Not Found deprovision exceptions as successful deletions | [#803](https://github.com/opensearch-project/flow-framework/issues/803) |
| [#809](https://github.com/opensearch-project/flow-framework/pull/809) | Wrap CreateIndexRequest mappings in _doc key as required | [#798](https://github.com/opensearch-project/flow-framework/issues/798) |
| [#811](https://github.com/opensearch-project/flow-framework/pull/811) | Have FlowFrameworkException status recognized by ExceptionsHelper | [#810](https://github.com/opensearch-project/flow-framework/issues/810) |
