---
tags:
  - multi-plugin
---
# Version Bumps & Release Notes

## Summary

Routine version bump and release notes PRs across 13 OpenSearch plugin repositories in preparation for the v2.16.0 release. This includes Java version upgrades from 11 to 21 for some plugins.

## Details

### Version Bumps

Standard version increment PRs to update plugin versions to 2.16.0-SNAPSHOT or 2.16.0.0:

| Repository | PR | Description |
|------------|-----|-------------|
| sql | [#2743](https://github.com/opensearch-project/sql/pull/2743) | Increment version to 2.16.0-SNAPSHOT |
| alerting | [#1589](https://github.com/opensearch-project/alerting/pull/1589) | Increment version to 2.16.0-SNAPSHOT |
| alerting | [#1009](https://github.com/opensearch-project/alerting/pull/1009) | Increment version to 2.16.0.0 |
| alerting | [#978](https://github.com/opensearch-project/alerting/pull/978) | Increment version to 2.16.0.0 |
| anomaly-detection | [#769](https://github.com/opensearch-project/anomaly-detection/pull/769) | Update 2.x to 2.16.0 |
| asynchronous-search | [#586](https://github.com/opensearch-project/asynchronous-search/pull/586) | Increment version to 2.16.0 |
| common-utils | [#688](https://github.com/opensearch-project/common-utils/pull/688) | Increment version to 2.16.0-SNAPSHOT |
| notifications | [#216](https://github.com/opensearch-project/notifications/pull/216) | Increment version to 2.16.0.0 |
| notifications | [#224](https://github.com/opensearch-project/notifications/pull/224) | Increment version to 2.16.0.0 |
| reporting | [#366](https://github.com/opensearch-project/reporting/pull/366) | Increment version to 2.16.0.0 |
| dashboards-reporting | [#375](https://github.com/opensearch-project/dashboards-reporting/pull/375) | Increment version to 2.16.0.0 |
| index-management | [#1187](https://github.com/opensearch-project/index-management/pull/1187) | Increment version to 2.16.0-SNAPSHOT |
| index-management | [#1089](https://github.com/opensearch-project/index-management/pull/1089) | Increment version to 2.16.0.0 |
| job-scheduler | [#638](https://github.com/opensearch-project/job-scheduler/pull/638) | Increment version to 2.16.0 |
| ml-commons | [#335](https://github.com/opensearch-project/ml-commons/pull/335) | Increment version to 2.16.0.0 |

### Release Notes

Release notes additions documenting changes for v2.16.0:

| Repository | PR | Description |
|------------|-----|-------------|
| alerting | [#1619](https://github.com/opensearch-project/alerting/pull/1619) | Added 2.16 release notes |
| alerting | [#1019](https://github.com/opensearch-project/alerting/pull/1019) | Added v2.16 release notes |
| common-utils | [#700](https://github.com/opensearch-project/common-utils/pull/700) | Added 2.16.0.0 release notes |
| notifications | [#227](https://github.com/opensearch-project/notifications/pull/227) | 2.16 release notes |
| notifications | [#935](https://github.com/opensearch-project/notifications/pull/935) | Add 2.16.0 release notes |
| security | [#1196](https://github.com/opensearch-project/security/pull/1196) | Added 2.16.0 release notes |
| security | [#1087](https://github.com/opensearch-project/security/pull/1087) | Added v2.16 release notes |
| dashboards-reporting | [#380](https://github.com/opensearch-project/dashboards-reporting/pull/380) | Adding 2.16.0 release notes |

### Java Version Upgrades

Some plugins upgraded their Java version from 11 to 21:

| Repository | PR | Description |
|------------|-----|-------------|
| reporting | [#1014](https://github.com/opensearch-project/reporting/pull/1014) | Bump java to 21 |
| observability | [#1940](https://github.com/opensearch-project/observability/pull/1940) | Updated java version from 11 to 21 |

## Limitations

None - these are routine maintenance changes.

## References

### Pull Requests

| PR | Repository | Type |
|----|------------|------|
| [#1014](https://github.com/opensearch-project/reporting/pull/1014) | reporting | Java upgrade |
| [#2743](https://github.com/opensearch-project/sql/pull/2743) | sql | Version bump |
| [#1619](https://github.com/opensearch-project/alerting/pull/1619) | alerting | Release notes |
| [#1019](https://github.com/opensearch-project/alerting/pull/1019) | alerting | Release notes |
| [#700](https://github.com/opensearch-project/common-utils/pull/700) | common-utils | Release notes |
| [#227](https://github.com/opensearch-project/notifications/pull/227) | notifications | Release notes |
| [#935](https://github.com/opensearch-project/notifications/pull/935) | notifications | Release notes |
| [#1196](https://github.com/opensearch-project/security/pull/1196) | security | Release notes |
| [#1087](https://github.com/opensearch-project/security/pull/1087) | security | Release notes |
| [#1940](https://github.com/opensearch-project/observability/pull/1940) | observability | Java upgrade |
| [#1589](https://github.com/opensearch-project/alerting/pull/1589) | alerting | Version bump |
| [#1009](https://github.com/opensearch-project/alerting/pull/1009) | alerting | Version bump |
| [#978](https://github.com/opensearch-project/alerting/pull/978) | alerting | Version bump |
| [#769](https://github.com/opensearch-project/anomaly-detection/pull/769) | anomaly-detection | Version bump |
| [#586](https://github.com/opensearch-project/asynchronous-search/pull/586) | asynchronous-search | Version bump |
| [#688](https://github.com/opensearch-project/common-utils/pull/688) | common-utils | Version bump |
| [#216](https://github.com/opensearch-project/notifications/pull/216) | notifications | Version bump |
| [#224](https://github.com/opensearch-project/notifications/pull/224) | notifications | Version bump |
| [#366](https://github.com/opensearch-project/reporting/pull/366) | reporting | Version bump |
| [#375](https://github.com/opensearch-project/dashboards-reporting/pull/375) | dashboards-reporting | Version bump |
| [#380](https://github.com/opensearch-project/dashboards-reporting/pull/380) | dashboards-reporting | Release notes |
| [#1187](https://github.com/opensearch-project/index-management/pull/1187) | index-management | Version bump |
| [#1089](https://github.com/opensearch-project/index-management/pull/1089) | index-management | Version bump |
| [#638](https://github.com/opensearch-project/job-scheduler/pull/638) | job-scheduler | Version bump |
| [#335](https://github.com/opensearch-project/ml-commons/pull/335) | ml-commons | Version bump |
