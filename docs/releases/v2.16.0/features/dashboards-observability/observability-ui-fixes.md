---
tags:
  - dashboards-observability
---
# Observability UI Fixes

## Summary

OpenSearch Dashboards Observability v2.16.0 includes several bug fixes addressing navigation issues, toast notifications, scroll bar behavior, Query Assist UI improvements, datasource registration, notebook UX copy changes, and saved objects redirection.

## Details

### What's New in v2.16.0

This release focuses on UI/UX bug fixes across multiple Observability components:

| Fix | Description |
|-----|-------------|
| Getting Started Toast | Added toast message and error handling for getting started asset creation |
| Trace Analytics Navigation | Fixed breadcrumb navigation bug when new nav changes are active |
| Scroll Bar Reset | Fixed scroll bar position reset after closing fly-out in Trace Analytics |
| Query Assist UI | Updated label from "PPL Query" to "Query Assist", auto-focus on form field, updated placeholder text and icon size |
| Datasource Unregistration | Unregistered observability datasource from old and new nav groups |
| Notebooks MDS Copy | UX copy changes for migrate notebook functionality with MDS |
| Saved Objects Redirection | Fixed URL redirection for notebooks in Saved Objects Management page |

### Technical Changes

#### Getting Started Toast Message (PR #1977)
- Added toast notification for successful/failed asset creation in Getting Started workflow
- Improved error handling with user-visible error messages

#### Trace Analytics Navigation Fix (PR #1977)
- Fixed breadcrumb display issue when new navigation mode is enabled
- Ensures consistent navigation experience across old and new nav modes

#### Scroll Bar Reset (PR #1917)
- Resets scroll bar to original position after closing trace detail fly-out
- Resolves issue [#1916](https://github.com/opensearch-project/dashboards-observability/issues/1916)

#### Query Assist UI Improvements (PR #1939)
- Renamed "PPL Query" label to "Query Assist" for clarity
- Auto-focuses Query Assist form field on page load
- Updated get started and placeholder text
- Adjusted icon sizing for consistency

#### Datasource Navigation Group (PR #1972)
- Unregistered observability datasource from both old and new navigation groups
- Related to OpenSearch Dashboards [#7323](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7323)

#### Notebooks MDS UX (PR #1971)
- Updated UX copy for notebook migration workflow
- Improved user guidance for MDS-enabled environments

#### Saved Objects URL Fix (PR #1998)
- Fixed incorrect URL redirection when clicking notebooks in Saved Objects Management
- Ensures proper navigation to notebook detail pages

## Limitations

- These fixes are specific to the Observability plugin UI and do not affect backend functionality
- Some fixes (PR #1972) depend on corresponding changes in OpenSearch Dashboards core

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1977](https://github.com/opensearch-project/dashboards-observability/pull/1977) | Add toast message for getting started / Fix Nav Bug for Traces | |
| [#1972](https://github.com/opensearch-project/dashboards-observability/pull/1972) | Unregister observability datasource from old and new nav group | [OSD #7323](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7323) |
| [#1971](https://github.com/opensearch-project/dashboards-observability/pull/1971) | UX copy changes for Notebooks with MDS | |
| [#1939](https://github.com/opensearch-project/dashboards-observability/pull/1939) | Fix minor issues in query assist UI | |
| [#1917](https://github.com/opensearch-project/dashboards-observability/pull/1917) | Trace analytics scroll bar reset | [#1916](https://github.com/opensearch-project/dashboards-observability/issues/1916) |
| [#1998](https://github.com/opensearch-project/dashboards-observability/pull/1998) | Fix redirection URL in saved objects management page for notebooks | |
