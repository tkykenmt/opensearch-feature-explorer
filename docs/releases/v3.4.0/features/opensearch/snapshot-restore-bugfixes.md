# Snapshot & Restore Bugfixes

## Summary

This release fixes a NullPointerException that occurred when restoring remote snapshots (searchable snapshots) when shard size information was unavailable in the ClusterInfo cache. The bug manifested during rapid successive restore operations where the cluster hadn't yet collected size information for recently restored shards.

## Details

### What's New in v3.4.0

Fixed a critical bug in the `validateSearchableSnapshotRestorable` method within `RestoreService` that caused restore operations to fail with a NullPointerException when restoring multiple remote snapshots in quick succession.

### Technical Changes

#### Root Cause

The `validateSearchableSnapshotRestorable` method calculates the total size of existing remote snapshot shards to validate against file cache capacity. The original implementation used a Java Stream with `mapToLong(Long::longValue)` which threw NPE when `ClusterInfo.getShardSize()` returned null:

```java
// Before (buggy code)
long totalRestoredRemoteIndexesSize = shardsIterator.getShardRoutings()
    .stream()
    .map(clusterInfo::getShardSize)
    .mapToLong(Long::longValue)  // NPE when getShardSize returns null
    .sum();
```

#### The Fix

The fix replaces the stream-based approach with an explicit loop that handles null values gracefully:

```java
// After (fixed code)
long totalRestoredRemoteIndicesSize = 0;
int missingSizeCount = 0;
List<ShardRouting> routings = shardsIterator.getShardRoutings();

for (ShardRouting shardRouting : routings) {
    Long shardSize = clusterInfo.getShardSize(shardRouting);
    if (shardSize != null) {
        totalRestoredRemoteIndicesSize += shardSize;
    } else {
        missingSizeCount++;
    }
}

if (missingSizeCount > 0) {
    logger.warn(
        "Size information unavailable for {} out of {} remote snapshot shards. "
            + "File cache validation will use available data only.",
        missingSizeCount,
        routings.size()
    );
}
```

#### Behavior Change

| Aspect | Before | After |
|--------|--------|-------|
| Null shard size | Throws NPE | Skips and logs warning |
| File cache validation | Fails on missing data | Uses available data only |
| Logging | None | Warns about missing size info |

### When This Bug Occurs

The bug occurs when:
1. Restoring indexes from snapshots using `storage_type: remote_snapshot` (searchable snapshots)
2. Performing multiple restore operations in rapid succession
3. The `ClusterInfo` cache hasn't been updated with shard size information for recently restored shards
4. The `cluster.info.update.interval` setting delays size information collection

### Usage Example

The following restore operations could trigger the bug before this fix:

```json
// First restore
POST /_snapshot/my-repo/snapshot-1/_restore
{
  "indices": "index-1",
  "storage_type": "remote_snapshot",
  "rename_pattern": "(.+)",
  "rename_replacement": "remote-$1"
}

// Second restore immediately after (could fail with NPE)
POST /_snapshot/my-repo/snapshot-2/_restore
{
  "indices": "index-2",
  "storage_type": "remote_snapshot",
  "rename_pattern": "(.+)",
  "rename_replacement": "remote-$1"
}
```

### Migration Notes

No migration required. This is a bugfix that improves reliability of searchable snapshot restore operations.

## Limitations

- File cache validation may be less accurate when shard size information is unavailable
- The warning log indicates validation is proceeding with incomplete data

## Related PRs

| PR | Description |
|----|-------------|
| [#19684](https://github.com/opensearch-project/OpenSearch/pull/19684) | Fix NPE in validateSearchableSnapshotRestorable when shard size is unavailable |

## References

- [Issue #19349](https://github.com/opensearch-project/OpenSearch/issues/19349): Bug report for NullPointerException when creating remote index from snapshot
- [Searchable Snapshots Documentation](https://docs.opensearch.org/3.0/tuning-your-cluster/availability-and-recovery/snapshots/searchable_snapshot/): Official documentation
- [Restore Snapshot API](https://docs.opensearch.org/3.0/api-reference/snapshots/restore-snapshot/): API reference

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/snapshot-restore-enhancements.md)
