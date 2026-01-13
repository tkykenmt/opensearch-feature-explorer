---
tags:
  - opensearch
---
# Cluster State

## Summary

Fixed a bug where stale cluster state custom files were not being deleted from remote storage when remote cluster state publication is enabled. The cleanup logic was incorrectly iterating over custom metadata map instead of cluster state custom map.

## Details

### What's New in v2.19.0

This release fixes a bug in the `RemoteClusterStateCleanupManager` that prevented proper cleanup of stale cluster state custom files (such as snapshots and restore metadata) from remote storage.

### Technical Changes

The bug was in the `deleteClusterMetadata` method of `RemoteClusterStateCleanupManager`. When iterating over cluster state custom objects to identify stale files for deletion, the code was incorrectly calling `getCustomMetadataMap()` instead of `getClusterStateCustomMap()`:

```java
// Before (incorrect)
clusterMetadataManifest.getCustomMetadataMap()
    .values()
    .stream()
    .filter(u -> !filesToKeep.contains(u.getUploadedFilename()))
    .forEach(u -> staleEphemeralAttributePaths.add(u.getUploadedFilename()));

// After (correct)
clusterMetadataManifest.getClusterStateCustomMap()
    .values()
    .stream()
    .filter(u -> !filesToKeep.contains(u.getUploadedFilename()))
    .forEach(u -> staleEphemeralAttributePaths.add(u.getUploadedFilename()));
```

This fix ensures that cluster state custom files (e.g., `snapshots`, `restore`) are properly identified and deleted during stale file cleanup.

## Limitations

- Only affects clusters with remote cluster state publication enabled (`cluster.remote_store.state.enabled: true`)

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16670](https://github.com/opensearch-project/OpenSearch/pull/16670) | Fix stale cluster state custom file deletion | - |
