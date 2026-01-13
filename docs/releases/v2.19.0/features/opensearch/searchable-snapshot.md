---
tags:
  - opensearch
---
# Searchable Snapshot Bug Fixes

## Summary

OpenSearch v2.19.0 includes three bug fixes for the Searchable Snapshot feature, addressing issues with alias rollover operations, scripted query permissions, and shallow copy snapshot failures on closed indexes.

## Details

### What's New in v2.19.0

#### Rollover Alias Support for Restored Searchable Snapshot Indexes

Previously, when using ISM (Index State Management) to rollover aliases that included restored searchable snapshot indexes, the operation would fail with a `FORBIDDEN/13/remote index is read-only` error. This occurred because the rollover operation checked all indexes using the alias and was blocked by the `METADATA_WRITE` block on read-only searchable snapshot indexes.

The fix excludes searchable snapshot indexes from the `checkBlock` validation during `_aliases` and `_rollover` API operations, allowing rollover to proceed correctly.

#### Scripted Query Permissions Fix

Searches on searchable snapshot indexes that included scripted queries (e.g., Painless scripts in aggregations) would fail with `AccessControlException` errors. The issue occurred because:

1. Scripted queries run in a different security context
2. The `TransferManager` needed elevated permissions when calling `getIndexInput()` on cache entries
3. File I/O operations for downloading blobs from remote snapshot stores required additional permissions

The fix wraps the `cacheEntry.getIndexInput()` call in a privileged block, granting the necessary permissions for disk I/O operations when fetching blobs from remote snapshots.

#### Shallow Copy Snapshot Fix for Closed Indexes

Shallow copy snapshots were failing for remote-store backed indexes that had been closed, with the error:
```
java.nio.file.NoSuchFileException: Metadata file is not present for given primary term <X> and generation <Y>
```

Root cause:
- When an index is closed, a new segment file is created during read-only engine recovery
- This new segment file is not uploaded to remote store (no refresh listener available)
- Shallow snapshots try to find the latest segment generation on remote store, which fails

The fix takes snapshots using the last successfully uploaded segment generation by fetching the latest metadata file from the remote directory and acquiring a lock on that commit generation.

### Technical Changes

| Component | Change |
|-----------|--------|
| `MetadataCreateIndexService` | Exclude searchable snapshot indexes from block checks during alias/rollover operations |
| `TransferManager` | Add privileged block for `getIndexInput()` calls during blob fetching |
| `SnapshotShardsService` | Use last uploaded segment generation for shallow copy snapshots on closed indexes |

## Limitations

- Searchable snapshot indexes remain read-only; write operations will still fail
- The shallow copy snapshot fix applies only to remote-store backed indexes

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16483](https://github.com/opensearch-project/OpenSearch/pull/16483) | Rollover alias supports restored searchable snapshot index | [#16419](https://github.com/opensearch-project/OpenSearch/issues/16419) |
| [#16544](https://github.com/opensearch-project/OpenSearch/pull/16544) | Make cacheEntry.getIndexInput() privileged when fetching blobs from remote snapshot | [#16542](https://github.com/opensearch-project/OpenSearch/issues/16542) |
| [#16868](https://github.com/opensearch-project/OpenSearch/pull/16868) | Fix Shallow copy snapshot failures on closed index | [#13805](https://github.com/opensearch-project/OpenSearch/issues/13805) |

### Documentation
- [Searchable Snapshots](https://docs.opensearch.org/2.19/tuning-your-cluster/availability-and-recovery/snapshots/searchable_snapshot/)
- [Shallow Snapshots](https://docs.opensearch.org/2.19/tuning-your-cluster/availability-and-recovery/remote-store/snapshot-interoperability/)
