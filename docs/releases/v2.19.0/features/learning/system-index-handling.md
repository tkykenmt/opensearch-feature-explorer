---
tags:
  - learning
---
# System Index Handling

## Summary

Bug fixes for the Learning to Rank (LTR) plugin to properly handle system index access in OpenSearch 2.19.0. The `.ltrstore*` indices are system indices, and accessing them without proper thread context stashing caused integration test failures and warnings.

## Details

### What's New in v2.19.0

The LTR plugin's REST handlers now properly stash the thread context before accessing system indices (`.ltrstore*`). This prevents warnings about direct system index access and ensures compatibility with OpenSearch's system index protection mechanisms.

### Technical Changes

#### Thread Context Stashing

Modified REST handlers to stash thread context before system index operations:

- `RestAddFeatureToSet` - Feature set modifications
- `RestCreateModelFromSet` - Model creation from feature sets
- `RestFeatureManager` - Feature CRUD operations (get, delete, add/update)
- `RestStoreManager` - LTR store deletion

**Pattern applied:**
```java
return (channel) -> {
    try (ThreadContext.StoredContext threadContext = 
            client.threadPool().getThreadContext().stashContext()) {
        ActionListener<Response> wrappedListener = ActionListener
            .runBefore(originalListener, () -> threadContext.restore());
        builder.execute(wrappedListener);
    } catch (Exception e) {
        channel.sendResponse(new BytesRestResponse(
            RestStatus.INTERNAL_SERVER_ERROR, e.getMessage()));
    }
};
```

#### Integration Test Fixes

- Added `allowed_warnings` directives in YAML tests to handle system index access warnings
- Refactored index refresh logic to target specific indices instead of all indices
- Fixed test cases to use proper LTR store deletion API instead of direct index deletion

### Build Infrastructure

- Added builds against Java 11 and 17
- Modified build scripts to onboard LTR to OpenSearch
- Backported commits from main to 2.x branch

## Limitations

- System index access warnings may still appear in logs but do not affect functionality
- The `.ltrstore*` indices remain system indices with restricted direct access

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#126](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/126) | Modified Rest Handlers to stash context before modifying system indices | [#120](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/120) |
| [#129](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/129) | Stashed context for GET calls |  |
| [#132](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/132) | Modify ITs to ignore transient warning |  |
| [#135](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/135) | Refactor index refresh logic in ITs |  |
| [#124](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/124) | Added builds against Java 11 and 17 |  |
| [#116](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/116) | Backporting commits from main to 2.x |  |
| [#98](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/98) | Modified build scripts to onboard LTR to OpenSearch |  |
| [#91](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/91) | Merge main into 2.x |  |

### Related Issues
| Issue | Description |
|-------|-------------|
| [#120](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/120) | Integration Test Failed for opensearch-learning-to-rank-base-2.19.0 |
