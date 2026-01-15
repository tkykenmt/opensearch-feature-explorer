---
tags:
  - opensearch-dashboards
---
# Aggregated View Fixes

## Summary

Bug fixes and test coverage improvements for the Multiple Datasource aggregated view component in OpenSearch Dashboards v2.16.0. These changes address padding inconsistencies in the UI and significantly increase test coverage for the `DataSourceAggregatedView` component and custom database icons.

## Details

### What's New in v2.16.0

#### Padding Size Adjustments
The aggregated view component had inconsistent padding that affected the visual appearance of data source lists. The fix adjusts CSS styles to ensure proper alignment and spacing:

- Added `padding-left: 0` and `margin-right: 0` to `.euiSelectableListItem__content`
- Added `margin-right: 0` to `.euiSelectableListItem__icon` and `.euiSelectableListItem__prepend`
- Created new CSS classes `dataSourceAggregatedViewOuiFlexItem` and `dataSourceListAllActiveOuiFlexItem` for consistent styling
- Applied conditional className based on `displayAllCompatibleDataSources` prop

#### Test Coverage Improvements
Added comprehensive unit tests for:

- `DataSourceAggregatedView` component:
  - Empty state tests with local cluster hiding
  - Empty state tests due to filter-out scenarios
  - Error state tests for both local cluster visible and hidden modes
  - Tests covering various combinations of `displayAllCompatibleDataSources`, `hideLocalCluster`, and `activeDataSourceIds`

- Custom database icons:
  - `EmptyIcon` component snapshot tests
  - `ErrorIcon` component snapshot tests

### Technical Changes

| File | Change Type | Description |
|------|-------------|-------------|
| `data_source_aggregated_view.scss` | Modified | Added padding and margin adjustments, new CSS classes |
| `data_source_aggregated_view.tsx` | Modified | Conditional className based on display mode |
| `data_source_aggregated_view.test.tsx` | Modified | Added 28 new test cases for empty/error states |
| `empty_icon.test.tsx` | Added | Snapshot test for EmptyIcon component |
| `error_icon.test.tsx` | Added | Snapshot test for ErrorIcon component |

## Limitations

- These are UI-only fixes; no functional changes to data source management behavior

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#6715](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6715) | Adjust the padding size for aggregated view | - |
| [#6729](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6729) | Add more test for icon and aggregated view | [#6723](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6723), [#6724](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6724) |
