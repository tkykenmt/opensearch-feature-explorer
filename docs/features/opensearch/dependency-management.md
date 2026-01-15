---
tags:
  - opensearch
---
# Dependency Management

## Summary

OpenSearch maintains a comprehensive set of third-party dependencies that are regularly updated to ensure security, performance, and compatibility. This document tracks major dependency categories and their update history.

## Details

### Dependency Categories

| Category | Key Libraries | Purpose |
|----------|---------------|---------|
| Networking | Netty, Commons Net | Network I/O, protocol handling |
| JSON Processing | Jackson, JSON Smart | Serialization/deserialization |
| Security | Nimbus JOSE+JWT, MSAL4J | JWT handling, authentication |
| Azure Integration | Azure SDK components | Cloud storage, identity |
| Observability | OpenTelemetry | Tracing, metrics |
| Build | Gradle plugins | Build tooling |
| Testing | WireMock | HTTP mocking |
| Configuration | Commons Configuration2 | Configuration management |
| Templating | Mustache | Template rendering |
| Reactive | Reactor | Reactive streams |

### Configuration

Dependencies are managed through Gradle build files. Version constraints are typically defined in:
- `buildSrc/version.properties`
- `gradle/libs.versions.toml`
- Individual module `build.gradle` files

## Limitations

- Dependency updates may introduce subtle behavioral changes
- Custom plugins should verify compatibility after OpenSearch upgrades
- Some dependencies have transitive dependency implications

## Change History

- **v2.16.0** (2024-08-06): Updated 16 core dependencies including Netty 4.1.111.Final, Jackson 2.17.2, OpenTelemetry 1.40.0, and Azure SDK components

## References

### Documentation
- [OpenSearch Contributing Guide](https://github.com/opensearch-project/OpenSearch/blob/main/CONTRIBUTING.md)

### Pull Requests
| Version | PR | Description |
|---------|-----|-------------|
| v2.16.0 | [#14356](https://github.com/opensearch-project/OpenSearch/pull/14356) | Bump netty from 4.1.110.Final to 4.1.111.Final |
| v2.16.0 | [#14457](https://github.com/opensearch-project/OpenSearch/pull/14457) | Bump OpenTelemetry from 1.36.0 to 1.40.0 |
| v2.16.0 | [#14687](https://github.com/opensearch-project/OpenSearch/pull/14687) | Bump jackson from 2.17.1 to 2.17.2 |
