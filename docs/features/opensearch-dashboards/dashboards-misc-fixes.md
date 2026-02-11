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

## Limitations

- Miscellaneous fixes are grouped together when they don't warrant individual feature reports.

## Change History
- **v3.5.0**: Fixed wildcard pattern validation in dataset selection (PR #10939), server basepath for recently accessed assets (PR #11193), alias type visibility in visualizations (PR #11212), CSV download column filtering (PR #11219), pivot function timestamp handling (PR #11242), and developer guide darwin-arm documentation (PR #10997)

## References

### Pull Requests
| Version | PR | Description |
|---------|-----|-------------|
| v3.5.0 | [#10939](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10939) | Fix wildcard pattern validation |
| v3.5.0 | [#11193](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11193) | Fix server basepath for recently accessed assets |
| v3.5.0 | [#11212](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11212) | Visualizations should hide alias type |
| v3.5.0 | [#11219](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11219) | Apply data table columns filter to download CSV |
| v3.5.0 | [#11242](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11242) | Fix pivot function timestamp handling |
| v3.5.0 | [#10997](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10997) | Update DEVELOPER_GUIDE.md to include darwin-arm |
