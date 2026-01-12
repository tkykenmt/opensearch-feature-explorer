---
tags:
  - performance
  - security
---

# Dependency Updates (OpenSearch Core)

## Summary

OpenSearch v3.4.0 includes 32 dependency updates for the core engine, covering networking frameworks, cloud SDKs, security libraries, CI/CD tooling, and build dependencies. The most significant update is the Netty 4.2 upgrade, which enables future HTTP/3 support.

## Details

### What's New in v3.4.0

This release focuses on keeping dependencies current with security patches, performance improvements, and compatibility updates.

### Technical Changes

#### Major Framework Updates

| Dependency | Previous | New | Impact |
|------------|----------|-----|--------|
| Netty | 4.1.x | 4.2.4 | HTTP/3 readiness, Project Reactor integration |
| JAXB Implementation | 2.2.3-1 | 4.0.6 | Jakarta EE compatibility |
| Google HTTP Client Gson | 1.47.1 | 2.0.0 | Major version upgrade |

#### Cloud SDK Updates

| Dependency | New Version | Purpose |
|------------|-------------|---------|
| Azure Core HTTP Netty | 1.16.1 | Azure networking |
| Azure Storage Common | 12.30.3 | Azure Blob Storage |
| Microsoft MSAL4J | 1.23.1 | Azure authentication |
| Google Cloud Storage | 2.60.0 | GCS repository |
| Google API Common | 2.55.1 | GCP base APIs |
| Google GAX HTTP JSON | 2.72.1 | GCP HTTP transport |
| Proto Google IAM v1 | 1.57.0 | GCP IAM |

#### Security Library Updates

| Dependency | New Version | Purpose |
|------------|-------------|---------|
| Nimbus JOSE+JWT | 10.6 | JWT token handling |
| Bouncy Castle FIPS | 2.1.2 | FIPS-compliant cryptography |

#### Build & CI Updates

| Dependency | Previous | New | Type |
|------------|----------|-----|------|
| peter-evans/create-or-update-comment | 4 | 5 | GitHub Action |
| peter-evans/create-issue-from-file | 5 | 6 | GitHub Action |
| stefanzweifel/git-auto-commit-action | 6 | 7 | GitHub Action |
| github/codeql-action | 3 | 4 | GitHub Action |
| gradle/actions | 4 | 5 | GitHub Action |
| tj-actions/changed-files | 46.0.5 | 47.0.0 | GitHub Action |
| actions/github-script | 7 | 8 | GitHub Action |
| actions/upload-artifact | 4 | 5 | GitHub Action |

#### Library Updates

| Dependency | New Version | Purpose |
|------------|-------------|---------|
| Apache ZooKeeper | 3.9.4 | Distributed coordination |
| Apache Avro | 1.12.1 | Data serialization |
| Apache Commons Text | 1.14.0 | String utilities |
| Apache Commons CLI | 1.11.0 | CLI parsing |
| Apache Commons Net | 3.12.0 | Network utilities |
| Commons Logging | 1.3.5 | Logging abstraction |
| OkHttp | 5.3.0 | HTTP client |
| Okio | 3.16.3 | I/O library |
| Logback | 1.5.20 | Logging (HDFS fixture) |
| SpotBugs Annotations | 4.9.8 | Static analysis |
| XZ | 1.11 | Compression |

### Netty 4.2 Upgrade Details

The Netty upgrade (PR #19178) is the most significant change:

- Enables Project Reactor integration for reactive streams
- Prepares infrastructure for HTTP/3 support
- Closes long-standing issue [#14804](https://github.com/opensearch-project/OpenSearch/issues/14804)

### Migration Notes

- No breaking changes for users
- Plugin developers using Netty directly should verify compatibility with 4.2.x APIs
- JAXB upgrade may affect plugins using XML binding (Jakarta namespace migration)

## Limitations

- Netty 4.2 is a prerequisite for HTTP/3 but does not enable it in this release
- Some transitive dependencies may have version conflicts requiring resolution

## References

### Documentation
- [Netty 4.2 Release Notes](https://netty.io/news/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#19178](https://github.com/opensearch-project/OpenSearch/pull/19178) | Netty 4.2.4 upgrade |
| [#19472](https://github.com/opensearch-project/OpenSearch/pull/19472) | JAXB 4.0.6 upgrade |
| [#19253](https://github.com/opensearch-project/OpenSearch/pull/19253) | Google HTTP Client Gson 2.0.0 |
| [#19533](https://github.com/opensearch-project/OpenSearch/pull/19533) | Azure Core HTTP Netty 1.16.1 |
| [#19615](https://github.com/opensearch-project/OpenSearch/pull/19615) | Azure Storage Common 12.30.3 |
| [#19688](https://github.com/opensearch-project/OpenSearch/pull/19688) | MSAL4J 1.23.1 |
| [#20023](https://github.com/opensearch-project/OpenSearch/pull/20023) | Google Cloud Storage 2.60.0 |
| [#20084](https://github.com/opensearch-project/OpenSearch/pull/20084) | Nimbus JOSE+JWT 10.6 |
| [#19818](https://github.com/opensearch-project/OpenSearch/pull/19818) | Bouncy Castle FIPS 2.1.2 |
| [#19535](https://github.com/opensearch-project/OpenSearch/pull/19535) | ZooKeeper 3.9.4 |
| [#19692](https://github.com/opensearch-project/OpenSearch/pull/19692) | Avro 1.12.1 |
| [#19614](https://github.com/opensearch-project/OpenSearch/pull/19614) | OkHttp 5.3.0 |
| [#19763](https://github.com/opensearch-project/OpenSearch/pull/19763) | Logback 1.5.20 |
| [#19536](https://github.com/opensearch-project/OpenSearch/pull/19536) | peter-evans/create-or-update-comment v5 |
| [#19785](https://github.com/opensearch-project/OpenSearch/pull/19785) | github/codeql-action v4 |
| [#19781](https://github.com/opensearch-project/OpenSearch/pull/19781) | gradle/actions v5 |

### Issues (Design / RFC)
- [Issue #14804](https://github.com/opensearch-project/OpenSearch/issues/14804): Netty 4.2 upgrade request

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/dependency-management.md)
