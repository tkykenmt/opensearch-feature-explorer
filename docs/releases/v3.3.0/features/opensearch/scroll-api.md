---
tags:
  - indexing
  - search
---

# Scroll API Error Handling Improvement

## Summary

This release improves error handling for the Scroll API when a scroll ID references a node that is no longer part of the cluster. Previously, this scenario returned an HTTP 500 (Internal Server Error), but now correctly returns an HTTP 400 (Bad Request) with a clear error message indicating the scroll ID is invalid or stale.

## Details

### What's New in v3.3.0

The Scroll API now provides more accurate HTTP status codes and error messages when processing scroll requests with outdated or invalid scroll IDs.

### Technical Changes

#### Error Response Change

| Aspect | Before v3.3.0 | v3.3.0+ |
|--------|---------------|---------|
| Exception Type | `IllegalStateException` | `IllegalArgumentException` |
| HTTP Status | 500 (Internal Server Error) | 400 (Bad Request) |
| Error Message | `node [nodeId] is not available` | `scroll_id references node [nodeId] which was not found in the cluster` |

#### Background

Scroll IDs in OpenSearch are Base64-encoded payloads containing:
- References to target nodes
- Shard-local searcher context IDs

When a client sends a scroll ID referencing a node that no longer exists (due to node replacement, cluster changes, or pointing to a different cluster), the coordinator now correctly identifies this as a client-side issue rather than a server-side error.

### Usage Example

When using an outdated scroll ID:

```json
GET _search/scroll
{
  "scroll": "1m",
  "scroll_id": "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAAUWdmpUZDhnRFBUcWFtV21nMmFwUGJEQQ=="
}
```

If the scroll ID references a node no longer in the cluster, the response is now:

```json
{
  "error": {
    "root_cause": [
      {
        "type": "illegal_argument_exception",
        "reason": "scroll_id references node [node123] which was not found in the cluster"
      }
    ],
    "type": "search_phase_execution_exception",
    "reason": "all shards failed",
    "phase": "query",
    "grouped": true,
    "failed_shards": [
      {
        "reason": {
          "type": "illegal_argument_exception",
          "reason": "scroll_id references node [node123] which was not found in the cluster"
        }
      }
    ]
  },
  "status": 400
}
```

### Migration Notes

- Clients should update error handling logic to expect HTTP 400 instead of HTTP 500 for invalid scroll IDs
- The error message format has changed - update any error parsing logic accordingly
- No changes required for normal scroll operations with valid scroll IDs

## Limitations

- This change only affects the error response when a scroll ID references a missing node
- Other scroll-related errors may still return different HTTP status codes

## References

### Documentation
- [Scroll API Documentation](https://docs.opensearch.org/3.0/api-reference/search-apis/scroll/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#19031](https://github.com/opensearch-project/OpenSearch/pull/19031) | IllegalArgumentException when scroll ID references a node not found in Cluster |

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/opensearch-scroll-api.md)
