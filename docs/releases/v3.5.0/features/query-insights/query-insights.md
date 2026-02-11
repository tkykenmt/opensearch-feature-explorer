---
tags:
  - query-insights
---
# Query Insights

## Summary

OpenSearch v3.5.0 brings significant enhancements to Query Insights, including user attribution for top queries, dedicated settings API endpoints for secure Dashboard configuration, optimized query storage with string-based source field storage and truncation, and improved testing infrastructure for multi-node environments.

## Details

### What's New in v3.5.0

#### User Attribution for Top N Queries
Query Insights now captures `username` and `user_roles` for each query record, enabling administrators to identify which users are running resource-intensive queries. This integration with OpenSearch Security maps backend roles to user roles (e.g., `admin` → `all_access`).

```json
{
  "top_queries": [
    {
      "timestamp": 1766522933488,
      "id": "d0463734-cf13-4daf-aa39-3acd20783081",
      "username": "testuser",
      "user_roles": ["own_index", "all_access", "readall"],
      "measurements": { ... }
    }
  ]
}
```

#### Dedicated Settings API Endpoints
New wrapper REST API endpoints provide secure, purpose-specific access for Dashboard UI configuration without requiring broad `/_cluster/settings` permissions:

- `GET /_insights/settings[/{metric_type}]` - Retrieve settings
- `PUT /_insights/settings` - Update settings

```bash
PUT /_insights/settings
{
  "latency": {"enabled": true, "top_n_size": 20, "window_size": "5m"},
  "cpu": {"enabled": true},
  "exporter": {"type": "local_index"}
}
```

#### Optimized Query Storage
The source field is now stored as a string in the local index instead of a SearchSourceBuilder object, providing significant storage savings:

| Query Complexity | Previous | String Storage | Memory Saved |
|------------------|----------|----------------|--------------|
| Small queries | 320B/record | 312B/record | 2.6% |
| Average queries | 1.8KB/record | 751B/record | 58.4% |
| Large queries | 4.0KB/record | 2.0KB/record | 49.3% |

Source strings are also truncated to prevent excessive storage usage for very long queries.

#### Performance Optimization
User info extraction is now delayed until after Top N filtering in `TopQueriesService.addToTopNStore`, reducing overhead for queries that don't make it into the top N.

### Technical Changes

#### Index Mapping Improvements
- Added missing mapping fields for all `Attribute`, `MetricType`, and `SearchPhaseName` enum values
- Added enum-based mapping validation tests to catch missing fields
- Removed index template dependency - now relies solely on explicit index mappings

#### Exporter Behavior Changes
- Local indices are now retained when exporter type changes (previously deleted)
- Daily deletion job runs regardless of current exporter setting
- Introduced `LocalIndexLifecycleManager` for delete-after state management

#### Testing Infrastructure
- Added `integTestRemote` Gradle target for remote cluster testing
- Added `integTest` script for multi-node Jenkins runs
- Improved Cypress test pipeline with better dashboards readiness checks

## Limitations

- User attribution requires OpenSearch Security plugin to be installed
- Source field truncation may affect query analysis for very complex queries
- Rolling upgrades maintain backward compatibility by writing source as SearchSourceBuilder to existing indices

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#508](https://github.com/opensearch-project/query-insights/pull/508) | Add username and user roles to top n queries | - |
| [#527](https://github.com/opensearch-project/query-insights/pull/527) | Delay username and user roles extraction to after Top N Filtering | - |
| [#491](https://github.com/opensearch-project/query-insights/pull/491) | Add wrapper endpoints for query insights settings | [#517](https://github.com/opensearch-project/query-insights/issues/517) |
| [#483](https://github.com/opensearch-project/query-insights/pull/483) | Store source field as a string in local index | [#352](https://github.com/opensearch-project/query-insights/issues/352), [#411](https://github.com/opensearch-project/query-insights/issues/411) |
| [#484](https://github.com/opensearch-project/query-insights/pull/484) | Truncate source string in local index | [#352](https://github.com/opensearch-project/query-insights/issues/352), [#411](https://github.com/opensearch-project/query-insights/issues/411) |
| [#519](https://github.com/opensearch-project/query-insights/pull/519) | Better strategy to identify missing mapping fields | [#490](https://github.com/opensearch-project/query-insights/issues/490) |
| [#465](https://github.com/opensearch-project/query-insights/pull/465) | Retain local indices on exporter type change | [#453](https://github.com/opensearch-project/query-insights/issues/453) |
| [#479](https://github.com/opensearch-project/query-insights/pull/479) | Remove index template | - |
| [#530](https://github.com/opensearch-project/query-insights/pull/530) | Add integTestRemote target to support remote cluster testing | [#526](https://github.com/opensearch-project/query-insights/issues/526) |
| [#533](https://github.com/opensearch-project/query-insights/pull/533) | Add integTest script for multinode run on Jenkins | [#526](https://github.com/opensearch-project/query-insights/issues/526) |
| [#512](https://github.com/opensearch-project/query-insights/pull/512) | Fix Installation Documentation | [#480](https://github.com/opensearch-project/query-insights/issues/480) |
| [#451](https://github.com/opensearch-project/query-insights-dashboards/pull/451) | More reliable check on dashboards readiness in cypress test pipelines | - |
