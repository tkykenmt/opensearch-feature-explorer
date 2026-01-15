---
tags:
  - opensearch-dashboards
---
# Workspace

## Summary

Bug fixes for the Workspace feature in OpenSearch Dashboards v2.16.0, addressing data source deletion, navigation, permission validation, and saved objects API issues.

## Details

### What's New in v2.16.0

This release includes 4 bug fixes for the Workspace feature:

| Fix | Description |
|-----|-------------|
| Data source preservation | Data sources are now unassigned before workspace deletion, preventing accidental data source removal |
| Navigation fix | Clicking workspaces with "all use case" now correctly navigates to the workspace detail page |
| Permission validation | Added permission validation on workspace detail page to prevent duplicate user ID entries |
| Bulk get API fix | Added `workspaces` and `permissions` fields to saved objects `_bulk_get` response |

### Technical Changes

#### Data Source Unassignment on Workspace Deletion

Previously, calling `deleteByWorkspace` would delete data sources that were only assigned to the workspace being deleted. The fix unassigns data sources before deletion to preserve them.

```typescript
// Before deletion, unassign data sources
await unassignDataSourcesFromWorkspace(workspaceId);
await deleteByWorkspace(workspaceId);
```

#### Permission Validation on Detail Page

The `WorkspaceDetailForm` component now receives `permissionEnabled` prop, enabling `useWorkspaceForm` to validate input data such as duplicate user IDs in "Manage Access and Permissions".

#### Saved Objects Bulk Get Response

The `_bulk_get` API response now includes `workspaces` and `permissions` fields for saved objects, enabling proper workspace context handling.

## Limitations

- Data source unassignment only applies to data sources exclusively assigned to the deleted workspace
- Permission validation requires the security plugin to be properly configured

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#7279](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7279) | Unassign data source before deleteByWorkspace |   |
| [#7405](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7405) | Navigate to detail page when clicking all use case workspace |   |
| [#7435](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7435) | Add permission validation at workspace detail page |   |
| [#7565](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7565) | Add workspaces and permissions fields into saved objects _bulk_get response | [#7564](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7564) |
