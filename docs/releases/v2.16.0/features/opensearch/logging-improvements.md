---
tags:
  - opensearch
---
# Logging Improvements

## Summary

OpenSearch v2.16.0 introduces optimized logging in the MasterService and TaskBatcher components to reduce performance overhead during cluster state updates. The change introduces short and long task summaries, deferring expensive summary computation to TRACE level logging only.

## Details

### What's New in v2.16.0

This release addresses a critical performance issue where computing task summaries for DEBUG logging could take up to 10 minutes in clusters with large numbers of pending tasks (e.g., 200K shards during recovery).

### Problem Addressed

When executing pending tasks in `TaskBatcher.runIfNotProcessed()`, the system previously computed a detailed task summary for all batched tasks regardless of log level. For scenarios with 200K tasks in a batching key's linked list, this summary computation blocked task execution for approximately 10 minutes.

### Technical Changes

#### TaskBatcher Changes

- Introduced a `Function<Boolean, String> taskSummaryGenerator` that lazily generates summaries
- Short summary (for DEBUG): `"Tasks batched with key: {batchingKey} and count: {taskCount}"`
- Long summary (for TRACE): Full task details with source and description

```java
// New short summary format
private String buildShortSummary(final Object batchingKey, final int taskCount) {
    return "Tasks batched with key: " + batchingKey.toString().split("\\$")[0] + " and count: " + taskCount;
}
```

#### MasterService Changes

- Modified `runTasks()` to use short summary for DEBUG logging
- Long summary only computed when TRACE logging is enabled
- `ClusterChangedEvent` now uses short summary as source field

```java
final String longSummary = logger.isTraceEnabled() ? taskInputs.taskSummaryGenerator.apply(true) : "";
final String shortSummary = taskInputs.taskSummaryGenerator.apply(false);
```

### Performance Impact

- Saves ~10 minutes during recovery phase for clusters with 200K shards
- Long summary computation only occurs when TRACE level logging is explicitly enabled
- No impact on cluster state update functionality

## Limitations

- Detailed task information requires TRACE level logging, which may not be practical in production
- Short summary provides less debugging information than previous DEBUG output

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14795](https://github.com/opensearch-project/OpenSearch/pull/14795) | Reduce logging in DEBUG for MasterService:run | [#12249](https://github.com/opensearch-project/OpenSearch/issues/12249) |

### Related Issues

| Issue | Description |
|-------|-------------|
| [#12249](https://github.com/opensearch-project/OpenSearch/issues/12249) | [BUG] Reduce TaskBatcher excessive logging in DEBUG mode |
