---
tags:
  - security
---
# Security Index Request Fixes

## Summary

OpenSearch v2.16.0 fixes a NullPointerException (NPE) that occurred in the Security plugin when handling close index requests with Field-Level Security (FLS) enabled. The issue was caused by attempting to retrieve metadata fields from a closed index's mapper service, which returns null.

## Details

### What's New in v2.16.0

#### Bug Fix: NPE on Close Index Request

A NullPointerException was thrown when the Security plugin's `SecurityFlsDlsIndexSearcherWrapper` attempted to get metadata fields from a closed index:

```
java.lang.NullPointerException: Cannot invoke "org.opensearch.index.mapper.MapperService.getMetadataFields()" 
because the return value of "org.opensearch.index.IndexService.mapperService()" is null
```

This occurred because:
1. PR [#4370](https://github.com/opensearch-project/security/pull/4370) changed the FLS implementation to dynamically retrieve metadata fields from the mapper service
2. For closed indices, `indexService.mapperService()` returns null since `needsMapperService` returns false for closed indices
3. The fix adds a check for the index state before attempting to retrieve metadata fields

#### Technical Implementation

The fix modifies `SecurityFlsDlsIndexSearcherWrapper` to:
1. Check if the index state is `CLOSE` using `indexService.getMetadata().getState()`
2. If closed, set `metadataFields` to an empty set (closed indices are not searchable anyway)
3. Log a debug message indicating the index was closed

```java
if (indexService.getMetadata().getState() == IndexMetadata.State.CLOSE) {
    log.debug("{} was closed. Setting metadataFields to empty. Closed index is not searchable.",
        indexService.index().getName());
    metadataFieldsCopy = Collections.emptySet();
} else {
    metadataFieldsCopy = new HashSet<>(indexService.mapperService().getMetadataFields());
    // ... add additional metadata fields
}
```

### Background

This bug was discovered during OpenSearch 2.15 RC generation when ISM (Index State Management) integration tests failed. A revert PR ([#4474](https://github.com/opensearch-project/security/pull/4474)) was introduced to unblock 2.15, and this fix was implemented for 2.16.0.

### Impact

- Affects clusters using Field-Level Security (FLS) with indices that are closed and reopened
- Without this fix, close/open index operations would fail with NPE when FLS is configured
- The fix ensures FLS works correctly with index lifecycle operations

## Limitations

- Closed indices remain unsearchable (expected behavior)
- The fix sets metadata fields to empty for closed indices, which is safe since closed indices cannot be searched

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#4497](https://github.com/opensearch-project/security/pull/4497) | Fix NPE getting metaFields from mapperService on a close index request | [#4475](https://github.com/opensearch-project/security/issues/4475) |
| [#4474](https://github.com/opensearch-project/security/pull/4474) | Revert PR (for 2.15 unblock) | [#4475](https://github.com/opensearch-project/security/issues/4475) |
| [#4370](https://github.com/opensearch-project/security/pull/4370) | Original change that introduced the regression | [#4349](https://github.com/opensearch-project/security/issues/4349) |

### Issues
| Issue | Description |
|-------|-------------|
| [#4475](https://github.com/opensearch-project/security/issues/4475) | Investigate ISM failures caused during 2.15 RC generation |
