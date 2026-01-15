---
tags:
  - opensearch-dashboards
---
# Workspace

## Summary

OpenSearch Dashboards v2.16.0 introduces significant enhancements to the Workspace feature, including use case-based workspace configuration, data source assignment, workspace detail pages, and improved UI components. This release focuses on making workspaces more functional and user-friendly with better navigation, admin controls, and data source integration.

## Details

### What's New in v2.16.0

#### Use Case System
- Added use case selector to workspace form, replacing the previous feature selector
- Workspaces can now be configured with specific use cases (Observability, Security Analytics, Search, Essentials, or All)
- Use cases determine which features and navigation items are available within a workspace
- Added "All use case" option allowing access to all features

#### Data Source Integration
- Data sources can now be assigned to workspaces during creation and update
- Added `addToWorkspaces` and `deleteFromWorkspaces` methods to saved object client
- Workspace-level default data source support
- Data source management recovered within workspace context
- Non-dashboard admins cannot see data source selection panel

#### Workspace Detail Page
- New dedicated workspace detail page with Overview, Settings, and Collaborators tabs
- Users can update workspace settings directly from the detail page
- Navigation to detail page from workspace list via edit button or workspace name click

#### UI Improvements
- Refactored workspace form UI with improved layout
- Changed description field from input to textarea
- Refactored workspace picker UI
- Workspace list card registered on home page
- Recent items now comply with workspace context
- Case-insensitive field name search filter

#### Admin Controls
- Dashboard admin flag added to capabilities service
- Admin-only controls for workspace management
- Configuration via `opensearchDashboards.dashboardAdmin.users` and `opensearchDashboards.dashboardAdmin.groups`

#### Architecture Changes
- Deleted virtual global workspace concept
- Only OSD admin users can see legacy saved objects not belonging to any workspace
- Registered nav groups used as workspace use cases
- Workspace settings registered under setup and settings

### Technical Changes

#### Configuration
```yaml
workspace.enabled: true
opensearchDashboards.dashboardAdmin.users: ['admin']
opensearchDashboards.dashboardAdmin.groups: ['dashboard_admin']
savedObjects.permission.enabled: true
```

#### Saved Object Client Extensions
```typescript
// New methods for data source assignment
savedObjectsClient.addToWorkspaces(objects, workspaces);
savedObjectsClient.deleteFromWorkspaces(objects, workspaces);

// Updated methods support workspace field updates
savedObjectsClient.update(type, id, attributes, { workspaces });
savedObjectsClient.bulkUpdate(objects);
```

## Limitations

- Multi-tenancy must be disabled when using workspaces
- Workspace use case can only be one specific use case or "All use case"
- Non-admin users cannot see legacy saved objects when workspace is enabled

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#6887](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6887) | Add use cases to workspace form | [#6902](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6902) |
| [#6907](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6907) | Change description field to textarea |  |
| [#7045](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7045) | Refactor workspace picker UI |  |
| [#7101](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7101) | Support data source assignment in workspace |  |
| [#7103](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7103) | Capabilities service add dashboard admin flag | [#7102](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7102) |
| [#7115](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7115) | Comply recent items with workspace |  |
| [#7133](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7133) | Refactor workspace form UI |  |
| [#7165](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7165) | Delete the virtual global workspace | [#7095](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7095) |
| [#7188](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7188) | Support workspace level default data source |  |
| [#7213](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7213) | Hide select data source panel for non dashboard admin |  |
| [#7221](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7221) | Use registered nav group as workspace use case | [#7222](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7222) |
| [#7241](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7241) | Support workspace detail page | [#7240](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7240) |
| [#7242](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7242) | Register workspace settings under setup and settings |  |
| [#7247](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7247) | Register workspace list card into home page |  |
| [#7296](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7296) | Recover data source management in workspace |  |
| [#7318](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7318) | Add "All use case" option to workspace form | [#7319](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7319) |
| [#6759](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6759) | Make field name search filter case insensitive |  |
