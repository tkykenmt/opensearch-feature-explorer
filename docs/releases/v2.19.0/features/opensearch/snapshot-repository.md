---
tags:
  - opensearch
---
# Snapshot Repository

## Summary

OpenSearch 2.19.0 introduces two significant enhancements to snapshot repository functionality: vertical scaling support with SoftReference for the repository data cache, and a new `remote_publication` prefix for configuring remote publication repositories.

## Details

### Vertical Scaling for Repository Data Cache

Previously, snapshot repository data was not cached if its compressed size exceeded a static 500KB limit. This caused repeated downloads during operations like clone, restore, and status checks, increasing latency. The limit did not adjust with vertical or horizontal scaling.

#### New Configuration Setting

A new setting `snapshot.repository_data.cache.threshold` allows users to configure the cache limit as a percentage of heap size or as an absolute value.

| Setting | Description | Default | Range |
|---------|-------------|---------|-------|
| `snapshot.repository_data.cache.threshold` | Maximum threshold for snapshot repository data cache | `min(max(500KB, 1% of heap), Integer.MAX_VALUE - 8)` | 500KB to 1% of heap |

#### SoftReference Implementation

The cache now uses Java's `SoftReference` to allow the JVM to reclaim memory under pressure while still benefiting from caching when memory is available. This provides:

- Automatic memory management under heap pressure
- Better cache utilization on nodes with larger heaps
- Reduced latency for snapshot operations when cache is available

#### Warning Thresholds

- Debug log when data exceeds configured threshold
- Warning log when data exceeds `min(threshold * 10, Integer.MAX_VALUE - 8)` bytes

### Remote Publication Repository Prefix

A new `remote_publication` prefix is introduced for configuring remote publication repositories, enabling clusters to store only metadata remotely without being incorrectly identified as full remote store nodes.

#### Configuration Prefixes

| Prefix | Use Case |
|--------|----------|
| `remote_store` | Full remote store (segment + translog + state) |
| `remote_publication` | Remote publication only (cluster state + routing table) |

#### Node Attributes

Nodes can now be configured with either prefix:
- `remote_store.<repository-type>.repository.*`
- `remote_publication.<repository-type>.repository.*`

This allows migrating a remote publication cluster from remote store to local storage.

## Technical Changes

### Modified Classes

| Class | Change |
|-------|--------|
| `BlobStoreRepository` | Added cache threshold setting, SoftReference wrapper |
| `RemoteStoreNodeAttribute` | Support for multiple attribute prefixes |
| `JoinTaskExecutor` | Updated repository compatibility checks |
| `DiscoveryNode` | Updated remote store detection logic |

### New Constants

```java
// Cache settings
SNAPSHOT_REPOSITORY_DATA_CACHE_THRESHOLD_SETTING_NAME = "snapshot.repository_data.cache.threshold"
SNAPSHOT_REPOSITORY_DATA_CACHE_THRESHOLD_DEFAULT_PERCENTAGE = 0.01
CACHE_MIN_THRESHOLD = 500KB
CACHE_MAX_THRESHOLD = min(max(500KB, 1% of heap), Integer.MAX_VALUE - 8)

// Repository prefixes
REMOTE_STORE_NODE_ATTRIBUTE_KEY_PREFIX = ["remote_store", "remote_publication"]
```

## Limitations

- The `snapshot.repository_data.cache.threshold` setting is static and requires node restart to change
- SoftReference behavior depends on JVM garbage collection, which may vary across implementations
- The `remote_publication` prefix is intended for specific migration scenarios

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16489](https://github.com/opensearch-project/OpenSearch/pull/16489) | Add vertical scaling and SoftReference for snapshot repository data cache | [#16298](https://github.com/opensearch-project/OpenSearch/issues/16298) |
| [#16271](https://github.com/opensearch-project/OpenSearch/pull/16271) | Support prefix list for remote repository attributes | [#16390](https://github.com/opensearch-project/OpenSearch/issues/16390) |

### Documentation

- [Register Snapshot Repository](https://docs.opensearch.org/2.19/api-reference/snapshots/create-repository/)
- [Get Snapshot Repository](https://docs.opensearch.org/2.19/api-reference/snapshots/get-snapshot-repository/)
