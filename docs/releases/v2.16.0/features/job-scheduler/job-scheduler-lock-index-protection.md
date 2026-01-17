---
tags:
  - job-scheduler
---
# Job Scheduler Lock Index Protection

## Summary

Enhanced the Job Scheduler plugin to wrap all interactions with the `.opendistro-job-scheduler-lock` system index inside `ThreadContext.stashContext()`. This ensures the plugin can properly read and write to the lock index even when system index protections are enabled.

## Details

### What's New in v2.16.0

The Job Scheduler plugin uses a lock index (`.opendistro-job-scheduler-lock`) to prevent concurrent job execution across cluster nodes. With enhanced system index protections in OpenSearch, direct access to system indices can be blocked even for plugins.

This enhancement wraps all lock index operations with `ThreadContext.stashContext()`, which temporarily clears the thread context to allow privileged access to system indices.

### Technical Changes

The `LockService` class was modified to wrap the following operations:

| Method | Operation |
|--------|-----------|
| `createLockIndex()` | Creating the lock index |
| `createLock()` | Creating a new lock document |
| `updateLock()` | Updating an existing lock |
| `findLock()` | Finding a lock by ID |
| `deleteLock()` | Deleting a lock |

Each method now uses the pattern:

```java
try (ThreadContext.StoredContext ignore = client.threadPool().getThreadContext().stashContext()) {
    // Lock index operation
} catch (Exception e) {
    logger.error(e);
    listener.onFailure(e);
}
```

### Why This Matters

System indices have special protections that prevent inadvertent modification by users, including admin users. Without this change, the Job Scheduler plugin could fail to acquire or release locks when system index protections are enforced, causing scheduled jobs to fail or run concurrently.

## Limitations

- This is a preparatory change for full system index registration (completed separately in PR #474)
- The lock index itself is not yet registered as a system index in this PR

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#347](https://github.com/opensearch-project/job-scheduler/pull/347) | Wrap interactions with `.opendistro-job-scheduler-lock` in ThreadContext.stashContext | [#305](https://github.com/opensearch-project/job-scheduler/issues/305) |

### Related Issues
| Issue | Description |
|-------|-------------|
| [#305](https://github.com/opensearch-project/job-scheduler/issues/305) | Make the job scheduler lock index a system index |
