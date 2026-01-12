# Dependency Updates

## Summary

OpenSearch v2.18.0 includes 19 dependency updates across 8 repositories, addressing security vulnerabilities (CVE-2024-7254, CVE-2024-47554) and upgrading build tools. Key updates include Gradle 8.10.2, protobuf-java security patches, and GitHub Actions artifact upload improvements.

## Details

### What's New in v2.18.0

This release focuses on security patches and build infrastructure modernization across the OpenSearch ecosystem.

### Security Fixes

| CVE | Severity | Component | Fix |
|-----|----------|-----------|-----|
| CVE-2024-7254 | High (7.5) | protobuf-java | Bump to 3.25.5 in ml-commons |
| CVE-2024-47554 | - | commons-io | Addressed in security plugin |
| - | - | dompurify | Bump to 3.0.11 in reporting |

### Build Tool Updates

| Component | Previous | New | Repositories |
|-----------|----------|-----|--------------|
| Gradle | Various | 8.10.2 | common, job, security |
| upload-artifact | v2/v3 | v4 | notifications, index-management |
| google-java-format | 1.2x | Latest | job, security |

### Dependency Updates by Repository

#### OpenSearch Core
| PR | Description |
|----|-------------|
| [#16254](https://github.com/opensearch-project/OpenSearch/pull/16254) | Fix protobuf-java leak through client library dependencies |

The protobuf-java dependency was unintentionally exposed through client library dependencies since the introduction of extensions support. This fix removes the unnecessary transitive dependency from client libraries.

#### Security Plugin
| PR | Description |
|----|-------------|
| [#4829](https://github.com/opensearch-project/security/pull/4829) | Bump Gradle to 8.10.2 |
| [#4807](https://github.com/opensearch-project/security/pull/4807) | Bump logback-classic 1.5.8 → 1.5.11 |
| [#4824](https://github.com/opensearch-project/security/pull/4824) | Bump passay 1.6.5 → 1.6.6 |
| [#4767](https://github.com/opensearch-project/security/pull/4767) | Bump junit-jupiter 5.11.0 → 5.11.2 |
| [#4789](https://github.com/opensearch-project/security/pull/4789) | Bump metrics-core 4.2.27 → 4.2.28 |
| [#4737](https://github.com/opensearch-project/security/pull/4737) | Bump nimbus-jose-jwt 9.40 → 9.41.2 |
| [#4788](https://github.com/opensearch-project/security/pull/4788) | Bump asm 9.7 → 9.7.1 |
| [#4786](https://github.com/opensearch-project/security/pull/4786) | Bump google-java-format |

#### ML Commons
| PR | Description |
|----|-------------|
| [#3083](https://github.com/opensearch-project/ml-commons/pull/3083) | Bump protobuf to 3.25.5 to patch CVE-2024-7254 DOS vulnerability |

This addresses a high-severity vulnerability in protobuf-java (transitive dependency of tribuo-clustering-kmeans) that could cause stack overflow through malicious Protocol Buffers data with deeply nested groups.

#### Job Scheduler
| PR | Description |
|----|-------------|
| [#679](https://github.com/opensearch-project/job-scheduler/pull/679) | Bump org.gradle.test-retry 1.5.10 → 1.6.0 |
| [#684](https://github.com/opensearch-project/job-scheduler/pull/684) | Bump google-java-format |
| [#688](https://github.com/opensearch-project/job-scheduler/pull/688) | Gradle 8.10.2 + JDK 23 CI checks |

#### Common Utils
| PR | Description |
|----|-------------|
| [#746](https://github.com/opensearch-project/common-utils/pull/746) | Update Gradle to 8.10.2 |

#### Notifications
| PR | Description |
|----|-------------|
| [#264](https://github.com/opensearch-project/notifications/pull/264) | Upgrade upload-artifact to v4 |

#### Reporting
| PR | Description |
|----|-------------|
| [#462](https://github.com/opensearch-project/reporting/pull/462) | Bump dompurify to 3.0.11 (CVE fix) |

#### OpenSearch Dashboards
| PR | Description |
|----|-------------|
| [#450](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/450) | Bump actions/upload-artifact |
| [#449](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/449) | Update to latest SVG |

#### Index Management
| PR | Description |
|----|-------------|
| [#1252](https://github.com/opensearch-project/index-management/pull/1252) | Upgrade upload-artifact to version 3 |

## Limitations

- Protobuf version bump in ml-commons may require testing K-Means clustering functionality
- Gradle 8.10.2 requires JDK 17+ for builds

## References

### Documentation
- [CVE-2024-7254](https://nvd.nist.gov/vuln/detail/CVE-2024-7254): Protobuf DOS vulnerability
- [GHSA-735f-pc8j-v9w8](https://github.com/advisories/GHSA-735f-pc8j-v9w8): GitHub Security Advisory

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#16254](https://github.com/opensearch-project/OpenSearch/pull/16254) | OpenSearch | Fix protobuf-java client leak |
| [#3083](https://github.com/opensearch-project/ml-commons/pull/3083) | ml-commons | CVE-2024-7254 fix |
| [#4829](https://github.com/opensearch-project/security/pull/4829) | security | Gradle 8.10.2 |
| [#746](https://github.com/opensearch-project/common-utils/pull/746) | common-utils | Gradle 8.10.2 |
| [#688](https://github.com/opensearch-project/job-scheduler/pull/688) | job-scheduler | Gradle 8.10.2 + JDK 23 |

### Issues (Design / RFC)
- [Issue #16253](https://github.com/opensearch-project/OpenSearch/issues/16253): protobuf-java leak bug report
- [Issue #2998](https://github.com/opensearch-project/ml-commons/issues/2998): tribuo-clustering-kmeans vulnerability

## Related Feature Report

- [Full feature documentation](../../../../features/multi-plugin/dependency-updates.md)
