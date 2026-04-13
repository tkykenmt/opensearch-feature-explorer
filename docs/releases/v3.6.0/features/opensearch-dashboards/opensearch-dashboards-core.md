---
tags:
  - opensearch-dashboards
---
# OpenSearch Dashboards Core

## Summary

OpenSearch Dashboards v3.6.0 includes 13 changes to the core platform spanning bug fixes, performance improvements, infrastructure enhancements, and a new extensibility feature. Key highlights include a major performance fix for large query results in Explore, share link fixes when session storage is enabled, defensive guards for index pattern fields, and a new Transport extension point for plugin-based client customization.

## Details

### What's New in v3.6.0

#### Bug Fixes

| Fix | Description | PR |
|-----|-------------|-----|
| Share links with session storage | Added `_q` and `_v` flags to hash/unhash logic, fixing broken share links in both Explore and classic Discover when session storage is enabled | #11506 |
| Index pattern fields as arrays | Added defensive guards (`Array.isArray` checks) at five call sites where `JSON.parse(fields)` would crash when fields were stored as native arrays by external tooling. Also fixed `DataViewsService` cache poisoning by plain `IndexPattern` objects | #11538 |
| Comma-separated terms pasting | Added `onPaste` wrapper with delimiter handling to correctly split comma-separated terms into individual filter values instead of overwriting with only the last term | #11489 |
| Table visualization links | Updated `dompurify` hooks placement in the rewritten `table_vis_dynamic_table.tsx` component so links in table fields correctly open in new tabs | #11458 |
| Prometheus credential exposure | Removed unused `meta` field from Prometheus data-connection saved objects to prevent potential credential exposure via `JSON.stringify` | #11280 |
| Zero-width space in field names | Replaced Unicode U+200B insertion with `<wbr>` elements in the `wrapOnDot` helper, preventing invisible characters from corrupting copied field names. Consolidated duplicated function from 6 files across 4 plugins into a shared utility in `opensearch_dashboards_react` | #11457 |
| `checkForFunctionProperty` arrays | Updated the function to handle array inputs, preventing errors when properties are arrays | #11404 |
| Duplicate save in field editor | Added `isSaving` state, early return guard, and `.finally()` reset to prevent duplicate save requests in the index pattern management field editor | #11530 |

#### Performance Improvements

| Improvement | Description | PR |
|-------------|-------------|-----|
| Large query result rendering | Eliminated three independent bottlenecks causing 20+ seconds of blocking JS after network response for indexes with 500+ fields and 10,000 rows: (1) removed per-field `dompurify.sanitize` by switching to text-mode formatting with `React.memo`, (2) rewrote `canResultsBeVisualized` from O(rows × fields) to O(fields) using `fieldSchema` alone, (3) excluded results slice from Redux dev-mode middleware traversal via `ignoredPaths` | #11390 |

#### Features

| Feature | Description | PR |
|---------|-------------|-----|
| Source filters save guard | Added `isSaving` guards to disable Add, Edit, and Delete buttons in the `SourceFiltersTable` component while save operations are in progress, preventing concurrent saves | #11377 |
| Transport extension point | Added `registerClientTransport()`, `hasClientTransport()`, and `getClientTransport()` to the OpenSearch service contracts, allowing plugins to register a custom Transport class that intercepts all HTTP-level communication with the backend cluster. Zero runtime overhead when no Transport is registered | #11493 |

#### Infrastructure

| Change | Description | PR |
|--------|-------------|-----|
| Compiler observer logging | Added logging for warnings and errors in `observeCompiler`, stopped treating warnings as failures, and allowed `ContextModules` during plugin builds | #11479 |
| Node v14 removal | Removed end-of-life Node v14 fallback version download from the build system, eliminating security scanner vulnerability flags | #11477 |

## Limitations

- The large query result performance fix uses `rowCount` as an upper bound for `uniqueValuesCount` in `canResultsBeVisualized`, which is a safe approximation but not exact. The actual visualization rendering still uses accurate stats.
- The underlying architectural issue of storing raw OpenSearch hits in Redux state remains and should be addressed separately.
- The Transport extension point allows only one custom Transport class to be registered (double-registration is guarded).

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#11377](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11377) | Add isSaving guard to source filters table | |
| [#11493](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11493) | Add Transport extension point to OpenSearch service | [RFC #11470](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/11470) |
| [#11390](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11390) | Improve performance with large query results | |
| [#11479](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11479) | Handle logs and warnings in compiler observer | |
| [#11506](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11506) | Fix share links when session storage is enabled | [#11491](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/11491) |
| [#11538](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11538) | Add defensive guards for index pattern fields as arrays | |
| [#11489](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11489) | Fix comma-separated terms pasting in filter input | |
| [#11458](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11458) | Fix open link in new tab from table field | [#3500](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/3500) |
| [#11280](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11280) | Remove meta field for Prometheus data connections | |
| [#11457](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11457) | Remove zero-width space from field name text | |
| [#11404](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11404) | Fix checkForFunctionProperty to handle arrays | |
| [#11530](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11530) | Prevent duplicate save requests in index pattern field editor | |
| [#11477](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11477) | Remove Node v14 fallback version download | |
