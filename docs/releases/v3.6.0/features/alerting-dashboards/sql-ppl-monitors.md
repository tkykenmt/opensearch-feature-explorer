---
tags:
  - alerting-dashboards
---
# SQL/PPL Monitors

## Summary
In v3.6.0, the lookback window feature for PPL/SQL monitors was moved from the OpenSearch Alerting backend to the Alerting Dashboards frontend. This gives users direct control over time-range filtering in the monitor creation UI, adds frontend validation, and injects time filters into PPL queries at preview and execution time.

## Details

### What's New in v3.6.0

The lookback window logic was previously handled entirely by the Alerting backend (`PPLSQLMonitorRunner.kt`, `TransportIndexMonitorV2Action.kt`). This release migrates three key pieces to the frontend:

1. Timestamp field validation — previously `TransportIndexMonitorV2Action.checkPplQueryIndicesForTimestampField`
2. Basic validation — lookback window bounds checking (min 1 minute, max 7 days / 10,080 minutes)
3. Time filter injection — previously `PPLSQLMonitorRunner.addTimeFilter`, now `addTimeFilterToQuery()` in the frontend

### Technical Changes

- `addTimeFilterToQuery()` injects a `| where {timestampField} > TIMESTAMP('{start}') and {timestampField} < TIMESTAMP('{end}')` clause before the first pipe in the PPL query
- `computeLookBackMinutes()` converts the user-specified lookback amount and unit (minutes/hours/days) into total minutes
- Lookback window metadata is now persisted in `ui_metadata.lookback` on the monitor object, storing `enabled`, `minutes`, `timestamp_field`, `amount`, and `unit`
- Maximum lookback window enforced at 7 days (`LOOKBACK_WINDOW_MAX_MINUTES = 10080`)
- Time filter injection applied in monitor preview, trigger preview, and trigger configuration flows
- Monitor details view reads lookback metadata from `ui_metadata.lookback` as a fallback when `look_back_window_minutes` is not set

### Changed Files

| Area | Files |
|------|-------|
| Monitor creation | `PplAlertingCreateMonitor.js` |
| Helper functions | `pplAlertingHelpers.js` (new: `addTimeFilterToQuery`, `computeLookBackMinutes`) |
| Constants | `constants.js` (`LOOKBACK_WINDOW_MAX_MINUTES`) |
| Formik mapping | `pplAlertingMonitorToFormik.js`, `pplFormikToMonitor.js` |
| Trigger config | `ConfigureTriggersPpl.js`, `CreateTriggerPpl.js` |
| Monitor details | `MonitorDetailsV2.js`, `getOverviewStatsV2.js` |
| Tests | `pplAlertingHelpers.test.js` (new, 157 lines) |

## Limitations
- Maximum lookback window is 7 days (10,080 minutes)
- Time filter injection uses simple string replacement on the first `|` character, which may not handle all edge cases in complex PPL queries

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| `https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1379` | Lookback window frontend for PPL/SQL monitors | - |

### Related PRs (Backend)
| PR | Description |
|----|-------------|
| `https://github.com/opensearch-project/alerting/pull/1960` | PPL Alerting: Execute Monitor and Monitor Stats |
| `https://github.com/opensearch-project/alerting/pull/1961` | PPL Alerting: Create and Update Monitor V2 |
| `https://github.com/opensearch-project/alerting/pull/1955` | PPL Alerting: Models |
