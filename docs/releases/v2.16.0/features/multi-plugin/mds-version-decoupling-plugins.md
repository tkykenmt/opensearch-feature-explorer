---
tags:
  - multi-plugin
---
# MDS Version Decoupling - Plugin Support

## Summary

In v2.16.0, multiple OpenSearch Dashboards plugins added version decoupling metadata for Multi-Data Source (MDS) support. This enables plugins to declare their supported OpenSearch versions and required backend plugins, allowing the MDS feature to filter out incompatible data sources from the data source picker.

## Details

### What's New in v2.16.0

Version decoupling support was added to 9 dashboards plugins through manifest metadata entries:

| Plugin | Repository | PR |
|--------|------------|-----|
| Observability | dashboards-observability | [#1953](https://github.com/opensearch-project/dashboards-observability/pull/1953) |
| Alerting | alerting-dashboards-plugin | [#1003](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1003) |
| Anomaly Detection | anomaly-detection-dashboards-plugin | [#806](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/806) |
| ML Commons | ml-commons-dashboards | [#338](https://github.com/opensearch-project/ml-commons-dashboards/pull/338) |
| Security | security-dashboards-plugin | [#2051](https://github.com/opensearch-project/security-dashboards-plugin/pull/2051) |
| Notifications | dashboards-notifications | [#223](https://github.com/opensearch-project/dashboards-notifications/pull/223) |
| Index Management | index-management-dashboards-plugin | [#1080](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1080) |
| Query Workbench | dashboards-query-workbench | [#353](https://github.com/opensearch-project/dashboards-query-workbench/pull/353) |

### Technical Changes

#### Plugin Manifest Metadata

Each plugin adds version decoupling metadata to its `opensearch_dashboards.json` manifest file:

```json
{
  "id": "plugin-name",
  "version": "2.16.0.0",
  "supportedOSDataSourceVersions": ">=2.13.0",
  "requiredOSDataSourcePlugins": ["opensearch-alerting"]
}
```

| Field | Description |
|-------|-------------|
| `supportedOSDataSourceVersions` | Semver range of supported OpenSearch versions |
| `requiredOSDataSourcePlugins` | List of required backend plugins on the data source |

#### Data Source Filter Function

Plugins implement a `dataSourceFilter` function that uses the manifest metadata to filter compatible data sources:

```typescript
const dataSourceFilter = (dataSource: DataSourceOption) => {
  // Check version compatibility
  if (!satisfies(dataSource.version, supportedOSDataSourceVersions)) {
    return false;
  }
  // Check required plugins
  return requiredOSDataSourcePlugins.every(
    plugin => dataSource.installedPlugins?.includes(plugin)
  );
};
```

### Plugin-Specific Version Requirements

| Plugin | Minimum Version | Required Backend Plugins |
|--------|-----------------|-------------------------|
| Alerting | >=2.13.0 | opensearch-alerting |
| Anomaly Detection | >=2.4.0 | opensearch-anomaly-detection |
| ML Commons | >=2.4.0 | opensearch-ml |
| Security | >=2.4.0 | opensearch-security |
| Notifications | >=2.0.0 | opensearch-notifications |
| Index Management | >=2.0.0 | opensearch-index-management |
| Observability | >=2.6.0 | opensearch-observability |
| Query Workbench | >=2.4.0 | opensearch-sql |

### User Experience

When MDS is enabled, the data source picker only shows data sources that meet the plugin's version and plugin requirements. Incompatible data sources are filtered out, preventing users from selecting clusters that don't support the plugin's functionality.

## Limitations

- Version decoupling only works when `data_source.enabled: true` is set in `opensearch_dashboards.yml`
- Backend plugin detection requires the connected cluster to expose plugin information via the `/_cat/plugins` API
- Some plugins may have additional compatibility requirements beyond version and plugin checks

## References

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#1953](https://github.com/opensearch-project/dashboards-observability/pull/1953) | dashboards-observability | Version-decoupling for Observability |
| [#1003](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1003) | alerting-dashboards-plugin | Plugin Version decoupling for MDS support |
| [#806](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/806) | anomaly-detection-dashboards-plugin | MDS version decoupling |
| [#338](https://github.com/opensearch-project/ml-commons-dashboards/pull/338) | ml-commons-dashboards | Add version decoupling meta for MDS |
| [#2051](https://github.com/opensearch-project/security-dashboards-plugin/pull/2051) | security-dashboards-plugin | Adds datasource filter for version decoupling |
| [#223](https://github.com/opensearch-project/dashboards-notifications/pull/223) | dashboards-notifications | Backport version decoupling |
| [#1080](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1080) | index-management-dashboards-plugin | Adding dataVersionFilter support to MDS |
| [#353](https://github.com/opensearch-project/dashboards-query-workbench/pull/353) | dashboards-query-workbench | Version decoupling for neo MDS support |

### Issues
| Issue | Description |
|-------|-------------|
| [#5877](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/5877) | RFC: Plugins Version Decoupling |
| [#1971](https://github.com/opensearch-project/security-dashboards-plugin/issues/1971) | Add datasource filter for version decoupling in Security |
