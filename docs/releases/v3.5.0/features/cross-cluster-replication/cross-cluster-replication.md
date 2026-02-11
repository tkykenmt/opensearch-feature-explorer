---
tags:
  - cross-cluster-replication
---
# Cross-Cluster Replication Bug Fixes

## Summary

OpenSearch v3.5.0 includes test stability improvements for the Cross-Cluster Replication (CCR) plugin. These changes fix flaky integration tests related to multi-node cluster configurations and improve error handling during test cleanup.

## Details

### What's New in v3.5.0

#### Test Infrastructure Improvements

1. **Multi-Node Test Support**: Fixed integration tests to properly handle multi-node cluster configurations by copying synonym files to all cluster nodes instead of just the first node.

2. **Flaky Test Fix**: Improved test cleanup reliability by allowing HTTP 500 errors during `stopAllReplication` operations. This addresses race conditions where synonym files may be deleted before replication is fully stopped.

3. **Connection Manager Fix**: Added proper cleanup of HTTP connection managers in test infrastructure to prevent resource leaks.

4. **Thread Safety Improvement**: Changed `BatchSizeSettings` to use `AtomicInteger` for thread-safe batch size adjustments.

5. **API Compatibility**: Updated `RemoteClusterRepository.snapshotShard()` method signature to include new `IndexMetadata` parameter for OpenSearch 3.5.0 compatibility.

### Technical Changes

#### Multi-Node Synonym File Handling

Tests now iterate over all cluster nodes when copying synonym files:

```kotlin
for (i in 0 until clusterNodes(LEADER)) {
    val config = PathUtils.get(buildDir, leaderClusterPath + i, "config")
    val synonymPath = config.resolve("synonyms.txt")
    Files.copy(javaClass.getResourceAsStream("/analyzers/synonyms.txt"), synonymPath)
}
```

#### Improved Error Handling in Test Cleanup

The `stopAllReplicationJobs` method now tolerates HTTP 500 errors during cleanup:

```kotlin
catch (e: ResponseException) {
    // 400 = index not being replicated, 500 = internal error (e.g., missing synonym files)
    // Both are acceptable during cleanup
    if (e.response.statusLine.statusCode != 400 && e.response.statusLine.statusCode != 500) {
        throw e
    }
}
```

#### Thread-Safe Batch Size Management

Changed from volatile variable to `AtomicInteger` for concurrent access:

```kotlin
private val dynamicBatchSize = AtomicInteger(-1)

fun reduceBatchSize() {
    dynamicBatchSize.updateAndGet { current ->
        val effectiveSize = if (current > 0) current else getBatchSize()
        maxOf(effectiveSize / 2, MIN_OPS_BATCH_SIZE)
    }
}
```

## Limitations

- These are test-only changes with no impact on production functionality
- The synonym file handling fix is specific to the test infrastructure

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1621](https://github.com/opensearch-project/cross-cluster-replication/pull/1621) | Fix replication tests and increment version to 3.5.0 | [#1617](https://github.com/opensearch-project/cross-cluster-replication/pull/1617) |
| [#1630](https://github.com/opensearch-project/cross-cluster-replication/pull/1630) | Fix flaky test by allowing 500 error on stopAllReplication for MultiNode tests | - |
