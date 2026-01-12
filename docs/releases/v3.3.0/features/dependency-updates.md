---
tags:
  - dashboards
  - k-nn
  - observability
  - performance
  - security
---

# Dependency Updates

## Summary

OpenSearch v3.3.0 includes 55 dependency updates across multiple repositories (OpenSearch, OpenSearch Dashboards, anomaly-detection, k-nn, and job-scheduler). These updates address security vulnerabilities (CVEs), replace deprecated libraries, and upgrade to newer versions of core dependencies for improved stability and performance.

## Details

### What's New in v3.3.0

This release focuses on three key areas:

1. **Security Fixes**: Multiple CVE patches for cryptographic and form handling libraries
2. **Library Modernization**: Migration from deprecated libraries to maintained alternatives
3. **Version Upgrades**: Major updates to observability, logging, and cloud SDK dependencies

### Technical Changes

#### Security Vulnerability Fixes

| CVE | Library | Old Version | New Version | Repository |
|-----|---------|-------------|-------------|------------|
| CVE-2025-54988 | Apache Tika | 2.9.2 | 3.2.2 | OpenSearch |
| CVE-2025-6545 | pbkdf2 | 3.1.2 | 3.1.3 | OpenSearch Dashboards |
| CVE-2025-7783 | form-data | - | 4.0.4 | OpenSearch Dashboards |
| GHSA-cpq7-6gpm-g9rc | cipher-base | 1.0.4 | 1.0.6 | OpenSearch Dashboards |
| GHSA-cpq7-6gpm-g9rc | sha.js | 2.4.11 | 2.4.12 | OpenSearch Dashboards |

#### Library Modernization

| Change | Old Library | New Library | Reason |
|--------|-------------|-------------|--------|
| commons-lang migration | commons-lang:commons-lang | org.apache.commons:commons-lang3 | Original library no longer maintained |

#### Major Version Upgrades

| Category | Library | Old Version | New Version |
|----------|---------|-------------|-------------|
| Observability | OpenTelemetry | - | 1.53.0 |
| Observability | OpenTelemetry SemConv | - | 1.34.0 |
| Logging | SLF4J | 1.7.36 | 2.0.17 |
| Cloud Storage | Google Cloud Storage SDK | 1.113.1 | 2.55.0 |
| Networking | Netty | 4.1.121.Final | 4.1.125.Final |
| Cryptography | Bouncy Castle (all modules) | 2.0.x | 2.1.x |
| gRPC | io.grpc dependencies | 1.68.2 | 1.75.0 |

#### Build & CI Updates

| Tool | Old Version | New Version |
|------|-------------|-------------|
| actions/checkout | 4 | 5 |
| actions/setup-java | 4 | 5 |
| actions/download-artifact | 4 | 5 |
| actions/github-script | 7 | 8 |
| actions/stale | 9 | 10 |
| aws-actions/configure-aws-credentials | 4 | 5 |
| 1password/load-secrets-action | 2 | 3 |
| lycheeverse/lychee-action | 2.4.1 | 2.6.1 |
| shadow-gradle-plugin | 8.3.5 | 8.3.9 |

### Migration Notes

#### SLF4J 2.x Migration
The upgrade from SLF4J 1.7.x to 2.0.x is a major version change. Key considerations:
- SLF4J 2.0 requires Java 8+ (already satisfied by OpenSearch)
- The `StaticLoggerBinder` mechanism is replaced with `ServiceLoader`
- Existing logging configurations should continue to work

#### commons-lang3 Migration
Code using `org.apache.commons.lang` package must be updated to use `org.apache.commons.lang3`:
- Package name change: `org.apache.commons.lang.*` → `org.apache.commons.lang3.*`
- Most APIs remain compatible

#### Bouncy Castle 2.1.x
The Bouncy Castle upgrade includes security improvements:
- `bouncycastle_jce`: 2.0.0 → 2.1.1
- `bouncycastle_tls`: 2.0.20 → 2.1.20
- `bouncycastle_pkix`: 2.0.8 → 2.1.9
- `bouncycastle_pg`: 2.0.11 → 2.1.11
- `bouncycastle_util`: 2.0.3 → 2.1.4

## Limitations

- Some dependency updates required resolution overrides in package.json for transitive dependencies (cipher-base, sha.js)
- The hadoop-minicluster dependency required explicit exclusions for commons-lang and org.jsonschema2pojo

## References

### Documentation
- [CVE-2025-54988](https://nvd.nist.gov/vuln/detail/CVE-2025-54988): Apache Tika vulnerability
- [GHSA-cpq7-6gpm-g9rc](https://github.com/advisories/GHSA-cpq7-6gpm-g9rc): cipher-base/sha.js vulnerability
- [commons-lang deprecation notice](https://mvnrepository.com/artifact/commons-lang/commons-lang)

### Pull Requests
| PR | Description |
|----|-------------|
| [#19068](https://github.com/opensearch-project/OpenSearch/pull/19068) | Update OpenTelemetry to 1.53.0 |
| [#19125](https://github.com/opensearch-project/OpenSearch/pull/19125) | Bump tika from 2.9.2 to 3.2.2 (CVE-2025-54988) |
| [#19136](https://github.com/opensearch-project/OpenSearch/pull/19136) | Bump slf4j from 1.7.36 to 2.0.17 |
| [#18922](https://github.com/opensearch-project/OpenSearch/pull/18922) | Bump GCS SDK to 2.55.0 |
| [#19229](https://github.com/opensearch-project/OpenSearch/pull/19229) | Replace commons-lang with commons-lang3 |
| [#19103](https://github.com/opensearch-project/OpenSearch/pull/19103) | Bump netty from 4.1.121.Final to 4.1.125.Final |
| [#19222](https://github.com/opensearch-project/OpenSearch/pull/19222) | Bump reactor-netty and Bouncy Castle modules |
| [#19495](https://github.com/opensearch-project/OpenSearch/pull/19495) | Bump io.grpc deps from 1.68.2 to 1.75.0 |
| PR | Description |
|----|-------------|
| [#10378](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10378) | CVE-2025-6545/CVE-2025-7783: Bump pbkdf2, form-data |
| [#10442](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10442) | Fix GHSA-cpq7-6gpm-g9rc: cipher-base, sha.js |
| PR | Repository | Description |
|----|------------|-------------|
| [#2863](https://github.com/opensearch-project/k-nn/pull/2863) | k-nn | Replace commons-lang with commons-lang3 |
| [#2833](https://github.com/opensearch-project/k-nn/pull/2833) | k-nn | Bump OpenSearch-Protobufs to 0.13.0 |
| [#1094](https://github.com/opensearch-project/anomaly-detection/pull/1094) | anomaly-detection | Bump axios from 1.8.2 to 1.12.1 |
| [#1084](https://github.com/opensearch-project/anomaly-detection/pull/1084) | anomaly-detection | Bump cipher-base from 1.0.4 to 1.0.6 |
| [#1085](https://github.com/opensearch-project/anomaly-detection/pull/1085) | anomaly-detection | Bump sha.js from 2.4.11 to 2.4.12 |

## Related Feature Report

- [Full feature documentation](../../features/dependency-updates.md)
