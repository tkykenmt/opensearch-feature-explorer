---
tags:
  - alerting
---
# Alerting

## Summary

OpenSearch 2.6.0 introduces 1 new feature(s) and 0 enhancement(s) to Alerting, along with 11 bug fixes.

## Details

### New Features

- **Multiple indices support in DocLevelMonitorInput**: Added in PR #784.

### Bug Fixes

- Added document _id as param for terms query when searching alerts by their ids
- Fix for ERROR alert state generation in doc-level monitors
- ExecuteMonitor inserting metadata doc during dry run
- Adjusting max field index setting dynamically for query index
- Fix setting default title only when no subject has been set
- Minor fix to prevent flaky tests in downstream plugins
- Publish snapshots to maven via GHA
- Added 2.6 release notes.
- Add 2.6.0 release notes.
- Updated MAINTAINERS.md format.
- Bumped version to 2.6.

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#784](https://github.com/opensearch-project/alerting/pull/784) | Multiple indices support in DocLevelMonitorInput | alerting |
| [#753](https://github.com/opensearch-project/alerting/pull/753) | Added document _id as param for terms query when searching alerts by their ids | alerting |
| [#768](https://github.com/opensearch-project/alerting/pull/768) | Fix for ERROR alert state generation in doc-level monitors | alerting |
| [#758](https://github.com/opensearch-project/alerting/pull/758) | ExecuteMonitor inserting metadata doc during dry run | alerting |
| [#776](https://github.com/opensearch-project/alerting/pull/776) | Adjusting max field index setting dynamically for query index | alerting |
| [#750](https://github.com/opensearch-project/alerting/pull/750) | Fix setting default title only when no subject has been set | alerting |
| [#804](https://github.com/opensearch-project/alerting/pull/804) | Minor fix to prevent flaky tests in downstream plugins | alerting |
| [#805](https://github.com/opensearch-project/alerting/pull/805) | Publish snapshots to maven via GHA | alerting |
| [#809](https://github.com/opensearch-project/alerting/pull/809) | Added 2.6 release notes. | alerting |
| [#493](https://github.com/opensearch-project/alerting/pull/493) | Add 2.6.0 release notes. | alerting |
| [#435](https://github.com/opensearch-project/alerting/pull/435) | Updated MAINTAINERS.md format. | alerting |
| [#492](https://github.com/opensearch-project/alerting/pull/492) | Bumped version to 2.6. | alerting |
