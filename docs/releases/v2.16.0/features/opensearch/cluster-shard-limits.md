---
tags:
  - opensearch
---
# Cluster Shard Limits

## Summary

Fixed an integer overflow bug in the cluster shard limit calculation that could cause shard allocation failures when `cluster.max_shards_per_node` was set to a high value and the cluster was scaled up.

## Details

### What's New in v2.16.0

The `ShardLimitValidator` class was updated to prevent integer overflow when computing the maximum number of shards allowed in a cluster.

### Technical Changes

The bug occurred when calculating `maxShardsInCluster` by multiplying `maxShardsPerNodeSetting * nodeCount`. With high values of `cluster.max_shards_per_node` (e.g., 500,000,000) and multiple nodes, this multiplication could overflow the 32-bit integer limit, resulting in negative values.

**Before (buggy):**
```java
maxShardsInCluster = maxShardsPerNodeSetting * nodeCount;
```

**After (fixed):**
```java
int computedMaxShards = (int) Math.min(Integer.MAX_VALUE, (long) maxShardsPerNodeSetting * nodeCount);
```

The fix:
1. Casts `maxShardsPerNodeSetting` to `long` before multiplication to prevent overflow
2. Uses `Math.min()` to cap the result at `Integer.MAX_VALUE`
3. Changed `currentOpenShards` from `int` to `long` for consistency

### Error Message Before Fix

When the overflow occurred, users would see confusing error messages like:
```
Validation Failed: 1: this action would add [2] total shards, but this cluster currently has [30101]/[-1089934592] maximum shards open
```

The negative number (`-1089934592`) was the result of integer overflow.

## Limitations

- The `cluster.max_shards_per_node` setting still accepts very high values, but the computed cluster maximum is now capped at `Integer.MAX_VALUE` (2,147,483,647)
- This is a breaking change for clusters that relied on the previous (buggy) behavior

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14155](https://github.com/opensearch-project/OpenSearch/pull/14155) | Fix the computed max shards of cluster to avoid int overflow | [#13907](https://github.com/opensearch-project/OpenSearch/issues/13907) |

### Documentation
- [Cluster Settings](https://docs.opensearch.org/2.16/install-and-configure/configuring-opensearch/cluster-settings/)
