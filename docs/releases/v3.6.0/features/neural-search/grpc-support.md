---
tags:
  - neural-search
---
# gRPC Support

## Summary

Bug fixes for gRPC integration testing in the neural-search plugin and a security policy fix in the OpenSearch core transport-grpc module. These changes add integration tests for Hybrid Query over gRPC, fix port discovery issues in CI and local environments, and resolve a Windows-specific security permission error for Unix domain sockets.

## Details

### What's New in v3.6.0

#### Hybrid Query gRPC Integration Tests (neural-search#1734)

Added end-to-end integration tests for HybridQuery execution over gRPC. The test suite (`HybridQueryGrpcIT`) validates the complete round-trip: client → gRPC → OpenSearch → response, covering:

- Basic hybrid query execution and result verification
- Filter push-down with term and bool filters
- Optional fields: `paginationDepth`, query name, boost validation
- Mixed query types: Term + Match + MatchAll + KNN combinations
- Error handling: max sub-queries exceeded, empty queries, non-default boost

A shared `GrpcTestHelper` utility class provides reusable gRPC channel management, search request builders, and retry logic for transient failures.

Build configuration changes:
- Added gRPC test dependencies (grpc-api, grpc-core, grpc-netty-shaded, grpc-stub, grpc-protobuf)
- Enabled gRPC transport in test clusters via `aux.transport.types` setting

#### gRPC Integration Test Port Discovery Fix (neural-search#1814)

Fixed two failure scenarios for gRPC integration tests:

1. **Local `./gradlew integTest`**: The gRPC transport binds to the first available port in 9400-9500. When port 9400 is occupied (e.g., by VPN) or dual-stack binding shifts the IPv4 port, tests failed because `GrpcTestHelper` hardcoded port 9400. The fix auto-discovers the actual gRPC port from the cluster log file using regex matching on `Netty4GrpcServerTransport` publish address.

2. **Distribution integration tests (external cluster)**: When `tests.rest.cluster` is set, the external cluster may not have gRPC transport configured. The fix adds `GrpcTestHelper.isGrpcTransportConfigured()` to gracefully skip gRPC tests via `assumeTrue()`.

Additional fixes:
- Bind gRPC to IPv4 loopback (`grpc.bind_host=127.0.0.1`) to prevent dual-stack port mismatch where IPv6 takes 9400 and IPv4 gets 9401
- Retry logic (up to 10 attempts) for port discovery to handle race conditions

| Environment | tests.rest.cluster | tests.grpc.port | gRPC tests |
|---|---|---|---|
| Local `./gradlew integTest` | not set | auto-discovered | RUN |
| External cluster without gRPC | set | not set | SKIPPED |
| External cluster with gRPC | set | explicitly passed | RUN |

#### Unix Domain Socket Permission Fix (OpenSearch#20649)

Fixed a Windows-specific `SecurityException` in the transport-grpc module. On Windows, Netty's `WEPollSelectorProvider` creates temporary socket files via `PipeImpl`, which requires `accessUnixDomainSocket` permission. The original fix in OpenSearch#20463 scoped the permission grant to `codeBase "${codebase.grpc-netty-shaded}"`, but this was insufficient. The fix broadens the security policy grant to apply to all code in the transport-grpc module.

Changed in `plugin-security.policy`:
```
// Before
grant codeBase "${codebase.grpc-netty-shaded}" {
// After
grant {
```

### Technical Changes

| Change | File | Description |
|--------|------|-------------|
| New test class | `GrpcTestHelper.java` | Shared gRPC test utilities: channel management, query builders, retry logic |
| New test class | `HybridQueryGrpcIT.java` | 16 integration tests for Hybrid Query over gRPC |
| Port discovery | `build.gradle` | Auto-discover gRPC port from cluster log, bind to IPv4 loopback |
| Skip logic | `GrpcTestHelper.isGrpcTransportConfigured()` | Gracefully skip gRPC tests on external clusters without gRPC |
| Security policy | `plugin-security.policy` | Broaden permission grant for Unix domain socket access on Windows |

## Limitations

- Port discovery relies on parsing cluster log files, which may fail if log format changes
- gRPC tests are automatically skipped on external clusters without explicit `tests.grpc.port` configuration
- The broadened security policy grant in transport-grpc applies to all code rather than specific codebases

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [neural-search#1734](https://github.com/opensearch-project/neural-search/pull/1734) | [GRPC] Add Integration test for Hybrid Query | [neural-search#1723](https://github.com/opensearch-project/neural-search/issues/1723) |
| [neural-search#1814](https://github.com/opensearch-project/neural-search/pull/1814) | Fix gRPC integration test port discovery for reliable local and CI execution | [OpenSearch#21027](https://github.com/opensearch-project/OpenSearch/issues/21027) |
| [OpenSearch#20649](https://github.com/opensearch-project/OpenSearch/pull/20649) | Add `accessUnixDomainSocket` permission for transport-grpc on Windows | [neural-search#1723](https://github.com/opensearch-project/neural-search/issues/1723) |
| [OpenSearch#20463](https://github.com/opensearch-project/OpenSearch/pull/20463) | Initial `accessUnixDomainSocket` permission (scoped to grpc-netty-shaded) | [neural-search#1723](https://github.com/opensearch-project/neural-search/issues/1723) |
