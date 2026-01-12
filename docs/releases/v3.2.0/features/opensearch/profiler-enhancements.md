---
tags:
  - indexing
  - search
---

# Profiler Enhancements

## Summary

This release fixes a bug in the Profile API where timing values were incorrectly displayed when using concurrent segment search. The profiler was showing extremely large values (representing start times instead of durations) for timing types that were never invoked on certain slices.

## Details

### What's New in v3.2.0

Fixed incorrect timing calculations in `ConcurrentQueryProfileBreakdown` when concurrent segment search is enabled. The bug caused timing types with zero invocations to display incorrect values in the profile output.

### Technical Changes

#### Bug Description

When running queries with the `profile` flag and concurrent segment search enabled, certain timing values in the breakdown were incorrectly large. For example:

```json
"next_doc": 221024744949916,
"advance": 221024744964625,
"score": 221024744964166
```

These values should have been `0` since the timers were never invoked.

#### Root Cause

The issue occurred in `ConcurrentQueryProfileBreakdown.buildQueryBreakdownMap()` at line 342. When computing min/max start/end times across slices for a timing type:

1. A timer for a particular slice had `count = 0` (never invoked)
2. The code still tried to use that slice's timing data
3. When the minimum start time was computed, a slice with `count = 0` had `startTime = 0`
4. This `0` became the minimum, making the duration calculation `endTime - 0 = endTime` (the raw nanosecond timestamp)

#### Fix Applied

The fix adds a check to skip slices where the timer was never invoked (`count = 0`) when computing start/end times:

```java
// only modify the start/end time of the TimingType if the slice used the timer
if (sliceBreakdownTypeCount > 0L) {
    // query start/end time for a TimingType is min/max of start/end time across slices
    queryTimingTypeEndTime = Math.max(
        queryTimingTypeEndTime,
        sliceBreakdown.getValue().getOrDefault(sliceEndTimeForTimingType, Long.MIN_VALUE)
    );
    queryTimingTypeStartTime = Math.min(
        queryTimingTypeStartTime,
        sliceBreakdown.getValue().getOrDefault(sliceStartTimeForTimingType, Long.MAX_VALUE)
    );
    queryTimingTypeCount += sliceBreakdownTypeCount;
}
```

Additionally, the final duration calculation now returns `0` when no invocations occurred:

```java
queryBreakdownMap.put(timingTypeKey, (queryTimingTypeCount > 0L) ? queryTimingTypeEndTime - queryTimingTypeStartTime : 0L);
```

### Usage Example

After the fix, profiling with concurrent segment search returns correct values:

```bash
# Enable concurrent segment search
curl -XPUT "http://localhost:9200/myindex/_settings" -H 'Content-Type: application/json' -d'
{
    "index.search.concurrent_segment_search.mode": "all"
}
'

# Run profiled query
curl -XGET "http://localhost:9200/myindex/_search" -H 'Content-Type: application/json' -d'
{
  "profile": true,
  "query": {
    "match": { "field": "value" }
  }
}
'
```

Timing types that were never invoked now correctly show `0` instead of large incorrect values.

## Limitations

- This fix only affects concurrent segment search profiling
- Non-concurrent search profiling was not affected by this bug

## References

### Documentation
- [Profile API Documentation](https://docs.opensearch.org/3.0/api-reference/search-apis/profile/): Official documentation
- [Concurrent Segment Search](https://docs.opensearch.org/3.0/search-plugins/concurrent-segment-search/): Feature documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#18540](https://github.com/opensearch-project/OpenSearch/pull/18540) | Fix concurrent timings in profiler |

### Issues (Design / RFC)
- [Issue #18534](https://github.com/opensearch-project/OpenSearch/issues/18534): Bug report - Profile timings incorrect for concurrent segments

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/opensearch-profiler.md)
