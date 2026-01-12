# Anomaly Detection Bugfixes

## Summary

OpenSearch v2.17.0 includes four important bugfixes for the Anomaly Detection plugin, addressing issues with real-time/historical task management, null aggregation value handling, and Dashboards data source integration. These fixes improve stability when running mixed real-time and historical analyses and resolve UI issues in multi-data-source environments.

## Details

### What's New in v2.17.0

This release focuses on stability improvements and bug fixes across both the backend anomaly-detection plugin and the anomaly-detection-dashboards-plugin.

### Technical Changes

#### Real-time and Historical Task Flag Management

**Problem**: When starting a historical analysis after a real-time analysis on the same detector, the real-time task's `is_latest` flag was incorrectly reset to `false` by the historical run.

**Solution**: The fix ensures that only the latest flags of the same analysis type are reset:
- Real-time analysis only resets the latest flag of previous real-time analyses
- Historical analysis only resets the latest flag of previous historical analyses

**Changed Files**:
- `ADTaskManager.java`: Simplified `getTaskTypes()` method to return task types based on date range without the `resetLatestTaskStateFlag` parameter
- `TaskManager.java`: Updated query filter to reset only same-type task flags
- `ForecastTaskManager.java`: Updated method signature for consistency

**Additional Changes in PR #1287**:
- Set minimum `recencyEmphasis` value to 2 to align with RCF (Random Cut Forest) requirements
- Updated imputation logic to execute only when the entity maps to the local node ID in the hash ring, reducing errors when models exist on multiple nodes

#### Null Max Aggregation Value Handling

**Problem**: When the max aggregation in SearchResponse returned a null value, it was converted to a negative number (`-9223372036854775808`), leading to erroneous timestamps and parse errors.

**Solution**: Added validation to ensure only valid positive aggregation values are considered for timestamps.

```java
// Before: Could return invalid negative values
.map(agg -> (long) agg.getValue());

// After: Filters out null/invalid values
.filter(agg -> agg != null && agg.getValue() > 0)
.map(agg -> (long) agg.getValue());
```

**Error Before Fix**:
```
OpenSearchParseException[failed to parse date field [-9223372036854775808] 
with format [strict_date_optional_time||epoch_millis]]
```

**Response After Fix**:
```json
{
  "model": {
    "time_field": {
      "message": "There isn't enough historical data found with current timefield selected."
    }
  }
}
```

#### DataSourceView Integration Fix

**Problem**: DataSourceView was broken on future playground and TrineoApp environments under OpenSearch 2.16, though no console/network errors were shown. The issue was caused by `dataSourceFilter` filtering out the version, causing DataSourceView to error with "cannot find data source".

**Solution**: Removed the `dataSourceFilter` check from all DataSourceView usage in the Anomaly Detection Dashboards plugin, as the scenarios where AD uses DataSourceView don't require data source filtering.

**Changed Files**:
- `ConfigureModel.tsx`
- `DefineDetector.tsx`
- `DetectorDetail.tsx`
- `DetectorJobs.tsx`
- `ReviewAndCreate.tsx`

#### DataSourceId URL Parameter Fix

**Problem**: The `dataSourceId` was not showing in the URL on the Overview landing page when using multi-data-source environments.

**Solution**: Fixed the condition check in `AnomalyDetectionOverview.tsx` to properly update URL parameters with the selected data source ID.

```typescript
// Before: Only updated when landingDataSourceId was defined
if (dataSourceEnabled && props.landingDataSourceId !== undefined) {

// After: Updates whenever dataSourceEnabled is true
if (dataSourceEnabled) {
```

### Usage Example

After these fixes, you can safely run historical analysis after real-time analysis without affecting the real-time task state:

```json
// Start real-time detection
POST _plugins/_anomaly_detection/detectors/<detector_id>/_start

// Later, start historical analysis - won't affect real-time task's is_latest flag
POST _plugins/_anomaly_detection/detectors/<detector_id>/_start
{
  "start_time": 1633048868000,
  "end_time": 1633394468000
}
```

## Limitations

- The `recencyEmphasis` parameter now requires a minimum value of 2 (previously allowed 1)
- DataSourceView no longer filters data sources by version compatibility in AD plugin

## References

### Documentation
- [Anomaly Detection Documentation](https://docs.opensearch.org/2.17/observing-your-data/ad/index/): Official documentation
- [Anomaly Detection API](https://docs.opensearch.org/2.17/observing-your-data/ad/api/): API reference

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#1287](https://github.com/opensearch-project/anomaly-detection/pull/1287) | anomaly-detection | Prevent resetting latest flag of real-time when starting historical analysis |
| [#1292](https://github.com/opensearch-project/anomaly-detection/pull/1292) | anomaly-detection | Correct handling of null max aggregation values in SearchResponse |
| [#828](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/828) | anomaly-detection-dashboards-plugin | Fix dataSourceId not showing in URL on Overview landing page |
| [#837](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/837) | anomaly-detection-dashboards-plugin | Remove dataSourceFilter that breaks DataSourceView |

## Related Feature Report

- [Full feature documentation](../../../../features/anomaly-detection/anomaly-detection.md)
