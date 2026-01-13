---
tags:
  - query-insights
---
# Query Insights Enhancements

## Summary

OpenSearch v2.19.0 introduces significant enhancements to the Query Insights plugin, including a new dashboards interface for monitoring top N queries, configurable data retention with automatic index deletion, usage counters for tracking API usage, and improved query identification capabilities.

## Details

### What's New in v2.19.0

#### Query Insights Dashboards

A new OpenSearch Dashboards plugin (`query-insights-dashboards`) provides a visual interface for monitoring and analyzing top N queries:

- **Top N Queries Overview Page**: Displays query metrics and details for the top queries
- **Query Details Page**: Shows detailed information for individual queries and query groups
- **Configuration Page**: Allows configuring Top N query settings through the UI
- **Historical Data Integration**: Supports viewing historical query data with time range selection
- **Query Grouping Support**: Visualizes grouped queries with aggregate statistics

#### Data Retention Management

New `delete_after_days` setting enables automatic cleanup of historical query data:

```bash
PUT _cluster/settings
{
  "persistent": {
    "search.insights.top_queries.delete_after_days": "10"
  }
}
```

| Setting | Description | Default | Range |
|---------|-------------|---------|-------|
| `search.insights.top_queries.delete_after_days` | Days to retain local index data | `7` | `1` to `180` |

- Scheduled job runs daily at 00:05 UTC to delete expired indices
- Only applicable when `exporter.type` is `local_index`
- Indices matching pattern `top_queries-YYYY.MM.dd-xxxxx` are automatically cleaned up

#### Usage Counter

New usage counter tracks Top N Queries API usage with metric type and group-by type as dimensions, enabling better monitoring of plugin utilization.

#### Query Identification

- Added `type` attribute to search query records for better categorization
- Added `query_group_hashcode` field to top queries response for consistent query identification
- Model changes for hashcode and ID fields improve query tracking

#### Exporter and Reader Refactoring

Major refactoring of exporters and readers addresses several issues:
- Consolidated exporter configuration from per-metric to service level
- Added index metadata to identify Query Insights-created indices
- Defined index mapping and index-level sorting for better query performance
- Implemented deduplication to prevent duplicate records when multiple metrics are enabled
- Fixed historical data hash generation for older dates

### Technical Changes

#### New Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `search.insights.top_queries.delete_after_days` | Retention period for local index data | `7` |

#### API Enhancements

**Fetch Top Queries by ID:**
```bash
GET /_insights/top_queries?id={query-id}&from={timestamp}&to={timestamp}
```

**Field Type Cache Stats:**
Added field type cache statistics to the health stats API for monitoring cache performance.

### Bug Fixes

- Fixed parsing error in SearchQueryRecord
- Fixed `node_id` missing in local index
- Fixed null indexFieldMap bug
- Fixed toString on operational metrics
- Fixed grouping integration tests

## Limitations

- `delete_after_days` setting only applies when exporter type is `local_index`
- Changing exporter type from `local_index` deletes all existing local indices

## References

### Documentation
- [Query Insights Documentation](https://docs.opensearch.org/2.19/observing-your-data/query-insights/index/)
- [Top N Queries Documentation](https://docs.opensearch.org/2.19/observing-your-data/query-insights/top-n-queries/)
- [Query Insights Dashboards](https://docs.opensearch.org/2.19/observing-your-data/query-insights/query-insights-dashboard/)

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#172](https://github.com/opensearch-project/query-insights/pull/172) | Top N indices auto deletion config & functionality | [#165](https://github.com/opensearch-project/query-insights/issues/165) |
| [#153](https://github.com/opensearch-project/query-insights/pull/153) | Usage counter for Top N queries |   |
| [#157](https://github.com/opensearch-project/query-insights/pull/157) | Add type attribute to search query record |   |
| [#156](https://github.com/opensearch-project/query-insights/pull/156) | Make default window size valid for all metric types |   |
| [#187](https://github.com/opensearch-project/query-insights/pull/187) | Ensure query_group_hashcode is present in all cases |   |
| [#191](https://github.com/opensearch-project/query-insights/pull/191) | Model changes for hashcode and id |   |
| [#195](https://github.com/opensearch-project/query-insights/pull/195) | Add fetch top queries by id API | [#159](https://github.com/opensearch-project/query-insights/issues/159) |
| [#193](https://github.com/opensearch-project/query-insights/pull/193) | Add field type cache stats |   |
| [#205](https://github.com/opensearch-project/query-insights/pull/205) | Always collect available metrics in top queries service |   |
| [#210](https://github.com/opensearch-project/query-insights/pull/210) | Refactor Exporters and Readers |   |
| [#184](https://github.com/opensearch-project/query-insights/pull/184) | Fix parsing error in SearchQueryRecord |   |
| [#207](https://github.com/opensearch-project/query-insights/pull/207) | Fix bug on node_id missing in local index |   |
| [#214](https://github.com/opensearch-project/query-insights/pull/214) | Fix null indexFieldMap bug & add UTs |   |
| [#219](https://github.com/opensearch-project/query-insights/pull/219) | Fix toString on operational metrics |   |
| [#223](https://github.com/opensearch-project/query-insights/pull/223) | Fix grouping integ tests |   |
