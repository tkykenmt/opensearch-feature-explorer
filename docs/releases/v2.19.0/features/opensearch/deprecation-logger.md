---
tags:
  - opensearch
---
# Deprecation Logger Cache Bound

## Summary

In v2.19.0, OpenSearch fixes a memory leak in the deprecation logger by bounding the size of the deduplication cache. Previously, the cache used to track logged deprecation messages could grow without limit, potentially causing out-of-memory (OOM) errors when clients sent requests with unique `X-Opaque-Id` headers.

## Details

### What's New in v2.19.0

The deprecation logger uses a deduplication mechanism to prevent the same deprecation warning from being logged multiple times. This mechanism tracks logged messages using a combination of the message key and the `X-Opaque-Id` request header.

**Problem**: The previous implementation used an unbounded `ConcurrentHashMap` to store these keys. When clients sent requests with unique `X-Opaque-Id` values per request, the cache would grow indefinitely, eventually causing memory exhaustion.

**Solution**: The fix introduces two key changes:

1. **Cache Size Limit**: A maximum cache size of 16,384 entries (`MAX_DEDUPE_CACHE_ENTRIES`) is enforced. Once this limit is reached, new deprecation messages are treated as "already logged" to prevent further cache growth.

2. **Logger Enabled Check**: Before creating a `DeprecatedMessage` object and checking the cache, the code now verifies if the deprecation logger is enabled. This optimization skips unnecessary overhead when deprecation logging is disabled.

### Technical Changes

**DeprecatedMessage.java**:
```java
// Maximum cache size constant
static final int MAX_DEDUPE_CACHE_ENTRIES = 16_384;

public boolean isAlreadyLogged() {
    if (keyDedupeCache.contains(keyWithXOpaqueId)) {
        return true;
    }
    if (keyDedupeCache.size() >= MAX_DEDUPE_CACHE_ENTRIES) {
        // Stop logging if max size is breached
        return true;
    }
    return !keyDedupeCache.add(keyWithXOpaqueId);
}
```

**DeprecationLogger.java**:
```java
public DeprecationLoggerBuilder withDeprecation(String key, String msg, Object[] params) {
    // Check if logger is enabled first to skip overhead
    if (logger.isEnabled(DEPRECATION)) {
        DeprecatedMessage deprecationMessage = new DeprecatedMessage(key, HeaderWarning.getXOpaqueId(), msg, params);
        if (!deprecationMessage.isAlreadyLogged()) {
            logger.log(DEPRECATION, deprecationMessage);
        }
    }
    return this;
}
```

### Behavior After Cache Limit

When the cache reaches 16,384 entries:
- New unique deprecation messages will not be logged
- Existing cached messages continue to be deduplicated correctly
- No additional memory is consumed
- Historical logs will already contain extensive deprecation warnings at this point

## Limitations

- Once the cache limit is reached, new unique deprecation warnings are silently suppressed
- The cache is not cleared automatically; it persists for the lifetime of the node
- The 16,384 entry limit is hardcoded and not configurable

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16724](https://github.com/opensearch-project/OpenSearch/pull/16724) | Bound the size of cache in deprecation logger | [#16702](https://github.com/opensearch-project/OpenSearch/issues/16702) |

### Related Issues

| Issue | Description |
|-------|-------------|
| [#16702](https://github.com/opensearch-project/OpenSearch/issues/16702) | [BUG] DeprecationLogger - Unbounded memory usage |
