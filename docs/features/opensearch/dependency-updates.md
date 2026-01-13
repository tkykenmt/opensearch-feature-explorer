---
tags:
  - opensearch
---
# Dependency Updates

## Summary

OpenSearch maintains a regular cadence of dependency updates to ensure security, performance, and compatibility. Each release includes updates to core libraries, cloud provider SDKs, build tools, and security-related dependencies.

## Details

### Key Dependencies

OpenSearch relies on several critical dependencies:

| Category | Dependencies |
|----------|-------------|
| Search Engine | Apache Lucene |
| Networking | Netty |
| Serialization | Jackson |
| Observability | OpenTelemetry |
| Logging | Log4j, Logback |
| Cloud Storage | Azure SDK, Google Cloud SDK |
| Security | Nimbus JOSE JWT, OAuth2 OIDC SDK |

### Update Process

Dependency updates follow OpenSearch's contribution guidelines:
1. Create PR with version bump
2. Update checksums and license files
3. Run full test suite
4. Backport to supported branches as needed

## Limitations

- Major version updates may require code changes for API compatibility
- Some dependencies have transitive dependency conflicts that require careful resolution
- Plugin authors should verify compatibility after dependency updates

## Change History

- **v2.19.0** (2025-01-21): 34 dependency updates including Lucene 9.12.1, Netty 4.1.117.Final, Jackson 2.18.2, OpenTelemetry 1.46.0, and CVE-2024-21538 fix for cross-spawn

## References

### Documentation
- [OpenSearch Contributing Guide](https://github.com/opensearch-project/OpenSearch/blob/main/CONTRIBUTING.md)

### Pull Requests

| Version | PR | Description |
|---------|-----|-------------|
| v2.19.0 | [#16846](https://github.com/opensearch-project/OpenSearch/pull/16846) | Update Apache Lucene to 9.12.1 |
| v2.19.0 | [#16661](https://github.com/opensearch-project/OpenSearch/pull/16661) | Update Netty to 4.1.117.Final |
| v2.19.0 | [#16733](https://github.com/opensearch-project/OpenSearch/pull/16733) | Update Jackson to 2.18.2 |
| v2.19.0 | [#16700](https://github.com/opensearch-project/OpenSearch/pull/16700) | Update OpenTelemetry to 1.46.0 |
| v2.19.0 | [#8882](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8882) | [CVE-2024-21538] Bump cross-spawn to 7.0.5 |
