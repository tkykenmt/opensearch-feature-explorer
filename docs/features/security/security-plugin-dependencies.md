# Security Plugin Dependencies

## Summary

The OpenSearch Security plugin maintains a set of third-party dependencies that provide essential functionality for security operations, including compression, logging, I/O operations, and build tooling. Regular updates to these dependencies ensure security, stability, and compatibility.

## Details

### Core Dependencies

| Dependency | Purpose | Category |
|------------|---------|----------|
| snappy-java | Fast compression/decompression | Runtime |
| commons-io | File and stream I/O utilities | Runtime |
| scala-library | Scala runtime support | Runtime |
| logback-classic | Logging framework | Runtime |
| checker-qual | Static analysis annotations | Build |
| gradle.test-retry | Flaky test retry | Build |

### Dependency Categories

#### Runtime Dependencies
These libraries are required at runtime for the Security plugin to function:

- **snappy-java**: Provides fast compression/decompression algorithms used for data serialization
- **commons-io**: Apache Commons I/O library for file operations and stream handling
- **scala-library**: Scala standard library required for Scala-based components
- **logback-classic**: SLF4J-compatible logging implementation

#### Build Dependencies
These libraries are used during the build process:

- **checker-qual**: Annotations for the Checker Framework static analysis tool
- **gradle.test-retry**: Gradle plugin that automatically retries failed tests to handle flaky tests

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
| v2.18.0 | [#4738](https://github.com/opensearch-project/security/pull/4738) | Bump snappy-java 1.1.10.6 → 1.1.10.7 |
| v2.18.0 | [#4736](https://github.com/opensearch-project/security/pull/4736) | Bump gradle.test-retry 1.5.10 → 1.6.0 |
| v2.18.0 | [#4750](https://github.com/opensearch-project/security/pull/4750) | Bump commons-io 2.16.1 → 2.17.0 |
| v2.18.0 | [#4749](https://github.com/opensearch-project/security/pull/4749) | Bump scala-library 2.13.14 → 2.13.15 |
| v2.18.0 | [#4717](https://github.com/opensearch-project/security/pull/4717) | Bump checker-qual and logback-classic |

## References

- [OpenSearch Security Repository](https://github.com/opensearch-project/security)
- [snappy-java](https://github.com/xerial/snappy-java)
- [Apache Commons IO](https://commons.apache.org/proper/commons-io/)
- [Scala Library](https://www.scala-lang.org/)
- [Logback](https://logback.qos.ch/)

## Change History

- **v2.18.0** (2024-10-22): Updated snappy-java, gradle.test-retry, commons-io, scala-library, checker-qual, and logback-classic
