---
tags:
  - opensearch-dashboards
---
# VisBuilder Fixes

## Summary

Bug fixes for VisBuilder visualization tool in OpenSearch Dashboards v2.16.0, addressing rendering issues with Metric and Table visualizations, configuration pane scrolling problems, legend toggle functionality, and data source compatibility.

## Details

### What's New in v2.16.0

Three PRs addressed critical VisBuilder bugs:

1. **Flat Render Structure Fix** (PR #6674): Fixed rendering issues in Metric and Table visualizations caused by callback behavior in `ReactExpressionRenderer`. The `VisualizationContainer` wrapper was preventing proper `isLoading` state updates.

2. **Configuration Pane and Legend Toggle Fixes** (PR #6811): Fixed two UI issues:
   - Configuration pane scrolling horizontally when dragging fields (caused by secondary edit pane being added to DOM even when not in use)
   - Legend toggle affordance not working after initial toggle

3. **Data Source Compatibility Fix** (PR #6948): Fixed VisBuilder visualizations not rendering when using multiple data sources. Added handling for `visbuilder` type to support data source by updating references with proper index pattern ID prefixes.

### Technical Changes

| Issue | Root Cause | Fix |
|-------|------------|-----|
| Metric/Table not rendering | `VisualizationContainer` wrapper breaking `isLoading` callback | Moved `VisualizationContainer` directly into `MetricVisComponent` |
| Config pane horizontal scroll | Secondary edit pane in DOM when not visible | Hide secondary pane properly when not in use |
| Legend toggle broken | State not updating correctly after first toggle | Fixed toggle state management |
| Data source rendering failure | Index pattern ID missing data source prefix | Added `visbuilder` type handling in sample data reference updates |

### Affected Components

| Component | File Path |
|-----------|-----------|
| MetricVisComponent | `src/plugins/vis_builder/public/visualizations/metric/` |
| TableVisComponent | `src/plugins/vis_builder/public/visualizations/table/` |
| Configuration Pane | `src/plugins/vis_builder/public/application/components/` |
| Sample Data Util | `src/plugins/home/server/services/sample_data/data_sets/util.ts` |

## Limitations

- These fixes are specific to VisBuilder; similar issues in other visualization types may require separate fixes
- Data source compatibility fix only addresses sample data scenarios

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#6674](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6674) | Flat render structure in Metric and Table Vis | [#6671](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6671) |
| [#6811](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6811) | Bug Fixes for Vis Builder | [#6679](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6679), [#6680](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6680) |
| [#6948](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6948) | Fix web log sample visualization & vis-builder not rendering with data source | [#6857](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6857), [#6938](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6938) |
