---
tags:
  - opensearch-dashboards
---
# MDS (Multiple Data Sources)

## Summary

OpenSearch Dashboards v2.16.0 introduces significant enhancements to the Multiple Data Sources (MDS) feature, including version decoupling support, improved data source management controls, dataframes support, and better UI/UX for data source selection.

## Details

### What's New in v2.16.0

#### Version Decoupling Support
- Added `dataSourceEngineType` field to data source saved objects
- New manifest entries: `supportedOSDataSourceVersions` and `requiredOSDataSourcePlugins`
- Plugins can now specify compatible OpenSearch versions and required backend plugins
- Improved messaging for incompatible data sources

#### Data Source Management Controls
- New `data_source.manageableBy` configuration option with values:
  - `all`: Anyone can manage data sources
  - `dashboard_admin`: Only OSD admins can manage data sources
  - `none`: Data source management is disabled
- Routes `/create`, `/configure/opensearch`, and `/configure/:type` are hidden when `manageableBy` is `none`
- Edit data source screen inputs are disabled based on `manageableBy` setting

#### Dataframes Support
- Dataframes now support MDS with `dataSourceId` in metadata
- Data source information is parsed from user query strings using `::datasource::` syntax
- Dataframes are created before the interceptor to preserve metadata

#### Data Source Selector Improvements
- Conditional rendering of data source selector based on query language
- Selector disappears when specific languages are selected with enhancements enabled
- Added `removedComponentIds` to handle component unmount race conditions
- Compressed DataSourceSelector for better UI

#### Timeline Visualization MDS Support
- Sample data for Timeline visualizations now includes data source name when MDS is enabled
- Fixed timeline visualization import with proper data source name handling

#### Security Enhancements
- Placeholder values used for data source credentials during export
- Credentials fields replaced with `pleaseUpdateCredentials` in exported `.ndjson` files
- Import still succeeds with placeholder credentials

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `data_source.enabled` | Enable/disable MDS feature | `false` |
| `data_source.manageableBy` | Control who can manage data sources (`all`, `dashboard_admin`, `none`) | `all` |
| `data_source.hideLocalCluster` | Hide local cluster from data source picker | `false` |

### Usage Example

Configure data source management restrictions:

```yaml
data_source.enabled: true
data_source.manageableBy: "dashboard_admin"
```

## Limitations

- Timeline visualization types are not fully supported with MDS
- `gantt-chart` plugin is not supported with MDS
- Reporting plugin is automatically de-registered when MDS is enabled
- Dataframe schema may not persist across initial calls

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#6919](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6919) | Allow adding sample data for Timeline visualizations with MDS | - |
| [#6920](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6920) | Add removedComponentIds for data source selection service | - |
| [#6928](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6928) | Use placeholder for data source credentials fields when export | [#6892](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6892) |
| [#7059](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7059) | Render the datasource selector component conditionally | [#7046](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7046) |
| [#7106](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7106) | Onboard dataframes support to MDS | [#6957](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6957) |
| [#7143](https://github.com/opensearch-project/dashboards-observability/pull/7143) | Observability Datasource Plugin migration with MDS support | - |
| [#7214](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7214) | Restrict to edit data source on the DSM UI | [#6889](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6889) |
| [#7298](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7298) | Disable certain routes when data_source.manageableBy is none | - |
| [#7307](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7307) | Disable inputs in edit data source screen when manageableBy is set | - |

### Documentation
- [Configuring and using multiple data sources](https://docs.opensearch.org/2.16/dashboards/management/multi-data-sources/)
