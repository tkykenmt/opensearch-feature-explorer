# Notifications Plugin Infrastructure

## Summary

Infrastructure updates for the OpenSearch Notifications plugin in v3.2.0, including Gradle 8.14 upgrade, JDK 24 CI support, JaCoCo 0.8.13 for code coverage, and dependency updates for nebula.ospackage plugin.

## Details

### What's New in v3.2.0

This release focuses on build infrastructure modernization and CI/CD improvements for the Notifications plugin.

### Technical Changes

#### Build System Updates

| Component | Previous | Updated |
|-----------|----------|---------|
| Gradle | 8.10.2 | 8.14 |
| JaCoCo | 0.8.12 | 0.8.13 |
| nebula.ospackage | 11.5.0 | 12.0.0 |
| CI JDK Matrix | 21, 23 | 21, 24 |

#### Gradle Wrapper Changes

The Gradle wrapper has been updated with:
- New distribution URL pointing to Gradle 8.14
- SHA256 checksum validation enabled
- Distribution URL validation enabled
- Updated wrapper JAR execution method (using `-jar` flag)

#### CI/CD Updates

The GitHub Actions workflow (`notifications-test-and-build-workflow.yml`) now tests against:
- JDK 21 (LTS)
- JDK 24 (latest)

This ensures compatibility with both the current LTS release and the latest JDK version.

#### Version Fetching Update

The build script now fetches the latest OpenSearch version from the `3.1` branch instead of `2.x`:
```groovy
def url = 'https://raw.githubusercontent.com/opensearch-project/OpenSearch/refs/heads/3.1/buildSrc/version.properties'
```

### Usage Example

No user-facing changes. These are internal build infrastructure updates.

### Migration Notes

No migration required. These changes are transparent to users.

## Limitations

None specific to this release.

## References

### Documentation
- [Gradle 8.14 Release Notes](https://docs.gradle.org/8.14/release-notes.html)
- [JaCoCo 0.8.13 Release](https://www.jacoco.org/jacoco/trunk/doc/changes.html)
- [OpenSearch Notifications Repository](https://github.com/opensearch-project/notifications)

### Pull Requests
| PR | Description |
|----|-------------|
| [#1057](https://github.com/opensearch-project/notifications/pull/1057) | Updated gradle, jdk and other dependencies |

## Related Feature Report

- [Full feature documentation](../../../../features/notifications/notifications-plugin.md)
