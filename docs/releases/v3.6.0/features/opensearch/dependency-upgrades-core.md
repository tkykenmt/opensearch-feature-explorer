---
tags:
  - opensearch
---
# Dependency Upgrades (Core)

## Summary

OpenSearch v3.6.0 includes 15 dependency upgrades across the core engine, covering critical libraries such as Apache Lucene, Netty, Jackson, and OpenTelemetry. These updates bring bug fixes, security patches, and performance improvements to the underlying platform.

## Details

### What's New in v3.6.0

The following core dependencies were upgraded:

| Dependency | Previous Version | New Version | Category |
|-----------|-----------------|-------------|----------|
| Apache Lucene | 10.3.2 | 10.4.0 | Search engine |
| Netty | 4.2.10.Final | 4.2.12.Final | Networking |
| Jackson | — | 2.21.2 | JSON processing |
| OpenTelemetry | — | 1.60.1 | Observability |
| OpenTelemetry Semconv | — | 1.40.0 | Observability |
| Project Reactor | 3.8.2 | 3.8.4 | Reactive streams |
| Reactor Netty | 1.3.2 | 1.3.4 | Reactive networking |
| Logback Classic | — | 1.5.32 | Logging |
| Logback Core | 1.5.24 | 1.5.27 | Logging |
| Nimbus JOSE+JWT | 10.7 | 10.8 | Security/JWT |
| JAXB Impl | 4.0.6 | 4.0.7 | XML binding |
| Nebula ospackage-base | 12.2.0 | 12.3.0 | Packaging |
| Commons Text | 1.14.0 | 1.15.0 | Text utilities |
| JLine | 3.30.6 | 4.0.0 | Terminal I/O |
| JCodings | 1.0.63 | 1.0.64 | Character encoding |
| Joni | 2.2.3 | 2.2.7 | Regex engine |
| XZ | 1.11 | 1.12 | Compression |
| Shadow Gradle Plugin | 8.3.9 | 9.3.1 | Build tooling |

### Technical Changes

#### Apache Lucene 10.3.2 → 10.4.0
The most significant upgrade. Lucene is the core search library underlying OpenSearch. The 10.4.0 release was merged from the `feature/3.x-lucene` branch, indicating coordinated integration work.

#### Jackson → 2.21.2 (Security Fix)
This update addresses security advisory GHSA-72hv-8253-57qq. The Jackson upgrade was also backported to the 3.5 branch, indicating the security fix was considered critical.

#### Shadow Gradle Plugin 8.3.9 → 9.3.1
A major version bump for the build tooling plugin. This required coordinated changes across multiple plugin repositories including job-scheduler, security, alerting, common-utils, index-management, and notifications.

#### Logback Core 1.5.24 → 1.5.27
Includes a fix for CVE-2026-1225 (ACE vulnerability in configuration file processing), MDC data transmission fix for SocketAppender, and license update to Eclipse Public License 2.0.

#### Nimbus JOSE+JWT 10.7 → 10.8
Fixes `getDeferredCriticalHeaderParams()` in multiple decrypter and verifier implementations, and adds `PasswordBasedDecrypter` constructor for specifying critical header parameters.

#### XZ 1.11 → 1.12
Fixes `ArrayIndexOutOfBoundsException` in the LZMA/LZMA2 encoder on x86-64 and ARM64 when running on Java 9+, and fixes ArrayCache usage in LZMAInputStream.

#### JLine 3.30.6 → 4.0.0
A major version bump. JLine 4.0.0 requires Java 11+ (up from Java 8), removes JNA provider, and adds JPMS support. Used in the HDFS test fixture.

#### Joni 2.2.3 → 2.2.7
Fixes multiplex backreferences near end of string in regexp match. Used by the Grok pattern matching library.

#### JCodings 1.0.63 → 1.0.64
Adds Unicode 17.0.0 support. Used by the Grok library for character encoding.

## References

### Pull Requests
| PR | Description |
|----|-------------|
| https://github.com/opensearch-project/OpenSearch/pull/20735 | Bump Apache Lucene from 10.3.2 to 10.4.0 |
| https://github.com/opensearch-project/OpenSearch/pull/20586 | Update Netty to 4.2.12.Final |
| https://github.com/opensearch-project/OpenSearch/pull/20989 | Update Jackson to 2.21.2 |
| https://github.com/opensearch-project/OpenSearch/pull/20737 | Bump OpenTelemetry to 1.60.1 and Semconv to 1.40.0 |
| https://github.com/opensearch-project/OpenSearch/pull/20589 | Bump Project Reactor to 3.8.4 and Reactor Netty to 1.3.4 |
| https://github.com/opensearch-project/OpenSearch/pull/20525 | Bump logback-classic to 1.5.32 and logback-core to 1.5.27 |
| https://github.com/opensearch-project/OpenSearch/pull/20715 | Bump nimbus-jose-jwt from 10.7 to 10.8 |
| https://github.com/opensearch-project/OpenSearch/pull/20886 | Bump jaxb-impl from 4.0.6 to 4.0.7 |
| https://github.com/opensearch-project/OpenSearch/pull/20799 | Bump ospackage-base from 12.2.0 to 12.3.0 |
| https://github.com/opensearch-project/OpenSearch/pull/20576 | Bump commons-text from 1.14.0 to 1.15.0 |
| https://github.com/opensearch-project/OpenSearch/pull/20800 | Bump jline from 3.30.6 to 4.0.0 |
| https://github.com/opensearch-project/OpenSearch/pull/20713 | Bump jcodings from 1.0.63 to 1.0.64 |
| https://github.com/opensearch-project/OpenSearch/pull/20714 | Bump joni from 2.2.3 to 2.2.7 |
| https://github.com/opensearch-project/OpenSearch/pull/20760 | Bump xz from 1.11 to 1.12 |
| https://github.com/opensearch-project/OpenSearch/pull/20569 | Bump shadow-gradle-plugin from 8.3.9 to 9.3.1 |

### Security Advisories
- GHSA-72hv-8253-57qq (Jackson)
- CVE-2026-1225 (Logback)
