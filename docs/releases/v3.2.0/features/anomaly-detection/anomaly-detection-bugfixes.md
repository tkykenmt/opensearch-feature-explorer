# Anomaly Detection Bugfixes

## Summary

OpenSearch v3.2.0 includes 10 bug fixes for the Anomaly Detection plugin, addressing concurrency issues in multi-node clusters, forecasting interval calculation problems, UI/UX improvements in the Dashboards plugin, and build infrastructure updates. These fixes improve stability for high-cardinality anomaly detection (HCAD) workloads and enhance the forecasting feature experience.

## Details

### What's New in v3.2.0

This release focuses on stability improvements and bug fixes across both the backend anomaly-detection plugin and the anomaly-detection-dashboards-plugin.

### Technical Changes

#### Backend Fixes (anomaly-detection)

| Fix | Description | Impact |
|-----|-------------|--------|
| Concurrency bug in BatchWorker | Fixed `ConcurrentModificationException` in bulk result handling | Prevents crashes in HCAD multi-node clusters |
| NullPointerException in ADTaskManager | Fixed null `rcfTotalUpdates` handling in `triageState()` | Improves real-time task state management |
| ConcurrentHashMap null key handling | Fixed NPE with null key handling | Prevents unexpected failures |
| Interval calculation search calls | Changed to use `asyncRequestWithInjectedSecurity` | Fixes security context issues |
| Early failure on no shards | Added early failure check for time-bound search | Better error handling |
| Forecast interval exploration | Changed `nextNiceInterval()` comparison from `>=` to `>` | Fixes `suggestForecast` failures on sample data |
| Interval anchoring | Anchor on current time instead of future timestamp | Consistent behavior across forecast modes |

#### Dashboards Fixes (anomaly-detection-dashboards-plugin)

| Fix | Description | Impact |
|-----|-------------|--------|
| Data filter wrapping | Truncate long filters and wrap multiple filters | Fixes "Next" button disappearing |
| Indicator helper text | Corrected forecasting indicator helper text | Better user guidance |
| Zero-value plotting | Explicit null check to avoid skipping 0 values | Accurate chart rendering |
| Absolute date handling | Support for absolute date inputs from date picker | Improved date selection |
| FORECAST_FAILURE state | Allow stopping forecaster from failure state | Better error recovery |
| Ribbon encoding | Fixed encoding issue in contextual launch | Correct navigation |
| Forecaster list fetch | Fetch complete list with explicit `size: MAX_FORECASTER` | Shows all forecasters |
| Delete bug | Fixed delete action using wrong forecaster object | Correct deletion behavior |
| Minimum shingle size | Enforce `min={4}` in SuggestParametersDialog | Prevent invalid configurations |
| Suggest anomaly detector | Restrict to OpenSearch datasets only | Appropriate feature availability |

### Usage Example

No configuration changes required. These fixes are automatically applied when upgrading to v3.2.0.

### Migration Notes

- No breaking changes
- Existing detectors and forecasters continue to work without modification
- Users experiencing HCAD crashes on multi-node clusters should upgrade to resolve concurrency issues

## Limitations

- The forecasting feature remains in active development
- High-cardinality detection still requires sufficient cluster resources

## Related PRs

### Backend (anomaly-detection)

| PR | Description |
|----|-------------|
| [#1508](https://github.com/opensearch-project/anomaly-detection/pull/1508) | Fixing concurrency bug on writer |
| [#1528](https://github.com/opensearch-project/anomaly-detection/pull/1528) | Fix: advance past current interval & anchor on now |
| [#1535](https://github.com/opensearch-project/anomaly-detection/pull/1535) | Changing search calls on interval calculation |
| [#1537](https://github.com/opensearch-project/anomaly-detection/pull/1537) | Bumping gradle and nebula versions |

### Dashboards (anomaly-detection-dashboards-plugin)

| PR | Description |
|----|-------------|
| [#1001](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1001) | Restrict Suggest anomaly detector to only show for OpenSearch datasets |
| [#1054](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1054) | Allow stopping forecaster from FORECAST_FAILURE state and minor cleanups |
| [#1058](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1058) | Improve indicator helper, fix zero-value plotting etc |
| [#1060](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1060) | Wrap data filter in detector creation |
| [#1064](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1064) | Fix ribbon encoding issue in contextual launch |
| [#1068](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1068) | Fix: fetch full forecaster list, and fix delete bug |

## References

- [Anomaly Detection Documentation](https://docs.opensearch.org/3.0/observing-your-data/ad/index/): Official documentation
- [GitHub Issue #715](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/issues/715): Data filter UI issue

## Related Feature Report

- [Full feature documentation](../../../../features/anomaly-detection/anomaly-detection.md)
