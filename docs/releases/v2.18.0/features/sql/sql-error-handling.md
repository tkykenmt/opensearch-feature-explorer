---
tags:
  - domain/search
  - component/server
  - indexing
  - search
  - sql
---
# SQL Error Handling

## Summary

OpenSearch 2.18.0 improves error handling in the SQL plugin for malformed queries and cursors. Previously, certain invalid inputs would return HTTP 500 errors with raw exception messages. This release ensures proper HTTP 400 responses with clear, user-friendly error messages.

## Details

### What's New in v2.18.0

Two categories of error handling improvements were introduced:

1. **Malformed cursor handling**: Invalid pagination cursors now return HTTP 400 with a clear "Malformed cursor" message instead of HTTP 500 with stack traces.

2. **Malformed query handling**: Several edge cases in query parsing now return proper error responses:
   - JOIN queries with invalid ON conditions
   - Subqueries with wildcard indices
   - Non-query SQL expressions

### Technical Changes

#### Components Modified

| Component | Description |
|-----------|-------------|
| `CursorResultExecutor` | Enhanced error handling for cursor parsing failures |
| `OpenSearchActionFactory` | Added validation for SQL expression types |
| `TermFieldRewriter` | Added null checks for table aliases and index mappings |

#### Error Response Format

Before v2.18.0:
```json
{
  "error": {
    "type": "IllegalArgumentException",
    "reason": "java.lang.IllegalArgumentException: ..."
  },
  "status": 500
}
```

After v2.18.0:
```json
{
  "error": {
    "type": "IllegalArgumentException",
    "reason": "Malformed cursor: unable to extract cursor information"
  },
  "status": 400
}
```

### Usage Example

Malformed cursor request:
```bash
POST /_plugins/_sql
{
  "cursor": "d:a11b4db33f"
}
```

Response (v2.18.0+):
```json
{
  "error": {
    "type": "IllegalArgumentException",
    "reason": "Malformed cursor: unable to extract cursor information"
  },
  "status": 400
}
```

### Migration Notes

No migration required. These are backward-compatible improvements to error responses. Applications that rely on specific error status codes should update their error handling to expect HTTP 400 for client errors instead of HTTP 500.

## Limitations

- Error messages are in English only
- Some complex malformed queries may still produce less descriptive error messages

## References

### Documentation
- [SQL and PPL API Documentation](https://docs.opensearch.org/2.18/search-plugins/sql/sql-ppl-api/)
- [SQL Plugin Documentation](https://docs.opensearch.org/2.18/search-plugins/sql/index/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#3066](https://github.com/opensearch-project/sql/pull/3066) | Improve error handling for malformed query cursors |
| [#3080](https://github.com/opensearch-project/sql/pull/3080) | Improve error handling for some more edge cases |
| [#3084](https://github.com/opensearch-project/sql/pull/3084) | Backport #3066 to 2.x |
| [#3112](https://github.com/opensearch-project/sql/pull/3112) | Backport #3080 to 2.18 |

## Related Feature Report

- [Full feature documentation](../../../../features/sql/sql-error-handling.md)
