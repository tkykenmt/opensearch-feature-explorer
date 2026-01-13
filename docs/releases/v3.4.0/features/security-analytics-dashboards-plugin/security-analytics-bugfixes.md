---
tags:
  - domain/security
  - component/dashboards
  - dashboards
  - search
  - security
---
# Security Analytics Bugfixes

## Summary

This release fixes a bug in the Security Analytics Dashboards plugin where the correlation table was not being populated correctly. The fix ensures proper data rendering in the correlations overview page table view.

## Details

### What's New in v3.4.0

This bugfix release addresses an issue where the correlation table in the Security Analytics Dashboards plugin was not displaying data. The table view, which shows correlated findings grouped by correlation rules, was failing to populate due to issues in the data fetching and filtering logic.

### Technical Changes

#### Bug Description

The correlation table on the Correlations overview page was not rendering data. Users could see the table structure but no correlation data was being displayed, making it difficult to analyze security event correlations.

#### Root Cause

Two issues were identified:

1. **Missing error handling**: The correlation data fetching logic lacked proper error handling and null checks, causing silent failures when fetching correlated findings
2. **Incorrect filter logic**: The log type and severity filters were incorrectly excluding all rows when no filters were selected

#### Fix Implementation

**CorrelationsContainer.tsx changes:**
- Added try-catch block around correlation data fetching
- Added null checks for `alertsSeverity` with fallback to empty array
- Added validation for `correlationRuleObj.queries` and `query.conditions` arrays
- Added null checks for `condition.name` and `condition.value` before pushing to resources

**CorrelationsTableView.tsx changes:**
- Fixed filter logic to include all rows when no filters are selected
- Changed filter behavior: empty filter selection now shows all data instead of hiding all data
- Added proper handling for rows with empty `logTypes` or `alertSeverity` arrays

### Code Changes

```typescript
// Before: Filter excluded all when no selection
const logTypeMatch = row.logTypes?.some((logType) => selectedLogTypes.includes(logType));

// After: Include all when no filters selected
const logTypeMatch =
  selectedLogTypes.length === 0 ||
  !row.logTypes?.length ||
  row.logTypes.some((logType) => selectedLogTypes.includes(logType));
```

### Migration Notes

No migration required. The fix is backward compatible and automatically applies when upgrading to v3.4.0.

## Limitations

- The correlation table requires findings data to be present for correlations to be displayed
- Correlation rules must be properly configured with at least two log sources

## References

### Documentation
- [Security Analytics Documentation](https://docs.opensearch.org/3.0/security-analytics/)
- [Creating Correlation Rules](https://docs.opensearch.org/3.0/security-analytics/sec-analytics-config/correlation-config/)
- [Working with the Correlation Graph](https://docs.opensearch.org/3.0/security-analytics/usage/correlation-graph/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#1360](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1360) | Correlation table rendering fixed |

## Related Feature Report

- [Full feature documentation](../../../../features/security-analytics-dashboards-plugin/security-analytics-dashboards-plugin-security-analytics.md)
