---
tags:
  - opensearch
---
# Platform & Distribution

## Summary

OpenSearch v3.6.0 includes platform and distribution improvements that expand multi-architecture support and fix several cross-platform compatibility issues. Docker builds now support ppc64le, arm64, and s390x architectures. The S3 repository plugin gracefully falls back to Netty when the AWS CRT client is unavailable. HTTP/3 detection is hardened to check Quic native library availability. Additional fixes address cgroups security policy expansion, SLF4J version mismatch, Windows service startup with OpenJDK, and ThreadContext header propagation during context restore.

## Details

### What's New in v3.6.0

#### Docker Multi-Architecture Support
The Dockerfile now maps additional architectures to the correct `tini` binary:
- `ppc64le` → `tini-ppc64le`
- `arm64` → `tini-arm64`
- `s390x` → `tini-s390x`

Previously, only `aarch64` and `x86_64` were supported in Docker builds.

#### AWS CRT Client Fallback
A new `AwsCrtUtils` utility class (`org.opensearch.repositories.s3.utils.AwsCrtUtils`) detects whether the AWS CRT native library is available on the current platform by calling `CRT.getArchIdentifier()`. When the CRT client is unavailable (e.g., on ppc64le or s390x), the S3 async service (`S3AsyncService.buildHttpClient()`) automatically falls back to the Netty HTTP client instead of throwing an `UnknownPlatformException`.

#### Hardened HTTP/3 Support Detection
`Http3Utils` now checks `Quic.isAvailable()` in addition to the HTTP/3 codec class presence. On platforms where the Quic native library (`libnetty_quiche*`) is not available (e.g., ppc64le), HTTP/3 is correctly reported as unavailable rather than failing at runtime with `FileNotFoundException` or `UnsatisfiedLinkError`.

#### Cgroups Hierarchy Override Security Fix
The `PolicyFile` class in the agent security manager now supports `${opensearch.cgroups.hierarchy.override}` placeholder expansion in security policy files. When `opensearch.cgroups.hierarchy.override` is set (e.g., `/test`), the corresponding cgroup file permissions are dynamically resolved:
```
/sys/fs/cgroup/${opensearch.cgroups.hierarchy.override}/memory.max → /sys/fs/cgroup/test/memory.max
```
This eliminates the `SecurityException` that previously occurred when using a custom cgroup hierarchy.

#### SLF4J Version Mismatch Fix
The `slf4j-api` was upgraded to version 2.x, but the Log4j binding remained at `log4j-slf4j-impl` (for SLF4J 1.x). This caused SLF4J component initialization errors. The fix switches the binding to `log4j-slf4j2-impl` across multiple modules:
- `client/rest`
- `plugins/repository-hdfs`
- `plugins/repository-s3`
- `qa/wildfly`

#### Windows Service Startup Fix
Updated Apache Commons Daemon procrun binaries (`opensearch-service-x64.exe`, `opensearch-service-mgr.exe`) from an older version to 1.5.1. The previous version failed to start the OpenSearch service on Windows when using OpenJDK.

#### ThreadContext Transient Header Preservation
`ThreadContext.newStoredContext()` now accepts a `preserveTransients` parameter. When enabled, propagator-declared transient headers (e.g., `CURRENT_SPAN` from the tracing infrastructure) are merged back into the restored context rather than being silently dropped. Additionally, `ThreadContextBasedTracerContextStorage.transients()` now checks for null spans within `SpanReference` to prevent propagation of stale span references from thread reuse.

### Technical Changes

| Area | Change | Files Modified |
|------|--------|----------------|
| Docker | Added ppc64le, arm64, s390x tini mappings | `distribution/docker/src/docker/Dockerfile` |
| S3 Plugin | AWS CRT availability check + Netty fallback | `S3AsyncService.java`, new `AwsCrtUtils.java` |
| HTTP/3 | Added `Quic.isAvailable()` check | `Http3Utils.java` |
| Security Policy | Cgroups hierarchy override expansion | `PolicyFile.java`, `security.policy` |
| Logging | SLF4J 2.x binding migration | Multiple `build.gradle` files |
| Windows | Updated procrun to 1.5.1 | `opensearch-service-x64.exe`, `opensearch-service-mgr.exe` |
| ThreadContext | Transient header preservation on restore | `ThreadContext.java`, `ThreadContextBasedTracerContextStorage.java` |

## Limitations

- AWS CRT fallback logs a warning but does not expose the fallback status via API
- HTTP/3 Quic native libraries remain unavailable on ppc64le and s390x
- The cgroups hierarchy override requires the system property to be set via `OPENSEARCH_JAVA_OPTS`

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#20678](https://github.com/opensearch-project/OpenSearch/pull/20678) | Support Docker distribution builds for ppc64le, arm64, and s390x | - |
| [#20698](https://github.com/opensearch-project/OpenSearch/pull/20698) | Fallback to Netty HTTP client when AWS CRT is unavailable | - |
| [#20565](https://github.com/opensearch-project/OpenSearch/pull/20565) | Fix SecurityException with cgroups hierarchy override | [#20522](https://github.com/opensearch-project/OpenSearch/issues/20522) |
| [#20587](https://github.com/opensearch-project/OpenSearch/pull/20587) | Fix SLF4J component error from version mismatch | [#20579](https://github.com/opensearch-project/OpenSearch/issues/20579) |
| [#20615](https://github.com/opensearch-project/OpenSearch/pull/20615) | Fix Windows service startup with OpenJDK | [#19141](https://github.com/opensearch-project/OpenSearch/issues/19141) |
| [#20680](https://github.com/opensearch-project/OpenSearch/pull/20680) | Harden HTTP/3 support detection for Quic availability | - |
| [#20854](https://github.com/opensearch-project/OpenSearch/pull/20854) | Ensure transient ThreadContext headers survive restore | [security#5990](https://github.com/opensearch-project/security/issues/5990) |
