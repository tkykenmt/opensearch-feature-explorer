---
tags:
  - domain/infra
  - component/dashboards
  - dashboards
  - security
---
# Reporting Bugfixes

## Summary

OpenSearch Dashboards Reporting v3.4.0 includes two important bugfixes: a security vulnerability fix for the jspdf library (CVE-2025-57810) and a fix for handling null/undefined datetime values when generating CSV reports from Discover.

## Details

### What's New in v3.4.0

This release addresses two bugs in the dashboards-reporting plugin:

1. **CVE-2025-57810 Security Fix**: Bumped jspdf dependency from v3.0.1 to v3.0.2 to address a security vulnerability
2. **DateTime Null Check Fix**: Added proper handling for null and undefined datetime field values when generating reports

### Technical Changes

#### Security Dependency Update

The jspdf library was updated to fix CVE-2025-57810:

| Dependency | Previous Version | New Version |
|------------|------------------|-------------|
| jspdf | 3.0.1 | 3.0.2 |

The update also brought in new transitive dependencies:
- `fast-png` ^6.2.0
- `pako` ^2.1.0
- `iobuffer` ^5.3.2

#### DateTime Null Check Implementation

The fix modifies `dataReportHelpers.ts` to properly handle cases where datetime fields may be null or undefined:

```typescript
// Before (would throw error on null/undefined)
const fieldDateValue = fields[dateField];

// After (safe access with optional chaining)
const fieldDateValue = fields?.[dateField];
```

Key changes in the datetime processing logic:
- Added optional chaining (`?.`) for accessing field values
- Added null checks before processing date arrays
- Added conditional checks before string type comparisons

### Usage Example

The fix ensures CSV reports can be generated even when datetime fields contain null values:

```json
// Document with null datetime field - now handled correctly
{
  "_source": {
    "time": "2025-10-16T09:30:00Z",
    "attributes": {
      "time": null,
      "logtime": "2025-10-16T09:30:00.123Z"
    },
    "timefield": null
  }
}
```

### Migration Notes

No migration required. The fixes are backward compatible and automatically applied when upgrading to v3.4.0.

## Limitations

- The datetime null check fix only applies to CSV report generation from Discover
- PDF report generation uses the updated jspdf library but behavior remains unchanged

## References

### Documentation
- [CVE-2025-57810](https://nvd.nist.gov/vuln/detail/CVE-2025-57810): Security vulnerability in jspdf

### Pull Requests
| PR | Description |
|----|-------------|
| [#650](https://github.com/opensearch-project/dashboards-reporting/pull/650) | Bump jspdf to fix CVE-2025-57810 |
| [#649](https://github.com/opensearch-project/dashboards-reporting/pull/649) | Undefined and null check for date time values |

### Issues (Design / RFC)
- [Issue #308](https://github.com/opensearch-project/dashboards-reporting/issues/308): Original bug report for undefined date error

## Related Feature Report

- Full feature documentation
