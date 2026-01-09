# OpenSearch Core Dependencies

## Summary

OpenSearch v2.18.0 includes 26 dependency updates across core libraries, security components, and build tooling. Key updates include Apache Lucene 9.12.0, Netty 4.1.114.Final, gRPC 1.68.0, and Protobuf 3.25.5, bringing performance improvements, security patches, and compatibility enhancements.

## Details

### What's New in v2.18.0

This release focuses on keeping OpenSearch dependencies current with upstream projects, addressing security vulnerabilities, and ensuring compatibility with modern tooling.

### Technical Changes

#### Core Library Updates

| Library | Previous Version | New Version | Impact |
|---------|------------------|-------------|--------|
| Apache Lucene | 9.11.1 | 9.12.0 | Search engine improvements |
| Netty | 4.1.112.Final | 4.1.114.Final | Network layer stability |
| Protobuf | 3.22.3 → 3.25.4 | 3.25.5 | Serialization updates |
| gRPC API | 1.57.2 | 1.68.0 | RPC framework updates |
| Log4j Core | 2.23.1 | 2.24.0 | Logging improvements |

#### Security & Authentication Libraries

| Library | Previous Version | New Version |
|---------|------------------|-------------|
| Azure Identity | 1.13.0 | 1.13.2 |
| Azure Core HTTP Netty | 1.15.3 | 1.15.5 |
| Azure JSON | 1.1.0 | 1.3.0 |
| MSAL4J | 1.17.0 | 1.17.2 |
| OAuth2 OIDC SDK | 11.9.1 | 11.19.1 |
| Nimbus JOSE JWT | 9.40 | 9.41.1 |

#### Google Cloud & API Libraries

| Library | Previous Version | New Version |
|---------|------------------|-------------|
| Google API Client | 2.2.0 | 2.7.0 |
| Google OAuth Client | 1.35.0 | 1.36.0 |
| Gson | 2.10.1 | 2.11.0 |

#### Utility Libraries

| Library | Previous Version | New Version |
|---------|------------------|-------------|
| RoaringBitmap | 1.2.1 | 1.3.0 |
| JLine | 3.26.3 | 3.27.0 |
| Logback Core | 1.5.6 | 1.5.10 |
| DNSJava | 3.6.1 | 3.6.2 |
| MaxMind GeoIP2 | 4.2.0 | 4.2.1 |
| MaxMind DB | 3.1.0 | 3.1.1 |
| Okio | 3.9.0 | 3.9.1 |

#### Build & CI Tools

| Tool | Previous Version | New Version |
|------|------------------|-------------|
| peter-evans/create-pull-request | 6 | 7 |
| actions/github-script | 5 | 7 |
| lycheeverse/lychee-action | 1.10.0 | 2.0.2 |
| japicmp Gradle plugin | 0.4.3 | 0.4.4 |

### Key Highlights

#### Apache Lucene 9.12.0
The Lucene upgrade brings search engine improvements including better query performance and index handling. See the [Lucene 9.12.0 changelog](https://lucene.apache.org/core/9_12_0/changes/Changes.html) for details.

#### Netty 4.1.114.Final
Network layer updates improve stability and performance for HTTP and transport communications.

#### gRPC 1.68.0
Major gRPC update with improvements to load balancing, xDS support, and OpenTelemetry tracing integration.

#### Protobuf 3.25.5
Updated serialization library with bug fixes and performance improvements.

### Migration Notes

These are internal dependency updates. No user-facing configuration changes are required. Plugin developers should verify compatibility if directly depending on any updated libraries.

## Limitations

- Some dependency updates may affect plugin compatibility if plugins directly depend on specific library versions
- The Lucene upgrade requires index compatibility verification for custom analyzers

## Related PRs

| PR | Description |
|----|-------------|
| [#15333](https://github.com/opensearch-project/OpenSearch/pull/15333) | Update Apache Lucene to 9.12.0 |
| [#16182](https://github.com/opensearch-project/OpenSearch/pull/16182) | Bump Netty to 4.1.114.Final |
| [#16213](https://github.com/opensearch-project/OpenSearch/pull/16213) | Bump gRPC API from 1.57.2 to 1.68.0 |
| [#15684](https://github.com/opensearch-project/OpenSearch/pull/15684) | Update protobuf from 3.22.3 to 3.25.4 |
| [#16011](https://github.com/opensearch-project/OpenSearch/pull/16011) | Update protobuf from 3.25.4 to 3.25.5 |
| [#15858](https://github.com/opensearch-project/OpenSearch/pull/15858) | Bump Log4j Core from 2.23.1 to 2.24.0 |
| [#15578](https://github.com/opensearch-project/OpenSearch/pull/15578) | Bump Azure Identity from 1.13.0 to 1.13.2 |
| [#15862](https://github.com/opensearch-project/OpenSearch/pull/15862) | Bump OAuth2 OIDC SDK from 11.9.1 to 11.19.1 |
| [#15945](https://github.com/opensearch-project/OpenSearch/pull/15945) | Bump MSAL4J from 1.17.0 to 1.17.2 |
| [#15946](https://github.com/opensearch-project/OpenSearch/pull/15946) | Bump Logback Core from 1.5.6 to 1.5.10 |
| [#16040](https://github.com/opensearch-project/OpenSearch/pull/16040) | Bump RoaringBitmap from 1.2.1 to 1.3.0 |
| [#16038](https://github.com/opensearch-project/OpenSearch/pull/16038) | Bump Nimbus JOSE JWT from 9.40 to 9.41.1 |
| [#16041](https://github.com/opensearch-project/OpenSearch/pull/16041) | Bump DNSJava from 3.6.1 to 3.6.2 |
| [#16042](https://github.com/opensearch-project/OpenSearch/pull/16042) | Bump GeoIP2 from 4.2.0 to 4.2.1 |
| [#16137](https://github.com/opensearch-project/OpenSearch/pull/16137) | Bump MaxMind DB from 3.1.0 to 3.1.1 |
| [#16133](https://github.com/opensearch-project/OpenSearch/pull/16133) | Bump Azure Core HTTP Netty from 1.15.3 to 1.15.5 |
| [#16216](https://github.com/opensearch-project/OpenSearch/pull/16216) | Bump Google API Client from 2.2.0 to 2.7.0 |
| [#16217](https://github.com/opensearch-project/OpenSearch/pull/16217) | Bump Azure JSON from 1.1.0 to 1.3.0 |
| [#16135](https://github.com/opensearch-project/OpenSearch/pull/16135) | Bump JLine from 3.26.3 to 3.27.0 |
| [#16212](https://github.com/opensearch-project/OpenSearch/pull/16212) | Bump Okio from 3.9.0 to 3.9.1 |
| [#16308](https://github.com/opensearch-project/OpenSearch/pull/16308) | Bump Gson from 2.10.1 to 2.11.0 |
| [#16306](https://github.com/opensearch-project/OpenSearch/pull/16306) | Bump Google OAuth Client from 1.35.0 to 1.36.0 |
| [#15863](https://github.com/opensearch-project/OpenSearch/pull/15863) | Bump peter-evans/create-pull-request from 6 to 7 |
| [#16039](https://github.com/opensearch-project/OpenSearch/pull/16039) | Bump actions/github-script from 5 to 7 |
| [#16310](https://github.com/opensearch-project/OpenSearch/pull/16310) | Bump lycheeverse/lychee-action from 1.10.0 to 2.0.2 |
| [#16309](https://github.com/opensearch-project/OpenSearch/pull/16309) | Bump japicmp Gradle plugin from 0.4.3 to 0.4.4 |

## References

- [Apache Lucene 9.12.0 Changes](https://lucene.apache.org/core/9_12_0/changes/Changes.html)
- [Netty Releases](https://github.com/netty/netty/releases)
- [gRPC Java Releases](https://github.com/grpc/grpc-java/releases)

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/opensearch-core-dependencies.md)
