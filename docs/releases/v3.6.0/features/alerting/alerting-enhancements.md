---
tags:
  - alerting
---
# Alerting Enhancements

## Summary

OpenSearch v3.6.0 includes a broad set of alerting plugin enhancements spanning configurable trigger limits, bug fixes for monitor execution and notification delivery, cluster metrics input validation, search cancellation improvements, and SDK persistence groundwork. Several changes also landed in the common-utils library. Notably, the experimental PPL alerting feature was removed from the 3.6 release branch pending refactoring for v3.7, and SdkClient integration was merged then reverted during code freeze.

## Details

### What's New in v3.6.0

#### Configurable Max Triggers Per Monitor

The previously hardcoded limit of 10 triggers per monitor is now configurable via a new dynamic cluster setting `plugins.alerting.monitor.max_triggers`. The hardcoded `MONITOR_MAX_TRIGGERS = 10` constant was removed from the `Monitor` data class in common-utils, and validation was moved to `TransportIndexMonitorAction` in the alerting plugin where it reads the cluster setting.

| Setting | Description | Default | Min |
|---------|-------------|---------|-----|
| `plugins.alerting.monitor.max_triggers` | Maximum number of triggers allowed per monitor | 10 | 1 |

#### Search Cancellation Timeout Coverage

`cancelAfterTimeInterval` is now set on all `SearchRequest` constructions across monitor runners. A prior fix (PR #1366) only covered `BucketLevelMonitorRunner` and `DocumentLevelMonitorRunner`. This release extends coverage to:

- `InputService.getSearchRequest()` (used by query-level and bucket-level monitors)
- `InputService.collectInputResultsForADMonitor()` (used by anomaly detection monitors)
- `TransportDocLevelMonitorFanOutAction` (3 search sites: max seq no query, percolate query, shard fetch)

A guard against the `-1` default prevents setting a negative timeout.

#### Cluster Metrics Input Validation

`ClusterMetricsInput.parseInner()` now validates that the user-provided `api_type` matches the type derived from the `path`. Previously, mismatched values (e.g., `api_type: CLUSTER_STATS` with `path: /_cat/indices`) were silently accepted, creating monitors that could not be deleted. A follow-up fix normalizes the URI path during validation to handle missing leading slashes.

#### Bug Fixes

- **SMTP STARTTLS notification failure**: User authentication context is now preserved when stashing thread context during alert notification sending. Previously, `stashContext()` cleared `OPENSEARCH_SECURITY_USER_INFO_THREAD_CONTEXT`, causing SMTP operations to fail with "Can't send command to SMTP host" during scheduled monitor execution (while the ExecuteMonitor API worked correctly).

- **Doc-level monitor NPE with nested fields**: Added null guard in `DocLevelMonitorQueries.traverseMappingsAndUpdate()` for nested field types without sub-properties (e.g., `"http_request_headers": {"type": "nested"}`). These fields are now safely skipped during mapping traversal.

- **JobSweeper fielddata error**: Replaced `FieldSortBuilder("_id")` with `FieldSortBuilder("_seq_no")` in JobSweeper's `search_after` pagination. When `indices.id_field_data.enabled` is false, the sweeper previously failed every cycle with a fielddata access error. `_seq_no` has doc_values enabled by default and is unique per shard.

- **Acknowledge alerts modal stuck loading**: Fixed the acknowledge alerts modal in OpenSearch Dashboards to properly update the table with acknowledged alerts instead of showing a stuck loading state.

- **Anomaly detector monitor definition**: Fixed broken anomaly detector monitor definition method in the OpenSearch UI.

#### Maintenance & Cleanup

- **PPL alerting removal**: Experimental PPL alerting feature assets were removed from the 3.6 release branch. The feature is being refactored and planned for v3.7.
- **Migration log noise**: Verbose "Cancelling the migration process" log output is now limited to only fire when a scheduled migration actually exists, reducing log noise during index creation.
- **Test reliability**: Replaced `Thread.sleep` with `OpenSearchTestCase.waitUntil` in integration tests for more reliable test execution.
- **SdkClient integration (merged then reverted)**: SdkClient was injected into 13 transport actions and the remote metadata SDK client was integrated with the alerting plugin, but these changes were reverted during code freeze (PR #2057). This groundwork is expected in a future release.
- **PPL alerting API refactoring**: PPL alerting APIs were refactored to use v1 endpoints, and legacy/PPL alerting separation was removed.

## Limitations

- The SdkClient/remote metadata SDK integration was reverted and is not available in v3.6.0
- PPL alerting is not available in v3.6.0; it is planned for v3.7

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#2036](https://github.com/opensearch-project/alerting/pull/2036) | Add configurable `plugins.alerting.monitor.max_triggers` cluster setting | [#468](https://github.com/opensearch-project/alerting/issues/468), [#1828](https://github.com/opensearch-project/alerting/issues/1828) |
| [common-utils#913](https://github.com/opensearch-project/common-utils/pull/913) | Remove hardcoded trigger limit from Monitor data class | [#468](https://github.com/opensearch-project/alerting/issues/468) |
| [#2042](https://github.com/opensearch-project/alerting/pull/2042) | Set `cancelAfterTimeInterval` on all remaining SearchRequest constructions | [#827](https://github.com/opensearch-project/alerting/issues/827) |
| [#1738](https://github.com/opensearch-project/alerting/pull/1738) | Limit verbose log output on scheduled migration cancellation | [#1183](https://github.com/opensearch-project/alerting/issues/1183) |
| [common-utils#912](https://github.com/opensearch-project/common-utils/pull/912) | Validate api_type matches path in ClusterMetricsInput | [#1987](https://github.com/opensearch-project/alerting/issues/1987) |
| [common-utils#921](https://github.com/opensearch-project/common-utils/pull/921) | Normalize cluster metrics input URI path during validation |  |
| [#2027](https://github.com/opensearch-project/alerting/pull/2027) | Preserve user auth context when stashing thread context for notifications | [alerting-dashboards#1368](https://github.com/opensearch-project/alerting-dashboards-plugin/issues/1368) |
| [#2049](https://github.com/opensearch-project/alerting/pull/2049) | Fix NPE when nested field type has no properties in doc-level monitor | [security-analytics#1472](https://github.com/opensearch-project/security-analytics/issues/1472) |
| [#2039](https://github.com/opensearch-project/alerting/pull/2039) | Replace `_id` sort with `_seq_no` in JobSweeper | [#2037](https://github.com/opensearch-project/alerting/issues/2037) |
| [#1363](https://github.com/opensearch-project/alerting/pull/1363) | Fix acknowledge alerts modal loading state |  |
| [#1371](https://github.com/opensearch-project/alerting/pull/1371) | Fix anomaly detector monitor definition in UI |  |
| [#2041](https://github.com/opensearch-project/alerting/pull/2041) | Replace Thread.sleep with waitUntil in integration tests |  |
| [#2017](https://github.com/opensearch-project/alerting/pull/2017) | Remove experimental PPL alerting feature assets |  |
| [#2052](https://github.com/opensearch-project/alerting/pull/2052) | Inject SdkClient into transport actions | [#2094](https://github.com/opensearch-project/alerting/issues/2094) |
| [#2047](https://github.com/opensearch-project/alerting/pull/2047) | Integrate remote metadata SDK client with alerting plugin |  |
| [#2057](https://github.com/opensearch-project/alerting/pull/2057) | Revert SdkClient changes merged during code freeze |  |
| [#1378](https://github.com/opensearch-project/alerting/pull/1378) | Refactor PPL alerting APIs to use v1 endpoints |  |
| [#1392](https://github.com/opensearch-project/alerting/pull/1392) | Remove legacy and PPL alerting separation |  |
| [common-utils#916](https://github.com/opensearch-project/common/pull/916) | Add Target object for external data source support |  |
| [common-utils#917](https://github.com/opensearch-project/common/pull/917) | Revert Target object addition |  |
