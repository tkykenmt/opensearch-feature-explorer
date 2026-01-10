# Tiered Caching

## Summary

This release fixes a critical bug in tiered caching where query execution exceptions (such as timeouts or task cancellations) caused subsequent identical queries to return cached exceptions instead of recomputing the query. The fix ensures proper cleanup of the concurrent request tracking map even when exceptions occur.

## Details

### What's New in v3.3.0

This release addresses a bug in the `TieredSpilloverCache` where query execution exceptions were not properly handled, leading to persistent error states for affected cache keys.

### Technical Changes

#### Bug Description

When a query running through the tiered cache encountered an exception (e.g., `TaskCancelledException` from timeouts or parent task cancellation), the following sequence occurred:

1. The exception caused a `NullPointerException` in the completion handler
2. The NPE was swallowed, but the key was never removed from `completableFutureMap`
3. The `completableFutureMap` is used to handle concurrent requests for the same key
4. Subsequent requests for the same key would return the cached exception instead of recomputing

This caused users to see the same exception repeatedly for identical queries until a cache refresh or invalidation changed the key.

#### Fix Implementation

The fix wraps the completion handler logic in a `try-finally` block to ensure the key is always removed from `completableFutureMap`, regardless of whether an exception occurred:

```java
BiFunction<Tuple<Tuple<ICacheKey<K>, V>, Boolean>, Throwable, Void> handler = (pairInfo, ex) -> {
    try {
        if (pairInfo != null) {
            // Normal processing logic
            Tuple<ICacheKey<K>, V> pair = pairInfo.v1();
            boolean rejectedByPolicy = pairInfo.v2();
            if (pair != null && !rejectedByPolicy) {
                // Add to cache
            }
        } else {
            if (ex != null) {
                logger.warn("Exception occurred while trying to compute the value", ex);
            }
        }
    } finally {
        completableFutureMap.remove(key); // Always cleanup
    }
    return null;
};
```

#### Key Changes

| Change | Description |
|--------|-------------|
| Null check for `pairInfo` | Added explicit null check before accessing tuple values |
| Try-finally block | Ensures `completableFutureMap.remove(key)` is always called |
| Exception logging | Moved exception logging inside the null check block |

### Usage Example

The fix is transparent to users. Queries that previously got stuck returning exceptions will now properly retry:

```bash
# Query that might timeout
GET /my-index/_search?request_cache=true
{
  "query": { "match_all": {} },
  "timeout": "1ms"
}

# If timeout occurs, subsequent identical queries will now
# properly recompute instead of returning cached exception
```

### Migration Notes

No migration required. The fix is automatically applied when upgrading to v3.3.0.

## Limitations

- This fix only addresses exception handling in the tiered cache
- The underlying query timeout or cancellation behavior is unchanged
- Tiered caching remains an experimental feature

## Related PRs

| PR | Description |
|----|-------------|
| [#19000](https://github.com/opensearch-project/OpenSearch/pull/19000) | Handle query execution exception in tiered cache |

## References

- [Tiered Cache Documentation](https://docs.opensearch.org/3.0/search-plugins/caching/tiered-cache/)
- [Tiered Caching Blog](https://opensearch.org/blog/tiered-cache/)

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/tiered-caching.md)
