---
tags:
  - domain/security
  - component/server
  - dashboards
  - observability
  - security
---
# Security Dependency Updates

## Summary

OpenSearch v3.1.0 includes 24 dependency updates for the Security plugin and Security Dashboards plugin. These updates address security vulnerabilities (including CVE-2024-52798), improve compatibility with newer library versions, and ensure the security components remain current with upstream dependencies.

## Details

### What's New in v3.1.0

This release focuses on maintaining security and stability through comprehensive dependency updates across both the backend Security plugin and the frontend Security Dashboards plugin.

### Technical Changes

#### Key Dependency Updates

| Category | Dependency | Previous Version | New Version |
|----------|------------|------------------|-------------|
| Cryptography | Bouncy Castle | 1.80 | 1.81 |
| Messaging | Apache Kafka | 3.7.1 | 4.0.0 |
| Framework | Spring | 6.2.5 | 6.2.7 |
| Serialization | Jackson Databind | 2.18.x | 2.19.x |
| Utilities | Google Guava | 33.4.6-jre | 33.4.8-jre |
| Testing | JUnit Jupiter | 5.12.2 | 5.13.1 |
| Testing | Mockito | 5.15.2 | 5.18.0 |
| Bytecode | Byte Buddy | 1.15.11 | 1.17.5 |
| Bytecode | ASM | 9.7.1 | 9.8 |
| Utilities | Commons IO | 2.18.0 | 2.19.0 |
| Utilities | Commons Codec | 1.16.1 | 1.18.0 |
| Utilities | Commons Collections4 | 4.4 | 4.5 |
| Metrics | Dropwizard Metrics | 4.2.30 | 4.2.31 |
| Build | Shadow Plugin | 8.1.7 | 8.1.8 |

#### Security Vulnerability Fixes

- **CVE-2024-52798**: Fixed in Security Dashboards plugin through dev dependency updates ([PR #2231](https://github.com/opensearch-project/security-dashboards-plugin/pull/2231))

#### Major Version Upgrades

1. **Apache Kafka 4.0.0**: Major version upgrade from 3.7.1, requiring test updates to accommodate API changes
2. **Bouncy Castle 1.81**: Updated cryptographic library with latest security patches
3. **JUnit Jupiter 5.13.x**: Testing framework upgrade for improved test capabilities

### Migration Notes

These dependency updates are transparent to users. No configuration changes are required. The updates maintain backward compatibility with existing security configurations.

## Limitations

- Kafka 4.0.0 upgrade required internal test adjustments but does not affect user-facing functionality
- Some dependency updates are automated via Dependabot and follow standard security plugin review processes

## References

### Documentation
- [CVE-2024-52798 Advisory](https://advisories.opensearch.org/advisories/CVE-2024-52798): Security vulnerability fixed in this release
- [Bouncy Castle Release Notes](https://github.com/bcgit/bc-java/blob/main/docs/releasenotes.html): Cryptographic library updates
- [Apache Kafka 4.0.0](https://kafka.apache.org/): Major version upgrade details

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#5380](https://github.com/opensearch-project/security/pull/5380) | security | Bump bouncycastle_version from 1.80 to 1.81 |
| [#5131](https://github.com/opensearch-project/security/pull/5131) | security | Upgrade kafka_version from 3.7.1 to 4.0.0 |
| [#5284](https://github.com/opensearch-project/security/pull/5284) | security | Bump guava from 33.4.6-jre to 33.4.8-jre |
| [#5283](https://github.com/opensearch-project/security/pull/5283) | security | Bump spring_version from 6.2.5 to 6.2.7 |
| [#5285](https://github.com/opensearch-project/security/pull/5285) | security | Bump error_prone_annotations |
| [#5296](https://github.com/opensearch-project/security/pull/5296) | security | Bump mockito-core from 5.15.2 to 5.18.0 |
| [#5294](https://github.com/opensearch-project/security/pull/5294) | security | Bump randomizedtesting-runner |
| [#5293](https://github.com/opensearch-project/security/pull/5293) | security | Bump asm from 9.7.1 to 9.8 |
| [#5295](https://github.com/opensearch-project/security/pull/5295) | security | Bump commons-codec from 1.16.1 to 1.18.0 |
| [#5313](https://github.com/opensearch-project/security/pull/5313) | security | Bump byte-buddy from 1.15.11 to 1.17.5 |
| [#5314](https://github.com/opensearch-project/security/pull/5314) | security | Bump awaitility from 4.2.2 to 4.3.0 |
| [#5315](https://github.com/opensearch-project/security/pull/5315) | security | Bump spring-kafka-test |
| [#5292](https://github.com/opensearch-project/security/pull/5292) | security | Bump jackson-databind |
| [#5316](https://github.com/opensearch-project/security/pull/5316) | security | Bump commons-collections4 from 4.4 to 4.5 |
| [#5330](https://github.com/opensearch-project/security/pull/5330) | security | Bump google-java-format |
| [#5329](https://github.com/opensearch-project/security/pull/5329) | security | Bump shadow plugin from 8.1.7 to 8.1.8 |
| [#5328](https://github.com/opensearch-project/security/pull/5328) | security | Bump commons-io from 2.18.0 to 2.19.0 |
| [#5361](https://github.com/opensearch-project/security/pull/5361) | security | Bump metrics-core from 4.2.30 to 4.2.31 |
| [#5371](https://github.com/opensearch-project/security/pull/5371) | security | Bump junit-jupiter from 5.12.2 to 5.13.1 |
| [#5383](https://github.com/opensearch-project/security/pull/5383) | security | Bump junit-jupiter-api |
| [#5381](https://github.com/opensearch-project/security/pull/5381) | security | Bump checker-qual |
| [#1517](https://github.com/opensearch-project/security/pull/1517) | security | Increment version to 3.1.0-SNAPSHOT |
| [#1301](https://github.com/opensearch-project/security/pull/1301) | security | Increment version to 3.1.0.0 |
| [#2231](https://github.com/opensearch-project/security-dashboards-plugin/pull/2231) | security-dashboards-plugin | Fix CVE-2024-52798 |

## Related Feature Report

- Full feature documentation
