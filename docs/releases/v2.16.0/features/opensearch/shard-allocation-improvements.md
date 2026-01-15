---
tags:
  - opensearch
---
# Shard Allocation Improvements

## Summary

OpenSearch v2.16.0 introduces time-bound reroute iterations for large shard allocations and fixes a NullPointerException in the ReplicaShardAllocator. These improvements enhance cluster stability during large-scale shard allocation operations by preventing cluster manager task queue buildup and API timeouts.

## Details

### What's New in v2.16.0

#### Time-Bound Reroute Iterations

The reroute operation now supports configurable timeouts for primary and replica shard batch allocation. This prevents long-running reroute iterations from blocking other cluster manager tasks.

**Problem Solved:**
- Single reroute iterations could take over 11 minutes for large clusters
- Pending tasks would queue up, causing cluster management API timeouts
- Index creation and cluster settings updates would fail with `ProcessClusterEventTimeoutException`

**Solution:**
- New `BatchRunnableExecutor` executes shard allocation batches with timeout awareness
- `TimeoutAwareRunnable` interface allows graceful handling when allocation exceeds timeout
- Shards that timeout are throttled and retried in subsequent reroute cycles

#### New Configuration Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `cluster.routing.allocation.shards_batch_gateway_allocator.primary_allocator_timeout` | Timeout for primary shard batch allocation | `-1` (disabled) |
| `cluster.routing.allocation.shards_batch_gateway_allocator.replica_allocator_timeout` | Timeout for replica shard batch allocation | `-1` (disabled) |

**Usage Example:**

```json
PUT /_cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.shards_batch_gateway_allocator.primary_allocator_timeout": "20s",
    "cluster.routing.allocation.shards_batch_gateway_allocator.replica_allocator_timeout": "20s"
  }
}
```

#### ReplicaShardAllocator NPE Fix

Fixed a NullPointerException that occurred in `ReplicaShardAllocator.cancelExistingRecoveryForBetterMatch()` when the primary shard was not yet active during node-left events.

**Root Cause:**
- During node drops, the replica shard allocator attempted to access the primary shard's node ID
- If the primary shard was not active (e.g., still initializing), this caused an NPE
- The assertion `primaryShard != null` was incorrect for edge cases

**Fix:**
- Added null check for primary shard before accessing its properties
- Returns early with trace logging when primary shard is not available
- Allows actual allocation logic to handle the situation appropriately

### Technical Changes

#### New Classes

| Class | Description |
|-------|-------------|
| `BatchRunnableExecutor` | Executes a batch of `TimeoutAwareRunnable` tasks with timeout support |
| `TimeoutAwareRunnable` | Interface for runnables that can handle timeout gracefully via `onTimeout()` |

#### Modified Classes

| Class | Change |
|-------|--------|
| `ShardsBatchGatewayAllocator` | Added timeout settings and `BatchRunnableExecutor` integration |
| `ExistingShardsAllocator` | Changed `allocateAllUnassignedShards()` to return `Runnable` |
| `AllocationService` | Updated to execute returned runnables from allocator |
| `BaseGatewayShardAllocator` | Added `allocateUnassignedBatchOnTimeout()` method |
| `ReplicaShardAllocator` | Added null check for primary shard |

## Limitations

- Timeout settings are disabled by default (`-1`); must be explicitly configured
- Very short timeouts may cause excessive throttling and slow overall allocation
- Timeout behavior shuffles batch order randomly, which may affect allocation predictability

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14848](https://github.com/opensearch-project/OpenSearch/pull/14848) | Make reroute iteration time-bound for large shard allocations | - |
| [#14385](https://github.com/opensearch-project/OpenSearch/pull/14385) | Fix NPE in ReplicaShardAllocator | [#13993](https://github.com/opensearch-project/OpenSearch/issues/13993) |

### Issues
| Issue | Description |
|-------|-------------|
| [#13993](https://github.com/opensearch-project/OpenSearch/issues/13993) | NPE in ReplicaShardBatchAllocator during node drops |
