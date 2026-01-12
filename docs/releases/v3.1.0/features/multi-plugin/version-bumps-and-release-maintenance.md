---
tags:
  - dashboards
  - indexing
  - search
---

# Version Bumps and Release Maintenance

## Summary

This release item covers version increments and release maintenance activities across 11 OpenSearch repositories for the v3.1.0 release cycle. These changes prepare the codebase for the 3.1.0 release by updating version numbers, adding release notes, and performing necessary CI/build updates.

## Details

### What's New in v3.1.0

Version bump PRs were merged across multiple repositories to increment versions from 3.0.x to 3.1.0-SNAPSHOT or 3.1.0.0, preparing for the v3.1.0 release.

### Technical Changes

#### Repositories Updated

| Repository | PR | Change Type |
|------------|-----|-------------|
| alerting | [#1837](https://github.com/opensearch-project/alerting/pull/1837) | Auto-increment to 3.1.0-SNAPSHOT |
| alerting | [#1249](https://github.com/opensearch-project/alerting/pull/1249) | Upgrade Java to 21 for binary CI |
| alerting | [#1251](https://github.com/opensearch-project/alerting/pull/1251) | Increment to 3.1.0.0 |
| asynchronous-search | [#726](https://github.com/opensearch-project/asynchronous-search/pull/726) | Increment to 3.1.0 |
| common-utils | [#820](https://github.com/opensearch-project/common-utils/pull/820) | Auto-increment to 3.1.0-SNAPSHOT |
| notifications-dashboards | [#735](https://github.com/opensearch-project/dashboards-notifications/pull/735) | Increment to 3.1.0.0 |
| notifications | [#357](https://github.com/opensearch-project/notifications/pull/357) | Increment to 3.1.0.0 |
| reporting | [#579](https://github.com/opensearch-project/reporting/pull/579) | Increment to 3.1.0.0 |
| reporting | [#587](https://github.com/opensearch-project/reporting/pull/587) | Adding release notes for 3.1.0 |
| index-management-dashboards | [#534](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/534) | Increment to 3.1.0.0 |
| index-management | [#1414](https://github.com/opensearch-project/index-management/pull/1414) | Auto-increment to 3.1.0-SNAPSHOT |
| index-management | [#1313](https://github.com/opensearch-project/index-management/pull/1313) | Increment to 3.1.0.0 |
| ml-commons | [#572](https://github.com/opensearch-project/ml-commons/pull/572) | Bump version to 3.1.0.0 |
| observability | [#2451](https://github.com/opensearch-project/observability/pull/2451) | Workflows - Version bump to 3.1.0 |
| sql | [#3671](https://github.com/opensearch-project/sql/pull/3671) | Bump setuptools to 78.1.1 |
| OpenSearch | [#18039](https://github.com/opensearch-project/OpenSearch/pull/18039) | Bump Core main branch to 3.0.0 |

#### Version Numbering Convention

OpenSearch plugins follow a versioning scheme where:
- Core OpenSearch uses semantic versioning (e.g., 3.1.0)
- Plugins use four-part versioning (e.g., 3.1.0.0) where the fourth digit allows for plugin-specific patches
- SNAPSHOT versions indicate development builds

### Usage Example

Version bumps are typically automated or follow a standard pattern:

```gradle
// build.gradle example
opensearch_version = System.getProperty("opensearch.version", "3.1.0-SNAPSHOT")
```

### Migration Notes

No migration required. Version bumps are internal maintenance changes that don't affect user-facing functionality.

## Limitations

- Version bump PRs are routine maintenance and don't introduce new features
- Some repositories may have additional version-specific changes bundled with the bump

## References

### Pull Requests
| PR | Description |
|----|-------------|
| [#18039](https://github.com/opensearch-project/OpenSearch/pull/18039) | Bump OpenSearch Core main branch to 3.0.0 |
| [#1837](https://github.com/opensearch-project/alerting/pull/1837) | Auto-increment alerting to 3.1.0-SNAPSHOT |
| [#1414](https://github.com/opensearch-project/index-management/pull/1414) | Auto-increment index-management to 3.1.0-SNAPSHOT |
| [#820](https://github.com/opensearch-project/common-utils/pull/820) | Auto-increment common-utils to 3.1.0-SNAPSHOT |

### Issues (Design / RFC)
- [Issue #3747](https://github.com/opensearch-project/opensearch-build/issues/3747): OpenSearch build version tracking

## Related Feature Report

- [Full feature documentation](../../../../features/multi-plugin/version-bumps-release-maintenance.md)
