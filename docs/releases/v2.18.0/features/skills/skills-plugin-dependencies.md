# Skills Plugin Dependencies

## Summary
This release includes dependency updates and a test fix for the Skills plugin in OpenSearch v2.18.0. The changes update testing frameworks (Mockito, JUnit5), build tools (Gradle, Lombok plugin), and runtime libraries (ByteBuddy) to their latest versions, along with a fix for test failures caused by external API changes.

## Details

### What's New in v2.18.0

#### Dependency Updates
The following dependencies were updated to improve stability, security, and compatibility:

| Dependency | Previous Version | New Version | Type |
|------------|-----------------|-------------|------|
| Mockito (core + junit-jupiter) | 5.13.0 | 5.14.2 | Testing |
| JUnit5 (jupiter-api + engine) | 5.10.2 | 5.11.2 | Testing |
| ByteBuddy | 1.14.9 | 1.15.4 | Runtime |
| ByteBuddy Agent | 1.14.12 | 1.15.4 | Runtime |
| Gradle | 8.10 | 8.10.2 | Build |
| io.freefair.lombok | 8.10 | 8.10.2 | Build Plugin |

#### Test Fix
Fixed test failures in the 2.x branch caused by changes to the `AnomalyDetector` constructor in the anomaly-detection plugin. The tests were updated to accommodate the new constructor signature.

### Technical Changes

#### Mockito 5.14.2 Improvements
- Improved Java agent installation within Mockito jar
- Fixed gradle mockitoAgent configuration transitivity
- Better error messages when accessing mocks after `clearInlineMocks`

#### JUnit5 5.11.2 Updates
- Updated test framework with latest bug fixes and improvements
- Better compatibility with modern Java versions

#### Gradle 8.10.2 Fixes
- Fixed dependency resolution performance issues from 8.10
- Fixed `LifecycleAwareProject` equals() contract
- Disabled isolated projects validation when feature is disabled

### Migration Notes
No migration steps required. These are internal dependency updates that maintain backward compatibility.

## Limitations
- ByteBuddy updates may require Java agent configuration adjustments in some environments

## References

### Documentation
- [Mockito 5.14.2 Release Notes](https://github.com/mockito/mockito/releases/tag/v5.14.2)
- [JUnit5 5.11.2 Release Notes](https://github.com/junit-team/junit5/releases/tag/r5.11.2)
- [Gradle 8.10.2 Release Notes](https://docs.gradle.org/8.10.2/release-notes.html)
- [ByteBuddy Project](https://bytebuddy.net)

### Pull Requests
| PR | Description |
|----|-------------|
| [#427](https://github.com/opensearch-project/skills/pull/427) | Fix test failure due to external change |
| [#437](https://github.com/opensearch-project/skills/pull/437) | Update mockito monorepo to v5.14.2 |
| [#363](https://github.com/opensearch-project/skills/pull/363) | Update junit5 monorepo to v5.11.2 |
| [#43](https://github.com/opensearch-project/skills/pull/43) | Update byte-buddy to v1.15.4 |
| [#279](https://github.com/opensearch-project/skills/pull/279) | Update byte-buddy-agent to v1.15.4 |
| [#432](https://github.com/opensearch-project/skills/pull/432) | Update Gradle to v8.10.2 |
| [#434](https://github.com/opensearch-project/skills/pull/434) | Update io.freefair.lombok to v8.10.2 |

## Related Feature Report
- [Full feature documentation](../../../features/skills/skills-plugin-dependencies.md)
