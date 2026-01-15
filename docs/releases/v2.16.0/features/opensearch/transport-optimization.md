---
tags:
  - opensearch
---
# Transport Optimization

## Summary

OpenSearch v2.16.0 introduces a significant performance optimization for `TransportNodesAction` that eliminates redundant discovery node information from inter-node transport requests. This optimization dramatically reduces network traffic and improves response times for node-level APIs, especially in large clusters.

## Details

### What's New in v2.16.0

The optimization addresses a performance bottleneck where every transport action extending `TransportNodesAction` included all discovery nodes in requests sent to each node. In a cluster with N nodes, this resulted in N² serialization of discovery node data, causing:

- Excessive network traffic
- Increased write/read latency
- Netty buffer overload

### Technical Changes

A new `includeDiscoveryNodes` flag was added to `BaseNodesRequest` that controls whether discovery nodes are included in transport requests:

```java
// BaseNodesRequest.java
private boolean includeDiscoveryNodes = true;

public void setIncludeDiscoveryNodes(boolean value) {
    includeDiscoveryNodes = value;
}

public boolean getIncludeDiscoveryNodes() {
    return includeDiscoveryNodes;
}
```

The `AsyncAction` class in `TransportNodesAction` now transfers ownership of concrete nodes and clears them from the request when the flag is false:

```java
// TransportNodesAction.java - AsyncAction constructor
this.concreteNodes = request.concreteNodes();

if (request.getIncludeDiscoveryNodes() == false) {
    request.setConcreteNodes(null);
}
```

### Affected APIs

The optimization is applied to REST layer requests for:

| API | Handler Class |
|-----|---------------|
| `GET /_nodes/stats` | `RestNodesStatsAction` |
| `GET /_nodes` | `RestNodesInfoAction` |
| `GET /_cat/nodes` | `RestNodesAction` |
| `GET /_cluster/stats` | `RestClusterStatsAction` |

### Performance Improvements

Benchmarks on a 1,000-node cluster showed significant improvements:

| API | Metric | Before | After | Improvement |
|-----|--------|--------|-------|-------------|
| `_nodes/stats` | Average | 10.03s | 1.42s | 86% |
| `_nodes/stats` | P90 | 12.55s | 5.81s | 54% |
| `_nodes` | Average | 8.62s | 3.67s | 58% |
| `_cat/nodes` | Average | 21.45s | 1.07s | 96% |
| `_cluster/stats` | Average | 9.83s | 2.02s | 80% |

## Limitations

- The optimization is opt-in via the `setIncludeDiscoveryNodes(false)` method
- Only REST layer requests are optimized by default; programmatic API calls retain the original behavior
- Custom plugins extending `TransportNodesAction` must explicitly opt-in to benefit

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14749](https://github.com/opensearch-project/OpenSearch/pull/14749) | Optimize TransportNodesAction to not send DiscoveryNodes for NodeStats, NodesInfo and ClusterStats | [#14713](https://github.com/opensearch-project/OpenSearch/issues/14713) |

### Issues
| Issue | Description |
|-------|-------------|
| [#14713](https://github.com/opensearch-project/OpenSearch/issues/14713) | Stats transport actions based on TransportNodeActions sends large payload of Discovery Nodes to all nodes |
