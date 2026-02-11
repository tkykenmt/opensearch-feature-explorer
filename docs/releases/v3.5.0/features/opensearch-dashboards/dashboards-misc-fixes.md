---
tags:
  - opensearch-dashboards
---
# Dashboards Misc Fixes

## Summary

A collection of miscellaneous bug fixes for OpenSearch Dashboards v3.5.0, addressing issues in wildcard pattern validation for dataset selection, server basepath handling for recently accessed assets, alias type visibility in visualizations, CSV download column filtering, pivot function timestamp handling, and developer guide documentation.

## Details

### What's New in v3.5.0

#### Fix Wildcard Pattern Validation (PR #10939)
Overhauled the dataset selection UI to fix wildcard pattern validation. Previously, the index picker had a hard limit of 100 results and caching issues that prevented newly created indices (e.g., from Dev Tools) from appearing. The fix introduces a search-based, multi-select index picker with popover search, live API-driven index resolution, and badge-based pattern display. Also adds support for comma-separated wildcard patterns, allowing users to type `otel*,` to automatically create a new wildcard entry.

#### Fix Server Basepath for Recently Accessed Assets (PR #11193)
Fixed a bug where the server base path was missing from URLs for recently accessed assets. When Dashboards was configured with a custom `server.basePath`, links to recently accessed items (saved searches, dashboards, visualizations) would fail because the base path was not prepended. Resolves issues [#11181](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/11181) and [#11148](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/11148).

#### Hide Alias Type in Visualizations (PR #11212)
Fixed the `hideTypes` function in the saved objects client to also hide the `alias` type when filtering saved object types for visualizations. Previously, alias-type saved objects could appear unexpectedly in visualization listings.

#### Apply Data Table Columns Filter to CSV Download (PR #11219)
Fixed a mismatch between the data table rendered in the Explore page and the downloaded CSV. Previously, the CSV download did not apply the same column filtering as the data table, resulting in extra or missing columns. The fix extracts the column filter logic into a shared helper function used by both the data table rendering and the CSV export workflow.

#### Fix Pivot Function Timestamp Handling (PR #11242)
Fixed an issue in the Explore visualization where the `pivot` function did not handle timestamp fields properly. After pivoting, timestamp values were incorrectly converted to plain strings instead of being preserved as date/time objects, causing incorrect rendering in time-based charts.

#### Update Developer Guide for Darwin ARM (PR #10997)
Updated `DEVELOPER_GUIDE.md` to include the `darwin-arm` build flag option, documenting the ARM64 macOS build target for developers building OpenSearch Dashboards locally.

## Limitations

- The wildcard pattern validation fix changes the dataset selection UI behavior; users accustomed to the previous single-select flow may need to adapt to the new multi-select interface.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#10939](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10939) | Fix wildcard pattern validation | - |
| [#11193](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11193) | Fix server basepath for recently accessed assets | [#11181](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/11181), [#11148](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/11148) |
| [#11212](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11212) | Visualizations should hide alias type | - |
| [#11219](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11219) | Apply data table columns filter to download CSV | - |
| [#11242](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11242) | Fix pivot function timestamp handling | - |
| [#10997](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10997) | Update DEVELOPER_GUIDE.md to include darwin-arm | - |
