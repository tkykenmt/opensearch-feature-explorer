---
tags:
  - flow-framework
---
# Flow Framework Enhancements

## Summary

OpenSearch 2.16.0 introduces three enhancements to the Flow Framework plugin: partial field updates for provisioned workflows, the `allow_delete` parameter for the Deprovision API, and improved builder patterns for Template and WorkflowState classes.

## Details

### What's New in v2.16.0

#### Partial Field Updates for Provisioned Workflows

Previously, the Update Workflow API rejected all updates to workflows that had been provisioned, even for non-critical fields like `name`, `description`, or `ui_metadata`. This prevented users from making simple metadata changes without deprovisioning first.

The new `update_fields=true` parameter allows updating specific fields on a provisioned workflow without affecting the underlying resources:

```bash
PUT /_plugins/_flow_framework/workflow/<workflow_id>?update_fields=true
{
  "name": "new-workflow-name",
  "description": "Updated description"
}
```

This enables:
- Updating workflow metadata (name, description) on provisioned workflows
- Saving frontend UI configuration stored in `ui_metadata` without disrupting deployed resources
- Lightweight saves during iterative workflow development

#### Deprovision API allow_delete Parameter

The Deprovision API now supports an `allow_delete` parameter for explicitly deleting resources that were previously protected from automatic deletion. Resources like indexes, ingest pipelines, and search pipelines require explicit consent to delete due to potential data loss.

```bash
POST /_plugins/_flow_framework/workflow/<workflow_id>/_deprovision?allow_delete=<resource_id1>,<resource_id2>
```

When deprovisioning requires the `allow_delete` parameter, the API returns a 403 (FORBIDDEN) response identifying the resources that need explicit deletion consent:

```json
{
  "error": "These resources require the allow_delete parameter to deprovision: [index_name my-index]."
}
```

New workflow steps added:
- `DeleteIndexStep` - Deletes indexes during deprovisioning
- `DeleteIngestPipelineStep` - Deletes ingest pipelines during deprovisioning
- `DeleteSearchPipelineStep` - Deletes search pipelines during deprovisioning

These steps are on a denylist and cannot be used during provisioning, only during deprovisioning with explicit `allow_delete` consent.

#### Improved Template and WorkflowState Builders

The `Template` class now uses the common static `.builder()` instantiation pattern, improving code consistency across the codebase.

The `WorkflowState` builder has been enhanced with:
- Enforced static `builder()` pattern
- Partial state update capability for updating resource states during deprovisioning
- Foundation for migrating away from Painless scripts for state updates

### Technical Changes

| Component | Change |
|-----------|--------|
| `RestCreateWorkflowAction` | Added `update_fields` query parameter handling |
| `RestDeprovisionWorkflowAction` | Added `allow_delete` query parameter handling |
| `Template.Builder` | Changed to static `.builder()` instantiation |
| `WorkflowState.Builder` | Added partial state update capability |
| `DeleteIndexStep` | New step for index deletion during deprovision |
| `DeleteIngestPipelineStep` | New step for ingest pipeline deletion |
| `DeleteSearchPipelineStep` | New step for search pipeline deletion |
| `GetWorkflowStepsAction` | Filters denylist steps from response |

## Limitations

- The `update_fields` parameter only allows updating non-workflow fields (name, description, ui_metadata)
- The `allow_delete` parameter requires explicit resource IDs; wildcards are not supported
- Delete steps are only available during deprovisioning, not provisioning

## References

### Documentation
- [Create or Update Workflow API](https://docs.opensearch.org/2.16/automating-configurations/api/create-workflow/)
- [Deprovision Workflow API](https://docs.opensearch.org/2.16/automating-configurations/api/deprovision-workflow/)

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#757](https://github.com/opensearch-project/flow-framework/pull/757) | Support editing of certain workflow fields on a provisioned workflow | [#749](https://github.com/opensearch-project/flow-framework/issues/749) |
| [#763](https://github.com/opensearch-project/flow-framework/pull/763) | Add allow_delete parameter to Deprovision API | [#748](https://github.com/opensearch-project/flow-framework/issues/748), [#579](https://github.com/opensearch-project/flow-framework/issues/579) |
| [#778](https://github.com/opensearch-project/flow-framework/pull/778) | Improve Template and WorkflowState builders | [#713](https://github.com/opensearch-project/flow-framework/issues/713), [#776](https://github.com/opensearch-project/flow-framework/issues/776) |
