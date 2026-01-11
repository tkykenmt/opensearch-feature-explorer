# Dashboards Workspace

## Summary

This release removes the restriction that required at least one data source to be selected when creating a workspace. Users can now create workspaces without associating any data sources, providing more flexibility for workspace setup and configuration.

## Details

### What's New in v3.4.0

The workspace creation flow has been simplified by removing the mandatory data source requirement. Previously, users were blocked from creating a workspace if no data sources were selected when the data source feature was enabled. This restriction has been removed.

### Technical Changes

#### Component Changes

The `WorkspaceCreateActionPanel` component was modified to remove the data source validation logic:

| Component | Change |
|-----------|--------|
| `WorkspaceCreateActionPanel` | Removed `dataSourceEnabled` prop and associated validation |
| `WorkspaceFormSummaryPanel` | Removed `dataSourceEnabled` prop propagation |

#### Before (v3.3.0 and earlier)

```typescript
// Create button was disabled when data source enabled but none selected
const createButtonDisabled =
  (formData.name?.length ?? 0) > MAX_WORKSPACE_NAME_LENGTH ||
  (formData.description?.length ?? 0) > MAX_WORKSPACE_DESCRIPTION_LENGTH ||
  (dataSourceEnabled && formData.selectedDataSourceConnections.length === 0);
```

#### After (v3.4.0)

```typescript
// Create button only validates name and description length
const createButtonDisabled =
  (formData.name?.length ?? 0) > MAX_WORKSPACE_NAME_LENGTH ||
  (formData.description?.length ?? 0) > MAX_WORKSPACE_DESCRIPTION_LENGTH;
```

### Usage Example

Users can now create a workspace without selecting any data sources:

1. Navigate to workspace creation page
2. Enter workspace name and description
3. Select use case
4. Skip data source selection (optional)
5. Click "Create workspace"

The workspace will be created successfully even without any associated data sources. Data sources can be added later through the workspace settings.

### Migration Notes

No migration required. Existing workspaces are unaffected. This change only affects the workspace creation flow.

## Limitations

- Workspaces created without data sources will have limited functionality until data sources are associated
- Some use cases may still require data sources for full functionality

## Related PRs

| PR | Description |
|----|-------------|
| [#10861](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10861) | Remove the restriction that workspace cannot be created without datasource |

## References

- [Workspace Documentation](https://docs.opensearch.org/3.0/dashboards/workspace/workspace/): Official workspace feature documentation
- [Create a Workspace](https://docs.opensearch.org/3.0/dashboards/workspace/create-workspace/): How to create workspaces

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch-dashboards/workspace.md)
