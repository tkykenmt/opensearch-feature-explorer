---
tags:
  - dashboards
  - observability
---

# Observability Bugfixes

## Summary

OpenSearch Dashboards Observability plugin received multiple bug fixes in v2.18.0, addressing navigation issues, workspace compatibility, Multi-Data Source (MDS) support, and UI improvements. These fixes improve the overall stability and user experience of the Observability features.

## Details

### What's New in v2.18.0

This release includes 12 bug fixes across several areas:

1. **Navigation and Redirection Fixes**: Fixed multiple issues with navigation between Observability components
2. **Workspace Compatibility**: Improved integration with the Workspaces feature
3. **Multi-Data Source (MDS) Support**: Fixed issues with MDS plugin registration and error handling
4. **UI/UX Improvements**: Enhanced visual design and fixed display issues

### Technical Changes

#### Navigation Fixes

| Issue | Fix | PR |
|-------|-----|-----|
| Getting started cards using `href` instead of `navigateToApp` | Replaced `href` with `navigateToApp` from core for proper workspace URL scoping | [#2146](https://github.com/opensearch-project/dashboards-observability/pull/2146) |
| Span to logs redirection broken | Fixed redirection from traces span flyout to Discover | [#2201](https://github.com/opensearch-project/dashboards-observability/pull/2201), [#2219](https://github.com/opensearch-project/dashboards-observability/pull/2219) |
| MDS label undefined during redirection | Updated MDS label handling when undefined | [#2225](https://github.com/opensearch-project/dashboards-observability/pull/2225) |

#### Workspace Integration Fixes

| Issue | Fix | PR |
|-------|-----|-----|
| Non-workspace admin updating `observability:defaultDashboard` shows error | Restricted `observability:defaultDashboard` updates to workspace owner/OSD admin only | [#2223](https://github.com/opensearch-project/dashboards-observability/pull/2223) |

#### Multi-Data Source (MDS) Fixes

| Issue | Fix | PR |
|-------|-----|-----|
| APIs returning 500 errors | Fixed error code handling for MDS-related APIs | [#2222](https://github.com/opensearch-project/dashboards-observability/pull/2222) |
| Plugins not in MDS causing issues | Added de-registration for plugins not onboarded to MDS | [#2222](https://github.com/opensearch-project/dashboards-observability/pull/2222) |
| Missing else condition in remote cluster calls | Added missing else condition for remote cluster handling | [#2213](https://github.com/opensearch-project/dashboards-observability/pull/2213) |

#### UI/UX Improvements

| Change | Description | PR |
|--------|-------------|-----|
| Overview page rework | Moved page options to header, added UI setting to persist card visibility, updated empty states | [#2210](https://github.com/opensearch-project/dashboards-observability/pull/2210) |
| Getting started cards redesign | Updated content and visual design of getting started cards | [#2209](https://github.com/opensearch-project/dashboards-observability/pull/2209) |
| X-axis label rotation | Rotated x-axis labels by 45 degrees counter-clockwise to prevent overlapping | [#2211](https://github.com/opensearch-project/dashboards-observability/pull/2211) |
| Metrics panel expand button | Disabled and hid expand button for metrics panel | [#2217](https://github.com/opensearch-project/dashboards-observability/pull/2217) |

#### Integration Fixes

| Issue | Fix | PR |
|-------|-----|-----|
| VPC integration MV creation query broken | Fixed the VPC integration's Materialized View creation query | [#2179](https://github.com/opensearch-project/dashboards-observability/pull/2179) |

### Migration Notes

No migration steps required. These are bug fixes that improve existing functionality.

## Limitations

- The `observability:defaultDashboard` setting can now only be updated by workspace owners or OSD admins when workspaces are enabled

## References

### Pull Requests
| PR | Description |
|----|-------------|
| [#2146](https://github.com/opensearch-project/dashboards-observability/pull/2146) | Fix getting started cards re-direction to integrations |
| [#2179](https://github.com/opensearch-project/dashboards-observability/pull/2179) | Fix the VPC integration's MV creation query |
| [#2201](https://github.com/opensearch-project/dashboards-observability/pull/2201) | Update traces span redirection |
| [#2209](https://github.com/opensearch-project/dashboards-observability/pull/2209) | Update getting started cards content and visual design |
| [#2210](https://github.com/opensearch-project/dashboards-observability/pull/2210) | Observability Overview page rework |
| [#2211](https://github.com/opensearch-project/dashboards-observability/pull/2211) | Rotate x-Axis labels by 45 degrees |
| [#2213](https://github.com/opensearch-project/dashboards-observability/pull/2213) | Fix missing else condition for MDS remote cluster calls |
| [#2217](https://github.com/opensearch-project/dashboards-observability/pull/2217) | Metrics fixes - disable expand button |
| [#2219](https://github.com/opensearch-project/dashboards-observability/pull/2219) | Re-direction fix for associated logs from traces |
| [#2222](https://github.com/opensearch-project/dashboards-observability/pull/2222) | MDS plugin de-registration and error code changes |
| [#2223](https://github.com/opensearch-project/dashboards-observability/pull/2223) | Fix non-workspace admin update observability:defaultDashboard |
| [#2225](https://github.com/opensearch-project/dashboards-observability/pull/2225) | Fixes span to logs redirection, updates MDS label when undefined |

### Issues (Design / RFC)
- [opensearch-catalog#195](https://github.com/opensearch-project/opensearch-catalog/issues/195): VPC integration MV creation issue

## Related Feature Report

- [Observability UI](../../../features/dashboards-observability/dashboards-observability-observability-ui.md)
- [Observability Multi-Data Source Support](../../../features/dashboards-observability/dashboards-observability-observability-multi-plugin-multi-data-source-support.md)
- [Observability Workspace Integration](../../../features/dashboards-observability/dashboards-observability-observability-workspace-integration.md)
