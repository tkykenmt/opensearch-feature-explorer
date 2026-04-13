---
tags:
  - opensearch
---
# Request Tracing

## Summary

In v3.6.0, the `X-Request-Id` header validation was relaxed to accept any non-empty string up to a configurable maximum length, replacing the previous strict requirement of exactly 32 hexadecimal characters. A new dynamic cluster setting `http.request_id.max_length` allows operators to configure the maximum allowed length.

## Details

### What's New in v3.6.0

Previously (v3.5.0), the `X-Request-Id` header required exactly 32 hexadecimal characters (`[0-9a-fA-F]{32}`). This was overly restrictive for real-world use cases where gateways, load balancers, and observability tools emit request IDs in various formats (UUIDs with dashes, ULIDs, base64url tokens, vendor-specific IDs).

v3.6.0 removes the format restriction entirely and replaces it with a simple length check:
- The header must be non-empty and non-blank
- The header length must not exceed `http.request_id.max_length`

### Configuration

| Setting | Description | Default | Min | Max | Scope |
|---------|-------------|---------|-----|-----|-------|
| `http.request_id.max_length` | Maximum allowed length for `X-Request-Id` header values | 128 | 16 | 1024 | Dynamic, Node |

The setting is dynamic and can be updated at runtime via the Cluster Settings API:

```json
PUT /_cluster/settings
{
  "transient": {
    "http.request_id.max_length": 256
  }
}
```

### Technical Changes

The validation logic in `RequestUtils.validateRequestId()` was simplified:

Before (v3.5.0):
```java
// Required exactly 32 hex characters
if (requestId.length() != 32) { throw ... }
for (char c : requestId) {
    if (!isHexDigit(c)) { throw ... }
}
```

After (v3.6.0):
```java
// Only checks non-empty and max length
if (requestId == null || requestId.isBlank()) { throw ... }
if (requestId.length() > maxLength) { throw ... }
```

Key implementation details:
- `HttpTransportSettings.SETTING_HTTP_REQUEST_ID_MAX_LENGTH` defines the setting with `Setting.Property.Dynamic` and `Setting.Property.NodeScope`
- `RestController` holds a `volatile int requestIdMaxLength` field, updated via `ClusterSettings.addSettingsUpdateConsumer()`
- The max length is passed to `RequestUtils.validateRequestId()` at request time

### Accepted Request ID Formats

| Format | Example | v3.5.0 | v3.6.0 |
|--------|---------|--------|--------|
| 32-char hex | `a1b2c3d4e5f67890abcdef1234567890` | ✅ | ✅ |
| UUID with dashes | `a1b2c3d4-e5f6-7890-abcd-ef1234567890` | ❌ | ✅ |
| ULID | `01ARZ3NDEKTSV4RRFFQ69G5FAV` | ❌ | ✅ |
| Short alphanumeric | `req-12345` | ❌ | ✅ |
| Base64url token | `dGhpcyBpcyBhIHRlc3Q` | ❌ | ✅ |

### Error Response

When a request ID exceeds the configured maximum length, the server returns HTTP 400:

```
X-Request-Id length [256] exceeds maximum allowed length [128]
```

## Limitations

- No minimum length enforcement beyond non-empty/non-blank
- No character set validation — any printable characters are accepted
- The default max length changed from an implicit 32 (exact match) to 128, which is a behavioral change for existing deployments

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| `https://github.com/opensearch-project/OpenSearch/pull/21048` | Remove X-Request-Id format restrictions and make size configurable | `https://github.com/opensearch-project/OpenSearch/issues/20688` |
| `https://github.com/opensearch-project/OpenSearch/pull/21096` | Backport to 3.6 branch | - |
