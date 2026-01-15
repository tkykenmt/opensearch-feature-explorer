---
tags:
  - opensearch
---
# FS Info Reporting Fix

## Summary

Fixed an issue where filesystem info could report negative available size values on nodes with both `data` and `search` roles when file cache space was occupied by other files (primarily local index files).

## Details

### What's New in v2.16.0

This release fixes a bug in the `FsProbe` class that caused `IllegalArgumentException` when calculating available disk space on nodes using file cache.

### Problem

On nodes with both `data` and `search` roles, the available disk space calculation could produce negative values when:

1. Space is reserved for file cache (`node.search.cache.size`)
2. The reserved file cache space is being used by other files (e.g., local index files)
3. The calculation `available -= (fileCacheReserved - fileCacheUtilized)` results in a negative value

This caused exceptions like:
```
java.lang.IllegalArgumentException: Values less than -1 bytes are not supported: -1781760b
    at org.opensearch.core.common.unit.ByteSizeValue.<init>(ByteSizeValue.java:78)
    at org.opensearch.monitor.fs.FsInfo$Path.getAvailable(FsInfo.java:141)
    at org.opensearch.cluster.InternalClusterInfoService.fillDiskUsagePerNode(...)
```

### Solution

The fix adds a bounds check in `FsProbe.stats()` to ensure available space is never reported as negative:

```java
paths[i].available -= (paths[i].fileCacheReserved - paths[i].fileCacheUtilized);
// occurs if reserved file cache space is occupied by other files, like local indices
if (paths[i].available < 0) {
    paths[i].available = 0;
}
```

### Technical Changes

| File | Change |
|------|--------|
| `FsProbe.java` | Added bounds check to prevent negative available size |
| `FsProbeTests.java` | Added test case `testFsInfoWhenFileCacheOccupied` |

## Limitations

- When file cache space is fully occupied by other files, available space will be reported as 0 rather than the actual negative value
- This may affect disk allocation decisions in edge cases where the reserved space is heavily contested

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#11573](https://github.com/opensearch-project/OpenSearch/pull/11573) | Fix fs info reporting negative available size | - |
