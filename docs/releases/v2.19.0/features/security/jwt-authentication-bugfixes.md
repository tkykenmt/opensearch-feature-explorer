---
tags:
  - security
---
# JWT Authentication Bug Fixes

## Summary

OpenSearch v2.19.0 includes two bug fixes for JWT authentication that improve reliability and reduce log noise in production environments.

## Details

### What's New in v2.19.0

#### Fix: JWT Attribute Parsing of Lists

When JWT claims contain list values (arrays), the previous implementation converted them using Java's `String.valueOf()`, which produced output like `[a, b, c]` without proper JSON quoting. This caused issues when using JWT attributes in Document Level Security (DLS) clauses with the `${attr.jwt.claim}` syntax, as the resulting JSON was invalid.

The fix converts list claims to proper JSON array strings using `DefaultObjectMapper.writeValueAsString()`, producing correctly formatted output like `["a","b","c"]`.

**Affected Components:**
- `HTTPJwtAuthenticator` - Standard JWT authenticator
- `OnBehalfOfAuthenticator` - On-behalf-of token authenticator

**Example:**

Before fix (invalid JSON):
```json
{
  "terms": {
    "group_permissions.keyword": [Ingest Management, Platform Admin]
  }
}
```

After fix (valid JSON):
```json
{
  "terms": {
    "group_permissions.keyword": ["Ingest Management","Platform Admin"]
  }
}
```

#### Fix: Reduced Log Level for JWT Authentication Failures

When multiple JWT authentication domains are configured, a request signed by a non-first issuer would log an ERROR message even though authentication eventually succeeded with a later domain. This created unnecessary noise in production logs.

The fix reduces the log level from ERROR to DEBUG for the message "Failed to parse JWT token using any of the available parsers" (now "Unable to authenticate JWT Token with any configured signing key"). This is expected behavior when multiple auth domains are configured, and a catch-all warning in `BackendRegistry` already handles actual authentication failures.

### Technical Changes

| File | Change |
|------|--------|
| `HTTPJwtAuthenticator.java` | Added Collection type check and JSON serialization for list claims; reduced log level from ERROR to DEBUG |
| `OnBehalfOfAuthenticator.java` | Added Collection type check and JSON serialization for list claims |

## Limitations

- The JSON serialization for list claims adds a small performance overhead
- Mixed-type lists (strings, numbers, nulls) are supported but may produce unexpected results in DLS queries

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#4885](https://github.com/opensearch-project/security/pull/4885) | Fix issue with jwt attribute parsing of lists | [#4267](https://github.com/opensearch-project/security/issues/4267) |
| [#4917](https://github.com/opensearch-project/security/pull/4917) | Reduce log level in HttpJwtAuthenticator if request cannot be authenticated | [#4910](https://github.com/opensearch-project/security/issues/4910) |

### Issues
- [#4267](https://github.com/opensearch-project/security/issues/4267): Bad parsing on DLS custom JWT attribute
- [#4910](https://github.com/opensearch-project/security/issues/4910): Regression in 2.17 - error log on each request when multiple JWT auth domains are configured
