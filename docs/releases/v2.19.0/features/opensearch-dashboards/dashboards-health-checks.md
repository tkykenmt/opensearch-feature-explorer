---
tags:
  - opensearch-dashboards
---
# Dashboards Health Checks

## Summary

OpenSearch Dashboards v2.19.0 optimizes health check operations by using local cluster state calls instead of querying the cluster manager node. This reduces load on the cluster manager, improving cluster stability for large deployments with many indices and shards.

## Details

### What's New in v2.19.0

The health check mechanism in OpenSearch Dashboards has been updated to use local cluster state when retrieving node attributes for optimized health checks.

**Before v2.19.0**: The `_cluster/state/nodes` API call was served by the cluster manager node, which could stress the cluster manager in large clusters.

**After v2.19.0**: The same API call now uses `local=true` parameter, serving the request from the local node's cluster state instead.

### Technical Changes

The change modifies `src/core/server/opensearch/version_check/ensure_opensearch_version.ts`:

```typescript
const state = (await internalClient.cluster.state({
  metric: 'nodes',
  local: true,  // New parameter added
  filter_path: [path],
})) as ApiResponse;
```

### How It Works

1. During health checks, Dashboards retrieves node attributes to determine if optimized health checks can be used
2. The `_cluster/state/nodes` call now reads from the local node's cluster state
3. Since cluster state is eventually consistent across nodes (with a 90-second timeout before lagging nodes are removed), this approach maintains correctness while reducing cluster manager load

### Impact

- **Reduced cluster manager load**: Health check requests no longer route to the cluster manager
- **Better scalability**: Large clusters with many Dashboards instances benefit from distributed request handling
- **Minimal latency impact**: Local cluster state may lag slightly but remains accurate for health check purposes

## Limitations

- Local cluster state may be slightly behind the cluster manager's state (typically milliseconds)
- Nodes with significantly lagging cluster state are automatically removed from the cluster after 90 seconds

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#8187](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8187) | Use local clusterState call during healthchecks | - |

### Documentation
- [Cluster Health API](https://docs.opensearch.org/2.19/api-reference/cluster-api/cluster-health/) - `local` parameter documentation
