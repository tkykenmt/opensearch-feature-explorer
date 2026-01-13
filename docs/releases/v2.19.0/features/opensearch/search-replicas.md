---
tags:
  - opensearch
---
# Search Replicas

## Summary

OpenSearch v2.19.0 enhances the Search Replicas feature with two key improvements: support for restoring indexes with search replicas from snapshots, and the addition of search replica statistics to the segment replication stats API. These changes improve operational capabilities for clusters using reader-writer separation.

## Details

### What's New in v2.19.0

#### Snapshot Restore Support for Search Replicas

Indexes with search replicas can now be restored from snapshots with proper validation rules:

| Snapshot Replication Type | Restore Replication Type | Search Replicas Allowed |
|---------------------------|--------------------------|-------------------------|
| DOCUMENT | DOCUMENT | No |
| DOCUMENT | SEGMENT | Yes |
| SEGMENT (no search replicas) | DOCUMENT | Yes (must set to 0) |
| SEGMENT (no search replicas) | SEGMENT | Yes |
| SEGMENT (with search replicas) | DOCUMENT | Only if set to 0 |
| SEGMENT (with search replicas) | SEGMENT | Yes |

The restore operation validates compatibility between the snapshot's replication type and the target configuration. If restoring to document replication with search replicas > 0, the operation fails with a descriptive error.

#### Search Replica Stats in Segment Replication API

The segment replication stats API (`GET /_cat/segment_replication`) now includes statistics for search replicas:

- `bytes_behind`: Bytes remaining to replicate from remote store
- `current_replication_lag`: Current replication lag in milliseconds
- `last_completed_replication_time`: Time of last completed replication

Stats are computed by comparing the search replica's checkpoint with the latest checkpoint from the remote store, enabling monitoring of replication health for search replicas.

### Technical Changes

#### Snapshot Restore Validation

The `RestoreService` class now includes validation logic in `validateReplicationTypeRestoreSettings()`:

```java
// Validation prevents restoring with search replicas when target is DOCUMENT replication
if (restoreNumberOfSearchReplicas > 0 
    && ReplicationType.DOCUMENT.equals(restoreReplicationType)) {
    throw new SnapshotRestoreException(...);
}
```

#### Search Replica Stats Computation

The `TransportSegmentReplicationStatsAction` computes stats for search replicas by:

1. Fetching the latest completed and ongoing replication states from `SegmentReplicationTargetService`
2. Calculating bytes remaining from file details in the replication index
3. Computing lag times from replication timers

## Limitations

- Snapshot restore with search replicas requires segment replication to be enabled
- Search replica stats are only available when segment replication is active
- Stats computation relies on remote store checkpoint information

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16111](https://github.com/opensearch-project/OpenSearch/pull/16111) | Add support for restoring from snapshot with search replicas | [#15532](https://github.com/opensearch-project/OpenSearch/issues/15532) |
| [#16678](https://github.com/opensearch-project/OpenSearch/pull/16678) | Add search replica stats to segment replication stats API | [#15534](https://github.com/opensearch-project/OpenSearch/issues/15534) |

### Related Issues
- [#15306](https://github.com/opensearch-project/OpenSearch/issues/15306): META - Reader/Writer Separation
- [#15532](https://github.com/opensearch-project/OpenSearch/issues/15532): Updates to restore from snapshot with added search replicas
- [#15534](https://github.com/opensearch-project/OpenSearch/issues/15534): Update Segment replication stats APIs to support pull based architecture
