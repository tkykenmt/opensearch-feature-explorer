---
tags:
  - opensearch
---
# REST High-Level Client Fixes

## Summary

Fixed endpoint path formatting in the deprecated Java REST High-Level Client (RHLC) for `searchTemplate` and `mtermVectors` operations. The endpoints were missing leading slashes, causing HTTP 400 errors when using strict intermediaries like proxies or load balancers.

## Details

### What's New in v2.16.0

The REST High-Level Client had two endpoints that constructed HTTP requests with non-absolute paths (missing leading `/`):

| Endpoint | Before | After |
|----------|--------|-------|
| `_render/template` | `GET _render/template HTTP/1.1` | `GET /_render/template HTTP/1.1` |
| `_mtermvectors` | `GET _mtermvectors HTTP/1.1` | `GET /_mtermvectors HTTP/1.1` |

### Technical Changes

The fix modifies `RequestConverters.java` in the `client/rest-high-level` module:

**searchTemplate endpoint:**
```java
// Before
request = new Request(HttpGet.METHOD_NAME, "_render/template");

// After
request = new Request(HttpGet.METHOD_NAME, "/_render/template");
```

**mtermVectors endpoint:**
```java
// Before
String endpoint = "_mtermvectors";
Request request = new Request(HttpGet.METHOD_NAME, endpoint);

// After
Request request = new Request(HttpGet.METHOD_NAME, "/_mtermvectors");
```

### Impact

- OpenSearch itself is lenient and accepts requests without leading slashes
- Strict HTTP intermediaries (proxies, load balancers) may reject these requests with HTTP 400 Bad Request
- Amazon OpenSearch Service users were particularly affected due to stricter request validation

## Limitations

- The REST High-Level Client is deprecated and will be removed in OpenSearch 3.0.0
- Users should migrate to the [Java client](https://opensearch.org/docs/latest/clients/java/) instead
- A more comprehensive fix in `RestClient` (PR #14423) remains open as a draft

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14465](https://github.com/opensearch-project/OpenSearch/pull/14465) | Correct RHLC searchTemplate & mtermVectors endpoints to have leading slash | Relates to #14423 |
| [#14423](https://github.com/opensearch-project/OpenSearch/pull/14423) | Normalize URI paths in RestClient (draft) | - |

### Documentation
- [Java high-level REST client](https://docs.opensearch.org/2.16/clients/java-rest-high-level/)
