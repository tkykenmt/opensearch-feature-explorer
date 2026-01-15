---
tags:
  - opensearch-dashboards
---
# MDS Version Decoupling

## Summary

This bugfix adds data source version and installed plugins information to the `DataSourceView` component returns, enabling version decoupling support for the Multiple Data Source (MDS) feature. It also fixes the filter logic to ensure filters are applied correctly after fetching data source details.

## Details

### What's New in v2.16.0

The `DataSourceView` component now returns additional metadata about connected data sources:

- `datasourceversion`: The OpenSearch version of the connected data source
- `installedplugins`: List of plugins installed on the connected data source

This enables plugins to make version-aware decisions when working with different data sources, supporting the broader version decoupling initiative.

### Technical Changes

#### DataSourceView Component Fix

The filter logic in `DataSourceView` was corrected to apply filters after fetching the full data source details, rather than before:

```typescript
// Before: Filter applied before fetching details (incorrect)
if (optionId === '' && this.props.hideLocalCluster ||
    (this.props.dataSourceFilter &&
     this.props.selectedOption.filter(this.props.dataSourceFilter).length === 0)) {
  // Clear selection
}

// After: Filter applied after fetching details (correct)
if (optionId === '' && this.props.hideLocalCluster) {
  // Clear selection for local cluster
}
// Then fetch details and apply filter
const selectedDataSource = await getDataSourceById(...);
if (this.props.dataSourceFilter &&
    [selectedDataSource].filter(this.props.dataSourceFilter).length === 0) {
  // Clear selection if filter doesn't match
}
```

#### Utils Enhancement

The `getDataSourceById` utility function now includes version and plugin information in its return value:

| Field | Description |
|-------|-------------|
| `datasourceversion` | OpenSearch version from `dataSourceVersion` attribute |
| `installedplugins` | Plugin list from `installedPlugins` attribute |

### Files Changed

| File | Change |
|------|--------|
| `src/plugins/data_source_management/public/components/data_source_view/data_source_view.tsx` | Fixed filter logic timing |
| `src/plugins/data_source_management/public/components/utils.ts` | Added version and plugins to return object |

## Limitations

- Version information is only available for data sources that have been properly configured with version metadata
- Plugin list availability depends on the connected cluster's configuration

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#7420](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7420) | Add data source version and installed plugins in data source viewer returns | [#7099](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7099) |

### Issues
| Issue | Description |
|-------|-------------|
| [#7099](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7099) | Support Version Decoupling in Index Patterns Dashboards Plugin |
| [#5877](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/5877) | RFC: Plugins Version Decoupling |
