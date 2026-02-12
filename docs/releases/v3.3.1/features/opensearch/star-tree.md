---
tags:
  - opensearch
---
# Star Tree Bug Fix: Sub-Aggregator Casting with Profile

## Summary

Fixed a `ClassCastException` that occurred when running star-tree aggregation queries with `profile=true`. The bug was caused by sub-aggregators being wrapped in `ProfilingAggregator`, which could not be directly cast to `StarTreePreComputeCollector`. The fix introduces an `unwrapAggregator()` method on the base `Aggregator` class to safely unwrap profiling wrappers before casting.

## Details

### What's New in v3.3.1

When search profiling is enabled (`"profile": true`), OpenSearch wraps aggregators in `ProfilingAggregator` to collect timing metrics. Star-tree bucket aggregators (terms, date histogram, range, multi-terms) cast their sub-aggregators to `StarTreePreComputeCollector` to set up star-tree bucket collectors. This cast failed when the sub-aggregator was wrapped in `ProfilingAggregator`.

### Technical Changes

A new `unwrapAggregator()` method was added to the base `Aggregator` class. By default it returns `this`, but `ProfilingAggregator` overrides it to return the delegate aggregator. This replaces the previous static `ProfilingAggregator.unwrap()` utility method with a polymorphic approach.

Affected aggregators updated to use `aggregator.unwrapAggregator()` before casting:
- `DateHistogramAggregator`
- `RangeAggregator`
- `GlobalOrdinalsStringTermsAggregator`
- `NumericTermsAggregator`
- `MultiTermsAggregator`

Additionally, `AggregationPath.resolveTopmostAggregator()` and `FlushModeResolver.getChildren()` were refactored to use the new `unwrapAggregator()` method instead of the removed static utility.

### Error Before Fix

```json
{
  "reason": {
    "type": "class_cast_exception",
    "reason": "class org.opensearch.search.profile.aggregation.ProfilingAggregator cannot be cast to class org.opensearch.search.aggregations.StarTreePreComputeCollector"
  }
}
```

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#19652](https://github.com/opensearch-project/OpenSearch/pull/19652) | Fix sub-aggregator casting for search with profile=true | [#19649](https://github.com/opensearch-project/OpenSearch/issues/19649) |
