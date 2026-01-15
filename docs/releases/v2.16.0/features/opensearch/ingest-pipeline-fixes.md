---
tags:
  - opensearch
---
# Ingest Pipeline Fixes

## Summary

This release fixes a regression in the ScriptProcessor where Short and Byte data types caused failures during ingest pipeline execution. The bug was introduced in v2.8.0 when a new deep copy operation was added to the ScriptProcessor flow.

## Details

### What's New in v2.16.0

The fix adds missing data type handlers for `Short` and `Byte` in the `IngestDocument.deepCopy()` method. Previously, when a Painless script assigned Short or Byte values to document fields, subsequent processors in the pipeline would fail because these types were not properly handled during the deep copy operation.

### Technical Changes

The `IngestDocument.deepCopyMap()` method was updated to handle additional primitive wrapper types:

| Data Type | Status Before | Status After |
|-----------|---------------|--------------|
| `Short` | ❌ Not handled | ✅ Handled |
| `Byte` | ❌ Not handled | ✅ Handled |
| `Character` | ❌ Not handled | ❌ Still broken (tracked separately) |

### Affected Scenario

The following pipeline configuration would fail before this fix:

```json
{
  "description": "Pipeline with Short/Byte types",
  "processors": [
    {
      "script": {
        "source": "ctx.byte = (byte)127; ctx.short = (short)32767"
      }
    },
    {
      "script": {
        "source": "ctx.other_field = 'other_field'"
      }
    }
  ]
}
```

The first script processor would succeed, but the second processor would fail because the deep copy of the document (containing Byte and Short values) was not handled correctly.

### Root Cause

PR #11725 (v2.8.0) added a new invocation of `deepCopyMap()` in the ScriptProcessor flow. The `deepCopyMap()` method did not have handlers for `Short` and `Byte` types, causing the copy operation to fail when these types were present in the document.

## Limitations

- The `Character` data type still fails in script processors (tracked in Issue #14382)
- This fix only addresses the deep copy regression; other data type handling issues may exist

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14380](https://github.com/opensearch-project/OpenSearch/pull/14380) | Add missing data types to IngestDocument deep copy | [#14379](https://github.com/opensearch-project/OpenSearch/issues/14379) |

### Issues
- [#14379](https://github.com/opensearch-project/OpenSearch/issues/14379): BUG - ScriptProcessor fails with Byte and Short data types
- [#14382](https://github.com/opensearch-project/OpenSearch/issues/14382): Character data type failure (separate issue)
- [#11725](https://github.com/opensearch-project/OpenSearch/pull/11725): Original PR that introduced the deep copy invocation
