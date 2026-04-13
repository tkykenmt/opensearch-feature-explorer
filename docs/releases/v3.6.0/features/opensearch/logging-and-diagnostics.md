---
tags:
  - opensearch
---
# Logging & Diagnostics

## Summary

OpenSearch v3.6.0 fixes invalid JSON in task details log files (`opensearch_task_detailslog.json`) caused by unescaped metadata field values. When metadata contained nested JSON content (e.g., search source queries), the quotation marks within the value were not escaped, producing malformed JSON log events that broke downstream log parsers.

## Details

### What's New in v3.6.0

This release fixes a long-standing bug (reported in 2023) where `OpenSearchJsonLayout` did not apply JSON encoding to custom message fields (`OpenSearchMessageField` values). The `metadata` field in task details logs frequently contains search source JSON, and without proper escaping the resulting log line was invalid JSON.

### Problem

When task resource consumers are enabled (`task_resource_consumers.enabled: true`), OpenSearch writes task details to `opensearch_task_detailslog.json`. The `metadata` field can contain nested JSON such as search queries:

```json
{
  "metadata": "source[{"size":1,"query":{"bool":{"must":[...]}}}]"
}
```

The inner quotes were not escaped, making the entire log event unparseable by JSON parsers (e.g., Fluent Bit, Logstash, jq).

### Technical Changes

The fix wraps `OpenSearchMessageField` values with Log4j's `%enc{...}{JSON}` encoder in `OpenSearchJsonLayout.pattern()`:

```java
// Before (no escaping)
map.put(key, inQuotes("%OpenSearchMessageField{" + key + "}"));

// After (JSON-escaped)
map.put(key, inQuotes("%enc{%OpenSearchMessageField{" + key + "}}{JSON}"));
```

This applies to all custom fields configured via `opensearchmessagefields` in Log4j appender layouts, including `metadata`, `x-opaque-id`, and any user-defined fields.

### Files Changed

| File | Change |
|------|--------|
| `server/src/main/java/org/opensearch/common/logging/OpenSearchJsonLayout.java` | Wrap `OpenSearchMessageField` values with `%enc{...}{JSON}` |
| `qa/logging-config/src/test/java/org/opensearch/common/logging/OpenSearchJsonLayoutTests.java` | Update expected patterns to include JSON encoding |
| `server/src/test/java/org/opensearch/tasks/consumer/SearchShardTaskDetailsLogMessageTests.java` | Add test for metadata containing nested JSON |

## Limitations

- Only affects JSON-formatted log files. Plain text log files are not impacted.
- Existing malformed log entries from prior versions are not retroactively fixed.

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#20802](https://github.com/opensearch-project/OpenSearch/pull/20802) | Fix JSON escaping in task details log metadata | [#8528](https://github.com/opensearch-project/OpenSearch/issues/8528) |

### Related Issues

| Issue | Description |
|-------|-------------|
| [#8528](https://github.com/opensearch-project/OpenSearch/issues/8528) | [BUG] Invalid JSON events - Task details JSON logs |
