---
tags:
  - opensearch
---
# Dependency Updates

## Summary

OpenSearch v2.19.0 includes 34 dependency updates across OpenSearch core and OpenSearch Dashboards. Key updates include Apache Lucene 9.12.1, Netty 4.1.117.Final, Jackson 2.18.2, and a security fix for CVE-2024-21538 in cross-spawn.

## Details

### What's New in v2.19.0

This release focuses on keeping dependencies current for security, performance, and compatibility.

### Key Updates

| Category | Dependency | Previous | New | PR |
|----------|------------|----------|-----|-----|
| Core | Apache Lucene | 9.12.0 | 9.12.1 | [#16846](https://github.com/opensearch-project/OpenSearch/pull/16846) |
| Networking | Netty | 4.1.114.Final | 4.1.117.Final | [#16661](https://github.com/opensearch-project/OpenSearch/pull/16661) |
| Serialization | Jackson | 2.17.2 | 2.18.2 | [#16733](https://github.com/opensearch-project/OpenSearch/pull/16733) |
| Observability | OpenTelemetry | 1.41.0 | 1.46.0 | [#16700](https://github.com/opensearch-project/OpenSearch/pull/16700) |
| Logging | Log4j Core | 2.24.1 | 2.24.2 | [#16718](https://github.com/opensearch-project/OpenSearch/pull/16718) |
| Logging | Logback Classic | 1.2.13 | 1.5.15 | [#16716](https://github.com/opensearch-project/OpenSearch/pull/16716) |

### Cloud Provider SDKs

| Dependency | Previous | New | PR |
|------------|----------|-----|-----|
| Azure Storage Blob | 12.23.0 | 12.28.1 | [#16501](https://github.com/opensearch-project/OpenSearch/pull/16501) |
| Azure Storage Common | 12.25.1 | 12.28.0 | [#16521](https://github.com/opensearch-project/OpenSearch/pull/16521) |
| Azure Identity | 1.13.2 | 1.14.2 | [#16778](https://github.com/opensearch-project/OpenSearch/pull/16778) |
| Azure Core | 1.51.0 | 1.54.1 | [#16856](https://github.com/opensearch-project/OpenSearch/pull/16856) |
| Azure Core HTTP Netty | 1.15.5 | 1.15.7 | [#16952](https://github.com/opensearch-project/OpenSearch/pull/16952) |
| Google Cloud Core HTTP | 2.23.0 | 2.47.0 | [#16504](https://github.com/opensearch-project/OpenSearch/pull/16504) |
| Google Auth Library | 1.7.0 | 1.29.0 | [#16520](https://github.com/opensearch-project/OpenSearch/pull/16520) |
| Google API Services Compute | v1-rev20240407 | v1-rev20241021 | [#16502](https://github.com/opensearch-project/OpenSearch/pull/16502) |

### Security Updates

| Dependency | Previous | New | PR | CVE |
|------------|----------|-----|-----|-----|
| cross-spawn (Dashboards) | 6.0.5/7.0.3 | 7.0.5 | [#8882](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8882) | CVE-2024-21538 |
| Nimbus JOSE JWT | 9.41.1 | 10.0.1 | [#16611](https://github.com/opensearch-project/OpenSearch/pull/16611) | - |
| Nimbus OAuth2 OIDC SDK | 11.19.1 | 11.21 | [#16895](https://github.com/opensearch-project/OpenSearch/pull/16895) | - |

### Build and Test Dependencies

| Dependency | Previous | New | PR |
|------------|----------|-----|-----|
| Hadoop Minicluster | 3.4.0 | 3.4.1 | [#16550](https://github.com/opensearch-project/OpenSearch/pull/16550) |
| Mockito | 5.14.1 | 5.14.2 | [#16655](https://github.com/opensearch-project/OpenSearch/pull/16655) |
| Objenesis | 3.2 | 3.4 | [#16655](https://github.com/opensearch-project/OpenSearch/pull/16655) |
| Gradle Develocity | 3.18.2 | 3.19 | [#16855](https://github.com/opensearch-project/OpenSearch/pull/16855) |
| Gradle JApiCmp | 0.4.4 | 0.4.5 | [#16614](https://github.com/opensearch-project/OpenSearch/pull/16614) |

### Other Updates

| Dependency | Previous | New | PR |
|------------|----------|-----|-----|
| Snappy Java | 1.1.10.6 | 1.1.10.7 | [#16665](https://github.com/opensearch-project/OpenSearch/pull/16665) |
| XMLBeans | 5.2.1 | 5.3.0 | [#16612](https://github.com/opensearch-project/OpenSearch/pull/16612) |
| JLine | 3.27.1 | 3.28.0 | [#16857](https://github.com/opensearch-project/OpenSearch/pull/16857) |
| Commons Text | 1.12.0 | 1.13.0 | [#16919](https://github.com/opensearch-project/OpenSearch/pull/16919) |
| Commons Lang3 | 3.14.0 | 3.17.0 | [#15580](https://github.com/opensearch-project/OpenSearch/pull/15580) |
| Re2j | 1.7 | 1.8 | [#17012](https://github.com/opensearch-project/OpenSearch/pull/17012) |
| Okio | 3.9.1 | 3.10.2 | [#17060](https://github.com/opensearch-project/OpenSearch/pull/17060) |
| JCodings | 1.0.58 | 1.0.61 | [#17061](https://github.com/opensearch-project/OpenSearch/pull/17061) |
| Logback Core | 1.5.12 | 1.5.16 | [#16951](https://github.com/opensearch-project/OpenSearch/pull/16951) |
| MSAL4J | 1.17.2 | 1.18.0 | [#16918](https://github.com/opensearch-project/OpenSearch/pull/16918) |
| Nebula OSPackage | 11.10.0 | 11.10.1 | [#16896](https://github.com/opensearch-project/OpenSearch/pull/16896) |

### CI/CD Updates

| Tool | Previous | New | PR |
|------|----------|-----|-----|
| Lychee Action | 2.0.2 | 2.2.0 | [#16610](https://github.com/opensearch-project/OpenSearch/pull/16610) |
| Codecov Action | 4 | 5 | [#16667](https://github.com/opensearch-project/OpenSearch/pull/16667) |

## Limitations

- Dependency updates may introduce subtle behavioral changes; review release notes of individual dependencies for details
- Some updates may require plugin recompilation for compatibility

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#16846](https://github.com/opensearch-project/OpenSearch/pull/16846) | Update Apache Lucene to 9.12.1 | opensearch |
| [#16661](https://github.com/opensearch-project/OpenSearch/pull/16661) | Update Netty to 4.1.117.Final | opensearch |
| [#16733](https://github.com/opensearch-project/OpenSearch/pull/16733) | Update Jackson to 2.18.2 | opensearch |
| [#16700](https://github.com/opensearch-project/OpenSearch/pull/16700) | Update OpenTelemetry to 1.46.0 | opensearch |
| [#8882](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8882) | [CVE-2024-21538] Bump cross-spawn to 7.0.5 | opensearch-dashboards |
