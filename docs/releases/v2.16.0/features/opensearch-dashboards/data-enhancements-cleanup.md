---
tags:
  - opensearch-dashboards
---
# Data Enhancements Cleanup

## Summary

This deprecation removes the `data.enhancements.enabled` configuration toggle and the `query:dataSource:readOnly` UI setting from OpenSearch Dashboards. The query enhancements feature now relies solely on the `query:enhancements:enabled` UI setting for enablement, simplifying the configuration model.

## Details

### What's Deprecated in v2.16.0

The following configuration options have been removed:

| Removed Setting | Type | Previous Default | Replacement |
|-----------------|------|------------------|-------------|
| `data.enhancements.enabled` | opensearch_dashboards.yml | `false` | Use `query:enhancements:enabled` UI setting |
| `query:dataSource:readOnly` | UI Setting | `true` | Removed (no replacement needed) |

### Technical Changes

1. **Configuration File Changes**
   - Removed `data.enhancements.enabled` from `opensearch_dashboards.yml`
   - The `start:enhancements` npm script no longer requires the `--data.enhancements.enabled=true` flag

2. **UI Settings Cleanup**
   - Removed `QUERY_DATA_SOURCE_READONLY` constant from UI settings
   - Removed the "Read-only data source in query editor" advanced setting
   - Query editor no longer checks `isDataSourceReadOnly` flag

3. **Code Simplification**
   - Settings class now initializes `isEnabled` to `false` instead of reading from config
   - Removed dead URL link reference in template.tsx

### Migration

Users who previously enabled data enhancements via `data.enhancements.enabled: true` in `opensearch_dashboards.yml` should:

1. Remove the `data.enhancements.enabled` line from configuration
2. Enable query enhancements via Advanced Settings: `query:enhancements:enabled = true`

## Limitations

- The `query:dataSource:readOnly` setting is removed without replacement as it was experimental and caused confusion

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#7291](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7291) | Remove data enhancements config and readonly flag | Followup to [#7212](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7212) |
| [#7212](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7212) | Add query enhancements plugin as a core plugin | [#6072](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6072) |
