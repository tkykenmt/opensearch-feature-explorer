---
tags:
  - security
---
# Security Netty

## Summary

Bug fixes for the Security plugin's Netty4 HTTP request handling and test infrastructure improvements in v2.19.0.

## Details

### What's New in v2.19.0

#### Netty4 Header Verifier Fix

The `Netty4HttpRequestHeaderVerifier` class was updated to handle HTTP upgrade requests properly. The handler now extends `SimpleChannelInboundHandler<HttpRequest>` instead of `SimpleChannelInboundHandler<DefaultHttpRequest>`, allowing it to process all HTTP request types including upgrade requests.

**Technical Change:**
```java
// Before (v2.18.x)
public class Netty4HttpRequestHeaderVerifier extends SimpleChannelInboundHandler<DefaultHttpRequest>

// After (v2.19.0)
public class Netty4HttpRequestHeaderVerifier extends SimpleChannelInboundHandler<HttpRequest>
```

This fix is a follow-up to PR #5035 which addressed Apache HttpClient5/HttpCore5 compatibility issues after the library update in OpenSearch core.

#### Test Infrastructure Improvements

- Updated `RestHelper` test class to use `DefaultClientTlsStrategy` instead of the deprecated `ClientTlsStrategyBuilder`
- Simplified TLS configuration in tests by removing custom `TlsDetailsFactory`
- Added JaCoCo code coverage report generation for the `integTestRemote` task

### Technical Changes

| Component | Change |
|-----------|--------|
| `Netty4HttpRequestHeaderVerifier` | Changed generic type from `DefaultHttpRequest` to `HttpRequest` |
| `RestHelper` | Migrated from `ClientTlsStrategyBuilder` to `DefaultClientTlsStrategy` |
| `build.gradle` | Added `jacocoTestReport` finalization for `integTestRemote` task |

## Limitations

- These are internal implementation changes with no user-facing configuration changes

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#5045](https://github.com/opensearch-project/security/pull/5045) | Fix Netty4 header verifier inbound handler to deal with upgrade requests | Follow-up to [#5035](https://github.com/opensearch-project/security/pull/5035) |
| [#5050](https://github.com/opensearch-project/security/pull/5050) | Generate jacoco report for integTestRemote task | Backport of [#5049](https://github.com/opensearch-project/security/pull/5049) |
| [#5035](https://github.com/opensearch-project/security/pull/5035) | Fix tests after Apache HttpClient5/HttpCore5 update | Related to [OpenSearch#16757](https://github.com/opensearch-project/OpenSearch/pull/16757) |
