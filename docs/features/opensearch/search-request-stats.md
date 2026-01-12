# Search Request Stats

## Summary

Search Request Stats provides coordinator-level search latency metrics for OpenSearch clusters. This feature tracks the total time spent on search requests at the coordinator node, including detailed phase breakdowns (query, fetch, DFS, expand, can_match). It enables better observability and performance monitoring of search operations.

## Details

### Architecture

```mermaid
graph TB
    subgraph "Coordinator Node"
        SR[Search Request] --> SRS[SearchRequestStats]
        SRS --> |onRequestStart| TookStats[Took Stats]
        SRS --> |onPhaseStart/End| PhaseStats[Phase Stats]
    end
    
    subgraph "Statistics Collection"
        TookStats --> |time_in_millis| TotalTime[Total Time]
        TookStats --> |current| CurrentRequests[Current Requests]
        TookStats --> |total| TotalCount[Total Count]
        PhaseStats --> QueryPhase[Query Phase]
        PhaseStats --> FetchPhase[Fetch Phase]
        PhaseStats --> DFSPhase[DFS Phases]
        PhaseStats --> OtherPhases[Other Phases]
    end
    
    subgraph "Nodes Stats API"
        TotalTime --> API[/_nodes/stats/indices/search]
        CurrentRequests --> API
        TotalCount --> API
        QueryPhase --> API
        FetchPhase --> API
    end
```

### Components

| Component | Description |
|-----------|-------------|
| `SearchRequestStats` | Main class that extends `SearchRequestOperationsListener` to collect statistics |
| `StatsHolder` | Inner class holding `current`, `total`, and `timing` metrics |
| `SearchRequestOperationsListener` | Base listener interface for search request lifecycle events |

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `search.request_stats_enabled` | Enable/disable coordinator search request statistics collection | `true` (since v2.18.0) |

The setting is:
- **Dynamic**: Can be changed at runtime via cluster settings API
- **Node-scoped**: Applies to individual nodes

### Statistics Breakdown

The feature collects the following metrics:

| Metric Category | Metrics | Description |
|-----------------|---------|-------------|
| `took` | `time_in_millis`, `current`, `total` | Overall search request statistics |
| `dfs_pre_query` | `time_in_millis`, `current`, `total` | Distributed frequency search prequery phase |
| `query` | `time_in_millis`, `current`, `total` | Query execution phase |
| `fetch` | `time_in_millis`, `current`, `total` | Document fetch phase |
| `dfs_query` | `time_in_millis`, `current`, `total` | DFS query phase |
| `expand` | `time_in_millis`, `current`, `total` | Search expansion phase |
| `can_match` | `time_in_millis`, `current`, `total` | Can match optimization phase |

### Usage Example

#### Enable/Disable Statistics

```bash
# Enable (default in v2.18.0+)
PUT _cluster/settings
{
  "persistent": {
    "search.request_stats_enabled": true
  }
}

# Disable
PUT _cluster/settings
{
  "persistent": {
    "search.request_stats_enabled": false
  }
}
```

#### Retrieve Statistics

```bash
# Get search stats for all nodes
GET _nodes/stats/indices/search

# Get search stats for specific node
GET _nodes/<node_id>/stats/indices/search
```

#### Example Response

```json
{
  "nodes": {
    "node_id": {
      "indices": {
        "search": {
          "request": {
            "took": {
              "time_in_millis": 129,
              "current": 0,
              "total": 10
            },
            "dfs_pre_query": {
              "time_in_millis": 0,
              "current": 0,
              "total": 0
            },
            "query": {
              "time_in_millis": 98,
              "current": 0,
              "total": 10
            },
            "fetch": {
              "time_in_millis": 6,
              "current": 0,
              "total": 10
            },
            "dfs_query": {
              "time_in_millis": 0,
              "current": 0,
              "total": 0
            },
            "expand": {
              "time_in_millis": 9,
              "current": 0,
              "total": 10
            },
            "can_match": {
              "time_in_millis": 0,
              "current": 0,
              "total": 0
            }
          }
        }
      }
    }
  }
}
```

## Limitations

- Statistics are collected per-node and not aggregated across the cluster
- Minimal performance overhead when enabled
- Only tracks coordinator-level statistics (not shard-level)

## Change History

- **v3.3.0** (2025-09-30): Fixed negative search stats handling - writes 0 instead of negative values to prevent serialization errors
- **v2.18.0** (2024-11-05): Enabled `search.request_stats_enabled` by default
- **v2.17.0** (2024-09-17): Initial implementation with `took` statistics and phase breakdowns

## References

### Documentation
- [Nodes Stats API Documentation](https://docs.opensearch.org/latest/api-reference/nodes-apis/nodes-stats/): Official API documentation

### Pull Requests
| Version | PR | Description |
|---------|-----|-------------|
| v3.3.0 | [#19340](https://github.com/opensearch-project/OpenSearch/pull/19340) | Handle negative search request nodes stats |
| v2.17.0 | [#15054](https://github.com/opensearch-project/OpenSearch/pull/15054) | Initial implementation - Add took time to request nodes stats |
| v2.18.0 | [#16290](https://github.com/opensearch-project/OpenSearch/pull/16290) | Enable search.request_stats_enabled by default |
| v2.18.0 | [#16320](https://github.com/opensearch-project/OpenSearch/pull/16320) | Backport to 2.x branch |

### Issues (Design / RFC)
- [Issue #16598](https://github.com/opensearch-project/OpenSearch/issues/16598): Bug report - Negative Search Stats causing nodes/stats API failures
- [Issue #10768](https://github.com/opensearch-project/OpenSearch/issues/10768): Original feature request - Search stats for coordinator node misses total search request time
