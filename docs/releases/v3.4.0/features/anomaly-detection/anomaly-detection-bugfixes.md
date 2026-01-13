---
tags:
  - domain/observability
  - component/server
  - dashboards
  - indexing
  - ml
---
# Anomaly Detection Bugfixes

## Summary

OpenSearch v3.4.0 includes three bugfixes for the Anomaly Detection plugin: a fix for forecast results index creation on 3-AZ domains, improved missing feature data detection that honors detector frequency, and suppression of spurious error toasts when data sources are unavailable.

## Details

### What's New in v3.4.0

This release addresses three distinct issues across the anomaly-detection backend and dashboards plugin:

1. **3-AZ Forecast Results Index Fix** - Resolves index creation failures on domains with 3 availability zones
2. **Detector Frequency-Aware Missing Data Detection** - Prevents false "missing data" warnings when detector frequency differs from detection interval
3. **Data Source Error Toast Suppression** - Eliminates spurious error notifications when remote data sources are unavailable

### Technical Changes

#### 3-AZ Forecast Results Index Fix (PR #1615)

The default forecast results index was created with `number_of_replicas: 1`, giving 2 total copies. On 3-AZ domains with awareness attributes=3, this violated the requirement that total copies must be a multiple of awareness attributes, causing forecaster initialization to fail.

**Before:**
```java
.put(IndexMetadata.SETTING_NUMBER_OF_REPLICAS, 1)
```

**After:**
```java
.put(IndexMetadata.SETTING_AUTO_EXPAND_REPLICAS, customResultIndexAutoExpandReplica)
```

The fix sets `number_of_replicas` to 0 and enables `auto_expand_replicas: "0-2"` for the default forecast results index. Single-AZ domains remain replica-free, while 3-AZ domains automatically allocate 2 replicas (3 total copies), satisfying the awareness constraint.

| Setting | Before | After |
|---------|--------|-------|
| `number_of_replicas` | 1 | 0 |
| `auto_expand_replicas` | Not set | `"0-2"` |

#### Detector Frequency-Aware Missing Data Detection (PR #1116)

When a detector's frequency (execution cadence) differs from its detection interval (data aggregation window), the dashboards plugin incorrectly flagged recent data as "missing" because it didn't account for the frequency delay.

**Changes:**
- Added `detectorFrequency` prop to `FeatureChart` component
- Modified `getFeatureDataPoints()` to skip frequency window when checking for missing data
- Updated `getFeatureMissingDataAnnotations()` to accept frequency parameter
- Adjusted `checkLatestFeatureDataPoints()` to subtract frequency from the poll window

```typescript
// Before: Only considered window delay
let adjustedCurrentTime = moment().subtract(windowDelayInMinutes, 'minutes');

// After: Also considers detector frequency
const minutesToSkip = detectorFrequencyInMin !== detectorIntervalInMin 
  ? detectorFrequencyInMin 
  : detectorIntervalInMin;
let adjustedCurrentTime = moment().subtract(
  windowDelayInMinutes + minutesToSkip, 'minutes'
);
```

#### Data Source Error Toast Suppression (PR #1126)

When multi-data-source is enabled but no local cluster exists, bootstrap API calls fail with "No Living connections". Previously, these errors triggered error toasts on page load.

**New utility function:**
```typescript
export const isNoLivingConnectionsError = (error: any): boolean => {
  return typeof error === 'string' && error.includes('No Living connections');
};
```

Applied to:
- `AssociatedDetectors.tsx`
- `AssociateExisting.tsx`
- `DashboardOverview.tsx`
- `List.tsx`

### Migration Notes

No migration required. These are backward-compatible bugfixes.

## Limitations

- The auto-expand replicas fix only applies to newly created forecast results indices; existing indices are not modified
- The frequency-aware missing data detection requires the detector to have a `frequency` field configured

## References

### Documentation
- [Anomaly Detection Documentation](https://docs.opensearch.org/3.0/observing-your-data/ad/index/): Official documentation
- [Anomaly Detection API](https://docs.opensearch.org/3.0/observing-your-data/ad/api/): API reference

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#1615](https://github.com/opensearch-project/anomaly-detection/pull/1615) | anomaly-detection | Fix auto-expand replicas for default results index on 3AZ domains |
| [#1116](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1116) | anomaly-detection-dashboards-plugin | Honor detector frequency when flagging missing feature data |
| [#1126](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/1126) | anomaly-detection-dashboards-plugin | Address error toast on page open with data source enabled |

## Related Feature Report

- [Full feature documentation](../../../../features/anomaly-detection/anomaly-detection.md)
