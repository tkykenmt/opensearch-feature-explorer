# WLM Dashboards Bugfixes

## Summary

This release fixes a bug where the data source selector dropdown was not visible on Workload Management (WLM) pages when the new home page UI setting (`home:useNewHomePage`) was enabled. This setting is enabled by default in Workspace environments, causing the MDS (Multiple Data Sources) selector to be hidden from users.

## Details

### What's New in v3.4.0

The fix removes the dependency on the `PageHeader` component for rendering the data source selector in WLM pages. Previously, the `PageHeader` component conditionally rendered the data source selector as a fallback, but when `home:useNewHomePage` was enabled, `PageHeader` returned an empty element, hiding the selector.

### Technical Changes

#### Problem

The WLM pages (WLMMain, WLMDetails, WLMCreate) used the `PageHeader` component with a `fallBackComponent` prop to render the `WLMDataSourceMenu`:

```tsx
// Before (problematic)
<PageHeader
  coreStart={core}
  depsStart={depsStart}
  fallBackComponent={
    <WLMDataSourceMenu ... />
  }
/>
```

When `home:useNewHomePage` was enabled (default in Workspace), `PageHeader` returned an empty element, causing the data source selector to disappear.

#### Solution

The fix directly renders the `WLMDataSourceMenu` component without wrapping it in `PageHeader`:

```tsx
// After (fixed)
<WLMDataSourceMenu
  coreStart={core}
  depsStart={depsStart}
  params={params}
  dataSourceManagement={dataSourceManagement}
  setDataSource={setDataSource}
  selectedDataSource={dataSource}
  onManageDataSource={() => {}}
  onSelectedDataSource={() => {
    window.history.replaceState({}, '', getDataSourceEnabledUrl(dataSource).toString());
  }}
  dataSourcePickerReadOnly={true}
/>
```

#### Files Changed

| File | Change |
|------|--------|
| `WLMMain.tsx` | Replaced `PageHeader` wrapper with direct `WLMDataSourceMenu` rendering |
| `WLMDetails.tsx` | Replaced `PageHeader` wrapper with direct `WLMDataSourceMenu` rendering |
| `WLMCreate.tsx` | Replaced `PageHeader` wrapper with direct `WLMDataSourceMenu` rendering |
| `*.test.tsx` | Updated test mocks to properly mock `dataSourceManagement.ui.getDataSourceMenu` |

#### Test Updates

The test files were updated to properly mock the data source management API:

```tsx
// Updated mock structure
const mockDataSourceManagement = {
  ui: {
    getDataSourceMenu: jest.fn(() => MockDataSourceMenu),
  },
} as any;
```

### Usage Example

After this fix, the data source selector is visible on all WLM pages regardless of the `home:useNewHomePage` setting:

1. Navigate to **Data administration > Performance > Query insights**
2. Select **Workload Management** tab
3. The data source selector dropdown is now visible at the top of the page

## Limitations

- This fix is specific to the Workload Management dashboards within the Query Insights plugin
- Other plugins may have similar issues if they rely on `PageHeader` for data source selector rendering

## References

### Documentation
- [Workload Management Documentation](https://docs.opensearch.org/3.0/tuning-your-cluster/availability-and-recovery/workload-management/wlm-feature-overview/)
- [Multiple Data Sources Documentation](https://docs.opensearch.org/3.0/dashboards/management/multi-data-sources/)
- [Query Insights Dashboards Repository](https://github.com/opensearch-project/query-insights-dashboards)

### Pull Requests
| PR | Description |
|----|-------------|
| [#421](https://github.com/opensearch-project/query-insights-dashboards/pull/421) | Fix MDS Selector for Workload Management Dashboards |

## Related Feature Report

- [Query Insights](../../../features/query-insights/query-insights.md)
