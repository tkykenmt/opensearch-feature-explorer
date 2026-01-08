# Version Bumps & Release Notes

## Summary

This release item covers the standard version bump and release notes updates across multiple OpenSearch plugins for the v3.0.0 release cycle. These changes ensure all plugins are properly versioned and documented for the major release.

## Details

### What's New in v3.0.0

Version bumps and release notes were added across 9 repositories to prepare for the OpenSearch 3.0.0 release:

- **alerting**: Version bumps from alpha1 → beta1 → GA, plus release notes
- **alerting-dashboards-plugin**: Version increments through alpha1, beta1, and GA
- **common-utils**: Shadow plugin repo update and version bumps
- **index-management**: Version bumps and SNAPSHOT updates
- **notifications**: Version increments and release notes
- **notifications-dashboards-plugin**: Version bumps through release cycle
- **query-insights-dashboards**: Release notes for alpha1 and beta1
- **security**: Release notes additions
- **security-dashboards-plugin**: Release notes for 3.0.0

### Technical Changes

#### Version Progression

| Phase | Version String | Qualifier |
|-------|---------------|-----------|
| Alpha | 3.0.0.0-alpha1 | alpha1 |
| Beta | 3.0.0.0-beta1 | beta1 |
| GA | 3.0.0.0 | (none) |
| Post-GA | 3.0.0-SNAPSHOT | SNAPSHOT |

#### Affected Files

Typical files modified in version bump PRs:

- `build.gradle` - Version number updates
- `gradle.properties` - Version properties
- `release-notes/*.md` - Release documentation
- Plugin descriptor files

### Repositories Affected

| Repository | PRs | Changes |
|------------|-----|---------|
| alerting | 6 | Version bumps, release notes |
| alerting-dashboards-plugin | 6 | Version increments |
| common-utils | 2 | Shadow plugin, version bumps |
| index-management | 3 | Version bumps |
| notifications | 2 | Version increments, release notes |
| notifications-dashboards-plugin | 3 | Version bumps |
| query-insights-dashboards | 2 | Release notes |
| security | 2 | Release notes |
| security-dashboards-plugin | 2 | Release notes |

## Limitations

- Version bump PRs are routine maintenance and do not introduce functional changes
- Release notes content depends on features merged before the cutoff date

## Related PRs

| PR | Repository | Description |
|----|------------|-------------|
| [#1843](https://github.com/opensearch-project/alerting/pull/1843) | alerting | Added 3.0 release notes |
| [#1837](https://github.com/opensearch-project/alerting/pull/1837) | alerting | Increment version to 3.0.0-SNAPSHOT |
| [#1816](https://github.com/opensearch-project/alerting/pull/1816) | alerting | Update version qualifier to beta1 |
| [#1786](https://github.com/opensearch-project/alerting/pull/1786) | alerting | Increment version to 3.0.0.0-alpha1 |
| [#1246](https://github.com/opensearch-project/alerting/pull/1246) | alerting | Added 3.0.0 release notes / Increment version |
| [#775](https://github.com/opensearch-project/common-utils/pull/775) | common-utils | Update shadow plugin repo and bump to 3.0.0.0-alpha1 |
| [#808](https://github.com/opensearch-project/common-utils/pull/808) | common-utils | Change 3.0.0 qualifier from alpha1 to beta1 |
| [#1384](https://github.com/opensearch-project/index-management/pull/1384) | index-management | Bump Version to 3.0.0-alpha1 |
| [#1398](https://github.com/opensearch-project/index-management/pull/1398) | index-management | Update 3.0.0 qualifier from alpha1 to beta1 |
| [#1412](https://github.com/opensearch-project/index-management/pull/1412) | index-management | Increment version to 3.0.0-SNAPSHOT |
| [#347](https://github.com/opensearch-project/notifications/pull/347) | notifications | Added 3.0.0 release notes / Increment version |
| [#1033](https://github.com/opensearch-project/notifications/pull/1033) | notifications | Add 3.0.0 release notes |
| [#1523](https://github.com/opensearch-project/security/pull/1523) | security | Added 3.0.0 release notes |
| [#1283](https://github.com/opensearch-project/security/pull/1283) | security | Added 3.0.0 release notes |
| [#3589](https://github.com/opensearch-project/sql/pull/3589) | sql | Remove beta1 qualifier |

## References

- [opensearch-build#5267](https://github.com/opensearch-project/opensearch-build/issues/5267): Release coordination issue
- [opensearch-build#3747](https://github.com/opensearch-project/opensearch-build/issues/3747): Build configuration issue

## Related Feature Report

- [Full feature documentation](../../../../features/multi-plugin/version-bumps-release-notes.md)
