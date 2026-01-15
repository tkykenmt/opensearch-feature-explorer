---
tags:
  - opensearch
---
# Index Creation NPE Fix

## Summary

Fixed a NullPointerException (NPE) that occurred when creating an index with `index.number_of_replicas` explicitly set to `null`. The fix ensures that when the replica count is null, OpenSearch falls back to the cluster default value (`cluster.default_number_of_replicas`) instead of throwing an exception.

## Details

### What's New in v2.16.0

This release fixes a bug where creating an index with `index.number_of_replicas` set to `null` caused a NullPointerException in `IndexSettings.getNumberOfReplicas()`.

### Root Cause

The `IndexSettings.getNumberOfReplicas()` method returned an `int` primitive type but called `settings.getAsInt()` with a `null` default value. When the setting was explicitly set to `null`, the auto-unboxing from `Integer` to `int` caused an NPE.

```java
// Before fix - caused NPE when setting was null
public int getNumberOfReplicas() {
    return settings.getAsInt(IndexMetadata.SETTING_NUMBER_OF_REPLICAS, null);
}
```

### Technical Changes

The fix was applied in `MetadataCreateIndexService.aggregateIndexSettings()`:

```java
// Before
if (INDEX_NUMBER_OF_REPLICAS_SETTING.exists(indexSettingsBuilder) == false) {
    indexSettingsBuilder.put(SETTING_NUMBER_OF_REPLICAS, DEFAULT_REPLICA_COUNT_SETTING.get(currentState.metadata().settings()));
}

// After
if (INDEX_NUMBER_OF_REPLICAS_SETTING.exists(indexSettingsBuilder) == false
    || indexSettingsBuilder.get(SETTING_NUMBER_OF_REPLICAS) == null) {
    indexSettingsBuilder.put(SETTING_NUMBER_OF_REPLICAS, DEFAULT_REPLICA_COUNT_SETTING.get(currentState.metadata().settings()));
}
```

The additional null check ensures that even when the setting key exists but has a null value, the cluster default is applied.

### Behavior After Fix

When creating an index with `index.number_of_replicas` set to `null`:
1. OpenSearch detects the null value
2. Falls back to `cluster.default_number_of_replicas` setting
3. If cluster default is not set, uses the hardcoded default of `1`

## Limitations

- This fix only addresses the NPE during index creation
- The underlying `IndexSettings.getNumberOfReplicas()` method signature remains unchanged

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14812](https://github.com/opensearch-project/OpenSearch/pull/14812) | Use default value when index.number_of_replicas is null | [#14783](https://github.com/opensearch-project/OpenSearch/issues/14783) |

### Issues
- [#14783](https://github.com/opensearch-project/OpenSearch/issues/14783): NPE when SETTING_NUMBER_OF_REPLICAS is null
