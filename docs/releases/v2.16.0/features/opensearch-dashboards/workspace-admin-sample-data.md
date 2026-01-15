---
tags:
  - opensearch-dashboards
---
# Workspace Admin and Sample Data

## Summary

OpenSearch Dashboards v2.16.0 introduces workspace administration capabilities and sample data management features. Dashboard admins can now be configured via YAML settings, with only admins allowed to create workspaces when permission control is enabled. Additionally, sample data can be imported directly into specific workspaces, and saved objects can be duplicated between workspaces.

## Details

### What's New in v2.16.0

#### Dashboard Admin Configuration
Users or groups can be designated as dashboard admins through configuration in `opensearch_dashboards.yml`. Dashboard admins have full access to all workspaces and saved objects within OpenSearch Dashboards.

```yaml
opensearchDashboards.dashboardAdmin.groups: ["dashboard_admin"]
opensearchDashboards.dashboardAdmin.users: ["admin_user"]
```

The system checks if a user is a dashboard admin by:
1. Matching backend roles against configured groups
2. Matching user ID against configured users

#### Workspace Creation Restriction
When saved objects permission control is enabled (`savedObjects.permission.enabled: true`), only dashboard admins can create new workspaces. This provides centralized control over workspace proliferation.

- Non-admin users see the "Create Workspace" button hidden
- Workspace creation API validates admin status before allowing creation
- If permission control is disabled, any user can create workspaces

#### Sample Data Import to Workspace
Sample data (Flights, eCommerce, Web Logs) can now be imported directly into the current workspace context:

- Import sample data page registered as a standalone application
- Entry point added to workspace overview page
- Sample data saved objects are associated with the current workspace
- Each workspace maintains its own copy of sample data
- Removing sample data only affects the current workspace

#### Duplicate Saved Objects Between Workspaces
Users can duplicate saved objects from one workspace to another:

- Three duplicate button locations on saved objects management page:
  - Individual object action
  - Bulk action for selected objects
  - "Duplicate All" button
- Modal allows selecting target workspace
- Creates new copies (not references) in the target workspace
- Supports all saved object types (dashboards, visualizations, index patterns, etc.)

### Technical Changes

#### Dashboard Admin Service
```typescript
// Check if current user is dashboard admin
const isDashboardAdmin = await capabilities.isDashboardAdmin();

// Configuration structure
interface DashboardAdminConfig {
  groups: string[];
  users: string[];
}
```

#### Sample Data Workspace Integration
- Sample data install/uninstall APIs now workspace-aware
- Saved object IDs prefixed with workspace ID for isolation
- `getDataSourceIntegratedDashboard` updated to support workspace context

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `opensearchDashboards.dashboardAdmin.groups` | Backend roles that grant dashboard admin access | `[]` |
| `opensearchDashboards.dashboardAdmin.users` | User IDs that have dashboard admin access | `[]` |
| `savedObjects.permission.enabled` | Enable permission control (required for admin-only workspace creation) | `false` |
| `workspace.enabled` | Enable workspace feature | `false` |

## Limitations

- Dashboard admin configuration requires security plugin to be installed for backend role matching
- Sample data import creates workspace-specific copies, increasing storage usage
- Duplicating large numbers of saved objects may take time
- Admin status is determined at request time; changes require re-authentication

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#6105](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6105) | Import sample data to current workspace | [#6106](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6106) |
| [#6478](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6478) | Duplicate selected/all saved objects between workspaces | [#6388](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6388) |
| [#6554](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6554) | Dashboard admin (groups/users) implementation | [#6389](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6389) |
| [#6831](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6831) | Only OSD admin can create workspace | [#6830](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6830) |
