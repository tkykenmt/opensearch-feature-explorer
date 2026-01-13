---
tags:
  - domain/infra
  - component/server
  - dashboards
  - indexing
  - ml
  - observability
  - performance
  - search
  - security
---
# Version Increment (Maintenance)

## Summary

Routine version increment PRs for v3.2.0 across 14 OpenSearch repositories. These automated changes update version strings and prepare repositories for the 3.2.0 release cycle.

## Details

### What's New in v3.2.0

Version bumps to 3.2.0.0 (release) and 3.2.0-SNAPSHOT (development) across multiple plugins and components.

### Technical Changes

#### Repositories Updated

| Repository | PRs | Type |
|------------|-----|------|
| alerting | 4 | Version bump + dependency fix |
| asynchronous-search | 1 | SNAPSHOT |
| custom | 1 | SNAPSHOT |
| index-management | 2 | Release + SNAPSHOT |
| ml-commons | 1 | Release |
| notifications | 1 | Release |
| observability | 2 | Release + SNAPSHOT |
| query | 2 | Release + SNAPSHOT |
| dashboards | 1 | Release |
| reporting | 2 | Release + SNAPSHOT |
| security | 1 | Release |
| learning | 1 | SNAPSHOT |
| performance | 1 | SNAPSHOT |
| system | 1 | SNAPSHOT |

#### Notable Changes

The alerting repository includes additional dependency fixes:
- PR #1892: Moved commons-beanutils pinning to core gradle file
- PR #1887: Pinned commons-beanutils dependency to 1.11.0 version

### Files Modified

| File | Purpose |
|------|---------|
| `build.gradle` | Plugin version declaration |
| `gradle.properties` | Version properties |

## Limitations

- Version bumps are mechanical changes with no functional impact
- Timing must coordinate with release branch creation

## References

### Documentation
- [OpenSearch Release Process](https://github.com/opensearch-project/opensearch-build/blob/main/RELEASING.md): Official release documentation

### Pull Requests
| PR | Title | Repository |
|----|-------|------------|
| [#1892](https://github.com/opensearch-project/alerting/pull/1892) | Moved the commons-beanutils pinning to the core gradle file | alerting |
| [#1887](https://github.com/opensearch-project/alerting/pull/1887) | Pinned the commons-beanutils dependency to 1.11.0 version | alerting |
| [#751](https://github.com/opensearch-project/asynchronous-search/pull/751) | [AUTO] Increment version to 3.2.0-SNAPSHOT | asynchronous-search |
| [#262](https://github.com/opensearch-project/custom-codecs/pull/262) | [AUTO] Increment version to 3.2.0-SNAPSHOT | custom |
| [#1271](https://github.com/opensearch-project/alerting/pull/1271) | Increment version to 3.2.0.0 | alerting |
| [#1332](https://github.com/opensearch-project/index-management/pull/1332) | Increment version to 3.2.0.0 | index-management |
| [#437](https://github.com/opensearch-project/ml-commons/pull/437) | Increment version to 3.2.0.0 | ml-commons |
| [#365](https://github.com/opensearch-project/notifications/pull/365) | [AUTO] Increment version to 3.2.0.0 | notifications |
| [#2481](https://github.com/opensearch-project/observability/pull/2481) | Increment version to 3.2.0.0 + Snapshots update | observability |
| [#295](https://github.com/opensearch-project/query-insights/pull/295) | [AUTO] Increment version to 3.2.0.0 | query |
| [#485](https://github.com/opensearch-project/dashboards-notifications/pull/485) | Increment version to 3.2.0.0 | dashboards |
| [#603](https://github.com/opensearch-project/reporting/pull/603) | Increment version to 3.2.0.0 | reporting |
| [#1316](https://github.com/opensearch-project/security/pull/1316) | [AUTO] Increment version to 3.2.0.0 | security |
| [#1435](https://github.com/opensearch-project/index-management/pull/1435) | [AUTO] Increment version to 3.2.0-SNAPSHOT | index-management |
| [#191](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/191) | [AUTO] Increment version to 3.2.0-SNAPSHOT | learning |
| [#1933](https://github.com/opensearch-project/observability/pull/1933) | [AUTO] Increment version to 3.2.0-SNAPSHOT | observability |
| [#1105](https://github.com/opensearch-project/reporting/pull/1105) | [AUTO] Increment version to 3.2.0-SNAPSHOT | reporting |
| [#86](https://github.com/opensearch-project/opensearch-system-templates/pull/86) | [AUTO] Increment version to 3.2.0-SNAPSHOT | system |
| [#823](https://github.com/opensearch-project/performance-analyzer/pull/823) | Increment version to 3.2.0-SNAPSHOT | performance |
| [#380](https://github.com/opensearch-project/query-insights/pull/380) | [AUTO] Increment version to 3.2.0-SNAPSHOT | query |

## Related Feature Report

- Full feature documentation
