---
tags:
  - opensearch
---
# Workload Management Logging

## Summary

Fixed a bug where `QueryGroupTask` warning logs were spamming OpenSearch logs when using the scroll API. The fix adds Workload Management (WLM) support for the search scroll API by properly setting the `queryGroupId` from the thread context.

## Details

### What's New in v2.19.0

This release fixes a logging bug introduced in v2.18.0 with the Workload Management feature. When using the scroll API, warning messages were being logged repeatedly:

```
[WARN ][o.o.w.QueryGroupTask] QueryGroup _id can't be null, It should be set before accessing it. This is abnormal behaviour
```

The issue occurred because the `TransportSearchScrollAction` was not setting the `queryGroupId` for scroll requests, causing the `QueryGroupTask.getQueryGroupId()` method to log warnings when the ID was accessed without being set.

### Technical Changes

**Modified Files:**

| File | Change |
|------|--------|
| `TransportSearchScrollAction.java` | Added `ThreadPool` injection and `setQueryGroupId()` call for scroll requests |
| `QueryGroupTask.java` | Added `isQueryGroupSet` flag and `isQueryGroupSet()` method |
| `QueryGroupResourceUsageTrackerService.java` | Added filter to exclude tasks without query group set |

**Key Implementation:**

1. `TransportSearchScrollAction` now checks if the task is a `QueryGroupTask` and sets the query group ID from the thread context before executing the scroll operation.

2. `QueryGroupTask` tracks whether the query group ID has been explicitly set via a new `isQueryGroupSet` boolean flag.

3. `QueryGroupResourceUsageTrackerService` filters out tasks that don't have a query group set, preventing them from being tracked and avoiding the warning logs.

### Code Changes

```java
// TransportSearchScrollAction.java
@Override
protected void doExecute(Task task, SearchScrollRequest request, ActionListener<SearchResponse> listener) {
    try {
        if (task instanceof QueryGroupTask) {
            ((QueryGroupTask) task).setQueryGroupId(threadPool.getThreadContext());
        }
        // ... rest of execution
    }
}
```

```java
// QueryGroupTask.java
private boolean isQueryGroupSet = false;

public final void setQueryGroupId(final ThreadContext threadContext) {
    isQueryGroupSet = true;
    // ... existing logic
}

public boolean isQueryGroupSet() {
    return isQueryGroupSet;
}
```

## Limitations

- This fix only addresses the scroll API. Other APIs using `SearchTask` or `SearchShardTask` must also call `setQueryGroupId()` to avoid similar warnings.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16981](https://github.com/opensearch-project/OpenSearch/pull/16981) | Add WLM support for search scroll API | [#16874](https://github.com/opensearch-project/OpenSearch/issues/16874) |

### Issues
| Issue | Description |
|-------|-------------|
| [#16874](https://github.com/opensearch-project/OpenSearch/issues/16874) | Bug report: QueryGroupTask warning spam in 2.18 when using scroll API |
