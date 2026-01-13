---
tags:
  - opensearch
---
# GetStats API

## Summary

The `GetStats` class provides statistics about document retrieval ("get") operations in OpenSearch. It is part of the Index Stats API response and tracks metrics such as total get operations, time spent, and counts for existing vs. missing documents.

## Details

### Overview

When you retrieve a document by ID using the Get Document API, OpenSearch tracks statistics about these operations. The `GetStats` class aggregates these metrics and exposes them through the Index Stats API (`GET /<index>/_stats/get`).

### Response Fields

| Field | Description |
|-------|-------------|
| `total` | Total number of get operations |
| `time` | Human-readable time spent on get operations (when `?human` is enabled) |
| `time_in_millis` | Time spent on get operations in milliseconds |
| `exists_total` | Number of successful get operations (document found) |
| `exists_time` | Human-readable time for successful gets |
| `exists_time_in_millis` | Time for successful gets in milliseconds |
| `missing_total` | Number of get operations where document was not found |
| `missing_time` | Human-readable time for missing document gets |
| `missing_time_in_millis` | Time for missing document gets in milliseconds |
| `current` | Number of get operations currently in progress |

### Usage Example

```bash
# Get stats for all indexes
GET /_stats/get

# Get stats for a specific index with human-readable values
GET /my-index/_stats/get?human

# Filter response to show only get stats
GET /my-index/_stats?human&filter_path=_all.primaries.get
```

**Example Response:**
```json
{
  "_all": {
    "primaries": {
      "get": {
        "total": 100,
        "time": "50ms",
        "time_in_millis": 50,
        "exists_total": 95,
        "exists_time": "45ms",
        "exists_time_in_millis": 45,
        "missing_total": 5,
        "missing_time": "5ms",
        "missing_time_in_millis": 5,
        "current": 0
      }
    }
  }
}
```

## Limitations

- Statistics are reset when a shard moves to a different node
- The deprecated `getTime` field (present in versions prior to v2.19.0) will be removed in a future major version

## Change History

- **v2.19.0** (2025-01-17): Added new `time` field and deprecated `getTime` field to fix naming inconsistency ([#17009](https://github.com/opensearch-project/OpenSearch/pull/17009))

## References

### Documentation

- [Index Stats API](https://docs.opensearch.org/latest/api-reference/index-apis/stats/)

### Pull Requests

| Version | PR | Description |
|---------|-----|-------------|
| v2.19.0 | [#17009](https://github.com/opensearch-project/OpenSearch/pull/17009) | Fix getTime field name to time in GetStats |
