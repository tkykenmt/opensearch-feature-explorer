---
tags:
  - domain/security
  - component/dashboards
  - dashboards
  - security
---
# Security Analytics UI Bugfixes

## Summary

OpenSearch 2.17.0 includes multiple bug fixes for the Security Analytics Dashboards plugin, addressing navigation issues, webpack build errors, multi-data source support, and various UI/UX improvements. These fixes improve stability and usability of the Security Analytics interface, particularly in workspace environments and multi-data source configurations.

## Details

### What's New in v2.17.0

This release focuses on stability and compatibility fixes across several areas:

1. **Navigation and Workspace Compatibility** - Fixed navigation category placement and workspace availability settings
2. **Webpack Build Errors** - Resolved module import issues causing runtime errors
3. **Multi-Data Source Support** - Added proper checks for multi-data source environments
4. **UI/UX Improvements** - Fixed page crashes, breadcrumb navigation, and URL state handling

### Technical Changes

#### Navigation Fixes

| Issue | Fix | PR |
|-------|-----|-----|
| Incorrect nav category placement | Updated nav category and workspaceAvailability | [#1093](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1093) |
| Data source ID not persisted on nav change | Persist dataSourceId when side nav changes | [#1123](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1123) |
| Incorrect breadcrumb entries | Fixed breadcrumbs for correlations, log types, edit rule pages | [#1123](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1123) |

#### Webpack/Module Import Fixes

| Issue | Fix | PR |
|-------|-----|-----|
| Webpack error from kuery.js import | Made import more specific to avoid importing incorrect modules | [#1136](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1136) |
| Section enum import causing webpack error | Removed problematic import, used enum value directly | [#1144](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1144) |

#### Multi-Data Source Support

| Issue | Fix | PR |
|-------|-----|-----|
| Threat alerts card fails in all-use-case workspace | Added check for multi data source support before rendering | [#1132](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1132) |

#### UI/UX Fixes

| Issue | Fix | PR |
|-------|-----|-----|
| Page crash on correlation graph node click | Fixed crash when clicking node for details | [#1107](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1107) |
| Incorrect help text for data source selection | Updated help text for data source controls | [#1107](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1107) |
| IOC pagination not working | Fixed pagination for IOCs inside threat intel source | [#1107](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1107) |
| Alert filtering for correlations broken | Fixed filtering of alerts for correlations | [#1107](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1107) |
| URL state lost on navigation | Pass through remaining location arguments when updating URL query params | [#1149](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1149) |
| Plugin version decoupling bug | Fixed installedPlugins list check (uses `opensearch-security-analytics` not `opensearch_security_analytics`) | [#1123](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1123) |

### Code Changes

#### Import Fix Example (PR #1136)

Before:
```typescript
import { IndexPatternsService } from '../../../../src/plugins/data/common';
```

After:
```typescript
import { IndexPatternsService } from '../../../../src/plugins/data/common/index_patterns';
```

This change avoids importing the entire `common` module which includes `kuery.js` that uses incompatible `module.exports` syntax.

## Limitations

- These fixes are specific to the Security Analytics Dashboards plugin UI
- Some fixes are workarounds for upstream OpenSearch Dashboards module compatibility issues

## References

### Documentation
- [About Security Analytics](https://docs.opensearch.org/2.17/security-analytics/): Official documentation
- [Setting up Security Analytics](https://docs.opensearch.org/2.17/security-analytics/sec-analytics-config/index/): Configuration guide

### Pull Requests
| PR | Description |
|----|-------------|
| [#1093](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1093) | Update nav category and workspaceAvailability |
| [#1107](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1107) | Fix UI issues (correlation graph, help text, pagination, filtering) |
| [#1123](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1123) | Bug fixes PageHeader and SideNav |
| [#1132](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1132) | Added check for multi data source support |
| [#1136](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1136) | Made import more specific to avoid incorrect modules |
| [#1144](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1144) | Remove import causing webpack error |
| [#1149](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1149) | Pass through URL state and params |

## Related Feature Report

- [Security Analytics Dashboards Plugin](../../../features/security-analytics-dashboards/security-analytics-dashboards-plugin.md)
