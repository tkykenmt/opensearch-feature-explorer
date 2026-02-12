---
tags:
  - opensearch
---
# BWC Timestamp Upgrade Fix

## Summary

Fixes a backward compatibility (BWC) issue where upgrading from pre-3.3.0 versions (e.g., 2.19.x) to 3.3.0 caused shard allocation failures on indices with `@timestamp` date fields. The root cause was that v3.3.0 unconditionally enabled `skip_list` (via `docValuesSkipIndexType=RANGE`) for `@timestamp` fields, but Lucene does not allow changing the skip index type on existing index segments. The fix adds a version check so that `skip_list` auto-enablement only applies to indices created on v3.3.0 or later.

## Details

### What's New in v3.3.1

In v3.3.0, the `isSkiplistDefaultEnabled()` method in `DateFieldMapper` was introduced to automatically enable skip list for `@timestamp` fields and index sort date fields. However, this applied to all indices regardless of when they were created. When a pre-3.3.0 index (with `docValuesSkipIndexType=NONE`) was opened on a 3.3.0 node and new documents were ingested, Lucene rejected the change with:

```
IllegalArgumentException: cannot change field "@timestamp" from docValuesSkipIndexType=NONE to inconsistent docValuesSkipIndexType=RANGE
```

The fix wraps the auto-enable logic in a version check (`indexCreatedVersion.onOrAfter(Version.V_3_3_0)`), ensuring only indices created on 3.3.0+ get automatic skip list enablement. Older indices retain `skip_list=false` for `@timestamp` and index sort fields, avoiding the Lucene incompatibility.

### Technical Changes

The change is in `DateFieldMapper.isSkiplistDefaultEnabled()`:

```java
boolean isSkiplistDefaultEnabled(IndexSortConfig indexSortConfig, String fieldName) {
    if (this.indexCreatedVersion.onOrAfter(Version.V_3_3_0)) {
        if (!isSkiplistConfigured) {
            if (indexSortConfig.hasPrimarySortOnField(fieldName)) {
                return true;
            }
            if (DataStreamFieldMapper.Defaults.TIMESTAMP_FIELD.getName().equals(fieldName)) {
                return true;
            }
        }
    }
    return false;
}
```

Tests were updated to verify that indices created with v3.2.0 do not get skip list auto-enabled, while v3.3.0+ indices continue to benefit from the optimization.

## Limitations

- Indices created before v3.3.0 will not automatically benefit from skip list on `@timestamp` fields, even after upgrading to v3.3.1. Users must reindex to enable skip list on those fields.
- The `skip_list` mapping parameter is not updatable after index creation.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#19671](https://github.com/opensearch-project/OpenSearch/pull/19671) | Fix bwc @timestamp upgrade issue by adding a version check on skip_list param | [#19660](https://github.com/opensearch-project/OpenSearch/issues/19660) |
| [#19661](https://github.com/opensearch-project/OpenSearch/pull/19661) | Revert attempt (closed, not merged) — superseded by #19671 | [#19660](https://github.com/opensearch-project/OpenSearch/issues/19660) |
