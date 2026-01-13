---
tags:
  - opensearch
---
# Tiered Caching Bug Fixes

## Summary

OpenSearch 2.19.0 includes two bug fixes for the Tiered Spillover Cache feature that address issues with cache statistics accuracy and maximum size settings when pluggable caching is enabled.

## Details

### What's New in v2.19.0

#### Fix 1: Cache Stats API Accuracy (PR #16560)

Fixed a bug where the total stats for TieredSpilloverCache were decremented incorrectly when shards were closed. Previously, misses and evictions from both the heap and disk tier were subtracted from the total, but this was incorrect behavior.

When the disk tier is enabled, only disk-tier misses and evictions should count towards the cache total. The fix ensures that only disk-tier statistics are subtracted when removing dimension statistics, maintaining consistency between tier-level and total statistics.

Key changes:
- Modified `TieredSpilloverCache.invalidate()` to properly handle stats removal
- Updated `TieredSpilloverCacheStatsHolder.removeDimensions()` to correctly aggregate stats across tiers
- Added comprehensive unit tests for `TieredSpilloverCacheStatsHolder`

#### Fix 2: Maximum Size Settings (PR #16636)

Fixed a bug where cache maximum size settings were not working correctly when pluggable caching was enabled. The issue occurred because:

1. Cache implementations like `OpenSearchOnHeapCache` were changed to allow the config value to override their setting value (to support TieredSpilloverCache segments)
2. However, `IndicesRequestCache` was also putting its default 1% heap size value into the cache config
3. This caused the implementation-specific size settings to be ignored

The fix ensures that:
- When pluggable caching is OFF: `IndicesRequestCache` puts max size into config (backward compatibility)
- When pluggable caching is ON: Cache implementations use their own size settings
- TieredSpilloverCache size settings (`tiered_spillover.onheap.store.size` and `tiered_spillover.disk.store.size`) always take precedence over individual tier implementation settings

### Technical Changes

| Component | Change |
|-----------|--------|
| `TieredSpilloverCache` | Fixed stats decrement logic in `invalidate()` method |
| `TieredSpilloverCacheStatsHolder` | Added `removeDimensions()` override for proper tier handling |
| `IndicesRequestCache` | Only sets max size in config when pluggable caching is disabled |
| `CacheService` | Added `pluggableCachingEnabled()` helper method |
| `OpenSearchOnHeapCache` | Updated to use `CacheService.pluggableCachingEnabled()` |
| `EhcacheDiskCache` | Added documentation clarifying setting behavior with tiered cache |

### Setting Deprecation

The `indices.requests.cache.size` setting is now deprecated when pluggable caching is enabled. Users should use implementation-specific settings instead:

| Setting | Description |
|---------|-------------|
| `indices.requests.cache.tiered_spillover.onheap.store.size` | On-heap tier size in tiered cache |
| `indices.requests.cache.tiered_spillover.disk.store.size` | Disk tier size in tiered cache |
| `indices.requests.cache.opensearch_onheap.size` | On-heap cache size (standalone) |
| `indices.requests.cache.ehcache_disk.max_size_in_bytes` | Disk cache size (standalone) |

## Limitations

- These fixes only affect clusters with the pluggable caching feature flag enabled (`opensearch.experimental.feature.pluggable.caching.enabled`)
- The `indices.requests.cache.size` setting will be removed in a future release

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16560](https://github.com/opensearch-project/OpenSearch/pull/16560) | Fix TieredSpilloverCache stats not adding correctly when shards are closed | [#16559](https://github.com/opensearch-project/OpenSearch/issues/16559) |
| [#16636](https://github.com/opensearch-project/OpenSearch/pull/16636) | Fix cache maximum size settings not working properly with pluggable caching | [#16631](https://github.com/opensearch-project/OpenSearch/issues/16631) |

### Documentation
- [Tiered Cache](https://docs.opensearch.org/2.19/search-plugins/caching/tiered-cache/)
- [Index Request Cache](https://docs.opensearch.org/2.19/search-plugins/caching/request-cache/)
