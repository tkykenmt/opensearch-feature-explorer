# Shard & Segment Bugfixes

## Summary

OpenSearch v3.4.0 includes three critical bugfixes related to shard and segment operations that improve cluster stability during node restarts, early cluster initialization, and when using custom engine configurations. These fixes prevent primary shard failures during merged segment warming, resolve assertion errors in resource usage collection, and fix `_cat/indices` API failures when using engine configuration builders.

## Details

### What's New in v3.4.0

This release addresses three distinct issues in shard and segment handling:

1. **Merged Segment Warmer Exception Handling** - Prevents primary shard failures caused by exceptions during the merged segment warming process
2. **ClusterService State Assertion Fix** - Resolves assertion errors when collecting resource usage stats during early cluster initialization
3. **EngineConfig Builder Fix** - Fixes missing `mergedSegmentTransferTracker` in the `toBuilder()` method causing `_cat/indices` API failures

### Technical Changes

#### 1. Merged Segment Warmer Exception Handling (PR #19436)

**Problem**: During node restarts with merged segment warmer enabled, a race condition could cause primary shard failures. When `InternalEngine` is created but `IndexShard.currentEngineReference` is not yet set, segment merges could trigger the warmer which calls `IndexShard.getEngine()`, throwing `AlreadyClosedException` and causing shard failure.

**Solution**: Wrap the entire warming logic in a try-catch block to gracefully handle exceptions without failing the merge operation.

```java
// MergedSegmentWarmer.java - Before
@Override
public void warm(LeafReader leafReader) throws IOException {
    if (shouldWarm() == false) {
        return;
    }
    // ... warming logic that could throw exceptions
}

// After
@Override
public void warm(LeafReader leafReader) throws IOException {
    try {
        if (shouldWarm() == false) {
            return;
        }
        // ... warming logic
    } catch (Exception e) {
        logger.warn("Exception during merged segment warmer, skip warming", e);
    }
}
```

#### 2. ClusterService State Assertion Fix (PR #19775)

**Problem**: `ResourceUsageCollectorService.collectLocalNodeResourceUsageStats()` called `clusterService.state()` to check if the cluster state was initialized. However, `ClusterApplierService.state()` throws an assertion error if the state is null (during early initialization), making the null check ineffective in assertion-enabled environments.

**Solution**: Use `clusterService.isStateInitialised()` instead of checking `clusterService.state() != null`.

```java
// Before
if (nodeResourceUsageTracker.isReady() && clusterService.state() != null) {
    collectNodeResourceUsageStats(...);
}

// After
if (nodeResourceUsageTracker.isReady() && clusterService.isStateInitialised()) {
    collectNodeResourceUsageStats(...);
}
```

#### 3. EngineConfig Builder Fix (PR #20105)

**Problem**: The `EngineConfig.toBuilder()` method was missing the `mergedSegmentTransferTracker` field (added in PR #18929). This caused `NullPointerException` when calling `_cat/indices` API on indexes using custom engine configurations (e.g., `opensearch-storage-encryption` plugin).

**Solution**: Add the missing field to the builder method.

```java
// EngineConfig.java
public Builder toBuilder() {
    return new Builder()
        // ... existing fields
        .clusterApplierService(this.clusterApplierService)
        .mergedSegmentTransferTracker(this.mergedSegmentTransferTracker); // Added
}
```

### Impact

| Fix | Impact | Affected Scenarios |
|-----|--------|-------------------|
| Warmer Exception Handling | Prevents shard failures | Node restarts with segment replication enabled |
| ClusterService Assertion | Prevents test failures | Early cluster initialization with assertions enabled |
| EngineConfig Builder | Fixes API errors | `_cat/indices` with custom engine plugins |

## Limitations

- The merged segment warmer exception handling logs warnings but silently skips warming - administrators should monitor logs for repeated warnings
- These fixes are specific to edge cases and do not change normal operation behavior

## References

### Documentation
- [Remote Segment Warmer Documentation](https://docs.opensearch.org/3.4/tuning-your-cluster/availability-and-recovery/remote-store/remote-segment-warmer/): Official docs
- [PR #18929](https://github.com/opensearch-project/OpenSearch/pull/18929): Original PR that added MergedSegmentTransferTracker to EngineConfig

### Pull Requests
| PR | Description |
|----|-------------|
| [#19436](https://github.com/opensearch-project/OpenSearch/pull/19436) | Avoid primary shard failure caused by merged segment warmer exceptions |
| [#19775](https://github.com/opensearch-project/OpenSearch/pull/19775) | Fixed assertion unsafe use of ClusterService.state() in ResourceUsageCollectorService |
| [#20105](https://github.com/opensearch-project/OpenSearch/pull/20105) | Fix toBuilder method in EngineConfig to include mergedSegmentTransferTracker |

### Issues (Design / RFC)
- [Issue #19435](https://github.com/opensearch-project/OpenSearch/issues/19435): BUG - Avoid primary shard failure caused by merge segment warmer exceptions

## Related Feature Report

- [Segment Warmer](../../../../features/opensearch/segment-warmer.md)
