---
tags:
  - dashboards
  - search
---

# Query Insights Bugfixes

## Summary

This release item addresses multiple UI bugs and improvements in the Query Insights Dashboards plugin for OpenSearch v3.2.0. The fixes include replacing the Vega charting library with react-vis to resolve build errors, fixing the search bar functionality on the Top N Queries page, improving table sorting with correct ID-based deduplication, and various UI polish improvements including number formatting, validation messages, and refresh functionality.

## Details

### What's New in v3.2.0

This release focuses on stability and usability improvements for the Query Insights Dashboards plugin:

1. **Charting Library Migration**: Replaced Vega with react-vis for Live Queries visualizations
2. **Search Bar Fix**: Fixed search functionality on Top N Queries overview page
3. **Table Sorting Fix**: Improved deduplication logic using query IDs instead of JSON strings
4. **UI Bug Fixes**: Multiple improvements to the detail page and rule creation workflow
5. **Test Maintenance**: Removed flaky Cypress tests for search bar due to framework limitations

### Technical Changes

#### Charting Library Migration (PR #243)

The Live Queries Dashboard previously used Vega for visualizations, which caused build errors in the distribution:

```
TypeError: vegaUtil.inherits is not a function
```

The fix replaces Vega with react-vis, a React-based visualization library that integrates better with the OpenSearch Dashboards build system.

#### Search Bar Fix (PR #267)

The search bar on the Top N Queries overview page was not functioning correctly:

**Problem:**
- When users entered a query record ID, the table results did not update
- The `onSearchChange` handler was not properly parsing the AST for free-text terms

**Solution:**
- Fixed `onSearchChange` to correctly parse AST for free-text terms and update `searchText` state
- Updated `filteredQueries` computation to properly filter by the ID column
- Added placeholder text indicating the search bar applies to the ID column only

#### Table Sorting Fix (PR #285)

The deduplication logic for the top queries table was error-prone when using JSON string comparison:

**Before:**
```typescript
// Error-prone JSON string comparison
const uniqueQueries = [...new Set(queries.map(q => JSON.stringify(q)))];
```

**After:**
```typescript
// Reliable ID-based deduplication
const uniqueQueries = [...new Map(queries.map(q => [q.id, q])).values()];
```

#### UI Bug Fixes (PR #258)

Multiple UI improvements for better user experience:

| Fix | Description |
|-----|-------------|
| Number formatting | Large numbers now formatted for readability on Detail page |
| Validation messages | Added validation for invalid CPU/Memory usage inputs |
| Error suppression | Suppressed unnecessary error for empty rule input during creation |
| Description display | Fixed edge case where description was not displayed correctly |
| Refresh button | Added Refresh button and "Last updated" timestamp to Detail page |
| Normalized limits | Normalized CPU/memory limits display |
| Box plot update | Updated box plot visualization |

#### Cypress Test Removal (PR #306)

Removed Cypress tests for the search bar functionality due to a known Cypress framework issue where the enter key event is not properly triggered after typing in the search bar. This is a documented Cypress limitation ([cypress-io/cypress#8267](https://github.com/cypress-io/cypress/issues/8267)).

### Revert: renderApp Export (PR #247)

Reverted PR #223 which changed `renderApp` to use default export. The original change was intended to prevent initialization race conditions but caused other issues.

### MDS Support for Inflight Queries (PR #217)

While labeled as an improvement, this PR adds Multi-Data Source (MDS) support to the Inflight Queries component:

- Integrated data source selection via `DataSourceContext`
- Unit tests wrapped with `DataSourceContext.Provider` to simulate data source selection

## Limitations

- Search bar on Top N Queries page only searches by query ID column
- Cypress tests for search bar functionality are disabled due to framework limitations

## References

### Documentation
- [Query Insights Dashboards Documentation](https://docs.opensearch.org/3.2/observing-your-data/query-insights/query-insights-dashboard/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#217](https://github.com/opensearch-project/query-insights-dashboards/pull/217) | MDS support for Inflight Queries |
| [#243](https://github.com/opensearch-project/query-insights-dashboards/pull/243) | react-vis implementation for Live Queries Dashboards |
| [#247](https://github.com/opensearch-project/query-insights-dashboards/pull/247) | Revert renderApp to use default export |
| [#258](https://github.com/opensearch-project/query-insights-dashboards/pull/258) | Fix for UI bugs |
| [#267](https://github.com/opensearch-project/query-insights-dashboards/pull/267) | Search bar fix |
| [#285](https://github.com/opensearch-project/query-insights-dashboards/pull/285) | Fix top queries table sorting with correct id |
| [#306](https://github.com/opensearch-project/query-insights-dashboards/pull/306) | Removed search bar Cypress tests |

### Issues (Design / RFC)
- [Issue #214](https://github.com/opensearch-project/query-insights-dashboards/issues/214): Search bar not working
- [Issue #152](https://github.com/opensearch-project/query-insights-dashboards/issues/152): MDS support for Live Queries
- [Cypress Issue #8267](https://github.com/cypress-io/cypress/issues/8267): Enter key not triggered after typing

## Related Feature Report

- [Full feature documentation](../../../features/query-insights/query-insights.md)
