---
tags:
  - domain/core
  - component/server
  - performance
  - search
---
# Tiered Caching

## Summary

OpenSearch v3.0.0 introduces two key improvements to tiered caching: a unified cache manager for disk caches and an extended took-time policy that now guards both heap and disk tiers. These changes reduce CPU overhead from excessive thread pools and prevent the heap tier from being flooded with cheap queries.

## Details

### What's New in v3.0.0

1. **Single Cache Manager for Disk Caches** ([#17513](https://github.com/opensearch-project/OpenSearch/pull/17513)): Previously, creating N ehcache disk caches resulted in N separate cache managers, each with its own disk write thread pool. This caused CPU spikes when tiered caching was enabled. The new implementation uses a single cache manager for all disk caches per cache type, with a shared thread pool sized between 2 and 1.5× CPU cores.

2. **Took-Time Policy Extended to Heap Tier** ([#17190](https://github.com/opensearch-project/OpenSearch/pull/17190)): The minimum took-time threshold policy now guards both the heap tier and disk tier, not just the disk tier. This prevents cheap queries from flooding the heap cache when caching size > 0 queries.

### Technical Changes

#### Architecture Changes

```mermaid
graph TB
    subgraph "Before v3.0.0"
        Q1[Query] --> HC1[Heap Cache]
        HC1 -->|Eviction| DC1[Disk Cache]
        DC1 -->|Disk Policy| DP1[Took-Time Check]
    end
    
    subgraph "v3.0.0"
        Q2[Query] --> CP[Cache Policy]
        CP -->|Took-Time Check| HC2[Heap Cache]
        HC2 -->|Eviction + Disk Policy| DC2[Disk Cache]
    end
```

#### New Components

| Component | Description |
|-----------|-------------|
| `EhcacheDiskCacheManager` | Singleton manager per cache type that creates and manages all disk caches via a single `PersistentCacheManager` |
| `TookTimePolicy` (extended) | Now accepts a target setting parameter to support both heap and disk tier policies |

#### New Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `indices.requests.cache.tiered_spillover.policies.took_time.threshold` | Minimum query execution time to enter the cache (heap tier) | `0ms` |
| `indices.requests.cache.tiered_spillover.disk.store.policies.took_time.threshold` | Minimum query execution time to enter the disk tier | `10ms` |

The disk tier setting key remains unchanged for backwards compatibility.

#### Thread Pool Changes

| Setting | Old Default | New Default |
|---------|-------------|-------------|
| `ehcache_disk.min_threads` | 2 | 2 |
| `ehcache_disk.max_threads` | 2 | 1.5 × CPU cores (search thread pool size) |

### Usage Example

```yaml
# opensearch.yml - Enable tiered caching with custom policies
indices.requests.cache.store.name: tiered_spillover
indices.requests.cache.tiered_spillover.onheap.store.name: opensearch_onheap
indices.requests.cache.tiered_spillover.disk.store.name: ehcache_disk

# Set heap tier threshold to 5ms (queries taking <5ms won't be cached)
indices.requests.cache.tiered_spillover.policies.took_time.threshold: 5ms

# Set disk tier threshold to 15ms (queries taking <15ms won't spill to disk)
indices.requests.cache.tiered_spillover.disk.store.policies.took_time.threshold: 15ms
```

### Migration Notes

- The disk took-time policy setting key (`tiered_spillover.disk.store.policies.took_time.threshold`) is unchanged for backwards compatibility
- The new heap tier policy defaults to `0ms`, maintaining previous behavior where all queries could enter the heap cache
- Existing configurations will continue to work without modification

## Limitations

- Tiered caching is still experimental and not recommended for production use
- Only supported for the request cache (not query cache)
- The `cache-ehcache` plugin must be installed for disk tier functionality

## References

### Documentation
- [Tiered Cache Documentation](https://docs.opensearch.org/3.0/search-plugins/caching/tiered-cache/)

### Blog Posts
- [Tiered Caching Blog](https://opensearch.org/blog/tiered-cache/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#17513](https://github.com/opensearch-project/OpenSearch/pull/17513) | Single cache manager for all ehcache disk caches |
| [#17190](https://github.com/opensearch-project/OpenSearch/pull/17190) | Took-time threshold guards heap tier as well as disk tier |

### Issues (Design / RFC)
- [Issue #16162](https://github.com/opensearch-project/OpenSearch/issues/16162): RFC - Optimize caching policy for Request cache

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/opensearch-tiered-caching.md)
