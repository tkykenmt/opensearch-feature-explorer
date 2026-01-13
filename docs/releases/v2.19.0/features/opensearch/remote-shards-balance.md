---
tags:
  - opensearch
---
# Remote Shards Balance Fix

## Summary

Fixed a bug in `RemoteShardsBalancer` that caused incorrect shard rebalancing calculations for searchable snapshot indexes in clusters with mixed node types (search nodes and dedicated data nodes).

## Details

### What's New in v2.19.0

The `RemoteShardsBalancer` component, responsible for balancing searchable snapshot index shards across search nodes, had a calculation error that prevented proper shard distribution.

### Technical Changes

The bug was in the `balance()` method of `RemoteShardsBalancer.java`. The original formula for calculating average primary shards per node was:

```
(totalNumberOfRemotePrimaryShards + totalNumberOfUnassignedShards) / totalNumberOfRoutingNodes
```

This formula had two problems:
1. It counted ALL unassigned shards instead of only remote (searchable snapshot) unassigned shards
2. It divided by the total number of routing nodes instead of only remote-capable (search) nodes

The fix corrects the formula to:

```
(totalNumberOfRemotePrimaryShards + totalNumberOfUnassignedRemoteShards) / totalNumberOfRemoteCapableNodes
```

### Code Changes

In `RemoteShardsBalancer.java`:
- Added filtering to count only unassigned primary shards that belong to the `REMOTE_CAPABLE` routing pool
- Changed the divisor from `routingNodes.size()` to `remoteRoutingNodes.size()` to use only remote-capable nodes

```java
int unassignedRemotePrimaryShardCount = 0;
for (ShardRouting shard : routingNodes.unassigned()) {
    if (RoutingPool.REMOTE_CAPABLE.equals(RoutingPool.getShardPool(shard, allocation)) && shard.primary()) {
        unassignedRemotePrimaryShardCount++;
    }
}
totalPrimaryShardCount += unassignedRemotePrimaryShardCount;
final int avgPrimaryPerNode = (totalPrimaryShardCount + remoteRoutingNodes.size() - 1) / remoteRoutingNodes.size();
```

## Limitations

- This fix only affects clusters using searchable snapshots with dedicated search nodes
- Clusters without mixed node types (search + data nodes) were not affected by the original bug

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#15335](https://github.com/opensearch-project/OpenSearch/pull/15335) | Fix remote shards balance | [#15302](https://github.com/opensearch-project/OpenSearch/issues/15302) |

### Documentation

- [Searchable Snapshots](https://docs.opensearch.org/2.19/tuning-your-cluster/availability-and-recovery/snapshots/searchable_snapshot/)
