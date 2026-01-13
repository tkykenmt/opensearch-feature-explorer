---
tags:
  - domain/observability
  - component/server
  - dashboards
  - indexing
  - performance
  - search
---
# Query Insights Bug Fixes

## Summary

OpenSearch v3.3.0 includes multiple bug fixes for the Query Insights plugin and its Dashboards component. These fixes address issues with query ID matching, live queries filtering, time range validation, flaky tests, and UI problems in the Configuration page and Top N Queries page.

## Details

### What's New in v3.3.0

This release focuses on stability and correctness improvements across both the backend plugin and the Dashboards UI.

### Technical Changes

#### Backend Plugin Fixes

**Query ID Matching Fix (PR #426)**

Changed from `matchQuery` to `termQuery` for query ID lookups. The previous implementation used `matchQuery` with OR logic, which could return incorrect results when query IDs contained similar numeric patterns (e.g., numbers between dashes). The fix also changes the `id` field mapping from `text` to `keyword` for exact matching.

```java
// Before: matchQuery with OR logic could match similar IDs
QueryBuilders.matchQuery("id", queryId)

// After: termQuery for exact matching
QueryBuilders.termQuery("id", queryId)
```

**Live Queries Shard Task Filtering (PR #420)**

Fixed the Live Queries API to filter out shard-level tasks. Previously, the pattern `indices:data/read/search*` matched both request-level and shard-level tasks. The fix removes the trailing wildcard to only match request-level search tasks.

```java
// Before: matched both search and shard tasks
"indices:data/read/search*"

// After: matches only search tasks
"indices:data/read/search"
```

**Time Range Validation (PR #413)**

Added validation to ensure the `from` timestamp is before the `to` timestamp in Top N queries API requests. Previously, invalid time ranges were accepted without error.

**Size Parameter Validation (PR #414)**

Fixed validation for the `size` parameter in Live Queries API to ensure it's a positive integer.

**Flaky Test Fix (PR #430)**

Fixed intermittent test failures in `TopQueriesRestIT.testTopQueriesResponses` caused by stale records in the shared queue. When metrics were disabled, the `queryRecordsQueue` wasn't cleared, causing old records to be processed alongside new ones.

```java
// Fix: Clear shared queue when disabling metrics
public void setEnabled(boolean enabled) {
    if (!enabled) {
        queryRecordsQueue.clear();
    }
    this.enabled = enabled;
}
```

#### Dashboards UI Fixes

**Group By Selector Fix (PR #366)**

Fixed the Configuration page where the "Group By" dropdown always showed "None" after page refresh, even when "Similarity" was enabled. The issue was reading from incorrect settings paths:

```typescript
// Before: incorrect path
persistentSettings?.group_by

// After: correct path
persistentSettings?.grouping?.group_by
```

Also fixed validation to hide the Save button when values exceed the maximum allowed (180 days).

**Query ID Matching in Detail Page (PR #367)**

Fixed `retrieveQueryById` function that was returning the first record from API response instead of filtering for the exact ID match. This caused users to be directed to incorrect query detail pages.

```typescript
// Before: returned first record blindly
return top_queries[0];

// After: explicitly filter by ID
return top_queries.find(q => q.id === id);
```

**Filter and Date Picker Fixes (PR #338)**

Fixed multiple UI bugs on the Top N Queries page:
1. Indices filter not filtering the table
2. Query Count shown for non-grouped (individual) queries
3. Metric headers not updating when toggling grouping mode
4. Date picker not working for relative ranges (Today, Yesterday, Last week, etc.)

#### CI/CD Improvements

**Cypress Workflow Fix (PR #329)**

Fixed Cypress tests by dynamically checking plugin versions to ensure consistency between plugin and core, and enabled WLM mode for tests.

**Delete Backport Branch Workflow (PR #327)**

Updated workflow to automatically delete `release-chores/` branches after merge, in addition to `backport/` branches.

### Migration Notes

No migration required. These are bug fixes that improve existing functionality.

## Limitations

- The query ID field mapping change from `text` to `keyword` only affects new indices; existing indices retain the old mapping

## References

### Documentation
- [Query Insights Documentation](https://docs.opensearch.org/3.0/observing-your-data/query-insights/index/)

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#426](https://github.com/opensearch-project/query-insights/pull/426) | query-insights | Change matchQuery to termQuery for query ID matching |
| [#420](https://github.com/opensearch-project/query-insights/pull/420) | query-insights | Filter out shard-level tasks from live queries |
| [#413](https://github.com/opensearch-project/query-insights/pull/413) | query-insights | Fix time range validation (from < to) |
| [#414](https://github.com/opensearch-project/query-insights/pull/414) | query-insights | Fix positive size parameter validation |
| [#430](https://github.com/opensearch-project/query-insights/pull/430) | query-insights | Fix flaky test by clearing stale queue records |
| [#435](https://github.com/opensearch-project/query-insights/pull/435) | query-insights | Add unit tests for queue clearing |
| [#366](https://github.com/opensearch-project/query-insights-dashboards/pull/366) | query-insights-dashboards | Fix Group By selector on Configuration page |
| [#367](https://github.com/opensearch-project/query-insights-dashboards/pull/367) | query-insights-dashboards | Fix query ID matching in retrieveQueryById |
| [#338](https://github.com/opensearch-project/query-insights-dashboards/pull/338) | query-insights-dashboards | Fix filter and date picker bugs |
| [#329](https://github.com/opensearch-project/query-insights-dashboards/pull/329) | query-insights-dashboards | Cypress workflow fix |
| [#327](https://github.com/opensearch-project/query-insights-dashboards/pull/327) | query-insights-dashboards | Update delete-backport-branch workflow |

### Issues (Design / RFC)
- [Issue #425](https://github.com/opensearch-project/query-insights/issues/425): Query ID matching returns incorrect results
- [Issue #350](https://github.com/opensearch-project/query-insights-dashboards/issues/350): Group By selector shows "None" after refresh
- [Issue #351](https://github.com/opensearch-project/query-insights-dashboards/issues/351): Configuration page validation issues

## Related Feature Report

- Full feature documentation
