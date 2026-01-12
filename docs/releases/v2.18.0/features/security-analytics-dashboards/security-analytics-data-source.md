# Security Analytics Data Source

## Summary

This release includes multiple bug fixes for data source handling in the Security Analytics Dashboards plugin. The fixes address issues with data source picker remounting, error toast notifications, default data source selection, and getting started cards visual design.

## Details

### What's New in v2.18.0

Five bug fixes improve the data source selection experience in Security Analytics:

1. **Data Source Picker Remount Fix**: Prevents the DataSourceSelector component from remounting on every render by using `useMemo`
2. **Error Toast Suppression**: Avoids showing unhelpful error toasts when a data source is not yet selected
3. **Default Data Source Selection**: Switches to the default data source instead of local cluster on initial loading
4. **Threat Alerts Card Default**: Uses the configured data source as default for the threat alerts card instead of local cluster
5. **Getting Started Cards Update**: Updates content and visual design of getting started cards on the overview page

### Technical Changes

#### Data Source Picker Optimization

The `DataSourceSelector` component was being recreated on every render, causing React to unmount and remount the element repeatedly. This was fixed by wrapping the component creation in `useMemo`:

```typescript
const DataSourceSelector = useMemo(() => {
  if (getDataSourceMenu) {
    return getDataSourceMenu();
  }
  return null;
}, [getDataSourceMenu]);
```

#### Default Data Source Handling

The default data source observable was changed from using `LocalCluster` to an empty object, allowing proper handling when local cluster is disabled:

```typescript
// Before: Local cluster as default
const LocalCluster: DataSourceOption = { label: 'Local cluster', id: '' };
export const dataSourceObservable = new BehaviorSubject<DataSourceOption>(LocalCluster);

// After: Empty object to allow data source picker to determine correct default
export const dataSourceObservable = new BehaviorSubject<DataSourceOption>({});
```

#### Error Handling Improvements

Added logic to suppress "no living connections" errors that occur during initial data source selection:

```typescript
if (errorMessage.toLowerCase().includes('no living connections')) {
  return;
}
```

#### Threat Alerts Card Data Source

Changed the threat alerts card to use undefined as initial state instead of hardcoded local cluster:

```typescript
// Before
const [dataSource, setDataSource] = useState<DataSourceOption>({
  label: 'Local cluster',
  id: '',
});

// After
const [dataSource, setDataSource] = useState<DataSourceOption>();
```

### Getting Started Cards Visual Update

The overview page getting started cards were redesigned with:

- Icon-based visual design using EuiIcon components
- Simplified card structure with direct onClick handlers
- Updated descriptions and footer text
- New CSS class `usecaseOverviewGettingStartedCard` for styling

| Card | Icon | Description |
|------|------|-------------|
| Get Started | rocket | Configure Security Analytics tools and components |
| Discover | compass | Explore data to uncover and discover insights |
| Threat Detection | pulse | Identify security threats with detection rules |
| Threat Intelligence | radar | Scan log data for malicious actors |

## Limitations

- These fixes are specific to the Security Analytics Dashboards plugin
- Requires proper data source configuration in OpenSearch Dashboards

## References

### Documentation
- [About Security Analytics](https://docs.opensearch.org/2.18/security-analytics/): Overview of Security Analytics
- [Configuring and using multiple data sources](https://docs.opensearch.org/2.18/dashboards/management/multi-data-sources/): Multi-data source configuration guide
- [security-analytics-dashboards-plugin](https://github.com/opensearch-project/security-analytics-dashboards-plugin): GitHub repository

### Pull Requests
| PR | Description |
|----|-------------|
| [#1186](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1186) | Avoid showing unhelpful error toast when datasource is not yet selected |
| [#1188](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1188) | Fix: Update getting started cards content and visual design |
| [#1192](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1192) | Fix: data source picker remount multiple times |
| [#1199](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1199) | Bug fix to switch to default datasource instead of local cluster when initial loading |
| [#1200](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1200) | Make data source default cluster for threat alerts card |

## Related Feature Report

- [Full feature documentation](../../../../features/security-analytics-dashboards/security-analytics-dashboards-plugin.md)
