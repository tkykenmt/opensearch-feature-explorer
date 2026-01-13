---
tags:
  - domain/data
  - component/server
  - indexing
  - observability
  - search
---
# Index Management Enhancements

## Summary

This release includes bug fixes and maintenance updates for the Index Management plugin, including a fix for rollup aggregation reduction when searching across rollup and raw indices together, build fixes for upstream OpenSearch changes, and a dependency update for the 1password/load-secrets-action GitHub Action.

## Details

### What's New in v3.3.0

#### Rollup Aggregation Fix (ScriptedAvg Class)

The main enhancement addresses a bug in the rollup feature when searching rollup and raw indices together (introduced in v2.18.0). The fix uses the `ScriptedAvg` class in `AvgAggregationBuilder` instead of raw double arrays, enabling proper handling during aggregation reduction.

**Problem**: When searching across both rollup and non-rollup indices, a `ClassCastException` occurred during the reduce phase of `InternalValueCount` and `InternalAvg` aggregations because both used `InternalScriptedMetric` internally.

**Solution**: Updated the scripted metric aggregation scripts in `RollupUtils.kt` to use `ScriptedAvg` class for proper type handling:

```kotlin
// Before (v3.2.0 and earlier)
combineScript: "def d = new double[2]; d[0] = state.sums; d[1] = state.counts; return d"
reduceScript: "... for (a in states) { sum += a[0]; count += a[1]; } ..."

// After (v3.3.0)
combineScript: "def d = new org.opensearch.search.aggregations.metrics.ScriptedAvg(state.sums, state.counts); return d"
reduceScript: "... for (a in states) { sum += a.getSum(); count += a.getCount(); } ..."
```

This change depends on OpenSearch core PR [#18411](https://github.com/opensearch-project/OpenSearch/pull/18411) which added support for `InternalScriptedMetric` in `InternalValueCount` and `InternalAvg` reduction.

#### Build Fixes

Updated test infrastructure to accommodate upstream OpenSearch changes:
- Changed `LockService` instantiation in unit tests from direct constructor to mock
- Updated `randomUser()` helper to generate proper custom attribute names format (`key=value`)
- Added `error_prone_annotations` dependency resolution
- Removed deprecated `log4j-core` test dependency

#### Dependency Update

Bumped `1password/load-secrets-action` from v2 to v3 in GitHub Actions workflows. This is a breaking change in the action that sets `export-env` to `false` by default.

### Technical Changes

#### Modified Files

| File | Change |
|------|--------|
| `RollupUtils.kt` | Updated scripted metric scripts to use `ScriptedAvg` class |
| `RollupInterceptorIT.kt` | Added `value_count` aggregation to test coverage |
| `spi/build.gradle` | Added `error_prone_annotations` dependency |
| `TestHelpers.kt` | Updated `randomUser()` for custom attribute format |
| Multiple `*StepTests.kt` | Changed `LockService` to mock |

### Usage Example

Searching across rollup and raw indices with avg aggregation now works correctly:

```json
GET sample-data-*,sample-rollup/_search
{
  "size": 0,
  "aggs": {
    "avg_value": { "avg": { "field": "value" } },
    "sum_value": { "sum": { "field": "value" } },
    "count_value": { "value_count": { "field": "value" } }
  }
}
```

## Limitations

- The rollup aggregation fix requires OpenSearch core v3.3.0+ with the `ScriptedAvg` class support
- Mixed rollup/raw index search still requires `plugins.rollup.search.search_source_indices: true`

## References

### Documentation
- [Index Rollups Documentation](https://docs.opensearch.org/3.3/im-plugin/index-rollups/index/)
- [Index Rollups API](https://docs.opensearch.org/3.3/im-plugin/index-rollups/rollup-api/)
- [OpenSearch PR #18411](https://github.com/opensearch-project/OpenSearch/pull/18411): Core changes for InternalScriptedMetric support in aggregation reduction
- [OpenSearch PR #18288](https://github.com/opensearch-project/OpenSearch/pull/18288): Related aggregation changes

### Pull Requests
| PR | Description |
|----|-------------|
| [#1460](https://github.com/opensearch-project/index-management/pull/1460) | Using Scripted Avg Class in AvgAggregationBuilder in place of double |
| [#1491](https://github.com/opensearch-project/index-management/pull/1491) | Fix the build |
| [#1473](https://github.com/opensearch-project/index-management/pull/1473) | Dependabot: bump 1password/load-secrets-action from 2 to 3 |

## Related Feature Report

- Full feature documentation
