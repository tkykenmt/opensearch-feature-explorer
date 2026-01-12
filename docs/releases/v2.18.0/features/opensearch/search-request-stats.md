---
tags:
  - observability
  - search
---

# Search Request Stats

## Summary

In v2.18.0, the `search.request_stats_enabled` setting is now enabled by default. This change allows coordinator-level search request statistics to be collected automatically without requiring manual configuration, providing better out-of-the-box observability for search operations.

## Details

### What's New in v2.18.0

The default value for `search.request_stats_enabled` has been changed from `false` to `true`. This means search request statistics are now collected by default on coordinator nodes.

### Technical Changes

#### Configuration Change

| Setting | Previous Default | New Default |
|---------|------------------|-------------|
| `search.request_stats_enabled` | `false` | `true` |

#### Code Change

The change was made in `SearchRequestStats.java`:

```java
public static final Setting<Boolean> SEARCH_REQUEST_STATS_ENABLED = Setting.boolSetting(
    SEARCH_REQUEST_STATS_ENABLED_KEY,
    true,  // Changed from false
    Setting.Property.Dynamic,
    Setting.Property.NodeScope
);
```

### Statistics Collected

When enabled, the following coordinator-level statistics are collected and available via the Nodes Stats API:

| Metric | Description |
|--------|-------------|
| `search.request.took` | Total search request time, count, and current |
| `search.request.dfs_pre_query` | DFS prequery phase statistics |
| `search.request.query` | Query phase statistics |
| `search.request.fetch` | Fetch phase statistics |
| `search.request.dfs_query` | DFS query phase statistics |
| `search.request.expand` | Expand phase statistics |
| `search.request.can_match` | Can match phase statistics |

### Usage Example

Statistics are available via the Nodes Stats API:

```bash
GET _nodes/stats/indices/search
```

Response includes:

```json
{
  "indices": {
    "search": {
      "request": {
        "took": {
          "time_in_millis": 129,
          "current": 0,
          "total": 1
        },
        "query": {
          "time_in_millis": 98,
          "current": 0,
          "total": 1
        },
        "fetch": {
          "time_in_millis": 6,
          "current": 0,
          "total": 1
        }
      }
    }
  }
}
```

### Migration Notes

- No action required for new clusters - statistics are collected automatically
- Existing clusters upgrading to v2.18.0 will have statistics enabled by default
- To disable (if needed for performance reasons), set:
  ```bash
  PUT _cluster/settings
  {
    "persistent": {
      "search.request_stats_enabled": false
    }
  }
  ```

## Limitations

- Statistics collection adds minimal overhead to search operations
- Statistics are per-node and not aggregated across the cluster

## References

### Documentation
- [Nodes Stats API Documentation](https://docs.opensearch.org/2.18/api-reference/nodes-apis/nodes-stats/): Official documentation
- [PR #15054](https://github.com/opensearch-project/OpenSearch/pull/15054): Original implementation adding took time to request nodes stats

### Pull Requests
| PR | Description |
|----|-------------|
| [#16290](https://github.com/opensearch-project/OpenSearch/pull/16290) | Enable coordinator search.request_stats_enabled by default |
| [#16320](https://github.com/opensearch-project/OpenSearch/pull/16320) | Backport to 2.x branch |

### Issues (Design / RFC)
- [Issue #10768](https://github.com/opensearch-project/OpenSearch/issues/10768): Feature request for total search request time on coordinator node

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/search-request-stats.md)
