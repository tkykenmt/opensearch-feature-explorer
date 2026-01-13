---
tags:
  - domain/data
  - component/server
  - indexing
---
# Cross-Cluster Replication Build Fix

## Summary

This release fixes a build failure in the Cross-Cluster Replication plugin caused by a missing method implementation in the `RemoteClusterRepository` class. The fix adds the required `getLowPriorityRemoteDownloadThrottleTimeInNanos()` method to maintain compatibility with the OpenSearch core `Repository` interface.

## Details

### What's New in v3.2.0

A build-breaking issue was identified where the `RemoteClusterRepository` class failed to compile because it did not implement the abstract method `getLowPriorityRemoteDownloadThrottleTimeInNanos()` from the `Repository` interface. This method was added to the core OpenSearch `Repository` interface, requiring all implementing classes to provide an implementation.

### Technical Changes

#### Code Changes

The fix adds a new method to `RemoteClusterRepository.kt`:

```kotlin
override fun getLowPriorityRemoteDownloadThrottleTimeInNanos(): Long {
    throw UnsupportedOperationException("Operation not permitted")
}
```

This follows the same pattern as other unsupported repository operations in the class, such as:
- `getRemoteUploadThrottleTimeInNanos()`
- `getRemoteDownloadThrottleTimeInNanos()`
- `getSnapshotThrottleTimeInNanos()`

#### Changed Files

| File | Change |
|------|--------|
| `src/main/kotlin/org/opensearch/replication/repository/RemoteClusterRepository.kt` | Added `getLowPriorityRemoteDownloadThrottleTimeInNanos()` method |

### Migration Notes

No migration required. This is a build fix that does not change any user-facing behavior.

## Limitations

- The `getLowPriorityRemoteDownloadThrottleTimeInNanos()` method throws `UnsupportedOperationException` as this operation is not applicable to cross-cluster replication's remote repository implementation

## References

### Documentation
- [Cross-cluster replication documentation](https://docs.opensearch.org/3.0/tuning-your-cluster/replication-plugin/index/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#1564](https://github.com/opensearch-project/cross-cluster-replication/pull/1564) | Add missing method for RemoteClusterRepository class |

### Issues (Design / RFC)
- [Issue #1557](https://github.com/opensearch-project/cross-cluster-replication/issues/1557): Distribution Build Failed for cross-cluster-replication-3.2.0

## Related Feature Report

- [Full feature documentation](../../../../features/cross-cluster-replication/cross-cluster-opensearch-replication.md)
