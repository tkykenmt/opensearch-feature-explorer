# Security Analytics Findings Bugfixes

## Summary

This release fixes two critical bugs in the Security Analytics Findings page in OpenSearch Dashboards: a page crash when custom rules are deleted after generating findings, and incorrect rule severity display in the findings table.

## Details

### What's New in v2.18.0

This bugfix release addresses stability and correctness issues in the Security Analytics Findings page:

1. **Findings Page Crash Fix**: Prevents the findings page from crashing when a custom rule that generated a finding is subsequently deleted
2. **Rule Severity Correctness**: Ensures the findings table always displays the highest severity rule when multiple rules match a finding
3. **Correlations Findings Table Fix**: Corrects the correlations findings flyout to show the rule with the highest severity

### Technical Changes

#### Problem Analysis

The findings page was experiencing crashes due to:
- Missing null checks when accessing rule data for deleted custom rules
- Incorrect severity prioritization when multiple rules matched a single finding

#### Code Changes

**Findings.tsx** - Main findings page component:
- Added null-safe access to rule data with fallback to `DEFAULT_EMPTY_DATA`
- Implemented proper rule matching across all queries in a finding
- Added severity-based sorting using `RuleSeverityPriority` to display highest severity rule

**constants.ts** - Rule severity constants:
- Added `RuleSeverityValue` enum for type-safe severity values
- Added `RuleSeverityPriority` mapping for severity comparison

**CorrelationsStore.ts** - Correlations data store:
- Updated to match rules by severity priority
- Ensures correlated findings display the most severe matching rule

#### New Components

| Component | Description |
|-----------|-------------|
| `RuleSeverityValue` | Enum defining severity levels: Critical, High, Medium, Low, Informational |
| `RuleSeverityPriority` | Priority mapping for severity comparison (1=Critical, 5=Informational) |

### Usage Example

The fix is transparent to users. The findings table now correctly shows:

```
Finding ID | Rule Name      | Severity
-----------+----------------+----------
abc123     | Critical Rule  | critical   <- Highest severity shown
def456     | High Rule      | high
```

When a finding matches multiple rules, the highest severity rule is displayed.

### Migration Notes

No migration required. The fix is automatically applied when upgrading to v2.18.0.

## Limitations

- Threat intel rules are currently excluded from severity prioritization in the correlations findings table

## References

### Documentation
- [Working with findings](https://docs.opensearch.org/2.18/security-analytics/usage/findings/): Official documentation
- [PR #1160](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1160): Main implementation

### Pull Requests
| PR | Description |
|----|-------------|
| [#1160](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1160) | Fix findings page crash and rule severity correctness |

## Related Feature Report

- [Security Analytics Dashboards Plugin](../../../features/security-analytics-dashboards/security-analytics-dashboards-plugin.md)
