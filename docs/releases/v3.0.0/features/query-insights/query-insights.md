# Query Insights

## Summary

OpenSearch v3.0.0 introduces significant enhancements to the Query Insights plugin, including a new Live Queries API for real-time monitoring of in-flight search queries, default index templates for improved data management, a verbose parameter for lightweight API responses, and profile query filtering. These improvements provide better observability, performance optimization, and operational flexibility for monitoring search query performance.

## Details

### What's New in v3.0.0

#### Live Queries API (New Feature)

A new API endpoint `GET /_insights/live_queries` enables real-time monitoring of currently executing search queries across the cluster. This is useful for identifying and debugging queries that are running for an unexpectedly long time or consuming significant resources.

**API Endpoint:**
```
GET /_insights/live_queries
```

**Query Parameters:**

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `verbose` | Boolean | Include detailed query information | `true` |
| `nodeId` | String | Filter results by node IDs (comma-separated) | All nodes |
| `sort` | String | Sort by metric: `latency`, `cpu`, or `memory` | `latency` |
| `size` | Integer | Number of query records to return | `100` |

**Example Request:**
```bash
GET /_insights/live_queries?verbose=false&sort=cpu&size=10
```

**Example Response:**
```json
{
  "live_queries": [
    {
      "timestamp": 1745359226777,
      "id": "troGHNGUShqDj3wK_K5ZIw:512",
      "description": "indices[my-index-*], search_type[QUERY_THEN_FETCH], source[...]",
      "node_id": "troGHNGUShqDj3wK_K5ZIw",
      "measurements": {
        "latency": { "number": 13959364458, "count": 1, "aggregationType": "NONE" },
        "memory": { "number": 3104, "count": 1, "aggregationType": "NONE" },
        "cpu": { "number": 405000, "count": 1, "aggregationType": "NONE" }
      }
    }
  ]
}
```

#### Default Index Template for Local Index

A default index template is now automatically created for Query Insights local indexes (`top_queries-*`), providing:

- Auto-expanding replicas (0-2) for high availability
- Single shard configuration for optimal performance
- Configurable template priority via cluster settings

**New Configuration:**

| Setting | Description | Default |
|---------|-------------|---------|
| `search.insights.top_queries.exporter.template_priority` | Priority of the index template | `1847` |

**Index Template Settings:**
```json
{
  "index_patterns": ["top_queries-*"],
  "template": {
    "settings": {
      "index": {
        "number_of_shards": "1",
        "auto_expand_replicas": "0-2"
      }
    }
  }
}
```

#### Top Queries API Verbose Parameter

The `top_queries` API now supports a `verbose` parameter for lightweight responses:

```bash
GET /_insights/top_queries?verbose=false
```

When `verbose=false`, the following fields are omitted:
- `task_resource_usages`
- `source`
- `phase_latency_map`

This reduces response payload size for monitoring and overview use cases.

#### Skip Profile Queries

Profile search requests are now automatically filtered out from Top N queries collection. This prevents diagnostic queries from polluting the query insights data.

#### Strict Hash Check on Top Queries Indices

Added strict hash validation for top queries indices to ensure data integrity and prevent potential data corruption issues.

### Technical Changes

#### Architecture Changes

```mermaid
graph TB
    subgraph "Query Insights Plugin v3.0.0"
        A[Search Request] --> B[Query Listener]
        B --> C{Profile Query?}
        C -->|Yes| D[Skip]
        C -->|No| E[Collectors]
        E --> F[Processors]
        F --> G[Exporters]
        G --> H[(Local Index)]
        H --> I[Index Template]
        
        J[Live Queries API] --> K[Task Manager]
        K --> L[Running Tasks]
        L --> M[SearchQueryRecord]
    end
    
    subgraph "APIs"
        N[/_insights/top_queries]
        O[/_insights/live_queries]
    end
    
    F --> N
    M --> O
```

#### New Components

| Component | Description |
|-----------|-------------|
| `LiveQueriesAction` | Transport action for fetching in-flight queries |
| `LiveQueriesRequest` | Request model with filtering and sorting options |
| `LiveQueriesResponse` | Response containing live query records |
| `QueryInsightsIndexTemplate` | Manages default index template creation |

#### New Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `search.insights.top_queries.exporter.template_priority` | Index template priority | `1847` |

### Usage Examples

**Monitor live queries sorted by CPU usage:**
```bash
curl -X GET "localhost:9200/_insights/live_queries?sort=cpu&size=5&pretty"
```

**Get lightweight top queries response:**
```bash
curl -X GET "localhost:9200/_insights/top_queries?verbose=false&pretty"
```

**Override index template priority:**
```bash
curl -X PUT 'localhost:9200/_cluster/settings' -H 'Content-Type: application/json' -d'
{
    "persistent": {
        "search.insights.top_queries.exporter.template_priority": "3000"
    }
}'
```

### Migration Notes

- The default index template is automatically created when the plugin starts
- Existing top queries indices are not affected; new indices will use the template
- Profile queries are now automatically excluded from Top N queries

## Limitations

- Live Queries API returns only coordinator node resource usage (not data node usage)
- The `verbose` parameter only affects response serialization, not data collection

## References

### Documentation
- [Documentation](https://docs.opensearch.org/3.0/observing-your-data/query-insights/index/): Query Insights overview
- [Live Queries Documentation](https://docs.opensearch.org/3.0/observing-your-data/query-insights/live-queries/): Live Queries API

### Pull Requests
| PR | Description |
|----|-------------|
| [#295](https://github.com/opensearch-project/query-insights/pull/295) | Inflight Queries API |
| [#254](https://github.com/opensearch-project/query-insights/pull/254) | Add default index template for query insights local index |
| [#300](https://github.com/opensearch-project/query-insights/pull/300) | Add top_queries API verbose param |
| [#298](https://github.com/opensearch-project/query-insights/pull/298) | Skip profile queries |
| [#266](https://github.com/opensearch-project/query-insights/pull/266) | Add strict hash check on top queries indices |

### Issues (Design / RFC)
- [Issue #285](https://github.com/opensearch-project/query-insights/issues/285): Inflight Queries API feature request
- [Issue #248](https://github.com/opensearch-project/query-insights/issues/248): Index template feature request
- [Issue #291](https://github.com/opensearch-project/query-insights/issues/291): Verbose parameter feature request
- [Issue #180](https://github.com/opensearch-project/query-insights/issues/180): Skip profile queries feature request

## Related Feature Report

- [Full feature documentation](../../../features/query-insights/query-insights.md)
