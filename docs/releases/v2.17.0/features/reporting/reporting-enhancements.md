---
tags:
  - dashboards
---

# Reporting Enhancements

## Summary

This release fixes a flaky integration test in the OpenSearch Reporting plugin by increasing the time accuracy tolerance from 1 second to 3 seconds when validating on-demand report generation timestamps.

## Details

### What's New in v2.17.0

The `OnDemandReportGenerationIT` integration test was failing intermittently due to timing issues in CI environments. The test validates that report timestamps are within an expected time range, but infrastructure delays caused occasional failures.

### Technical Changes

#### Test Fix

The fix increases the accuracy tolerance in the `validateTimeNearRefTime` function call:

```kotlin
// Before (v2.16.0)
validateTimeNearRefTime(
    Instant.ofEpochMilli(reportInstance.get("beginTimeMs").asLong),
    Instant.now().minus(Duration.parse(reportDefinition.get("format").asJsonObject.get("duration").asString)),
    1  // 1 second tolerance
)

// After (v2.17.0)
validateTimeNearRefTime(
    Instant.ofEpochMilli(reportInstance.get("beginTimeMs").asLong),
    Instant.now().minus(Duration.parse(reportDefinition.get("format").asJsonObject.get("duration").asString)),
    3  // 3 seconds tolerance
)
```

#### Root Cause

The test failures occurred because:

1. CI infrastructure (especially Windows ARM64) has variable execution times
2. The 1-second tolerance was too strict for environments with higher latency
3. Time differences observed in failures ranged from 1.04 to 2.76 seconds

#### Changed Files

| File | Change |
|------|--------|
| `src/test/kotlin/org/opensearch/integTest/rest/OnDemandReportGenerationIT.kt` | Increased accuracy parameter from 1 to 3 |

### Migration Notes

No migration required. This is a test-only change with no impact on production functionality.

## Limitations

- This fix addresses test flakiness but does not change the actual report generation behavior
- The increased tolerance may mask genuine timing regressions in edge cases

## References

### Documentation
- [Reporting Documentation](https://docs.opensearch.org/2.17/reporting/): Official OpenSearch Reporting docs

### Pull Requests
| PR | Description |
|----|-------------|
| [#1022](https://github.com/opensearch-project/reporting/pull/1022) | Increase accuracy seconds while testing create on-demand report from definition |

### Issues (Design / RFC)
- [Issue #1019](https://github.com/opensearch-project/reporting/issues/1019): Integration test failure for opensearch-reports 2.16.0

## Related Feature Report

- [Integration Test Stability](../../../features/reporting/integration-test-stability.md)
