---
tags:
  - domain/core
  - component/server
  - indexing
---
# Snapshot/Repository Fixes

## Summary

OpenSearch v3.1.0 includes two critical bug fixes for snapshot and repository operations. The first fix prevents an infinite loop that could occur when simultaneously creating a snapshot and updating the repository configuration. The second fix addresses a NullPointerException when restoring searchable snapshots created in older OpenSearch versions that lack the `remote_store_index_shallow_copy` field.

## Details

### What's New in v3.1.0

These fixes improve the stability and backward compatibility of snapshot operations:

1. **Infinite Loop Prevention**: Fixed a race condition where updating a repository while a snapshot creation is in progress could cause the snapshot operation to enter an infinite loop.

2. **NPE Fix for Legacy Snapshots**: Fixed a NullPointerException that occurred when restoring searchable snapshots created in OpenSearch versions prior to 2.10 (before the `remote_store_index_shallow_copy` field was introduced).

### Technical Changes

#### Fix 1: Repository Update During Snapshot Creation

When a repository is updated, `RepositoriesService` creates a new repository instance and closes the old one. Previously, an ongoing snapshot creation that depended on the closed repository would enter an infinite loop in `BlobStoreRepository.executeConsistentStateUpdate()` because the condition check would always fail.

**Solution**: Added a `closed` flag to `BlobStoreRepository` that is set when the repository is closed. The `executeConsistentStateUpdate()` method now checks this flag and returns a `RepositoryException` if the repository has been closed, allowing the snapshot operation to fail gracefully with a clear error message.

```java
// BlobStoreRepository.java
private volatile boolean closed;

@Override
protected void doClose() {
    // ...
    closed = true;
    store.close();
    // ...
}

public void executeConsistentStateUpdate(...) {
    if (this.closed) {
        onFailure.accept(new RepositoryException(metadata.name(), 
            "the repository has been changed, try again"));
        return;
    }
    // ... continue with normal operation
}
```

#### Fix 2: NPE on SnapshotInfo Shallow Copy Field

Snapshots created in older OpenSearch versions (before 2.10) do not contain the `remote_store_index_shallow_copy` field in their metadata. When restoring such snapshots as searchable snapshots, the code attempted to call `booleanValue()` on a null `Boolean` object.

**Solution**: Changed the null-unsafe boolean check to use `Boolean.TRUE.equals()` which safely handles null values.

```java
// Before (NPE-prone)
} else if (snapshotInfo.isRemoteStoreIndexShallowCopyEnabled()) {

// After (null-safe)
} else if (Boolean.TRUE.equals(snapshotInfo.isRemoteStoreIndexShallowCopyEnabled())) {
```

### Migration Notes

No migration steps required. These are bug fixes that improve stability without changing any APIs or configurations.

## Limitations

- The infinite loop fix causes the snapshot operation to fail with a `RepositoryException` when the repository is updated during snapshot creation. Users should retry the snapshot operation after the repository update completes.
- Backward compatibility testing for snapshots created in very old OpenSearch versions may still have gaps.

## References

### Documentation
- [Snapshot Repository Documentation](https://docs.opensearch.org/3.0/api-reference/snapshots/create-repository/): Official documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#17532](https://github.com/opensearch-project/OpenSearch/pull/17532) | Fix simultaneously creating a snapshot and updating the repository can potentially trigger an infinite loop |
| [#18218](https://github.com/opensearch-project/OpenSearch/pull/18218) | Avoid NPE if on SnapshotInfo if 'shallow' boolean not present |

### Issues (Design / RFC)
- [Issue #17531](https://github.com/opensearch-project/OpenSearch/issues/17531): Bug report for infinite loop during concurrent snapshot/repository update
- [Issue #18187](https://github.com/opensearch-project/OpenSearch/issues/18187): Bug report for NPE when restoring legacy searchable snapshots

## Related Feature Report

- Full feature documentation
