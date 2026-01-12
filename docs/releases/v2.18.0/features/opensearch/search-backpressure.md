---
tags:
  - search
---

# Search Backpressure Validation

## Summary

This release adds validation for search backpressure cancellation settings (`cancellation_rate`, `cancellation_ratio`, `cancellation_burst`) to prevent cluster crashes when updating these settings to invalid values. Previously, setting these values to 0 or updating `cancellation_burst` to a non-default value could crash the cluster.

## Details

### What's New in v2.18.0

This release fixes a critical bug where updating certain search backpressure settings could crash the cluster:

1. **Bug Fix**: Setting `cancellation_burst` to a non-default value caused cluster crash because `cancellationRate` was always 0 when passed to `SearchBackpressureState`
2. **Validation Added**: `cancellation_rate` and `cancellation_ratio` now validate that values must be greater than 0
3. **New Setting API**: Added `Setting.doubleSetting()` overloads that accept custom validators

### Technical Changes

#### Root Cause

The `SearchBackpressureState` constructor was not receiving the `cancellationRate` value from cluster settings. When `cancellation_burst` was updated, the `TokenBucket` constructor threw an exception because `rate must be greater than zero`.

#### Fix Implementation

1. **SearchBackpressureState.java**: Added `cancellationRate` parameter to constructor and properly initialized the field
2. **SearchBackpressureService.java**: Now passes `getCancellationRate()` to `SearchBackpressureState` constructor
3. **Setting.java**: Added new `doubleSetting()` methods with `Validator<Double>` parameter support

#### New Validation Rules

| Setting | Validation |
|---------|------------|
| `search_backpressure.cancellation_rate` | Must be > 0 |
| `search_backpressure.cancellation_ratio` | Must be > 0 and <= 1.0 |
| `search_backpressure.search_task.cancellation_rate` | Must be > 0 |
| `search_backpressure.search_task.cancellation_ratio` | Must be > 0 and <= 1.0 |
| `search_backpressure.search_shard_task.cancellation_rate` | Must be > 0 |
| `search_backpressure.search_shard_task.cancellation_ratio` | Must be > 0 and <= 1.0 |

### Usage Example

```bash
# These settings now work correctly
PUT _cluster/settings
{
  "transient": {
    "search_backpressure.search_task.cancellation_burst": 11,
    "search_backpressure.search_task.cancellation_rate": 0.1,
    "search_backpressure.search_task.cancellation_ratio": 0.2
  }
}

# Invalid values now return proper validation errors instead of crashing
PUT _cluster/settings
{
  "transient": {
    "search_backpressure.search_task.cancellation_rate": 0.0
  }
}
# Returns: "search_backpressure.search_task.cancellation_rate must be > 0"
```

### Migration Notes

- No migration required
- Clusters that previously crashed due to invalid settings will now properly reject invalid values with clear error messages
- Existing valid configurations are unaffected

## Limitations

- The fix is included in v2.18.0 and later versions
- Clusters running earlier versions should avoid setting `cancellation_burst` to non-default values

## References

### Documentation
- [Search Backpressure Documentation](https://docs.opensearch.org/2.18/tuning-your-cluster/availability-and-recovery/search-backpressure/): Official documentation
- [Forum Post](https://forum.opensearch.org/t/unable-to-start-opensearch-loop-failed-to-apply-settings-and-rate-must-be-greater-than-zero/20908): Original bug report

### Pull Requests
| PR | Description |
|----|-------------|
| [#15501](https://github.com/opensearch-project/OpenSearch/pull/15501) | Add validation for the search backpressure cancellation settings |

### Issues (Design / RFC)
- [Issue #15495](https://github.com/opensearch-project/OpenSearch/issues/15495): [BUG] Updating some search backpressure settings crash the cluster

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/opensearch-search-backpressure.md)
