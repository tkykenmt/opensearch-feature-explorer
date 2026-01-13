---
tags:
  - domain/core
  - component/server
  - performance
  - search
---
# Node Stats & API Fixes

## Summary

OpenSearch v3.0.0 includes three important bug fixes addressing issues with node stats, the CAT recovery API, and feature flag performance. These fixes resolve a NullPointerException in node stats caused by QueryGroupTasks, correct byte display formatting in the `_cat/recovery` API, and significantly improve the performance of feature flag checks.

## Details

### What's New in v3.0.0

This release addresses three distinct issues that affected cluster monitoring and API usability:

1. **Node Stats NPE Fix**: Resolves a NullPointerException that occurred when the search backpressure service gathered node stats with QueryGroupTasks that didn't have a queryGroupId set.

2. **CAT Recovery Bytes Parameter Fix**: Fixes the `bytes` parameter on `_cat/recovery` API to properly display byte values in the requested unit format.

3. **FeatureFlags Performance Optimization**: Refactors the FeatureFlags implementation to eliminate slow `System.getProperty()` calls in hot paths, improving search query performance.

### Technical Changes

#### Fix 1: Node Stats NPE (PR #17576)

The issue occurred in `QueryGroupService.shouldSBPHandle()` when a `QueryGroupTask` had a null `queryGroupId`. The fix adds a null check before accessing the queryGroupId:

```java
// Before (caused NPE)
if (!task.getQueryGroupId().equals(QueryGroupTask.DEFAULT_QUERY_GROUP_ID_SUPPLIER.get())) {
    // ...
}

// After (safe null check)
if (task.isQueryGroupSet() && !QueryGroupTask.DEFAULT_QUERY_GROUP_ID_SUPPLIER.get().equals(task.getQueryGroupId())) {
    // ...
}
```

The `onTaskCompleted()` method was also updated to check if the queryGroupId is set before processing.

#### Fix 2: CAT Recovery Bytes Parameter (PR #17598)

The `_cat/recovery` API now properly wraps byte values with `ByteSizeValue` to support the `bytes` parameter:

| Field | Before | After |
|-------|--------|-------|
| bytes | Raw number (e.g., `69220`) | Formatted (e.g., `67.5kb`) |
| bytes_recovered | Raw number | Formatted with unit |
| bytes_total | Raw number | Formatted with unit |

**Example Output:**

Without `bytes` parameter:
```
bytes  bytes_recovered bytes_percent bytes_total
49.4kb 49.4kb          100.0%        49.4kb
```

With `bytes=b` parameter:
```
bytes bytes_recovered bytes_percent bytes_total
50676 50676           100.0%        50676
```

#### Fix 3: FeatureFlags Performance (PR #17611)

The FeatureFlags implementation was refactored to address performance issues caused by `System.getProperty()` calls in hot paths:

| Component | Description |
|-----------|-------------|
| `FeatureFlagsImpl` | New internal class managing feature flag state |
| `ConcurrentHashMap` | Replaces immutable Settings for flag storage |
| `TestUtils` | New test utilities including `@LockFeatureFlag` annotation |
| `FlagWriteLock` | AutoCloseable helper for test flag management |

**Key Changes:**
- Feature flags are now pre-populated into a `ConcurrentHashMap` during initialization
- `isEnabled()` no longer calls `System.getProperty()` at runtime
- JVM system properties are only read once during `initializeFeatureFlags()`
- New `@LockFeatureFlag` annotation for test cases requiring specific flag values

### Usage Example

**CAT Recovery API with bytes parameter:**
```bash
# Default output (human-readable)
GET /_cat/recovery?v

# Output in bytes
GET /_cat/recovery?v&bytes=b

# Output in kilobytes
GET /_cat/recovery?v&bytes=kb
```

**Using FeatureFlags in tests (new pattern):**
```java
// Using annotation
@LockFeatureFlag(STAR_TREE_INDEX)
public void testWithFeatureFlag() {
    assertTrue(FeatureFlags.isEnabled(STAR_TREE_INDEX));
}

// Using helper method
FeatureFlags.TestUtils.with(STAR_TREE_INDEX, () -> {
    // Test code with flag enabled
});

// Using explicit lock
try (var lock = new FeatureFlags.TestUtils.FlagWriteLock(STAR_TREE_INDEX)) {
    // Test code with flag enabled
}
```

### Migration Notes

- **CAT Recovery API**: Output format for byte fields has changed from raw numbers to human-readable format by default. Use `bytes=b` parameter to get raw byte values.
- **FeatureFlags in Tests**: Replace `FeatureFlagSetter.set()` and `FeatureFlags.initializeFeatureFlags()` with the new `@LockFeatureFlag` annotation or `FeatureFlags.TestUtils` methods.

## Limitations

- The FeatureFlags refactoring is a breaking change for test code that relied on the old `FeatureFlagSetter` pattern
- The CAT recovery output format change may affect scripts that parse the raw output

## References

### Documentation
- [CAT Recovery API Documentation](https://docs.opensearch.org/3.0/api-reference/cat/cat-recovery/)
- [Nodes Stats API Documentation](https://docs.opensearch.org/3.0/api-reference/nodes-apis/nodes-stats/)
- [Experimental Feature Flags Documentation](https://docs.opensearch.org/3.0/install-and-configure/configuring-opensearch/experimental/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#17576](https://github.com/opensearch-project/OpenSearch/pull/17576) | Fix NPE in node stats due to QueryGroupTasks |
| [#17598](https://github.com/opensearch-project/OpenSearch/pull/17598) | Fix bytes parameter on `_cat/recovery` |
| [#17611](https://github.com/opensearch-project/OpenSearch/pull/17611) | Refactor FeatureFlags for performance |

### Issues (Design / RFC)
- [Issue #17518](https://github.com/opensearch-project/OpenSearch/issues/17518): NPE in node stats due to QueryGroupTasks
- [Issue #17596](https://github.com/opensearch-project/OpenSearch/issues/17596): Bytes parameter doesn't work on `_cat/recovery`
- [Issue #16519](https://github.com/opensearch-project/OpenSearch/issues/16519): FeatureFlags.isEnabled is slow
