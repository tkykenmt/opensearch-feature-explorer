---
tags:
  - opensearch
---
# Segment Replication

## Summary

OpenSearch 3.6.0 includes two segment replication improvements: adding IndexWarmer support for replica shards to eliminate cold start latency, and fixing an infinite retry loop caused by stale metadata checkpoints after transient failures.

## Details

### What's New in v3.6.0

#### IndexWarmer Support for Replica Shards (Enhancement)

Prior to this change, `NRTReplicationEngine` (used by replica shards with segment replication) did not register an `IndexWarmer` refresh listener. This meant that after each replication checkpoint, global ordinals were not pre-loaded on replica shards, causing a "cold start" penalty on the first search request after each refresh. Primary shards using `InternalEngine` did not have this issue because they already had the warmer wired up.

The fix adds a `WarmerRefreshListener` to `NRTReplicationReaderManager` inside `NRTReplicationEngine`. This listener triggers `Engine.Warmer` (which loads eager global ordinals into the fielddata cache) every time segments are updated on replica shards via segment replication.

Key implementation details:
- New inner class `NRTReplicationEngine.WarmerRefreshListener` implements `ReferenceManager.RefreshListener`
- Acquires an `OpenSearchDirectoryReader` from the reader manager, invokes `warmer.warm(reader)`, then releases the reader
- Warmer exceptions are caught and logged without disrupting segment replication
- Particularly impactful for indices using `eager_global_ordinals: true` on keyword or join fields

#### Fix Infinite Retry Due to Stale Metadata Checkpoint (Bug Fix)

When a segment replication failure occurred (e.g., `CircuitBreakingException` on the primary node), the retry mechanism could enter an infinite loop. The root cause was a race condition:

1. Replica receives checkpoint ckp1 and starts replication
2. Primary publishes ckp2 while ckp1 replication is in progress; replica updates its latest received checkpoint to ckp2
3. Replication for ckp1 fails (e.g., circuit breaker trips on primary)
4. Replica retries, but primary still holds stale replication info for ckp1
5. Primary returns ckp1 metadata, which is behind replica's latest checkpoint ckp2
6. Replica rejects ckp1 as stale → retry → same failure → infinite loop

The fix introduces an `isRetry` flag that propagates through the replication chain:
- `SegmentReplicationTargetService.onNewCheckpoint()` accepts an `isRetry` parameter
- `SegmentReplicationTarget` and `AbstractSegmentReplicationTarget` carry the flag
- During retry, the stale checkpoint validation is skipped (`false == isRetry`), allowing the replication to proceed to `GET_SEGMENT_FILES` phase where the primary clears residual replication state

## Limitations

- The IndexWarmer enhancement applies only to local segment replication; remote-backed segment replication has a different code path
- The stale checkpoint fix addresses the specific race condition between `CircuitBreakingException` and checkpoint advancement; other failure modes may have different retry behaviors

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| `https://github.com/opensearch-project/OpenSearch/pull/20650` | Add IndexWarmer support for replica shards with segment replication | `https://github.com/opensearch-project/OpenSearch/issues/20642` |
| `https://github.com/opensearch-project/OpenSearch/pull/20551` | Fix segment replication infinite retry due to stale metadata checkpoint | `https://github.com/opensearch-project/OpenSearch/issues/20550` |

### Documentation
- https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/segment-replication/index/
