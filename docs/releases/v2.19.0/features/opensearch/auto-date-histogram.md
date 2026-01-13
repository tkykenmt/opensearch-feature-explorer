---
tags:
  - opensearch
---
# Auto Date Histogram Bug Fix

## Summary

Fixed an assertion failure in the `auto_date_histogram` aggregation that occurred when using the `time_zone` parameter with certain data distributions. The bug caused clusters running with assertions enabled to crash when the filter rewrite optimization interacted with timezone-aware rounding.

## Details

### What's New in v2.19.0

The fix ensures that the filter rewrite optimization path correctly handles timezone-aware rounding by:

1. Preventing `preparedRounding` from shrinking during segment collection
2. Excluding non-UTC timezones from the filter rewrite optimization path
3. Adding proper bounds checking for timezone transitions (e.g., daylight saving time)

### Technical Changes

The `auto_date_histogram` aggregation uses a filter rewrite optimization that pre-aggregates document counts from BKD tree structures instead of collecting documents individually. This optimization updates the `preparedRounding` based on segment min/max values.

The bug occurred when:
- Documents were indexed one-by-one (creating multiple segments)
- A non-UTC timezone was specified (e.g., `America/New_York`)
- The timezone crossed transitions like daylight saving time

In this scenario, the prepared rounding could shrink between segments, causing bucket keys from previous segments to fall outside the bounds of the newly prepared rounding structure.

#### Key Code Changes

| File | Change |
|------|--------|
| `Rounding.java` | Added `isUTC()` method to check timezone |
| `AutoDateHistogramAggregator.java` | Ensured `preparedRounding` never shrinks; added detailed comments |
| `DateHistogramAggregatorBridge.java` | Added UTC check to disable optimization for non-UTC timezones |
| `CompositeAggregator.java` | Added UTC check for composite aggregation date histogram source |

### Affected Aggregations

- `auto_date_histogram` with `time_zone` parameter
- `date_histogram` with `time_zone` parameter (via filter rewrite)
- `composite` aggregation with date histogram source and timezone

## Limitations

- The filter rewrite optimization is now disabled for non-UTC timezones, which may result in slightly slower performance for timezone-aware date histogram queries
- This is a trade-off for correctness over performance

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#17023](https://github.com/opensearch-project/OpenSearch/pull/17023) | Fix auto date histogram rounding assertion bug | [#16932](https://github.com/opensearch-project/OpenSearch/issues/16932) |

### Documentation
- [Auto-interval date histogram](https://docs.opensearch.org/2.19/aggregations/bucket/auto-interval-date-histogram/)
