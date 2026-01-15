---
tags:
  - opensearch
---
# File Cache Initialization Fix

## Summary

Fixed file cache initialization to use total disk space instead of available space when calculating cache size. This prevents the cache from being incorrectly reduced after node restarts when existing cached data occupies disk space.

## Details

### What's New in v2.16.0

This release fixes a critical issue with file cache initialization on search nodes. Previously, the file cache size was calculated using `Math.min(capacity, availableCapacity)`, which could cause problems when a node restarts with existing cached data on disk.

### Problem

When a search node starts, the file cache is initialized based on available disk space. Consider this scenario:

1. A search node has 100GB local storage with file cache configured to 80GB
2. After running, 90% of the file cache (72GB) is used
3. On node restart, available space is only ~28GB (100GB - 72GB cached data)
4. The file cache would be incorrectly reduced to 28GB instead of 80GB
5. This caused filesystem stats to report incorrect values, including negative available space

### Solution

The fix changes the cache size calculation to use total disk space instead of available space:

- **Before**: `capacity = Math.min(configuredSize, availableSpace)`
- **After**: `capacity = calculateFromTotalSpace(configuredSize, totalSpace)`

### Technical Changes

| Component | Change |
|-----------|--------|
| `Node.java` | Changed `NODE_SEARCH_CACHE_SIZE_SETTING` from `ByteSizeValue` to `String` to support percentage values |
| `Node.java` | Added `calculateFileCacheSize()` method to compute cache size from total space |
| `Node.java` | Added `isDedicatedSearchNode()` check for default cache size |
| `FsProbe.java` | Added `getTotalSize()` and `getAvailableSize()` helper methods |
| `FsProbe.java` | Fixed negative available space calculation when cache is over-subscribed |
| `SegmentedCache.java` | Fixed capacity calculation to account for segment rounding |
| `DiscoveryNode.java` | Added `isDedicatedSearchNode()` method |

### Configuration Changes

The `node.search.cache.size` setting now supports both absolute values and percentages:

```yaml
# Absolute size
node.search.cache.size: 50gb

# Percentage of total disk space
node.search.cache.size: 80%
```

**Default behavior:**
- Dedicated search nodes: defaults to `80%` of total disk space
- Non-dedicated search nodes with `TIERED_REMOTE_INDEX` feature enabled: defaults to `80%`
- Non-dedicated search nodes without the feature: requires explicit configuration

### Validation

The fix adds validation to ensure:
- Cache size must be greater than zero
- Cache size must be less than total disk capacity

## Limitations

- The cache size is now based on total space, not available space, so users must ensure sufficient disk space is available for other operations
- Non-dedicated search nodes (nodes with both `search` and `data` roles) require explicit `node.search.cache.size` configuration unless `TIERED_REMOTE_INDEX` feature is enabled

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14004](https://github.com/opensearch-project/OpenSearch/pull/14004) | Fix file cache initialization | - |
