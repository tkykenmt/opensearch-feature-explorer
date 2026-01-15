---
tags:
  - opensearch
---
# Searchable Snapshots

## Summary

OpenSearch 2.16.0 includes two bug fixes for searchable snapshots: proper shard-level metadata blob creation when snapshotting searchable snapshot indexes, and a fix for scripted field queries on remote snapshot indexes.

## Details

### What's New in v2.16.0

#### Shard-Level Metadata Blob Fix

Previously, when taking a snapshot of a searchable snapshot index, OpenSearch only captured index metadata without creating shard-level snapshot metadata (`snap-{uuid}.dat` blob). This caused failures when:
- Calling the snapshot status API
- Cloning snapshots containing searchable snapshot indexes

The fix ensures shard-level metadata blobs are written even for searchable snapshot indexes, enabling proper snapshot status reporting and cloning operations.

#### Scripted Field Query Fix

Queries using scripted fields on searchable snapshot indexes failed with `AccessControlException` when the file cache needed to evict entries. The error occurred because:
1. Scripted queries run with restricted permissions
2. Cache eviction requires file deletion permissions
3. The `AccessController.doPrivileged` call was not positioned correctly in the call stack

The fix moves the privileged action wrapper to encompass the entire `fileCache.compute()` operation, ensuring proper permissions for both cache reads and evictions during scripted queries.

### Technical Changes

#### BlobStoreRepository.java
- Added check for `store.indexSettings().isRemoteSnapshot()` before determining files to upload
- Searchable snapshot indexes now create empty `indexCommitPointFiles` list instead of skipping shard snapshot entirely

#### TransferManager.java
- Moved `AccessController.doPrivileged` wrapper from `createIndexInput()` to `fetchBlob()`
- Ensures file cache operations (including evictions) have proper permissions when triggered by plugins

## Limitations

- Searchable snapshot indexes remain read-only
- Snapshot status for searchable snapshot shards shows 0 total file count (expected behavior since no files are uploaded)

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#13190](https://github.com/opensearch-project/OpenSearch/pull/13190) | Write shard level metadata blob when snapshotting searchable snapshot indexes | - |
| [#14411](https://github.com/opensearch-project/OpenSearch/pull/14411) | Add perms for remote snapshot cache eviction on scripted query | [#14268](https://github.com/opensearch-project/OpenSearch/issues/14268) |

### Documentation

- [Searchable Snapshots](https://docs.opensearch.org/2.16/tuning-your-cluster/availability-and-recovery/snapshots/searchable_snapshot/)
