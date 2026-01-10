# Version Bumps & Maintenance

## Summary

Routine version increment PRs across 12 OpenSearch plugin repositories to prepare for the v2.18.0 release. These PRs update version numbers in build configurations and add release notes.

## Details

### What's New in v2.18.0

Standard release preparation activities including:

- Version number increments to `2.18.0.0` or `2.18.0-SNAPSHOT`
- Release notes additions for v2.18.0
- Backward compatibility version bumps after v2.17 release

### Repositories Updated

| Repository | PRs | Changes |
|------------|-----|---------|
| security | #1205 | Added 2.18.0 release notes |
| k-nn | #2181 | Fix sed command in DEVELOPER_GUIDE.md |
| dashboards-alerting | #315, #1098 | Version increment to 2.18.0.0 |
| alerting | #1653 | Version increment to 2.18.0-SNAPSHOT |
| anomaly-detection | #877 | Version increment to 2.18.0.0 |
| asynchronous-search | #615 | Version increment to 2.18.0 |
| common-utils | #729 | Version increment to 2.18.0-SNAPSHOT |
| dashboards-notifications | #278, #445, #396, #398 | Version increment and release notes |
| index-management | #1241, #1259, #1180 | Version increment and BWC bump |
| job-scheduler | #676 | Version increment to 2.18.0 |
| dashboards-ml-commons | #370 | Version increment to 2.18.0.0 |
| notifications | #957 | Version increment to 2.18.0-SNAPSHOT |
| dashboards-reporting | #1037 | Version increment to 2.18.0-SNAPSHOT |

## Limitations

These are routine maintenance PRs with no functional changes.

## Related PRs

| PR | Repository | Description |
|----|------------|-------------|
| [#1205](https://github.com/opensearch-project/security/pull/1205) | security | Added 2.18.0 release notes |
| [#2181](https://github.com/opensearch-project/k-NN/pull/2181) | k-nn | Fix sed command in DEVELOPER_GUIDE.md |
| [#315](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/315) | dashboards-alerting | Version increment |
| [#1653](https://github.com/opensearch-project/alerting/pull/1653) | alerting | Version increment |
| [#1098](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1098) | dashboards-alerting | Version increment |
| [#877](https://github.com/opensearch-project/anomaly-detection/pull/877) | anomaly-detection | Version increment |
| [#615](https://github.com/opensearch-project/asynchronous-search/pull/615) | asynchronous-search | Version increment |
| [#729](https://github.com/opensearch-project/common-utils/pull/729) | common-utils | Version increment |
| [#278](https://github.com/opensearch-project/dashboards-notifications/pull/278) | dashboards-notifications | Version increment |
| [#445](https://github.com/opensearch-project/dashboards-notifications/pull/445) | dashboards-notifications | Version increment |
| [#396](https://github.com/opensearch-project/dashboards-notifications/pull/396) | dashboards-notifications | Version increment |
| [#398](https://github.com/opensearch-project/dashboards-notifications/pull/398) | dashboards-notifications | Release notes |
| [#1241](https://github.com/opensearch-project/index-management/pull/1241) | index-management | Version increment |
| [#1259](https://github.com/opensearch-project/index-management/pull/1259) | index-management | BWC version bump |
| [#1180](https://github.com/opensearch-project/index-management/pull/1180) | index-management | Version increment |
| [#676](https://github.com/opensearch-project/job-scheduler/pull/676) | job-scheduler | Version increment |
| [#370](https://github.com/opensearch-project/ml-commons-dashboards/pull/370) | dashboards-ml-commons | Version increment |
| [#957](https://github.com/opensearch-project/notifications/pull/957) | notifications | Version increment |
| [#1037](https://github.com/opensearch-project/dashboards-reporting/pull/1037) | dashboards-reporting | Version increment |

## References

- [GitHub Issue #611](https://github.com/tkykenmt/opensearch-feature-explorer/issues/611): Investigation tracking issue
