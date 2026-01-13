---
tags:
  - domain/observability
  - component/server
  - dashboards
  - indexing
  - observability
  - performance
  - search
---
# Query Insights Enhancements

## Summary

OpenSearch v3.1.0 brings significant enhancements to the Query Insights plugin, including metric labels for historical data filtering, consolidated grouping settings, index exclusion capabilities, asynchronous search operations for improved performance, and a new `isCancelled` field in the Live Queries API. The dashboards also receive major updates with a new Live Queries Dashboard and Workload Management (WLM) Dashboard for comprehensive query monitoring and management.

## Details

### What's New in v3.1.0

#### Backend Enhancements

1. **Metric Labels for Historical Data** - Added `top_n_query` attribute to `SearchQueryRecord` that tracks which metric types (latency, cpu, memory) a query was in the top N for. This enables filtering historical queries by metric type when reading from local indexes.

2. **Consolidated Grouping Settings** - Reorganized grouping-related settings under a unified namespace:
   - `search.insights.top_queries.group_by` → `search.insights.top_queries.grouping.group_by`
   - `search.insights.top_queries.max_groups_excluding_topn` → `search.insights.top_queries.grouping.max_groups_excluding_topn`

3. **Index Exclusion Setting** - New `excluded_indices` setting allows users to exclude specific indices from query insights collection, useful for filtering out system indices or high-volume internal queries.

4. **Asynchronous Search Operations** - Refactored the local index reader to use asynchronous operations with listener-based approaches, improving performance and scalability when retrieving historical query data.

5. **Live Queries API Enhancement** - Added `is_cancelled` boolean field to the Live Queries API response to indicate whether a query has been cancelled.

#### Dashboard Enhancements

1. **New Live Queries Dashboard** - A comprehensive real-time monitoring interface featuring:
   - Auto-refresh toggle with configurable intervals (5s, 10s, etc.)
   - Dashboard metrics: total active queries, average latency, longest running query, CPU/memory usage
   - Visual breakdown by Node and Index with Donut/Bar chart toggle
   - Query cancellation (individual and bulk)
   - Dynamic time and memory formatting

2. **New Workload Management Dashboard** - Full WLM UI for query group management:
   - Main page with real-time workload stats at node level
   - Detail page with resource consumption breakdown
   - Create, update, and delete query groups
   - Integration with Live Queries for bi-directional navigation

3. **Performance Improvement** - Fixed duplicate API requests on overview page loading.

### Technical Changes

#### New Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `search.insights.top_queries.grouping.group_by` | Group queries by: `none`, `similarity` | `none` |
| `search.insights.top_queries.grouping.max_groups_excluding_topn` | Maximum groups to track excluding top N | `100` |
| `search.insights.top_queries.grouping.attributes.field_name` | Include field names in grouping | `true` |
| `search.insights.top_queries.grouping.attributes.field_type` | Include field types in grouping | `true` |
| `search.insights.top_queries.excluded_indices` | Indices to exclude from insights | `[]` |

#### API Changes

**Live Queries API Response Enhancement:**
```json
{
  "live_queries": [
    {
      "timestamp": 1749187466964,
      "id": "node-A1B2C3D4E5:3600",
      "description": "indices[top_queries-*], search_type[QUERY_THEN_FETCH]",
      "node_id": "node-A1B2C3D4E5",
      "measurements": {
        "latency": { "number": 7990852130, "count": 1, "aggregationType": "NONE" },
        "cpu": { "number": 89951, "count": 1, "aggregationType": "NONE" },
        "memory": { "number": 3818, "count": 1, "aggregationType": "NONE" }
      },
      "is_cancelled": true
    }
  ]
}
```

**Historical Query Filtering by Metric Type:**
```bash
# Only returns queries that were in top N for latency
GET /_insights/top_queries?from=2025-01-01T00:00:00.000Z&to=2026-01-01T00:00:00.000Z&type=latency

# Only returns queries that were in top N for CPU
GET /_insights/top_queries?from=2025-01-01T00:00:00.000Z&to=2026-01-01T00:00:00.000Z&type=cpu
```

### Usage Example

**Configure grouping settings (new namespace):**
```bash
PUT _cluster/settings
{
  "persistent": {
    "search.insights.top_queries.grouping.group_by": "similarity",
    "search.insights.top_queries.grouping.max_groups_excluding_topn": 100,
    "search.insights.top_queries.grouping.attributes.field_name": true,
    "search.insights.top_queries.grouping.attributes.field_type": true
  }
}
```

**Exclude indices from insights:**
```bash
PUT _cluster/settings
{
  "persistent": {
    "search.insights.top_queries.excluded_indices": [".kibana*", "top_queries-*"]
  }
}
```

### Migration Notes

- **Grouping Settings Migration**: If you were using `search.insights.top_queries.group_by` or `search.insights.top_queries.max_groups_excluding_topn`, update to the new `grouping.*` namespace.
- **Dashboard Updates**: The new Live Queries and WLM dashboards are automatically available after upgrading the Query Insights Dashboards plugin.

## Limitations

- The `is_cancelled` field in Live Queries API reflects the cancellation status at the time of the API call
- Asynchronous reader operations require integration tests for full transport layer validation
- WLM Dashboard requires the Workload Management plugin to be installed for full functionality

## References

### Documentation
- [Query Insights Documentation](https://docs.opensearch.org/3.0/observing-your-data/query-insights/index/)

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#326](https://github.com/opensearch-project/query-insights/pull/326) | query-insights | Add metric labels to historical data |
| [#336](https://github.com/opensearch-project/query-insights/pull/336) | query-insights | Consolidate grouping settings |
| [#308](https://github.com/opensearch-project/query-insights/pull/308) | query-insights | Add setting to exclude certain indices |
| [#344](https://github.com/opensearch-project/query-insights/pull/344) | query-insights | Asynchronous search operations in reader |
| [#355](https://github.com/opensearch-project/query-insights/pull/355) | query-insights | Added isCancelled field in Live Queries API |
| [#199](https://github.com/opensearch-project/query-insights-dashboards/pull/199) | query-insights-dashboards | New Live Queries Dashboard |
| [#155](https://github.com/opensearch-project/query-insights-dashboards/pull/155) | query-insights-dashboards | New Workload Management Dashboard |
| [#179](https://github.com/opensearch-project/query-insights-dashboards/pull/179) | query-insights-dashboards | Remove duplicate requests on overview page |
| [#209](https://github.com/opensearch-project/query-insights-dashboards/pull/209) | query-insights-dashboards | Add unit tests for WLM dashboard |

### Issues (Design / RFC)
- [Issue #301](https://github.com/opensearch-project/query-insights/issues/301): Metric labels for historical data
- [Issue #136](https://github.com/opensearch-project/query-insights/issues/136): Consolidate grouping settings
- [Issue #260](https://github.com/opensearch-project/query-insights/issues/260): Exclude indices from insights
- [Issue #354](https://github.com/opensearch-project/query-insights/issues/354): isCancelled field in Live Queries
- [Issue #152](https://github.com/opensearch-project/query-insights-dashboards/issues/152): Live Queries Dashboard
- [Issue #105](https://github.com/opensearch-project/query-insights-dashboards/issues/105): Duplicate requests bug

## Related Feature Report

- [Full feature documentation](../../../../features/query-insights/query-insights.md)
