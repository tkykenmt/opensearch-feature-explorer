# Dependency Bumps

## Summary

Dependency bumps are routine maintenance updates performed across OpenSearch repositories to keep third-party libraries current, address security vulnerabilities, and maintain compatibility with the latest tooling. These updates are typically automated via Dependabot and reviewed by maintainers.

## Details

### Dependency Update Workflow

```mermaid
flowchart TB
    A[Dependabot Scan] --> B{Security Issue?}
    B -->|Yes| C[Priority Update]
    B -->|No| D[Scheduled Update]
    C --> E[PR Created]
    D --> E
    E --> F[CI Tests]
    F --> G{Tests Pass?}
    G -->|Yes| H[Review & Merge]
    G -->|No| I[Fix Compatibility]
    I --> F
```

### Common Dependency Categories

| Category | Examples | Purpose |
|----------|----------|---------|
| Build Tools | Gradle, Maven plugins | Build automation |
| Testing | JUnit, Mockito | Test frameworks |
| Logging | SLF4J, Log4j | Logging infrastructure |
| Security | Cryptacular, Passay | Security utilities |
| Utilities | Commons CLI, Guava | General utilities |
| Frameworks | Spring | Application framework |

### Dependabot Configuration

Most OpenSearch repositories use Dependabot with configuration in `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "gradle"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
```

### Security-Related Updates

Security-related dependency updates are prioritized and may include:
- CVE fixes in transitive dependencies
- Cryptographic library updates
- Authentication/authorization library patches

## Limitations

- Dependency updates may introduce breaking changes requiring code modifications
- Some updates may be blocked by compatibility requirements with OpenSearch core
- Transitive dependency conflicts may require manual resolution

## Related PRs

### v2.18.0

#### OpenSearch Core
| PR | Description |
|----|-------------|
| [#16254](https://github.com/opensearch-project/OpenSearch/pull/16254) | Fix protobuf-java leak through client library dependencies |

#### Security
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
| [#3083](https://github.com/opensearch-project/ml-commons/pull/3083) | Bump protobuf to 3.25.5 (CVE-2024-7254 fix) |

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

### v2.17.0

#### Job Scheduler
| PR | Description |
|----|-------------|
| [#653](https://github.com/opensearch-project/job-scheduler/pull/653) | Bump org.gradle.test-retry from 1.5.9 to 1.5.10 |
| [#663](https://github.com/opensearch-project/job-scheduler/pull/663) | Bump google-java-format |
| [#666](https://github.com/opensearch-project/job-scheduler/pull/666) | Bump slf4j-api from 2.0.13 to 2.0.16 |
| [#668](https://github.com/opensearch-project/job-scheduler/pull/668) | Bump nebula.ospackage from 11.9.1 to 11.10.0 |

#### Security
| PR | Description |
|----|-------------|
| [#4696](https://github.com/opensearch-project/security/pull/4696) | Bump error_prone_annotations from 2.30.0 to 2.31.0 |
| [#4682](https://github.com/opensearch-project/security/pull/4682) | Bump passay from 1.6.4 to 1.6.5 |
| [#4661](https://github.com/opensearch-project/security/pull/4661) | Bump spring_version from 5.3.37 to 5.3.39 |
| [#4659](https://github.com/opensearch-project/security/pull/4659) | Bump commons-cli from 1.8.0 to 1.9.0 |
| [#4657](https://github.com/opensearch-project/security/pull/4657) | Bump junit-jupiter from 5.10.3 to 5.11.0 |
| [#4656](https://github.com/opensearch-project/security/pull/4656) | Bump cryptacular from 1.2.6 to 1.2.7 |
| [#4646](https://github.com/opensearch-project/security/pull/4646) | Update Gradle to 8.10 |
| [#4639](https://github.com/opensearch-project/security/pull/4639) | Bump snappy-java from 1.1.10.5 to 1.1.10.6 |
| [#4622](https://github.com/opensearch-project/security/pull/4622) | Bump google-java-format from 1.22.0 to 1.23.0 |
| [#4660](https://github.com/opensearch-project/security/pull/4660) | Bump metrics-core from 4.2.26 to 4.2.27 |
| [#4681](https://github.com/opensearch-project/security/pull/4681) | Bump nebula.ospackage from 11.9.1 to 11.10.0 |
| [#4623](https://github.com/opensearch-project/security/pull/4623) | Bump checker-qual from 3.45.0 to 3.46.0 |

## References

- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [CVE-2024-7254](https://nvd.nist.gov/vuln/detail/CVE-2024-7254): Protobuf DOS vulnerability
- [Issue #16253](https://github.com/opensearch-project/OpenSearch/issues/16253): protobuf-java leak bug report
- [Issue #2998](https://github.com/opensearch-project/ml-commons/issues/2998): tribuo-clustering-kmeans vulnerability
- [Job Scheduler Repository](https://github.com/opensearch-project/job-scheduler)
- [Security Plugin Repository](https://github.com/opensearch-project/security)

## Change History

- **v2.18.0** (2024-11-05): 19 dependency updates including CVE-2024-7254 fix (protobuf), Gradle 8.10.2, upload-artifact v4
- **v2.17.0** (2024-09-17): 16 dependency updates across Job Scheduler (4 PRs) and Security (12 PRs) plugins
