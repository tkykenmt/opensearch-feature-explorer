---
tags:
  - opensearch-dashboards
---
# Workspace

## Summary

Workspace feature enhancements and bug fixes in OpenSearch Dashboards v2.16.0, including new home page get started cards, admin-only workspace creation controls, enriched breadcrumbs with workspace context, and fixes for saved objects access control and name duplication validation.

## Details

### What's New in v2.16.0

This release includes 3 feature enhancements and 6 bug fixes for the Workspace feature:

#### Feature Enhancements

| Feature | Description |
|---------|-------------|
| Get started cards | Four new get started cards registered on the home page when workspace is enabled |
| Admin-only workspace creation | Create workspace button hidden for non-dashboard admin users in workspace menu and list |
| Enriched breadcrumbs | Breadcrumbs now include workspace name and use case context for better navigation |

#### Bug Fixes

| Fix | Description |
|-----|-------------|
| Saved objects access restriction | Non-dashboard admin users can only access saved objects within their permitted workspaces |
| Name duplication check | Workspace name duplication check now uses exact match instead of partial match |
| Data source preservation | Data sources are now unassigned before workspace deletion, preventing accidental removal |
| Navigation fix | Clicking workspaces with "all use case" now correctly navigates to the workspace detail page |
| Permission validation | Added permission validation on workspace detail page to prevent duplicate user ID entries |
| Bulk get API fix | Added `workspaces` and `permissions` fields to saved objects `_bulk_get` response |

### Technical Changes

#### Get Started Cards on Home Page

When workspace is enabled with the new home page, four get started cards are registered to help users onboard:

```yaml
# Enable in opensearch_dashboards.yml
workspace.enabled: true
uiSettings:
  overrides:
    "home:useNewHomePage": true
```

#### Admin-Only Workspace Creation

Only dashboard admin users can create workspaces. The create workspace button is hidden in both the workspace picker menu and workspace list page for non-admin users.

```yaml
# Configure dashboard admin users
opensearchDashboards.dashboardAdmin.users: ['admin_user']
```

#### Enriched Breadcrumbs

Breadcrumbs are now enriched with workspace and use case context:
- When workspace is enabled: breadcrumbs show workspace name and its use case
- When workspace is disabled: breadcrumbs show current nav group

#### Saved Objects Access Restriction

Non-dashboard admin users are restricted to accessing saved objects only within their permitted workspaces:
- `options.workspaces`: Non-permitted workspaces are filtered out
- `options.ACLSearchParams`: Principals are replaced with the requesting user
- Default ACLSearchParams are used if no workspace or ACL params provided

#### Workspace Name Duplication Check

The name duplication check now uses exact match by enclosing the workspace name in double quotes:

```json
{
  "query": {
    "simple_query_string": {
      "query": "\"demo workspace\"",
      "fields": ["workspace.name"]
    }
  }
}
```

This converts to a `TermQuery` for exact matching on the `keyword` field type.

## Limitations

- Dashboard admin configuration requires the security plugin to be properly configured
- Saved objects access restriction only applies when workspace is enabled
- Get started cards only appear with the new home page enabled

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#7333](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7333) | Register four get started cards in home page | [#7332](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7332) |
| [#7357](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7357) | Hide create workspace button for non dashboard admin | [#7358](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7358) |
| [#7360](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7360) | Enrich breadcrumbs by workspace and use case | [#7359](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7359) |
| [#7125](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7125) | Restrict saved objects finding when workspace enabled | [#7127](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7127) |
| [#6776](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6776) | Fix workspace name duplication check | [#6480](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6480) |
| [#7279](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7279) | Unassign data source before deleteByWorkspace |   |
| [#7405](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7405) | Navigate to detail page when clicking all use case workspace |   |
| [#7435](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7435) | Add permission validation at workspace detail page |   |
| [#7565](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7565) | Add workspaces and permissions fields into saved objects _bulk_get response | [#7564](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7564) |
