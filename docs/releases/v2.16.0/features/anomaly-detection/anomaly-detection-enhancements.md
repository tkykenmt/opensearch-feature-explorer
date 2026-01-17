---
tags:
  - anomaly-detection
---
# Anomaly Detection Enhancements

## Summary

OpenSearch 2.16.0 includes enhancements to the Anomaly Detection plugin focused on improving feature sparsity validation, interval recommendation accuracy, and code coverage infrastructure.

## Details

### What's New in v2.16.0

#### Feature Filtering in Model Validation (PR #1258)

Previously, the anomaly detection plugin used date histogram aggregation for feature sparsity validation and interval recommendation. However, features can have their own filters in addition to the detector's filter, which could cause incorrect interval recommendations and make it difficult to identify if feature definitions themselves were causing data sparsity.

This enhancement integrates feature aggregation into the sparsity validation and interval recommendation processes. When a feature is defined, the plugin now uses date range aggregation (consistent with cold start methodology) to ensure accurate data retrieval and sparsity verification.

**Key Changes:**

- **Feature Sparsity Validation**: Integrated feature aggregation in sparsity validation and interval recommendation
- **AggregationPrep Class**: New class replacing `HistogramAggregationHelper`, supporting both histogram and date_range aggregations
- **Top Entities Retrieval Logic**: Improved `LatestTimeRetriever` to retrieve latest time first, then fetch top entities based on this time (increases likelihood of obtaining top entities when window delay is high)
- **Bug Fix**: Fixed issue in `ModelValidationActionHandler` where missing colons in messages caused index out of bounds exception
- **Bucket Coverage Rate**: Updated `getNumberOfSamples` to limit data queries to `config.getHistoryIntervals()`, improving accuracy of bucket coverage rate calculations

#### BWC Test Version Update and Code Coverage (PR #1253)

- Updated BWC (Backward Compatibility) test version to 2.16
- Added new integration and unit tests to enhance code coverage (increased from 71.83% to 77.05%)
- Fixed issue where integration tests were not being counted towards coverage
- Upgraded codecov GitHub Action from v3 to v4
- Limited coverage upload to macOS environment to avoid redundant uploads

### Technical Changes

#### New/Modified Classes

| Class | Change |
|-------|--------|
| `AggregationPrep` | New class for histogram and date_range aggregations |
| `SearchFeatureDao` | Added methods for cold start sample parsing and train sample ranges |
| `ModelColdStart` | Refactored to use `SearchFeatureDao.getTrainSampleRanges()` |
| `IntervalCalculation` | Simplified to use `AggregationPrep` |
| `LatestTimeRetriever` | Changed to retrieve latest time before top entities |
| `ModelValidationActionHandler` | Added feature filtering support |

#### Removed Classes

| Class | Reason |
|-------|--------|
| `HistogramAggregationHelper` | Replaced by `AggregationPrep` |

## Limitations

- The feature filtering enhancement requires features to be properly defined with valid aggregation queries
- Bucket coverage rate calculations are now limited to `config.getHistoryIntervals()` which may affect detectors with very limited historical data

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1258](https://github.com/opensearch-project/anomaly-detection/pull/1258) | Add Feature Filtering in Model Validation | - |
| [#1253](https://github.com/opensearch-project/anomaly-detection/pull/1253) | Update BWC Test Version and Enhance Code Coverage | - |

### Documentation

- [Anomaly Detection](https://docs.opensearch.org/2.16/observing-your-data/ad/index/)
- [Anomaly Detection API](https://docs.opensearch.org/2.16/observing-your-data/ad/api/)
