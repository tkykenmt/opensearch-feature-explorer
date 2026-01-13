---
tags:
  - domain/core
  - component/server
  - indexing
  - performance
---
# Request Cache

## Summary

OpenSearch v3.3.0 introduces two improvements to the request cache: optimized cache clear operations and prevention of stale responses when keyword field mapping parameters are dynamically updated.

## Details

### What's New in v3.3.0

#### 1. Optimized Cache Clear Performance

The cache clear operation has been significantly optimized by removing unnecessary per-shard iterations. Previously, when clearing the request cache via the Clear Cache API, the system would iterate through all cache keys once per shard, causing high latency especially when using disk-based tiered caching.

**Performance Improvement:**

| Scenario | Before | After | Improvement |
|----------|--------|-------|-------------|
| 2M keys, 10 indices (disk tier) | 131.56 sec | 60.62 sec | ~54% faster |

#### 2. Stale Response Prevention for Keyword Fields

Queries on keyword fields with non-default values for `use_similarity` or `split_queries_on_whitespace` parameters are now automatically excluded from the request cache. This prevents stale/incorrect results when these dynamically updateable parameters are changed.

### Technical Changes

#### Architecture Changes

```mermaid
graph TB
    subgraph "Cache Clear Flow (Before v3.3.0)"
        A1[Clear Cache API] --> B1[Per-Shard Operation]
        B1 --> C1[Queue Cleanup Key]
        C1 --> D1[Force Clean Cache]
        D1 --> E1[Iterate All Keys]
        E1 --> B1
    end
    
    subgraph "Cache Clear Flow (v3.3.0)"
        A2[Clear Cache API] --> B2[Per-Shard Operation]
        B2 --> C2[Queue Cleanup Key]
        C2 --> D2[Node Operation Hook]
        D2 --> E2[Single Force Clean]
        E2 --> F2[Iterate All Keys Once]
    end
```

#### New Components

| Component | Description |
|-----------|-------------|
| `TransportBroadcastByNodeAction.nodeOperation()` | New node-level hook that executes once per node after all shard-level operations complete |
| `IndicesRequestCache.forceCleanCache()` | Separated method to force cache cleanup without enqueueing cleanup keys |
| `IndicesService.forceClearNodewideCaches()` | Node-wide cache clearing method called from the node operation hook |
| `QueryShardContext.setIsCacheable()` | New method to mark queries as non-cacheable |

#### Code Changes

**TransportBroadcastByNodeAction** - Added node-level hook:
```java
protected void nodeOperation(
    List<ShardOperationResult> results, 
    List<BroadcastShardOperationFailedException> accumulatedExceptions
) {}
```

**KeywordFieldMapper** - Added cacheability check:
```java
private void checkToDisableCaching(QueryShardContext context) {
    if (useSimilarity || splitQueriesOnWhitespace) {
        context.setIsCacheable(false);
    }
}
```

### Usage Example

The cache clear API behavior remains unchanged from a user perspective:

```bash
# Clear request cache for specific index
POST /my_index/_cache/clear?request=true

# Clear request cache for all indices
POST /_cache/clear?request=true
```

For keyword fields, queries are automatically excluded from caching when non-default parameters are used:

```json
PUT /my_index
{
  "mappings": {
    "properties": {
      "tags": {
        "type": "keyword",
        "use_similarity": true
      }
    }
  }
}
```

Queries on the `tags` field will not be cached, preventing stale results if `use_similarity` is later changed.

### Migration Notes

- No migration required - changes are backward compatible
- Existing cache clear operations will automatically benefit from improved performance
- Queries on keyword fields with `use_similarity: true` or `split_queries_on_whitespace: true` will no longer be cached

## Limitations

- The node-level hook is specific to `TransportBroadcastByNodeAction` subclasses
- Field data cache optimization using the same pattern is planned for a future release
- Queries on keyword fields with non-default `use_similarity` or `split_queries_on_whitespace` cannot be cached

## References

### Documentation
- [Documentation: Index request cache](https://docs.opensearch.org/3.0/search-plugins/caching/request-cache/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#19263](https://github.com/opensearch-project/OpenSearch/pull/19263) | Remove unnecessary iteration per-shard in request cache cleanup |
| [#19385](https://github.com/opensearch-project/OpenSearch/pull/19385) | Disable request cache for queries on fields with non-default `use_similarity` or `split_queries_on_whitespace` |

### Issues (Design / RFC)
- [Issue #19118](https://github.com/opensearch-project/OpenSearch/issues/19118): Repeated iteration through keys on cache clear API
- [Issue #19183](https://github.com/opensearch-project/OpenSearch/issues/19183): Add node-level hook to TransportBroadcastByNodeAction
- [Issue #19279](https://github.com/opensearch-project/OpenSearch/issues/19279): Dynamically updating mapping parameters does not wipe request cache entries

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/opensearch-request-cache.md)
