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

## Related PRs

| Version | PR | Description |
|---------|-----|-------------|
| v3.3.0 | [#5595](https://github.com/opensearch-project/security/pull/5595) | Upgrade nimbus-jose-jwt 9.48 → 10.4.2 (CVE-2025-53864) |
| v3.3.0 | [#5629](https://github.com/opensearch-project/security/pull/5629) | Bump nimbus-jose-jwt 10.4.2 → 10.5 |
| v3.3.0 | [#5568](https://github.com/opensearch-project/security/pull/5568) | Bump jjwt_version 0.12.6 → 0.13.0 |
| v3.3.0 | [#5569](https://github.com/opensearch-project/security/pull/5569) | Bump spring_version 6.2.9 → 6.2.11 |
| v3.3.0 | [#5567](https://github.com/opensearch-project/security/pull/5567) | Bump open_saml_version 5.1.4 → 5.1.6 |
| v3.3.0 | [#5585](https://github.com/opensearch-project/security/pull/5585) | Bump open_saml_shib_version 9.1.4 → 9.1.6 |
| v3.3.0 | [#5665](https://github.com/opensearch-project/security/pull/5665) | Bump guava 33.4.8-jre → 33.5.0-jre |
| v3.3.0 | [#5589](https://github.com/opensearch-project/security/pull/5589) | Bump metrics-core 4.2.33 → 4.2.37 |
| v3.3.0 | [#5566](https://github.com/opensearch-project/security/pull/5566) | Bump mockito-core 5.18.0 → 5.20.0 |
| v3.3.0 | [#5584](https://github.com/opensearch-project/security/pull/5584) | Bump com.github.spotbugs 6.2.4 → 6.4.1 |
| v3.3.0 | [#5572](https://github.com/opensearch-project/security/pull/5572) | Bump actions/checkout 4 → 5 |
| v3.3.0 | [#5582](https://github.com/opensearch-project/security/pull/5582) | Bump actions/setup-java 4 → 5 |
| v3.1.0 | [#5380](https://github.com/opensearch-project/security/pull/5380) | Bump bouncycastle_version 1.80 → 1.81 |
| v3.1.0 | [#5131](https://github.com/opensearch-project/security/pull/5131) | Upgrade kafka_version 3.7.1 → 4.0.0 |
| v3.1.0 | [#5284](https://github.com/opensearch-project/security/pull/5284) | Bump guava 33.4.6-jre → 33.4.8-jre |
| v3.1.0 | [#5283](https://github.com/opensearch-project/security/pull/5283) | Bump spring_version 6.2.5 → 6.2.7 |
| v3.1.0 | [#5296](https://github.com/opensearch-project/security/pull/5296) | Bump mockito-core 5.15.2 → 5.18.0 |
| v3.1.0 | [#5293](https://github.com/opensearch-project/security/pull/5293) | Bump asm 9.7.1 → 9.8 |
| v3.1.0 | [#5295](https://github.com/opensearch-project/security/pull/5295) | Bump commons-codec 1.16.1 → 1.18.0 |
| v3.1.0 | [#5313](https://github.com/opensearch-project/security/pull/5313) | Bump byte-buddy 1.15.11 → 1.17.5 |
| v3.1.0 | [#5328](https://github.com/opensearch-project/security/pull/5328) | Bump commons-io 2.18.0 → 2.19.0 |
| v3.1.0 | [#5316](https://github.com/opensearch-project/security/pull/5316) | Bump commons-collections4 4.4 → 4.5 |
| v3.1.0 | [#5371](https://github.com/opensearch-project/security/pull/5371) | Bump junit-jupiter 5.12.2 → 5.13.1 |
| v3.1.0 | [#5292](https://github.com/opensearch-project/security/pull/5292) | Bump jackson-databind |
| v3.1.0 | [#2231](https://github.com/opensearch-project/security-dashboards-plugin/pull/2231) | Fix CVE-2024-52798 |
| v2.18.0 | [#4738](https://github.com/opensearch-project/security/pull/4738) | Bump snappy-java 1.1.10.6 → 1.1.10.7 |
| v2.18.0 | [#4736](https://github.com/opensearch-project/security/pull/4736) | Bump gradle.test-retry 1.5.10 → 1.6.0 |
| v2.18.0 | [#4750](https://github.com/opensearch-project/security/pull/4750) | Bump commons-io 2.16.1 → 2.17.0 |
| v2.18.0 | [#4749](https://github.com/opensearch-project/security/pull/4749) | Bump scala-library 2.13.14 → 2.13.15 |
| v2.18.0 | [#4717](https://github.com/opensearch-project/security/pull/4717) | Bump checker-qual and logback-classic |

## References

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

## Change History

- **v3.3.0** (2026-01-14): Security fix for CVE-2025-53864 (nimbus-jose-jwt), plus 24 dependency updates including Spring 6.2.11, JJWT 0.13.0, Guava 33.5.0, and CI tooling updates
- **v3.1.0** (2025-06-03): Major dependency updates including Bouncy Castle 1.81, Kafka 4.0.0, Spring 6.2.7, Guava 33.4.8, JUnit 5.13.1, and CVE-2024-52798 fix
- **v2.18.0** (2024-10-22): Updated snappy-java, gradle.test-retry, commons-io, scala-library, checker-qual, and logback-classic
