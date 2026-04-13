---
tags:
  - opensearch-dashboards
---
# Dashboards Misc Fixes

## Summary

A collection of miscellaneous bug fixes and minor improvements to OpenSearch Dashboards that don't fall under a specific feature area. These fixes address various UI, data handling, and developer experience issues across the Dashboards platform.

## Details

### Areas Covered

| Area | Description |
|------|-------------|
| Dataset Selection | Wildcard pattern validation, multi-select index picker, API-driven index resolution |
| Server Basepath | Correct basepath handling for recently accessed assets |
| Saved Objects | Proper alias type hiding in visualization listings |
| CSV Export | Column filter consistency between data table and CSV download |
| Explore Visualizations | Correct timestamp handling in pivot function |
| Developer Guide | Documentation for darwin-arm build target |
| Share Links | Hash/unhash logic for `_q` and `_v` flags with session storage |
| Index Patterns | Defensive guards for fields stored as arrays; cache poisoning fix for DataViewsService |
| Filter Input | Comma-separated terms pasting with delimiter handling |
| Table Visualization | Link opening in new tab via dompurify hooks in rewritten component |
| Data Connections | Prometheus meta field removal to prevent credential exposure |
| Field Names | Zero-width space replaced with `<wbr>` elements; shared `wrapOnDot` utility |
| Utility Functions | `checkForFunctionProperty` array input handling |
| Save Guards | Concurrent save prevention in source filters table and field editor |
| Performance | Large query result rendering optimization (Explore) |
| Extensibility | Transport extension point for plugin-based client customization |
| Build Infrastructure | Compiler observer logging improvements; Node v14 fallback removal |

## Limitations

- Miscellaneous fixes are grouped together when they don't warrant individual feature reports.

## Change History
- **v3.6.0**: Fixed share links with session storage (PR #11506), added defensive guards for index pattern fields as arrays and DataViewsService cache poisoning (PR #11538), fixed comma-separated terms pasting (PR #11489), fixed table visualization link opening in new tab (PR #11458), removed Prometheus meta field to prevent credential exposure (PR #11280), replaced zero-width space with `<wbr>` in field names and consolidated `wrapOnDot` utility (PR #11457), fixed `checkForFunctionProperty` for arrays (PR #11404), prevented duplicate saves in field editor (PR #11530) and source filters table (PR #11377), improved large query result performance in Explore (PR #11390), added Transport extension point for client customization (PR #11493), improved compiler observer logging and ContextModule support (PR #11479), removed Node v14 fallback (PR #11477)
- **v3.5.0**: Fixed wildcard pattern validation in dataset selection (PR #10939), server basepath for recently accessed assets (PR #11193), alias type visibility in visualizations (PR #11212), CSV download column filtering (PR #11219), pivot function timestamp handling (PR #11242), and developer guide darwin-arm documentation (PR #10997)

## References

### Pull Requests
| Version | PR | Description |
|---------|-----|-------------|
| v3.6.0 | [#11377](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11377) | Add isSaving guard to source filters table |
| v3.6.0 | [#11493](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11493) | Add Transport extension point to OpenSearch service |
| v3.6.0 | [#11390](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11390) | Improve performance with large query results |
| v3.6.0 | [#11479](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11479) | Handle logs and warnings in compiler observer |
| v3.6.0 | [#11506](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11506) | Fix share links when session storage is enabled |
| v3.6.0 | [#11538](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11538) | Add defensive guards for index pattern fields as arrays |
| v3.6.0 | [#11489](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11489) | Fix comma-separated terms pasting in filter input |
| v3.6.0 | [#11458](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11458) | Fix open link in new tab from table field |
| v3.6.0 | [#11280](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11280) | Remove meta field for Prometheus data connections |
| v3.6.0 | [#11457](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11457) | Remove zero-width space from field name text |
| v3.6.0 | [#11404](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11404) | Fix checkForFunctionProperty to handle arrays |
| v3.6.0 | [#11530](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11530) | Prevent duplicate save requests in field editor |
| v3.6.0 | [#11477](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11477) | Remove Node v14 fallback version download |
| v3.5.0 | [#10939](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10939) | Fix wildcard pattern validation |
| v3.5.0 | [#11193](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11193) | Fix server basepath for recently accessed assets |
| v3.5.0 | [#11212](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11212) | Visualizations should hide alias type |
| v3.5.0 | [#11219](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11219) | Apply data table columns filter to download CSV |
| v3.5.0 | [#11242](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11242) | Fix pivot function timestamp handling |
| v3.5.0 | [#10997](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10997) | Update DEVELOPER_GUIDE.md to include darwin-arm |
