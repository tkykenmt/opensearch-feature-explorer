---
tags:
  - domain/infra
  - component/server
  - indexing
  - observability
  - security
  - sql
---
# Dependency Updates

## Summary

OpenSearch v3.4.0 includes 28 dependency updates across 7 repositories (index-management, common-utils, observability, anomaly-detection, reporting, security, sql). These updates address multiple CVEs including CVE-2025-11226 (logback), CVE-2025-58457 and CVE-2025-41249 (Spring Framework/Zookeeper), and include major version bumps for Calcite, Spring Framework, and various security libraries.

## Details

### What's New in v3.4.0

This release focuses on security-critical dependency updates across the OpenSearch plugin ecosystem:

- **Logback updates** to 1.5.19/1.5.20 addressing CVE-2025-11226 (ACE vulnerability in `<if>` condition attribute)
- **Spring Framework upgrade** to 7.0.1 addressing CVE-2025-58457
- **Zookeeper upgrade** to 3.9.4 addressing CVE-2025-41249
- **Apache Calcite** bump to 1.41.0 for SQL plugin

### Technical Changes

#### Security Library Updates

| Library | Previous | New | Repository |
|---------|----------|-----|------------|
| logback-classic | 1.5.18 | 1.5.19/1.5.20 | security, common-utils, index-management |
| logback-core | - | 1.15.20 | observability, reporting |
| springframework | 6.2.x | 7.0.1 | security |
| spring-kafka-test | 4.0.0-M5 | 4.0.0-RC1 | security |
| bouncycastle bcpkix-jdk18on | 1.82 | 1.83 | security |
| nimbus-jose-jwt | 10.5 | 10.6 | security |

#### Build & Test Library Updates

| Library | Previous | New | Repository |
|---------|----------|-----|------------|
| junit-jupiter | 5.13.4 | 5.14.1 | security |
| gradle test-retry | 1.6.2 | 1.6.4 | security |
| spotbugs | 6.4.2 | 6.4.4 | security |
| build-health | 3.0.4 | 3.5.1 | security |
| google-java-format | 1.28.0 | 1.32.0 | security |

#### Runtime Library Updates

| Library | Previous | New | Repository |
|---------|----------|-----|------------|
| Apache Calcite | - | 1.41.0 | sql |
| kafka_version | 4.0.0 | 4.1.1 | security |
| scala-library | 2.13.16 | 2.13.18 | security |
| byte-buddy | 1.17.7 | 1.18.2 | security |
| asm | 9.8 | 9.9 | security |
| checker-qual | 3.51.0 | 3.52.0 | security |
| error_prone_annotations | 2.42.0 | 2.44.0 | security |
| json-path | 2.9.0 | 2.10.0 | security |
| xmlschema-core | 2.3.1 | 2.3.2 | security |
| commons-io | 2.20.0 | 2.21.0 | security |
| commons-validator | 1.10.0 | 1.10.1 | security |
| commons-codec | 1.19.0 | 1.20.0 | security |
| js-yaml | 3.14.1 | 3.14.2 | anomaly-detection |
| zookeeper | - | 3.9.4 | security |

### CVE Fixes

| CVE | Severity | Library | Fix |
|-----|----------|---------|-----|
| CVE-2025-11226 | High | logback | Disallow "new" operator in `<if>` condition attribute |
| CVE-2025-58457 | - | Spring Framework | Upgrade to 7.0.1 |
| CVE-2025-41249 | - | Zookeeper | Upgrade to 3.9.4 |

## Limitations

- Spring Framework 7.0.1 is a major version upgrade that may require testing for compatibility
- Some updates are repository-specific and may not apply to all deployment configurations

## References

### Documentation
- [CVE-2025-11226](https://nvd.nist.gov/vuln/detail/CVE-2025-11226): Logback ACE vulnerability
- [Logback 1.5.19 Release Notes](https://logback.qos.ch/news.html#1.5.19)
- [Apache Calcite 1.41.0 Release](https://calcite.apache.org/docs/history.html)

### Pull Requests
| PR | Title | Repository |
|----|-------|------------|
| [#893](https://github.com/opensearch-project/common-utils/pull/893) | Update logback dependencies to version 1.5.19 | common-utils |
| [#1537](https://github.com/opensearch-project/index-management/pull/1537) | Update logback dependencies to version 1.5.19 | index-management |
| [#1960](https://github.com/opensearch-project/observability/pull/1960) | Bump logback core to 1.15.20 | observability |
| [#1143](https://github.com/opensearch-project/reporting/pull/1143) | Bump logback core to 1.15.20 | reporting |
| [#1121](https://github.com/opensearch-project/anomaly-detection/pull/1121) | Bump js-yaml from 3.14.1 to 3.14.2 | anomaly-detection |
| [#5678](https://github.com/opensearch-project/security/pull/5678) | Bump org.junit.jupiter:junit-jupiter from 5.13.4 to 5.14.1 | security |
| [#5680](https://github.com/opensearch-project/security/pull/5680) | Bump ch.qos.logback:logback-classic from 1.5.18 to 1.5.20 | security |
| [#5682](https://github.com/opensearch-project/security/pull/5682) | Bump org.scala-lang:scala-library from 2.13.16 to 2.13.18 | security |
| [#5613](https://github.com/opensearch-project/security/pull/5613) | Bump kafka_version from 4.0.0 to 4.1.1 | security |
| [#5706](https://github.com/opensearch-project/security/pull/5706) | Bump org.gradle.test-retry from 1.6.2 to 1.6.4 | security |
| [#5705](https://github.com/opensearch-project/security/pull/5705) | Bump org.checkerframework:checker-qual from 3.51.0 to 3.52.0 | security |
| [#5707](https://github.com/opensearch-project/security/pull/5707) | Bump org.ow2.asm:asm from 9.8 to 9.9 | security |
| [#5703](https://github.com/opensearch-project/security/pull/5703) | Bump net.bytebuddy:byte-buddy from 1.17.7 to 1.18.2 | security |
| [#5727](https://github.com/opensearch-project/security/pull/5727) | Bump com.github.spotbugs from 6.4.2 to 6.4.4 | security |
| [#5726](https://github.com/opensearch-project/security/pull/5726) | Bump com.autonomousapps.build-health from 3.0.4 to 3.5.1 | security |
| [#5725](https://github.com/opensearch-project/security/pull/5725) | Bump spring_version from 6.2.11 to 6.2.14 | security |
| [#5742](https://github.com/opensearch-project/security/pull/5742) | Bump org.springframework.kafka:spring-kafka-test from 4.0.0-M5 to 4.0.0-RC1 | security |
| [#5743](https://github.com/opensearch-project/security/pull/5743) | Bump com.google.errorprone:error_prone_annotations from 2.42.0 to 2.44.0 | security |
| [#5741](https://github.com/opensearch-project/security/pull/5741) | Bump com.google.googlejavaformat:google-java-format from 1.28.0 to 1.32.0 | security |
| [#5767](https://github.com/opensearch-project/security/pull/5767) | Bump com.jayway.jsonpath:json-path from 2.9.0 to 2.10.0 | security |
| [#5781](https://github.com/opensearch-project/security/pull/5781) | Bump org.apache.ws.xmlschema:xmlschema-core from 2.3.1 to 2.3.2 | security |
| [#5780](https://github.com/opensearch-project/security/pull/5780) | Bump commons-io:commons-io from 2.20.0 to 2.21.0 | security |
| [#5782](https://github.com/opensearch-project/security/pull/5782) | Bump com.nimbusds:nimbus-jose-jwt from 10.5 to 10.6 | security |
| [#5807](https://github.com/opensearch-project/security/pull/5807) | Bump commons-validator:commons-validator from 1.10.0 to 1.10.1 | security |
| [#5825](https://github.com/opensearch-project/security/pull/5825) | Bump org.bouncycastle:bcpkix-jdk18on from 1.82 to 1.83 | security |
| [#5823](https://github.com/opensearch-project/security/pull/5823) | Bump commons-codec:commons-codec from 1.19.0 to 1.20.0 | security |
| [#5829](https://github.com/opensearch-project/security/pull/5829) | Upgrade springframework to 7.0.1 and zookeeper to 3.9.4 | security |
| [#4714](https://github.com/opensearch-project/sql/pull/4714) | Bump Calcite to 1.41.0 | sql |

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch-dashboards-dependency-updates.md)
