---
tags:
  - observability
---
# Observability MDS & System Index

## Summary

OpenSearch Dashboards Observability plugin v2.16.0 introduces Multi-Data Source (MDS) support for routers and migrates notebooks storage to the `.kibana` system index for improved data management and consistency.

## Details

### What's New in v2.16.0

#### MDS Support for Routers
- Added MDS support for data connection routers
- Fixed missing `callAsCurrentUser` method for the data connections router with MDS ID parameter
- Enables proper routing of requests when using multiple data sources

#### Notebooks Migration to System Index
- Notebooks data is now stored in the `.kibana` system index instead of a custom index
- Aligns notebooks storage with other OpenSearch Dashboards saved objects
- Improves data consistency and management

#### S3 Datasource UI Improvement
- Removed duplicate description text in the S3 datasource creation flow
- Cleaner user interface when creating S3 data connections

### Technical Changes

| Component | Change |
|-----------|--------|
| Data Connections Router | Added MDS ID parameter support and `callAsCurrentUser` fix |
| Notebooks Storage | Migrated from custom index to `.kibana` system index |
| S3 Datasource Form | Removed duplicate description field |

## Limitations

- Existing notebooks may require migration when upgrading to v2.16.0
- MDS support requires proper configuration of multiple data sources in OpenSearch Dashboards

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1942](https://github.com/opensearch-project/dashboards-observability/pull/1942) | Add MDS support for routers and fix missing callAsCurrentUser | - |
| [#1937](https://github.com/opensearch-project/dashboards-observability/pull/1937) | Move notebooks to .kibana system index | - |
| [#1915](https://github.com/opensearch-project/dashboards-observability/pull/1915) | Remove duplicate description for S3 datasource flow | - |

### Documentation
- [Configuring and using multiple data sources](https://docs.opensearch.org/2.16/dashboards/management/multi-data-sources/)
- [Observability](https://docs.opensearch.org/2.16/observing-your-data/)
