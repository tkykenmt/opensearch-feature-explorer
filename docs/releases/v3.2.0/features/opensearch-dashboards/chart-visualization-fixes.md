---
tags:
  - domain/core
  - component/dashboards
  - dashboards
  - observability
---
# Chart & Visualization Fixes

## Summary

This release includes two bug fixes for chart and visualization components in OpenSearch Dashboards: fixing the line chart legend display logic and resolving a popover toggle issue in the data source association UI.

## Details

### What's New in v3.2.0

#### Line Chart Legend Fix

The line chart visualization in the Explore plugin had incorrect logic for determining when to hide the legend. Previously, the legend was hidden when there was 1 metric, 0 categorical columns, and 0 date columns. This was incorrect because a typical time-series line chart has 1 metric and 1 date column.

**Before (incorrect)**:
```typescript
const notShowLegend =
    numericalColumns.length === 1 && categoricalColumns.length === 0 && dateColumns.length === 0;
```

**After (correct)**:
```typescript
const notShowLegend =
    numericalColumns.length === 1 && categoricalColumns.length === 0 && dateColumns.length === 1;
```

The legend is now correctly hidden only when displaying a simple time-series chart with a single metric over time, where showing a legend would be redundant.

#### Popover Toggle Fix

The "Associate data sources" button in the Data Sources page had a bug where clicking the button twice would not close the popover. The popover would remain open and could not be dismissed by clicking outside.

**Before**: The button always called `setIsOpen(true)`, so clicking it again had no effect.

**After**: The button now toggles the state with `setIsOpen((prevState) => !prevState)`, allowing users to close the popover by clicking the button again.

### Technical Changes

#### Modified Components

| Component | File | Change |
|-----------|------|--------|
| LineVisStyleControls | `src/plugins/explore/public/components/visualizations/line/line_vis_options.tsx` | Fixed legend visibility condition |
| DataSourceAssociation | `src/plugins/workspace/public/components/data_source_association/data_source_association.tsx` | Changed popover open to toggle |

## Limitations

- The line chart legend fix is specific to the Explore plugin's line visualization
- The popover fix is specific to the workspace data source association component

## References

### Documentation
- [PR #9911](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9911): Line chart legend fix
- [PR #9993](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9993): Popover toggle fix

### Pull Requests
| PR | Description |
|----|-------------|
| [#9911](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9911) | Disable legend for line chart when it is 1 metric and 1 date |
| [#9993](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9993) | Fix popover not close if double click |

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch-dashboards/chart-visualization-fixes.md)
