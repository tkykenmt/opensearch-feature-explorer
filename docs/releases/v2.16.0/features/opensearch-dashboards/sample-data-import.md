---
tags:
  - opensearch-dashboards
---
# Sample Data Import

## Summary

Fixed two bugs related to sample data import when Multiple Data Sources (MDS) is enabled. Index pattern references now correctly include data source information, and TSVB visualizations properly render data from external data sources.

## Details

### What's New in v2.16.0

Two critical bug fixes improve sample data functionality with Multiple Data Sources:

1. **Index Pattern Data Source Reference Fix**: When importing sample data with a data source selected, index patterns now correctly retain the data source reference. Previously, the data source connection was lost after import.

2. **TSVB Visualization Data Source Support**: Time Series Visual Builder (TSVB) visualizations in sample data now properly connect to external data sources. Previously, TSVB visualizations failed to render data when sample data was imported to a non-local data source.

### Technical Changes

#### Index Pattern Reference Update (PR #6851)

The fix restores the reference update logic for index pattern saved objects during sample data import:

- Added back references update for index pattern saved objects when importing sample data
- Index patterns now correctly show the selected data source connection in the management page
- Unit tests added to verify references are updated when generating sample data with data source method

#### TSVB Data Source Support (PR #6940)

The fix adds proper data source handling for TSVB visualizations:

- Attaches `data_source_id` to the TSVB `visState` during sample data generation
- Adds data source reference to TSVB saved objects
- TSVB visualizations now render correctly in both edit view and dashboard view when MDS is enabled
- `DataSourceSelector` component properly displays the correct data source option

### Affected Components

| Component | Change |
|-----------|--------|
| Sample Data Service | Updated to properly handle data source references |
| Index Pattern Saved Objects | References now include data source information |
| TSVB Visualizations | Added data source ID attachment and reference handling |
| Sample Flights | Fixed for MDS compatibility |
| Sample E-commerce | Fixed for MDS compatibility |
| Sample Web Logs | Fixed for MDS compatibility |

## Limitations

- Fixes only apply when `data_source.enabled: true` is set in `opensearch_dashboards.yml`
- Local cluster sample data import is unaffected by these changes

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#6851](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6851) | Fix index pattern data source reference not updated in sample data | [#6850](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6850) |
| [#6940](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6940) | Fix sample data to use datasources for TSVB visualizations | [#6936](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6936) |

### Related Resources
- [Multiple Data Sources Saved Objects Import Blog](https://opensearch.org/blog/enhancement-multiple-data-source-import-saved-object/)
