---
tags:
  - opensearch-dashboards
---
# MDS (Multiple Data Sources)

## Summary

OpenSearch Dashboards v2.16.0 introduces significant enhancements to the Multiple Data Sources (MDS) feature, including version decoupling support, improved data source management, and various bug fixes. These changes enable better compatibility between Dashboards plugins and different OpenSearch cluster versions.

## Details

### What's New in v2.16.0

#### Version Decoupling Support
- Added `dataSourceEngineType` field to data source saved objects to distinguish between OpenSearch, Elasticsearch, and OpenSearch Serverless clusters
- Added `supportedOSDataSourceVersions` manifest entry for plugins to specify compatible data source version ranges
- Added `requiredOSDataSourcePlugins` manifest entry for plugins to specify required backend plugins
- Incompatible data sources are automatically filtered from the data source picker

#### Data Connection Details Page with MDS Support
- New Data Connection details page supporting MDS environments
- Acceleration flyout with associated object tables
- Support for creating and managing covering indexes on remote clusters
- Integration flow conditionally enabled based on MDS status and observability plugin availability

#### SQL Auto-Suggest MDS Support
- OpenSearch SQL auto-suggest now works with multiple data sources
- Query suggestions are context-aware based on selected data source

#### UI Improvements
- Compressed DataSourceSelector on management's data sources page for better space utilization
- Improved toast and popover messages for incompatible data sources
- Better handling of scenarios where all data sources are filtered out by `dataSourceFilter`

#### Bug Fixes
- Removed endpoint validation for create data source saved object API to enable data source import
- Fixed timeline visualization import to include data source name in MDS scenarios
- Fixed DSM plugin setup when MDS feature flag is disabled
- Fixed version decoupling support in Index Patterns Dashboards Plugin

### Technical Changes

#### Data Source Saved Object Schema

New `dataSourceEngineType` field added:

| Engine Type | Description |
|-------------|-------------|
| `OpenSearch` | Standard OpenSearch cluster |
| `Elasticsearch` | Elasticsearch cluster (7.10.2 compatible) |
| `OpenSearch Serverless` | AWS OpenSearch Serverless |

#### Plugin Manifest Extensions

```json
{
  "supportedOSDataSourceVersions": ">=1.0.0",
  "requiredOSDataSourcePlugins": ["plugin-name"]
}
```

#### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `data_source.enabled` | Enable MDS feature | `false` |
| `data_source.hideLocalCluster` | Hide local cluster option | `false` |
| `data_source.authTypes.NoAuthentication.enabled` | Show no-auth option | `true` |
| `data_source.authTypes.UsernamePassword.enabled` | Show username/password auth | `true` |
| `data_source.authTypes.AWSSigV4.enabled` | Show AWS SigV4 auth | `true` |

## Limitations

- Timeline visualization types not supported with MDS
- `gantt-chart` plugin not supported with MDS
- Integration flow for direct query data sources only enabled when MDS is disabled AND dashboards-observability is installed

## References

### Documentation
- [Configuring and using multiple data sources](https://docs.opensearch.org/2.16/dashboards/management/multi-data-sources/)

### Pull Requests
| PR | Repository | Description | Related Issue |
|----|------------|-------------|---------------|
| [#7323](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7323) | OpenSearch-Dashboards | Data Connection details page with MDS support | [#7143](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7143) |
| [#7463](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7463) | OpenSearch-Dashboards | Add MDS support for OpenSearch SQL auto-suggest |  |
| [#7329](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7329) | OpenSearch-Dashboards | Use compressed DataSourceSelector |  |
| [#6899](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6899) | OpenSearch-Dashboards | Remove endpoint validation for create data source saved object API | [#6893](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6893) |
| [#6678](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6678) | OpenSearch-Dashboards | Add message for incompatible data sources |  |
| [#6954](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6954) | OpenSearch-Dashboards | Include data source name when importing timeline visualization | [#6919](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6919) |
| [#7026](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7026) | OpenSearch-Dashboards | Add data source engine type to saved object | [#7021](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7021) |
| [#7100](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7100) | OpenSearch-Dashboards | Version Decoupling in Index Patterns Plugin | [#7099](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7099) |
| [#7146](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7146) | OpenSearch-Dashboards | Add required backend plugins check | [#7099](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7099) |
| [#7163](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7163) | OpenSearch-Dashboards | Fix DSM plugin setup when MDS disabled | [#7154](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7154) |
