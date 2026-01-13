---
tags:
  - domain/security
  - component/server
  - observability
  - performance
  - security
---
# Dependency Bumps (Security)

## Summary

Routine dependency updates for the Security plugin in v2.17.0, including updates to testing frameworks, security libraries, build tools, and Gradle to maintain security and compatibility.

## Details

### What's New in v2.17.0

The Security plugin received 12 dependency updates:

| Dependency | From | To | Category |
|------------|------|-----|----------|
| com.google.errorprone:error_prone_annotations | 2.30.0 | 2.31.0 | Static Analysis |
| org.passay:passay | 1.6.4 | 1.6.5 | Password Validation |
| spring_version | 5.3.37 | 5.3.39 | Framework |
| commons-cli:commons-cli | 1.8.0 | 1.9.0 | CLI Parsing |
| org.junit.jupiter:junit-jupiter | 5.10.3 | 5.11.0 | Testing |
| org.cryptacular:cryptacular | 1.2.6 | 1.2.7 | Cryptography |
| Gradle | - | 8.10 | Build Tool |
| org.xerial.snappy:snappy-java | 1.1.10.5 | 1.1.10.6 | Compression |
| com.google.googlejavaformat:google-java-format | 1.22.0 | 1.23.0 | Code Formatting |
| io.dropwizard.metrics:metrics-core | 4.2.26 | 4.2.27 | Metrics |
| com.netflix.nebula.ospackage | 11.9.1 | 11.10.0 | Packaging |
| org.checkerframework:checker-qual | 3.45.0 | 3.46.0 | Static Analysis |

### Technical Changes

#### Security-Related Updates

- **Passay (1.6.4 → 1.6.5)**: Password validation library with bug fixes
- **Cryptacular (1.2.6 → 1.2.7)**: Cryptographic utilities library update
- **Spring Framework (5.3.37 → 5.3.39)**: Security and bug fixes for the Spring framework

#### Build & Testing Updates

- **Gradle 8.10**: Major build tool update with performance improvements
- **JUnit Jupiter (5.10.3 → 5.11.0)**: Testing framework update with new features
- **Error Prone Annotations (2.30.0 → 2.31.0)**: Static analysis improvements
- **Checker Framework (3.45.0 → 3.46.0)**: Type checking annotations update

#### Utility Updates

- **Commons CLI (1.8.0 → 1.9.0)**: Command-line parsing library
- **Snappy Java (1.1.10.5 → 1.1.10.6)**: Compression library bug fixes
- **Metrics Core (4.2.26 → 4.2.27)**: Metrics collection library

## Limitations

- These are maintenance updates with no functional changes
- No migration required

## References

### Documentation
- [Security Plugin Repository](https://github.com/opensearch-project/security)

### Pull Requests
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

## Related Feature Report

- [Dependency Management](../../../../features/multi-plugin/multi-plugin-dependency-bumps.md)
