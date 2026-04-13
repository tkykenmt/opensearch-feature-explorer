---
tags:
  - security
---
# Security Plugin Dependencies

## Summary

The OpenSearch Security plugin maintains a set of third-party dependencies that provide essential functionality for security operations, including cryptography, compression, logging, I/O operations, messaging, and build tooling. Regular updates to these dependencies ensure security, stability, and compatibility.

## Details

### Core Dependencies

| Dependency | Purpose | Category |
|------------|---------|----------|
| Bouncy Castle | Cryptographic operations | Runtime |
| Apache Kafka | Messaging and audit logging | Runtime |
| Spring Framework | Application framework | Runtime |
| Jackson | JSON serialization | Runtime |
| Google Guava | Core utilities | Runtime |
| snappy-java | Fast compression/decompression | Runtime |
| commons-io | File and stream I/O utilities | Runtime |
| commons-codec | Encoding/decoding utilities | Runtime |
| commons-collections4 | Collection utilities | Runtime |
| scala-library | Scala runtime support | Runtime |
| logback-classic | Logging framework | Runtime |
| checker-qual | Static analysis annotations | Build |
| gradle.test-retry | Flaky test retry | Build |
| JUnit Jupiter | Testing framework | Test |
| Mockito | Mocking framework | Test |
| Byte Buddy | Bytecode manipulation | Test |
| ASM | Bytecode analysis | Test |

### Dependency Categories

#### Runtime Dependencies
These libraries are required at runtime for the Security plugin to function:

- **Bouncy Castle**: Cryptographic provider for TLS, encryption, and certificate operations
- **Apache Kafka**: Messaging system used for audit logging and event streaming
- **Spring Framework**: Application framework for dependency injection and configuration
- **Jackson**: JSON processing library for serialization/deserialization
- **Google Guava**: Core utility library providing collections, caching, and primitives
- **snappy-java**: Provides fast compression/decompression algorithms used for data serialization
- **commons-io**: Apache Commons I/O library for file operations and stream handling
- **commons-codec**: Encoding/decoding utilities for Base64, Hex, and other formats
- **commons-collections4**: Extended collection implementations and utilities
- **scala-library**: Scala standard library required for Scala-based components
- **logback-classic**: SLF4J-compatible logging implementation

#### Test Dependencies
These libraries are used for testing:

- **JUnit Jupiter**: Modern testing framework for unit and integration tests
- **Mockito**: Mocking framework for creating test doubles
- **Byte Buddy**: Runtime bytecode generation for mocking
- **ASM**: Bytecode manipulation and analysis framework
- **Awaitility**: DSL for asynchronous testing

#### Build Dependencies
These libraries are used during the build process:

- **checker-qual**: Annotations for the Checker Framework static analysis tool
- **gradle.test-retry**: Gradle plugin that automatically retries failed tests to handle flaky tests
- **Shadow Plugin**: Gradle plugin for creating fat JARs
- **Google Java Format**: Code formatting tool

### Update Process

Dependency updates in the Security plugin follow this process:

1. Dependabot or maintainers identify available updates
2. Updates are first applied to the `main` branch
3. Backport PRs are created for the `2.x` branch
4. CI tests verify compatibility
5. Updates are merged after review

## Limitations

- Dependency updates may require coordination with OpenSearch core version requirements
- Some dependencies have transitive dependencies that must also be compatible

## Change History

- **v3.6.0** (2026-04-08): 30 dependency updates including Kafka 4.2.0, OpenSAML 5.2.1, Spring 7.0.6, nimbus-jose-jwt 10.8 (critical header params fix), ipaddress 5.6.2, Gradle 9.4.0, and CI actions updates (download-artifact v8, upload-artifact v7, configure-aws-credentials v6)
- **v3.3.0** (2026-01-14): Security fix for CVE-2025-53864 (nimbus-jose-jwt), plus 24 dependency updates including Spring 6.2.11, JJWT 0.13.0, Guava 33.5.0, and CI tooling updates
- **v3.1.0** (2025-06-03): Major dependency updates including Bouncy Castle 1.81, Kafka 4.0.0, Spring 6.2.7, Guava 33.4.8, JUnit 5.13.1, and CVE-2024-52798 fix
- **v3.0.0** (2025-02-25): 13 dependency updates including Spring 6.2.5, Bouncy Castle 1.80, OpenSAML 5.1.4/9.1.4, ASM 9.8, Commons IO 2.19.0, JUnit Jupiter 5.12.2
- **v2.19.0** (2024-12-10): Security fixes for Cypress and cross-spawn dependencies
- **v2.18.0** (2024-10-22): Updated snappy-java, gradle.test-retry, commons-io, scala-library, checker-qual, and logback-classic
- **v2.16.0** (2024-07-23): 7 dependency updates including Spring 5.3.37, JJWT 0.12.6 (memory leak fix), Kafka 3.7.1, JUnit Jupiter 5.10.3, woodstox-core 6.7.0, checker-qual 3.45.0, eclipse.core.runtime 3.31.100


## References

### Documentation
- [OpenSearch Security Repository](https://github.com/opensearch-project/security)
- [OpenSearch Security Dashboards Plugin](https://github.com/opensearch-project/security-dashboards-plugin)
- [CVE-2025-53864 Advisory](https://github.com/advisories/GHSA-xwmg-2g98-w7v9)
- [CVE-2024-52798 Advisory](https://advisories.opensearch.org/advisories/CVE-2024-52798)
- [Bouncy Castle](https://www.bouncycastle.org/)
- [Apache Kafka](https://kafka.apache.org/)
- [snappy-java](https://github.com/xerial/snappy-java)
- [Apache Commons IO](https://commons.apache.org/proper/commons-io/)
- [Scala Library](https://www.scala-lang.org/)
- [Logback](https://logback.qos.ch/)

### Pull Requests
| Version | PR | Description | Related Issue |
|---------|-----|-------------|---------------|
| v3.6.0 | [#6030](https://github.com/opensearch-project/security/pull/6030) | Bump nimbus-jose-jwt 10.7 → 10.8 | |
| v3.6.0 | [#5965](https://github.com/opensearch-project/security/pull/5965) | Bump open_saml_version 5.1.6 → 5.2.1 | |
| v3.6.0 | [#5982](https://github.com/opensearch-project/security/pull/5982) | Bump open_saml_shib_version 9.2.0 → 9.2.1 | |
| v3.6.0 | [#5968](https://github.com/opensearch-project/security/pull/5968) | Bump kafka_version 4.1.1 → 4.2.0 | |
| v3.6.0 | [#5957](https://github.com/opensearch-project/security/pull/5957) | Bump spring_version 7.0.3 → 7.0.4 | |
| v3.6.0 | [#5967](https://github.com/opensearch-project/security/pull/5967) | Bump spring_version 7.0.4 → 7.0.5 | |
| v3.6.0 | [#6008](https://github.com/opensearch-project/security/pull/6008) | Bump spring_version 7.0.5 → 7.0.6 | |
| v3.6.0 | [#5949](https://github.com/opensearch-project/security/pull/5949) | Bump ipaddress 5.5.1 → 5.6.1 | |
| v3.6.0 | [#6010](https://github.com/opensearch-project/security/pull/6010) | Bump ipaddress 5.6.1 → 5.6.2 | |
| v3.6.0 | [#5994](https://github.com/opensearch-project/security/pull/5994) | Bump lz4-java 1.10.3 → 1.10.4 | |
| v3.6.0 | [#5948](https://github.com/opensearch-project/security/pull/5948) | Bump logback-classic 1.5.26 → 1.5.28 | |
| v3.6.0 | [#5995](https://github.com/opensearch-project/security/pull/5995) | Bump logback-classic 1.5.28 → 1.5.32 | |
| v3.6.0 | [#5978](https://github.com/opensearch-project/security/pull/5978) | Bump jakarta.xml.bind-api 4.0.4 → 4.0.5 | |
| v3.6.0 | [#5996](https://github.com/opensearch-project/security/pull/5996) | Bump Gradle Wrapper 9.2.0 → 9.4.0 | |
| v3.6.0 | [#5947](https://github.com/opensearch-project/security/pull/5947) | Bump google-java-format 1.33.0 → 1.34.1 | |
| v3.6.0 | [#6011](https://github.com/opensearch-project/security/pull/6011) | Bump google-java-format 1.34.1 → 1.35.0 | |
| v3.6.0 | [#6029](https://github.com/opensearch-project/security/pull/6029) | Bump build-health 3.5.1 → 3.6.1 | |
| v3.6.0 | [#5955](https://github.com/opensearch-project/security/pull/5955) | Bump checker-qual 3.53.0 → 3.53.1 | |
| v3.6.0 | [#6009](https://github.com/opensearch-project/security/pull/6009) | Bump checker-qual 3.53.1 → 3.54.0 | |
| v3.6.0 | [#6027](https://github.com/opensearch-project/security/pull/6027) | Bump eclipse.core.runtime 3.34.100 → 3.34.200 | |
| v3.6.0 | [#5979](https://github.com/opensearch-project/security/pull/5979) | Bump actions/download-artifact 7 → 8 | |
| v3.6.0 | [#5980](https://github.com/opensearch-project/security/pull/5980) | Bump actions/upload-artifact 6 → 7 | |
| v3.6.0 | [#5946](https://github.com/opensearch-project/security/pull/5946) | Bump aws-actions/configure-aws-credentials 5 → 6 | |
| v3.6.0 | [#6007](https://github.com/opensearch-project/security/pull/6007) | Bump release-drafter/release-drafter 6 → 7 | |
| v3.6.0 | [#6012](https://github.com/opensearch-project/security/pull/6012) | Bump byte-buddy 1.18.4 → 1.18.7 | |
| v3.6.0 | [#5993](https://github.com/opensearch-project/security/pull/5993) | Bump randomizedtesting-runner 2.8.3 → 2.8.4 | |
| v3.6.0 | [#5956](https://github.com/opensearch-project/security/pull/5956) | Bump junit-jupiter-api 5.14.2 → 5.14.3 | |
| v3.6.0 | [#5981](https://github.com/opensearch-project/security/pull/5981) | Bump spring-kafka-test 4.0.2 → 4.0.3 | |
| v3.6.0 | [#6026](https://github.com/opensearch-project/security/pull/6026) | Bump spring-kafka-test 4.0.3 → 4.0.4 | |
| v3.3.0 | [#5595](https://github.com/opensearch-project/security/pull/5595) | Upgrade nimbus-jose-jwt 9.48 → 10.4.2 (CVE-2025-53864) | [#5593](https://github.com/opensearch-project/security/issues/5593) |
| v3.3.0 | [#5629](https://github.com/opensearch-project/security/pull/5629) | Bump nimbus-jose-jwt 10.4.2 → 10.5 |   |
| v3.3.0 | [#5568](https://github.com/opensearch-project/security/pull/5568) | Bump jjwt_version 0.12.6 → 0.13.0 |   |
| v3.3.0 | [#5569](https://github.com/opensearch-project/security/pull/5569) | Bump spring_version 6.2.9 → 6.2.11 |   |
| v3.3.0 | [#5567](https://github.com/opensearch-project/security/pull/5567) | Bump open_saml_version 5.1.4 → 5.1.6 |   |
| v3.3.0 | [#5585](https://github.com/opensearch-project/security/pull/5585) | Bump open_saml_shib_version 9.1.4 → 9.1.6 |   |
| v3.3.0 | [#5665](https://github.com/opensearch-project/security/pull/5665) | Bump guava 33.4.8-jre → 33.5.0-jre |   |
| v3.3.0 | [#5589](https://github.com/opensearch-project/security/pull/5589) | Bump metrics-core 4.2.33 → 4.2.37 |   |
| v3.3.0 | [#5566](https://github.com/opensearch-project/security/pull/5566) | Bump mockito-core 5.18.0 → 5.20.0 |   |
| v3.3.0 | [#5584](https://github.com/opensearch-project/security/pull/5584) | Bump com.github.spotbugs 6.2.4 → 6.4.1 |   |
| v3.3.0 | [#5572](https://github.com/opensearch-project/security/pull/5572) | Bump actions/checkout 4 → 5 |   |
| v3.3.0 | [#5582](https://github.com/opensearch-project/security/pull/5582) | Bump actions/setup-java 4 → 5 |   |
| v3.1.0 | [#5380](https://github.com/opensearch-project/security/pull/5380) | Bump bouncycastle_version 1.80 → 1.81 |   |
| v3.1.0 | [#5131](https://github.com/opensearch-project/security/pull/5131) | Upgrade kafka_version 3.7.1 → 4.0.0 |   |
| v3.1.0 | [#5284](https://github.com/opensearch-project/security/pull/5284) | Bump guava 33.4.6-jre → 33.4.8-jre |   |
| v3.1.0 | [#5283](https://github.com/opensearch-project/security/pull/5283) | Bump spring_version 6.2.5 → 6.2.7 |   |
| v3.1.0 | [#5296](https://github.com/opensearch-project/security/pull/5296) | Bump mockito-core 5.15.2 → 5.18.0 |   |
| v3.1.0 | [#5293](https://github.com/opensearch-project/security/pull/5293) | Bump asm 9.7.1 → 9.8 |   |
| v3.1.0 | [#5295](https://github.com/opensearch-project/security/pull/5295) | Bump commons-codec 1.16.1 → 1.18.0 |   |
| v3.1.0 | [#5313](https://github.com/opensearch-project/security/pull/5313) | Bump byte-buddy 1.15.11 → 1.17.5 |   |
| v3.1.0 | [#5328](https://github.com/opensearch-project/security/pull/5328) | Bump commons-io 2.18.0 → 2.19.0 |   |
| v3.1.0 | [#5316](https://github.com/opensearch-project/security/pull/5316) | Bump commons-collections4 4.4 → 4.5 |   |
| v3.1.0 | [#5371](https://github.com/opensearch-project/security/pull/5371) | Bump junit-jupiter 5.12.2 → 5.13.1 |   |
| v3.1.0 | [#5292](https://github.com/opensearch-project/security/pull/5292) | Bump jackson-databind |   |
| v3.1.0 | [#2231](https://github.com/opensearch-project/security-dashboards-plugin/pull/2231) | Fix CVE-2024-52798 |   |
| v3.0.0 | [#5203](https://github.com/opensearch-project/security/pull/5203) | Bump spring_version 6.2.4 → 6.2.5 |   |
| v3.0.0 | [#5202](https://github.com/opensearch-project/security/pull/5202) | Bump bouncycastle_version 1.78 → 1.80 |   |
| v3.0.0 | [#5231](https://github.com/opensearch-project/security/pull/5231) | Bump google-java-format 1.25.2 → 1.26.0 |   |
| v3.0.0 | [#5230](https://github.com/opensearch-project/security/pull/5230) | Bump open_saml_shib_version 9.1.3 → 9.1.4 |   |
| v3.0.0 | [#5229](https://github.com/opensearch-project/security/pull/5229) | Bump randomizedtesting-runner 2.8.2 → 2.8.3 |   |
| v3.0.0 | [#5227](https://github.com/opensearch-project/security/pull/5227) | Bump open_saml_version 5.1.3 → 5.1.4 |   |
| v3.0.0 | [#5244](https://github.com/opensearch-project/security/pull/5244) | Bump asm 9.7.1 → 9.8 |   |
| v3.0.0 | [#5246](https://github.com/opensearch-project/security/pull/5246) | Bump nebula.ospackage 11.11.1 → 11.11.2 |   |
| v3.0.0 | [#5245](https://github.com/opensearch-project/security/pull/5245) | Bump error_prone_annotations 2.36.0 → 2.37.0 |   |
| v3.0.0 | [#5267](https://github.com/opensearch-project/security/pull/5267) | Bump commons-io 2.18.0 → 2.19.0 |   |
| v3.0.0 | [#5266](https://github.com/opensearch-project/security/pull/5266) | Bump commons-text 1.13.0 → 1.13.1 |   |
| v3.0.0 | [#5268](https://github.com/opensearch-project/security/pull/5268) | Bump junit-jupiter-api 5.12.1 → 5.12.2 |   |
| v3.0.0 | [#5265](https://github.com/opensearch-project/security/pull/5265) | Bump failureaccess 1.0.2 → 1.0.3 |   |
| v2.19.0 | [#1251](https://github.com/opensearch-project/security/pull/1251) | Bump cypress and cross-spawn version |   |
| v2.18.0 | [#4738](https://github.com/opensearch-project/security/pull/4738) | Bump snappy-java 1.1.10.6 → 1.1.10.7 |   |
| v2.18.0 | [#4736](https://github.com/opensearch-project/security/pull/4736) | Bump gradle.test-retry 1.5.10 → 1.6.0 |   |
| v2.18.0 | [#4750](https://github.com/opensearch-project/security/pull/4750) | Bump commons-io 2.16.1 → 2.17.0 |   |
| v2.18.0 | [#4749](https://github.com/opensearch-project/security/pull/4749) | Bump scala-library 2.13.14 → 2.13.15 |   |
| v2.18.0 | [#4717](https://github.com/opensearch-project/security/pull/4717) | Bump checker-qual and logback-classic |   |
| v2.16.0 | [#4531](https://github.com/opensearch-project/security/pull/4531) | Bump checker-qual 3.44.0 → 3.45.0 |   |
| v2.16.0 | [#4501](https://github.com/opensearch-project/security/pull/4501) | Bump kafka 3.7.0 → 3.7.1 |   |
| v2.16.0 | [#4503](https://github.com/opensearch-project/security/pull/4503) | Bump junit-jupiter 5.10.2 → 5.10.3 |   |
| v2.16.0 | [#4483](https://github.com/opensearch-project/security/pull/4483) | Bump woodstox-core 6.6.2 → 6.7.0 |   |
| v2.16.0 | [#4484](https://github.com/opensearch-project/security/pull/4484) | Bump jjwt 0.12.5 → 0.12.6 |   |
| v2.16.0 | [#4467](https://github.com/opensearch-project/security/pull/4467) | Bump eclipse.core.runtime 3.31.0 → 3.31.100 |   |
| v2.16.0 | [#4466](https://github.com/opensearch-project/security/pull/4466) | Bump spring 5.3.36 → 5.3.37 |   |
