# Anomaly Detection Enhancements

## Summary

This release includes fixes to the real-time inference logic and standardizes the config index mapping field naming convention. The inference logic fix addresses an issue where anomaly detection was skipping inference excessively, and the mapping change ensures consistency with OpenSearch naming conventions.

## Details

### What's New in v2.17.0

#### Inference Logic Fix

The `RealTimeInferencer` component had an issue where inference was being skipped more often than intended. The root cause was that the `lastUsedTime` field was being updated whenever the model state was retrieved from the cache (via `PriorityCache.get`), not just when actual inference occurred.

**Problem**: When checking if inference should be skipped for the current interval, the code compared `curExecutionEnd` against `lastUsedTime`. Since `lastUsedTime` was updated on cache retrieval, this caused false positives where inference was incorrectly skipped.

**Solution**: Introduced a new field `lastSeenExecutionEndTime` in `ModelState` that specifically tracks when a sample was last processed during inference (not training). This provides accurate control over when inference should be skipped.

#### Config Index Mapping Standardization

Changed the field name `defaultFill` to `default_fill` in the imputation option configuration to follow the underscore naming convention used throughout OpenSearch.

**Affected files:**
- `src/main/resources/mappings/config.json`
- `src/main/java/org/opensearch/timeseries/dataprocessor/ImputationOption.java`

#### Improved Null Checks for Imputation

Added comprehensive null checks for the `defaultFill` field in the `Config` constructor to handle edge cases:

1. **Case 1**: `enabledFeatures == null && defaultFill != null` - Returns validation error
2. **Case 2**: `enabledFeatures != null && defaultFill == null/empty` - Returns validation error  
3. **Case 3**: `enabledFeatures.size() != defaultFill.size()` - Returns validation error with detailed message

### Technical Changes

#### New Components

| Component | Description |
|-----------|-------------|
| `lastSeenExecutionEndTime` | New field in `ModelState` tracking last inference execution time |

#### Modified Components

| Component | Change |
|-----------|--------|
| `RealTimeInferencer.tryProcess()` | Uses `lastSeenExecutionEndTime` instead of `lastUsedTime` for skip logic |
| `ModelManager.score()` | Sets `lastSeenExecutionEndTime` after scoring |
| `ModelState` | Added `lastSeenExecutionEndTime` field with getter/setter |
| `ImputationOption` | Changed `DEFAULT_FILL_FIELD` constant from `"defaultFill"` to `"default_fill"` |
| `Config` | Enhanced validation logic for imputation options |

#### Configuration Changes

| Setting | Old Value | New Value |
|---------|-----------|-----------|
| Imputation default fill field | `defaultFill` | `default_fill` |

### Usage Example

When using fixed value imputation, the field name has changed:

**Before (v2.16.x and earlier):**
```json
{
  "imputation_option": {
    "method": "fixed_values",
    "defaultFill": [
      {"feature_name": "feature1", "data": 1.0}
    ]
  }
}
```

**After (v2.17.0+):**
```json
{
  "imputation_option": {
    "method": "fixed_values",
    "default_fill": [
      {"feature_name": "feature1", "data": 1.0}
    ]
  }
}
```

### Migration Notes

- **Breaking Change**: The `defaultFill` field in imputation options has been renamed to `default_fill`. Existing detector configurations using fixed value imputation will need to be updated.
- Detectors created before v2.17.0 with `defaultFill` may need to be recreated or updated via the API.

## Limitations

- The field name change is a breaking change for existing configurations using fixed value imputation
- Existing detectors with the old field name may not work correctly until updated

## References

### Documentation
- [Anomaly Detection Documentation](https://docs.opensearch.org/2.17/observing-your-data/ad/index/): Official documentation
- [Imputation Options](https://docs.opensearch.org/2.17/observing-your-data/ad/index/#setting-an-imputation-option): Imputation configuration guide

### Pull Requests
| PR | Description |
|----|-------------|
| [#1284](https://github.com/opensearch-project/anomaly-detection/pull/1284) | Fix inference logic and standardize config index mapping |

## Related Feature Report

- [Full feature documentation](../../../features/anomaly-detection/anomaly-detection.md)
