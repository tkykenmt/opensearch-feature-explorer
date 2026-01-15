---
tags:
  - opensearch-dashboards
---
# Data Source API

## Summary

In v2.16.0, the endpoint validation for the create data source saved object API was removed. This change enables users to import data sources without being blocked by the previously added endpoint validation, which was conflicting with the import functionality.

## Details

### What's New in v2.16.0

The data source plugin previously performed endpoint validation when creating a data source saved object through the API. This validation checked whether the endpoint was a valid OpenSearch endpoint by attempting to connect to it. However, this validation conflicted with the ability to import data sources, as imported data sources might not be immediately accessible during the import process.

### Technical Changes

The following changes were made to the `data_source` plugin:

| Component | Change |
|-----------|--------|
| `DataSourceSavedObjectsClientWrapper` | Removed `DataSourceServiceSetup` and `CustomApiSchemaRegistry` dependencies |
| `validateEndpoint` method | Simplified to only check URL validity using `isValidURL()`, removed connection validation |
| `validateAttributes` method | Removed `request` parameter, simplified validation flow |
| Plugin initialization | Reordered service initialization, moved `dataSourceService.setup()` after auditor registration |

### Before vs After

**Before (v2.15.0 and earlier):**
- Creating a data source saved object triggered endpoint validation
- The system attempted to connect to the endpoint to verify it was a valid OpenSearch cluster
- Import operations could fail if the endpoint was not immediately reachable

**After (v2.16.0):**
- Endpoint validation only checks URL format and blocked IP addresses
- No connection attempt is made during saved object creation
- Import operations succeed regardless of endpoint reachability
- Connection validation still occurs through the "Test connection" feature in the UI

### Impact

This change improves the user experience for:
- Importing data sources from exported NDJSON files
- Creating data sources programmatically via the API
- Bulk data source provisioning scenarios

## Limitations

- Endpoint validation is no longer performed at creation time; users should use "Test connection" to verify connectivity
- Invalid endpoints will only be detected when attempting to use the data source

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#6899](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6899) | Remove endpoint validation for create data source saved object API | [#6893](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6893) |

### Documentation
- [Configuring and using multiple data sources](https://docs.opensearch.org/2.16/dashboards/management/multi-data-sources/)
