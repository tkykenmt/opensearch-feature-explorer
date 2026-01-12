# Version Bumps & Release Qualifiers (Batch 2)

## Summary

This release item covers version bump and release qualifier updates across 6 additional OpenSearch plugin repositories for the v3.0.0 release cycle. These changes ensure consistent versioning from alpha1 through beta1 to GA release, and prepare for the next development cycle with SNAPSHOT versions.

## Details

### What's New in v3.0.0

Version bumps and qualifier updates were applied across 6 repositories:

- **learning**: Learning to Rank plugin version progression
- **security**: Security plugin version updates and qualifier removal
- **performance**: Performance Analyzer version bumps including JDK 21 upgrade
- **query**: Query Insights plugin version progression and Gradle upgrade
- **dashboards**: Dashboards Query Workbench version updates
- **reporting**: Reporting plugin version bumps

### Technical Changes

#### Version Progression

| Phase | Version String | Qualifier |
|-------|---------------|-----------|
| Alpha | 3.0.0.0-alpha1 | alpha1 |
| Beta | 3.0.0.0-beta1 | beta1 |
| GA | 3.0.0.0 | (none) |
| Post-GA | 3.1.0-SNAPSHOT | SNAPSHOT |

#### Changes by Repository

| Repository | PRs | Changes |
|------------|-----|---------|
| learning | 2 | alpha1 → beta1, remove beta1 qualifier |
| security | 4 | Version increment, beta1 qualifier, remove qualifier, SNAPSHOT |
| performance | 2 | alpha1 + JDK 21, beta1 |
| query | 4 | alpha1 + Gradle 8.10.2, beta1, remove qualifier, SNAPSHOT |
| dashboards | 2 | alpha1, beta1 |
| reporting | 2 | alpha1-SNAPSHOT, beta1-SNAPSHOT |

### Usage Example

Version bump PRs typically modify `build.gradle` or `gradle.properties`:

```groovy
// Before (alpha1)
version = '3.0.0.0-alpha1'

// After (beta1)
version = '3.0.0.0-beta1'

// GA release
version = '3.0.0.0'

// Post-GA SNAPSHOT
version = '3.1.0-SNAPSHOT'
```

## Limitations

- Version bump PRs are routine maintenance with no functional changes
- These changes must be coordinated with the release branch creation timeline

## Related PRs

| PR | Title | Repository |
|----|-------|------------|
| [#154](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/154) | Update 3.0.0 qualifier from alpha1 to beta1 | learning |
| [#169](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/169) | Remove beta1 qualifier | learning |
| [#791](https://github.com/opensearch-project/performance-analyzer/pull/791) | Bumps OS to 3.0.0-alpha1 and JDK 21 | performance |
| [#794](https://github.com/opensearch-project/performance-analyzer/pull/794) | Bumps plugin version to 3.0.0.0-beta1 in PA | performance |
| [#247](https://github.com/opensearch-project/query-insights/pull/247) | Bump version to 3.0.0-alpha1 & upgrade to gradle 8.10.2 | query |
| [#290](https://github.com/opensearch-project/query-insights/pull/290) | Update 3.0.0 qualifier from alpha1 to beta1 | query |
| [#329](https://github.com/opensearch-project/query-insights/pull/329) | Remove beta1 qualifier | query |
| [#325](https://github.com/opensearch-project/query-insights/pull/325) | Increment version to 3.1.0-SNAPSHOT | query |
| [#127](https://github.com/opensearch-project/dashboards-query-workbench/pull/127) | Bump to 3.0.0-alpha1 | dashboards |
| [#154](https://github.com/opensearch-project/dashboards-query-workbench/pull/154) | Update 3.0.0 qualifier from alpha1 to beta1 | dashboards |
| [#462](https://github.com/opensearch-project/sql/pull/462) | Bump dashboards query workbench to version 3.0.0.0-beta1 | query |
| [#444](https://github.com/opensearch-project/sql/pull/444) | Bump dashboards query workbench to version 3.0.0.0-alpha1 | query |
| [#1073](https://github.com/opensearch-project/reporting/pull/1073) | Bump version 3.0.0-alpha1-SNAPSHOT | reporting |
| [#1083](https://github.com/opensearch-project/reporting/pull/1083) | Bump version 3.0.0-beta1-SNAPSHOT | reporting |
| [#1517](https://github.com/opensearch-project/security/pull/1517) | Increment version to 3.1.0-SNAPSHOT | security |
| [#1519](https://github.com/opensearch-project/security/pull/1519) | Remove beta1 qualifier | security |
| [#1500](https://github.com/opensearch-project/security/pull/1500) | Update version qualifier to beta1 | security |
| [#1283](https://github.com/opensearch-project/security/pull/1283) | Increment version to 3.0.0.0 | security |

## References

- [Issue #201](https://github.com/tkykenmt/opensearch-feature-explorer/issues/201): Tracking issue

## Related Feature Report

- [Full feature documentation](../../../../features/multi-plugin/version-bumps-release-notes.md)
