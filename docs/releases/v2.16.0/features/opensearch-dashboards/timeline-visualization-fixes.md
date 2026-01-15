---
tags:
  - opensearch-dashboards
---
# Timeline Visualization Fixes

## Summary

Improved error messaging in the Timeline visualization plugin when Multiple Data Sources (MDS) is disabled. The error message now provides clearer guidance to users attempting to use the `data_source_name` parameter without MDS enabled.

## Details

### What's New in v2.16.0

The Timeline visualization plugin's error handling was updated to provide a more user-friendly and actionable error message when users attempt to query a named data source while the MDS feature is disabled.

### Technical Changes

The `fetchDataSourceIdByName` function in `src/plugins/vis_type_timeline/server/lib/fetch_data_source_id.ts` was modified to display an improved error message:

| Before | After |
|--------|-------|
| "To query from multiple data sources, first enable the data source feature" | "data_source_name is not supported. Contact your administrator to start using multiple data sources" |

The new message:
- Clearly indicates that `data_source_name` is not supported in the current configuration
- Directs users to contact their administrator for assistance
- Aligns with UX requirements for consistent error messaging across Dashboards

### Changed Files

| File | Change |
|------|--------|
| `src/plugins/vis_type_timeline/server/lib/fetch_data_source_id.ts` | Updated error message |
| `src/plugins/vis_type_timeline/server/lib/fetch_data_source_id.test.ts` | Updated test expectation |

## Limitations

- Timeline visualization types are not fully supported when using multiple data sources (as noted in official documentation)
- The `data_source_name` parameter requires MDS to be enabled via `data_source.enabled: true` in `opensearch_dashboards.yml`

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#7069](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7069) | Update error message in timeline visualization when MDS disabled | [#7000](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7000) |

### Documentation
- [Configuring and using multiple data sources](https://docs.opensearch.org/2.16/dashboards/management/multi-data-sources/)
- [Building data visualizations - Timeline](https://docs.opensearch.org/2.16/dashboards/visualize/viz-index/)
