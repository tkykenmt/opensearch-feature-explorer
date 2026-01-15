---
tags:
  - opensearch
---
# Dependency Bumps (Core)

## Summary

OpenSearch v2.16.0 includes 16 dependency updates for core libraries, improving security, performance, and compatibility with upstream projects.

## Details

### What's New in v2.16.0

The following dependencies were updated:

| Category | Dependency | From | To | PR |
|----------|------------|------|----|----|
| Networking | Netty | 4.1.110.Final | 4.1.111.Final | [#14356](https://github.com/opensearch-project/OpenSearch/pull/14356) |
| Testing | WireMock | 3.3.1 | 3.6.0 | [#14361](https://github.com/opensearch-project/OpenSearch/pull/14361) |
| Reactive | Reactor | 3.5.17 | 3.5.19 | [#14395](https://github.com/opensearch-project/OpenSearch/pull/14395) |
| Networking | Commons Net | 3.10.0 | 3.11.1 | [#14396](https://github.com/opensearch-project/OpenSearch/pull/14396) |
| Security | Nimbus JOSE+JWT | 9.37.3 | 9.40 | [#14398](https://github.com/opensearch-project/OpenSearch/pull/14398) |
| Configuration | Commons Configuration2 | 2.10.1 | (updated) | [#14399](https://github.com/opensearch-project/OpenSearch/pull/14399) |
| Build | Gradle Develocity | 3.17.4 | 3.17.5 | [#14397](https://github.com/opensearch-project/OpenSearch/pull/14397) |
| Telemetry | OpenTelemetry | 1.36.0 | 1.40.0 | [#14457](https://github.com/opensearch-project/OpenSearch/pull/14457) |
| Telemetry | OpenTelemetry Semconv | 1.25.0-alpha | 1.26.0-alpha | [#14674](https://github.com/opensearch-project/OpenSearch/pull/14674) |
| Azure | Azure Identity | 1.11.4 | 1.13.0 | [#14506](https://github.com/opensearch-project/OpenSearch/pull/14506) |
| Azure | Azure Storage Common | 12.21.2 | 12.25.x | [#14517](https://github.com/opensearch-project/OpenSearch/pull/14517) |
| Azure | MSAL4J | 1.15.1 | 1.16.0 | [#14610](https://github.com/opensearch-project/OpenSearch/pull/14610) |
| Templating | Mustache Compiler | 0.9.1x | (updated) | [#14672](https://github.com/opensearch-project/OpenSearch/pull/14672) |
| JSON | Accessors Smart | 2.5.0 | 2.5.1 | [#14673](https://github.com/opensearch-project/OpenSearch/pull/14673) |
| JSON | Jackson | 2.17.1 | 2.17.2 | [#14687](https://github.com/opensearch-project/OpenSearch/pull/14687) |
| JSON | JSON Smart | 2.5.0 | 2.5.1 | [#14748](https://github.com/opensearch-project/OpenSearch/pull/14748) |

### Key Updates

**Networking & Transport**
- Netty 4.1.111.Final brings bug fixes and performance improvements for network I/O
- Commons Net 3.11.1 includes FTP/SFTP protocol improvements

**Observability**
- OpenTelemetry 1.40.0 is a significant update from 1.36.0, providing improved tracing and metrics capabilities
- OpenTelemetry Semantic Conventions updated to align with latest standards

**Azure Integration**
- Azure SDK components updated for improved cloud storage and authentication support
- MSAL4J update improves Microsoft authentication library compatibility

**Security**
- Nimbus JOSE+JWT 9.40 includes security fixes and JWT handling improvements

**JSON Processing**
- Jackson 2.17.2 provides JSON serialization bug fixes
- JSON Smart and Accessors Smart minor version updates

## Limitations

- These are routine dependency updates with no breaking changes expected
- Users should verify compatibility if using custom plugins that depend on these libraries

## References

### Pull Requests
| PR | Description |
|----|-------------|
| [#14356](https://github.com/opensearch-project/OpenSearch/pull/14356) | Bump netty from 4.1.110.Final to 4.1.111.Final |
| [#14361](https://github.com/opensearch-project/OpenSearch/pull/14361) | Bump wiremock-standalone from 3.3.1 to 3.6.0 |
| [#14395](https://github.com/opensearch-project/OpenSearch/pull/14395) | Bump reactor from 3.5.17 to 3.5.19 |
| [#14396](https://github.com/opensearch-project/OpenSearch/pull/14396) | Bump commons-net from 3.10.0 to 3.11.1 |
| [#14397](https://github.com/opensearch-project/OpenSearch/pull/14397) | Bump Gradle Develocity from 3.17.4 to 3.17.5 |
| [#14398](https://github.com/opensearch-project/OpenSearch/pull/14398) | Bump nimbus-jose-jwt from 9.37.3 to 9.40 |
| [#14399](https://github.com/opensearch-project/OpenSearch/pull/14399) | Bump commons-configuration2 from 2.10.1 |
| [#14457](https://github.com/opensearch-project/OpenSearch/pull/14457) | Bump OpenTelemetry from 1.36.0 to 1.40.0 |
| [#14506](https://github.com/opensearch-project/OpenSearch/pull/14506) | Bump azure-identity from 1.11.4 to 1.13.0 |
| [#14517](https://github.com/opensearch-project/OpenSearch/pull/14517) | Bump azure-storage-common from 12.21.2 to 12.25.x |
| [#14610](https://github.com/opensearch-project/OpenSearch/pull/14610) | Bump msal4j from 1.15.1 to 1.16.0 |
| [#14672](https://github.com/opensearch-project/OpenSearch/pull/14672) | Bump mustache compiler |
| [#14673](https://github.com/opensearch-project/OpenSearch/pull/14673) | Bump accessors-smart from 2.5.0 to 2.5.1 |
| [#14674](https://github.com/opensearch-project/OpenSearch/pull/14674) | Bump opentelemetry-semconv from 1.25.0-alpha to 1.26.0-alpha |
| [#14687](https://github.com/opensearch-project/OpenSearch/pull/14687) | Bump jackson from 2.17.1 to 2.17.2 |
| [#14748](https://github.com/opensearch-project/OpenSearch/pull/14748) | Bump json-smart from 2.5.0 to 2.5.1 |
