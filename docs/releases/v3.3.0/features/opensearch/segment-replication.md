---
tags:
  - indexing
---

# Segment Replication

## Summary

This release fixes a NullPointerException (NPE) in the `SegmentReplicator` class that occurred during concurrent indexing and stats requests. The bug caused intermittent test failures in `IndexStatsIT.testConcurrentIndexingAndStatsRequests` when using segment replication strategy.

## Details

### What's New in v3.3.0

Fixed a race condition in `SegmentReplicator.getSegmentReplicationStats()` that could throw a NullPointerException when retrieving replication checkpoint statistics.

### Technical Changes

#### Bug Fix

The issue occurred in the `getSegmentReplicationStats()` method of `SegmentReplicator.java`. The original code checked if the concurrent map was empty using `isEmpty()`, but entries could be removed between the check and subsequent `firstEntry()`/`lastEntry()` calls, resulting in null values.

**Before (vulnerable to race condition):**
```java
if (existingCheckpointStats == null || existingCheckpointStats.isEmpty()) {
    return ReplicationStats.empty();
}
Map.Entry<Long, ReplicationCheckpointStats> lowestEntry = existingCheckpointStats.firstEntry();
Map.Entry<Long, ReplicationCheckpointStats> highestEntry = existingCheckpointStats.lastEntry();
// NPE if entries removed between isEmpty() check and here
```

**After (thread-safe):**
```java
if (existingCheckpointStats == null) {
    return ReplicationStats.empty();
}
Map.Entry<Long, ReplicationCheckpointStats> lowestEntry = existingCheckpointStats.firstEntry();
Map.Entry<Long, ReplicationCheckpointStats> highestEntry = existingCheckpointStats.lastEntry();
if (lowestEntry == null || highestEntry == null) {
    return ReplicationStats.empty();
}
```

#### Root Cause

The `ConcurrentNavigableMap` used for storing checkpoint stats is modified concurrently:
- Entries are added when new checkpoints arrive
- Entries are pruned when old checkpoints are cleaned up

The `isEmpty()` check was not atomic with the subsequent `firstEntry()`/`lastEntry()` calls, creating a time-of-check to time-of-use (TOCTOU) race condition.

### Migration Notes

No migration required. This is a bug fix that improves stability when using segment replication with concurrent stats requests.

## Limitations

None specific to this fix.

## References

### Documentation
- [Segment Replication Documentation](https://docs.opensearch.org/3.0/tuning-your-cluster/availability-and-recovery/segment-replication/index/): Official documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#18997](https://github.com/opensearch-project/OpenSearch/pull/18997) | Fix NPE in segment replicator |

### Issues (Design / RFC)
- [Issue #15836](https://github.com/opensearch-project/OpenSearch/issues/15836): Flaky test report for IndexStatsIT

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/segment-replication.md)
