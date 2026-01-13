---
tags:
  - opensearch
---
# System Indices

## Summary

OpenSearch v2.19.0 introduces two important fixes for system indices handling: preventing index templates from being applied to system indices, and ensuring consistency of the `isSystem` flag on IndexMetadata across cluster nodes during rolling upgrades.

## Details

### What's New in v2.19.0

#### Index Template Exclusion for System Indices

System indices are now protected from user-defined index templates. Previously, composable index templates with wildcard patterns (e.g., `*`) could inadvertently apply mappings to system indices, potentially causing mapping conflicts that prevented index creation or even node startup.

The fix adds a check in `MetadataCreateIndexService.applyCreateIndexRequest()` that bypasses all template matching for system indices:

```java
// Do not apply any templates to system indices
if (systemIndices.isSystemIndex(name)) {
    return applyCreateIndexRequestWithNoTemplates(currentState, request, silent, metadataTransformer);
}
```

This ensures system indices are created with only their explicitly defined mappings, regardless of any matching index templates.

#### IndexMetadata System Flag Consistency

Fixed a bug where the `isSystem` flag on IndexMetadata could become inconsistent between cluster manager and follower nodes during rolling upgrades. This occurred when plugins retroactively declared indices as system indices (via `SystemIndexPlugin.getSystemIndexDescriptors`).

The root cause was in `IndexMetadataDiff.apply()`, which incorrectly used the previous metadata's `isSystem` value instead of the value from the incoming diff:

```java
// Before (incorrect)
builder.system(part.isSystem);

// After (correct)
builder.system(isSystem);
```

### Technical Changes

| Component | Change |
|-----------|--------|
| `MetadataCreateIndexService` | Added `applyCreateIndexRequestWithNoTemplates()` method to bypass template matching for system indices |
| `IndexMetadata.IndexMetadataDiff` | Fixed `apply()` method to use `isSystem` from diff instead of previous metadata |
| `SystemIndexRestIT` | Added integration test `testSystemIndexCreatedWithoutAnyTemplates()` |
| `IndexMetadataTests` | Added unit test `testIndicesMetadataDiffSystemFlagFlipped()` |

## Limitations

- The template exclusion applies only to system indices identified by `SystemIndices.isSystemIndex()`. Custom indices not registered as system indices will still have templates applied.
- The IndexMetadata fix requires all nodes to be upgraded to v2.19.0+ for full consistency during cluster state publication.

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16418](https://github.com/opensearch-project/OpenSearch/pull/16418) | Ensure index templates are not applied to system indices | [#16340](https://github.com/opensearch-project/OpenSearch/issues/16340) |
| [#16644](https://github.com/opensearch-project/OpenSearch/pull/16644) | Ensure consistency of system flag on IndexMetadata after diff is applied | [#16643](https://github.com/opensearch-project/OpenSearch/issues/16643) |

### Documentation

- [System indexes](https://docs.opensearch.org/2.19/security/configuration/system-indices/)
