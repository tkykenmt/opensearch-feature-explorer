---
tags:
  - domain/core
  - component/server
  - indexing
  - security
---
# HTTP API Improvements

## Summary

OpenSearch v3.0.0 introduces several improvements to HTTP API error handling and configuration. These changes provide more accurate HTTP status codes for various error conditions and increase the default maximum header size to better support modern authentication mechanisms like JWT tokens.

## Details

### What's New in v3.0.0

This release includes four key improvements to the HTTP API layer:

1. **Create Index API Error Code Fix**: Changed HTTP response code from 500 to 400 when invalid input raises `NotXContentException`
2. **Settings Error Messages**: Improved error messages for invalid setting updates by using `SettingsException` instead of `IllegalArgumentException`
3. **Snapshot Conflict Status**: Changed HTTP status from 503 to 409 for concurrent snapshot execution failures
4. **Increased Max Header Size**: Changed default `http.max_header_size` from 8KB to 16KB

### Technical Changes

#### HTTP Status Code Corrections

| Scenario | Before | After | Rationale |
|----------|--------|-------|-----------|
| Create index with invalid content | 500 Internal Server Error | 400 Bad Request | Client error, not server error |
| Invalid settings update | 500 Internal Server Error | 400 Bad Request | Proper `SettingsException` with BAD_REQUEST status |
| Concurrent snapshot execution | 503 Service Unavailable | 409 Conflict | Resource conflict, not service unavailability |

#### New Configuration Default

| Setting | Description | Old Default | New Default |
|---------|-------------|-------------|-------------|
| `http.max_header_size` | Maximum size of HTTP request headers | 8KB | 16KB |

### Usage Example

The increased header size is particularly beneficial for JWT token-based authentication:

```yaml
# opensearch.yml - no change needed for most use cases
# The new default of 16KB accommodates larger JWT tokens

# If you need even larger headers (not recommended):
http.max_header_size: 32kb
```

Example of improved error response for invalid index creation:

```bash
# Before v3.0.0: Returns 500 Internal Server Error
# After v3.0.0: Returns 400 Bad Request
curl -X PUT "localhost:9200/test-index" -H 'Content-Type: application/json' -d'invalid-json'

# Response (v3.0.0):
{
  "error": {
    "root_cause": [{
      "type": "not_x_content_exception",
      "reason": "Compressor detection can only be called on some xcontent bytes or compressed xcontent bytes"
    }],
    "type": "not_x_content_exception",
    "reason": "Compressor detection can only be called on some xcontent bytes or compressed xcontent bytes"
  },
  "status": 400
}
```

### Migration Notes

- **No action required** for most users - these are backward-compatible improvements
- Applications relying on specific HTTP status codes (500, 503) for error handling may need updates
- The increased header size default benefits JWT authentication without configuration changes

## Limitations

- The `http.max_header_size` setting is a node-level setting and requires a node restart to change
- Very large headers (>16KB) still require explicit configuration

## References

### Pull Requests
| PR | Description |
|----|-------------|
| [#4773](https://github.com/opensearch-project/OpenSearch/pull/4773) | Change HTTP code on create index API with bad input from 500 to 400 |
| [#4792](https://github.com/opensearch-project/OpenSearch/pull/4792) | Improve summary error message for invalid setting updates |
| [#8986](https://github.com/opensearch-project/OpenSearch/pull/8986) | Return 409 Conflict instead of 503 for concurrent snapshot execution |
| [#18024](https://github.com/opensearch-project/OpenSearch/pull/18024) | Change default max header size from 8KB to 16KB |

### Issues (Design / RFC)
- [Issue #2756](https://github.com/opensearch-project/OpenSearch/issues/2756): Wrong HTTP code returned from create index API with bad input
- [Issue #4745](https://github.com/opensearch-project/OpenSearch/issues/4745): Update AbstractScopedSettings to throw OpenSearchExceptions
- [Issue #18022](https://github.com/opensearch-project/OpenSearch/issues/18022): Increase http.max_header_size default to 16KB
- [Security Dashboards Plugin Issue #1311](https://github.com/opensearch-project/security-dashboards-plugin/issues/1311): JWT header size issues

## Related Feature Report

- Full feature documentation
