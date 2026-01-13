---
tags:
  - opensearch
---
# GetStats API

## Summary

In v2.19.0, the `GetStats` class was updated to fix a long-standing field naming inconsistency. A new `time` field was added to replace the incorrectly named `getTime` field in the Index Stats API response. The `getTime` field is now deprecated and will be removed in a future version.

## Details

### What's New in v2.19.0

The Index Stats API returns statistics about index operations, including "get" operations (document retrieval by ID). When using the `?human` parameter, the API returns human-readable time values alongside millisecond values.

Prior to this fix, the human-readable field for get operation time was incorrectly named `getTime` instead of `time`. This inconsistency originated from a refactoring error nearly twelve years ago (pre-fork from Elasticsearch).

### Technical Changes

The `GetStats.java` class was modified to:

1. Add a new `time` field that correctly follows the naming convention used by other stats fields
2. Deprecate the `getTime` field with `@Deprecated(forRemoval = true)` annotation
3. Output both fields during the deprecation period for backward compatibility

**Before (v2.18.0 and earlier):**
```json
{
  "get": {
    "total": 0,
    "getTime": "0s",
    "time_in_millis": 0,
    ...
  }
}
```

**After (v2.19.0+):**
```json
{
  "get": {
    "total": 0,
    "time": "0s",
    "getTime": "0s",
    "time_in_millis": 0,
    ...
  }
}
```

### Migration Guide

- Update any code that parses the `getTime` field to use the new `time` field instead
- Both fields are available during the deprecation period
- The `getTime` field will be removed in a future major version

## Limitations

- The deprecated `getTime` field will continue to be returned alongside `time` until it is removed in a future version
- Clients should migrate to using the `time` field before the deprecation period ends

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#17009](https://github.com/opensearch-project/OpenSearch/pull/17009) | Fix getTime field name to time in GetStats | [#16894](https://github.com/opensearch-project/OpenSearch/issues/16894) |

### Related Resources

- [Index Stats API Documentation](https://docs.opensearch.org/2.19/api-reference/index-apis/stats/)
- [OpenSearch API Specification PR #785](https://github.com/opensearch-project/opensearch-api-specification/pull/785)
