# Data Connections Bugfixes

## Summary

OpenSearch Dashboards v2.18.0 includes several bug fixes for the Data Connections feature, improving Multi-Data Source (MDS) compatibility, UI consistency, and navigation flows. These fixes address issues with direct query data connections, including endpoint unification, UI component updates, and proper handling of the hide local cluster flag.

## Details

### What's New in v2.18.0

This release focuses on improving the Data Connections management experience in OpenSearch Dashboards, particularly for environments using Multi-Data Source (MDS) functionality.

### Technical Changes

#### UI Component Updates

| Change | Description |
|--------|-------------|
| Tabs Navigation | Replaced segmented button with tabs for switching between OpenSearch connections and Direct query connections |
| Empty Description Display | Updated en-dash (-) to em-dash (—) for empty descriptions |
| Data Source View Menu | Added datasource-view menu for direct query connections details page |
| Data Source Type Display | Added data source type column (S3, Prometheus) to the data sources page |

#### MDS Endpoint Improvements

| Change | Description |
|--------|-------------|
| Non-MDS Endpoint Muting | Muted non-MDS endpoints for direct query data connections when MDS is enabled |
| Unified Endpoint Usage | Use MDS data connection endpoint for fetching local cluster direct query content |
| Hide Local Cluster Flag | Fixed passing of `hideLocalCluster` flag to data source menu in sample data page |

#### Redirection Fixes

| Scenario | Behavior |
|----------|----------|
| Tables and Skipping Indices | Redirect to 'flint' datasource with datasource, database, and table name |
| Covering Indices and Materialized Views | Redirect to the associated index name |
| MDS Enabled | Redirect to Discover instead of Log Explorer |
| MDS Disabled | Redirect to Log Explorer |
| Query Enhancements Disabled | All redirection points are disabled |

#### Auto-Complete API Enhancement

Added MDS support to the value suggestion API, enabling auto-complete functionality to work correctly with external data sources.

### Usage Example

The Data Connections page now displays connection types:

```
Data Sources
├── OpenSearch Connections (Tab)
│   └── [List of OpenSearch cluster connections]
└── Direct Query Connections (Tab)
    ├── S3 Connection (Type: S3)
    └── Prometheus Connection (Type: Prometheus)
```

### Migration Notes

- If using MDS, the non-MDS endpoints (`/api/directquery/dataconnections`) are now muted
- Use MDS endpoints (`/api/directquery/dataconnections/dataSourceMDSId={dataSourceMDSId?}`) for all data connection operations
- Pass empty string `''` as cluster ID for local cluster calls when using MDS endpoints

## Limitations

- When `query:enhancements:enabled` is disabled, all redirection points from data connections are disabled
- The "Query data in Observability Logs" card redirects to Discover without the datasource pre-selected (limitation of current Discover implementation)

## References

### Documentation
- [Data Sources Documentation](https://docs.opensearch.org/2.18/dashboards/management/data-sources/): Official docs

### Pull Requests
| PR | Description |
|----|-------------|
| [#8460](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8460) | Replace segmented button with tabs for OpenSearch connections and Direct query connections |
| [#8492](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8492) | Updated DataSource Management to redirect to Discover and display DataSource type |
| [#8503](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8503) | Pass hide local cluster flag to data source menu in sample data page |
| [#8537](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8537) | Mute non-MDS endpoints for direct query data connections |
| [#8544](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8544) | Direct query connections fit and finish fixes |
| [#8713](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8713) | Update auto-complete API with MDS support |

### Issues (Design / RFC)
- [Issue #8256](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/8256): Redirection issue for direct query datasource in dashboards management
- [Issue #8536](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/8536): Deprecate non-MDS data connection endpoint for direct query data source

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch-dashboards/data-connections.md)
