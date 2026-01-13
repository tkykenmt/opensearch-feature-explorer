---
tags:
  - dashboards-observability
---
# Observability

## Summary

OpenSearch Dashboards Observability plugin v2.19.0 introduces significant improvements to Trace Analytics, including a redesigned Gantt chart with zoom and minimap functionality, enhanced Service Map with focus filtering, and numerous bug fixes for Multi-Data Source support, query optimization, and UI stability.

## Details

### What's New in v2.19.0

#### Gantt Chart / Span List Rework
- Added minimap above the Gantt chart for navigation overview
- Enabled zoom functionality with reset button
- Added duration text display on the right side of spans
- Moved pie chart above Gantt chart with improved margins
- Fixed resizing issues when sidebar is opened
- Added "Tree view" tab for hierarchical span visualization
- Fixed text cutoff for left-hand labels

#### Service Map Updates
- Searchable focus field popover listing all service options
- Focus selection enlarges the selected node following filter behavior
- Reset button recenters the tree and clears focus
- Adjusted zoom speed to 0.5 with min/max zoom constraints
- Loading state indicator while rendering
- Darker/thicker borders on each node
- Consistent diagram layout using seed for physics generation
- Focus now filters to display only connected nodes

#### Focus Field Rework
- Focus field no longer applies a filter; renders connected services only
- Dropdown reflects connected viewable services for switching
- Reset icon clears existing filter if it matches focus field
- Focus field disabled while a service filter is active
- Clicking a service redirects to the corresponding service view page

#### VPC Materialized View Enhancement
- Removed `maxFilesPerTrigger` limits for VPC MV creation queries

#### Overview Page Improvements
- Added state handling for missing data source in workspaces
- Users prompted to configure data source when not present

### Technical Changes

#### Query Optimization
- Removed `all_services` aggregation field from `getRelatedServiceQuery` (reduced bucket requirements from 460 to 110)
- Removed unused `traceGroupName` aggregation field from `getServiceNodesQuery`
- Removed false-positive toast messages during service map rendering

#### Bug Fixes
- Fixed infinite refresh when MDS disabled and service page traces link clicked
- Fixed MDS support for missing `datasourceId` in traceGroup requests
- Fixed workspace visualizations fetching error
- Fixed notebook routes for savedNotebook endpoints
- Fixed integration assets MDS reference updates
- Fixed error field handling for custom spans (status.code === 2 check)
- Added loading status to all pages in traces and services
- Replaced index mapping with field caps API for trace filters

#### New Settings
- `TRACE_CUSTOM_MODE_DEFAULT_SETTING`: Option to enable custom source as default landing page

## Limitations

- Custom source mode requires explicit configuration via flyout
- Service map rendering may take time with large numbers of nodes

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#2318](https://github.com/opensearch-project/dashboards-observability/pull/2318) | Remove maxFilesPerTrigger limits for VPC MV | [#2314](https://github.com/opensearch-project/dashboards-observability/issues/2314) |
| [#2283](https://github.com/opensearch-project/dashboards-observability/pull/2283) | Gantt chart / Span list rework (backport) |   |
| [#2264](https://github.com/opensearch-project/dashboards-observability/pull/2264) | Service map redirection/Focus field rework |   |
| [#2255](https://github.com/opensearch-project/dashboards-observability/pull/2255) | Notebooks cypress test updates | [#1886](https://github.com/opensearch-project/dashboards-observability/issues/1886) |
| [#2237](https://github.com/opensearch-project/dashboards-observability/pull/2237) | Overview page missing data source state |   |
| [#2230](https://github.com/opensearch-project/dashboards-observability/pull/2230) | Service map updates |   |
| [#2336](https://github.com/opensearch-project/dashboards-observability/pull/2336) | Add loading status to traces/services pages |   |
| [#2333](https://github.com/opensearch-project/dashboards-observability/pull/2333) | MDS support for missing datasourceId |   |
| [#2321](https://github.com/opensearch-project/dashboards-observability/pull/2321) | Traces filter adjustment and DataGrid abstraction |   |
| [#2315](https://github.com/opensearch-project/dashboards-observability/pull/2315) | Remove redundant traces call for related services |   |
| [#2310](https://github.com/opensearch-project/dashboards-observability/pull/2310) | Query optimization / UI setting / Bugfix |   |
| [#2298](https://github.com/opensearch-project/dashboards-observability/pull/2298) | Traces custom source bug fixes |   |
| [#2294](https://github.com/opensearch-project/dashboards-observability/pull/2294) | Gantt Chart / Service Map followup |   |
| [#2279](https://github.com/opensearch-project/dashboards-observability/pull/2279) | Fix notebook routes for savedNotebook endpoints |   |
| [#2268](https://github.com/opensearch-project/dashboards-observability/pull/2268) | Fix fetching workspace visualizations error |   |
| [#2246](https://github.com/opensearch-project/dashboards-observability/pull/2246) | Replace index mapping with field caps API |   |
| [#2242](https://github.com/opensearch-project/dashboards-observability/pull/2242) | Metrics datasource fixes |   |
| [#2241](https://github.com/opensearch-project/dashboards-observability/pull/2241) | Use savedObjects client for notebook visualizations |   |
| [#2240](https://github.com/opensearch-project/dashboards-observability/pull/2240) | Fix MDS ref update on integration assets |   |
| [#2238](https://github.com/opensearch-project/dashboards-observability/pull/2238) | Return 503 if OpenSearch calls failed |   |
| [#2235](https://github.com/opensearch-project/dashboards-observability/pull/2235) | Traces/Services bugfixes and UI update |   |
| [#2228](https://github.com/opensearch-project/dashboards-observability/pull/2228) | Remove fallback restore keys from build cache |   |
| [#1466](https://github.com/opensearch-project/dashboards-observability/pull/1466) | Fix create observability dashboard after invalid name |   |
| [#2293](https://github.com/opensearch-project/dashboards-observability/pull/2293) | Fix flaky cypress tests |   |
| [#2304](https://github.com/opensearch-project/dashboards-observability/pull/2304) | Update maintainer doc links |   |
