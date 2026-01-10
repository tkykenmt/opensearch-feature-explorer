# Security Plugin Dependencies

## Summary

This release item updates several third-party dependencies in the OpenSearch Security plugin to their latest versions. These updates address potential security vulnerabilities, improve stability, and ensure compatibility with the latest library features.

## Details

### What's New in v2.18.0

The Security plugin received dependency updates for 5 libraries:

| Dependency | Previous Version | New Version | Purpose |
|------------|------------------|-------------|----------|
| snappy-java | 1.1.10.6 | 1.1.10.7 | Fast compression/decompression |
| gradle.test-retry | 1.5.10 | 1.6.0 | Gradle test retry plugin |
| commons-io | 2.16.1 | 2.17.0 | I/O utility library |
| scala-library | 2.13.14 | 2.13.15 | Scala runtime library |
| checker-qual | 3.46.0 | 3.47.0 | Checker Framework annotations |
| logback-classic | 1.5.7 | 1.5.8 | Logging framework |

### Technical Changes

#### snappy-java 1.1.10.7
- Provides fast compression/decompression for data serialization
- Minor bug fixes and performance improvements

#### gradle.test-retry 1.6.0
- Gradle plugin for retrying flaky tests
- Improves CI/CD reliability

#### commons-io 2.17.0
- Apache Commons I/O library for file and stream operations
- Bug fixes and new utility methods

#### scala-library 2.13.15
- Scala standard library runtime
- Bug fixes and minor improvements

#### checker-qual 3.47.0 & logback-classic 1.5.8
- Checker Framework annotations for static analysis
- Logback logging framework updates
- Combined in a single backport PR

## Limitations

- These are maintenance updates with no functional changes
- All updates are backward compatible

## Related PRs

| PR | Description |
|----|-------------|
| [#4738](https://github.com/opensearch-project/security/pull/4738) | Bump snappy-java from 1.1.10.6 to 1.1.10.7 |
| [#4736](https://github.com/opensearch-project/security/pull/4736) | Bump gradle.test-retry from 1.5.10 to 1.6.0 |
| [#4750](https://github.com/opensearch-project/security/pull/4750) | Bump commons-io from 2.16.1 to 2.17.0 |
| [#4749](https://github.com/opensearch-project/security/pull/4749) | Bump scala-library from 2.13.14 to 2.13.15 |
| [#4717](https://github.com/opensearch-project/security/pull/4717) | Bump checker-qual and logback-classic |

## References

- [OpenSearch Security Repository](https://github.com/opensearch-project/security)

## Related Feature Report

- [Full feature documentation](../../../features/security/security-plugin.md)
