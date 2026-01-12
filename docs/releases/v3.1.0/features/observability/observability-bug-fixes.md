# Observability Bug Fixes

## Summary

This release includes two bug fixes for the OpenSearch Dashboards Observability plugin: a fix for Jaeger trace analytics end time processing that caused empty results with certain time picker options, and a fix for Network Firewall (NFW) integration Vega visualization warnings when materialized view indexes are empty.

## Details

### What's New in v3.1.0

Two bug fixes improve the reliability of trace analytics and NFW integration dashboards.

### Technical Changes

#### Jaeger End Time Processing Fix

The Trace Analytics plugin issues DSL queries when Jaeger requests are made. The time filter processing was not correctly handling end times for certain time picker options.

**Problem**: When using time picker options like "Today", "This year", "This month", or "This day", the start and end times could resolve to the same value, resulting in no data being returned.

**Solution**: Added `roundUp: true` option to `dateMath.parse()` for end time processing, ensuring end times are rounded up to the end of the period.

| Component | Change |
|-----------|--------|
| `helper_functions.tsx` | Added `isEndTime` parameter to `processTimeStamp()` function |
| `dashboard_content.tsx` | Pass `true` for end time in `processTimeStamp()` calls |
| `services_content.tsx` | Pass `true` for end time in `processTimeStamp()` calls |
| `service_view.tsx` | Pass `true` for end time in `processTimeStamp()` calls |
| `traces_content.tsx` | Pass `true` for end time in `processTimeStamp()` calls |
| `trace_view.tsx` | Pass `true` for end time in `processTimeStamp()` calls |

**Code Change**:
```typescript
// Before
export function processTimeStamp(time: string, mode: TraceAnalyticsMode) {
  if (mode === 'jaeger') {
    const timeMoment = dateMath.parse(time)!;
    return timeMoment.unix() * 1000000;
  }
  return time;
}

// After
export function processTimeStamp(time: string, mode: TraceAnalyticsMode, isEndTime = false) {
  if (mode === 'jaeger') {
    const timeMoment = isEndTime ? dateMath.parse(time, { roundUp: true })! : dateMath.parse(time)!;
    return timeMoment.unix() * 1000000;
  }
  return time;
}
```

#### NFW Integration Vega Visualization Warning Fix

The Network Firewall integration dashboards displayed warning messages when the materialized view (MV) index was empty.

**Solution**: 
1. Added `hideWarnings: true` to Vega panel configurations to suppress warnings
2. Assigned default values using `COALESCE()` to all NFW MV index fields
3. Rearranged visualization panels for better readability at low resolutions (e.g., CloudWatch console iframe embedding)

**Configuration Change**:
```json
{
  "kibana": {
    "hideWarnings": true
  }
}
```

**SQL Changes**: Added `COALESCE()` with default values for all fields:
```sql
COALESCE(CAST(firewall_name AS STRING), 'UNKNOWN_FIREWALL') AS `firewall_name`,
COALESCE(CAST(event.src_ip AS STRING), '-') AS `event_src_ip`,
COALESCE(CAST(event.src_port AS INTEGER), -1) AS `event_src_port`,
-- ... additional fields with defaults
```

### Usage Example

The Jaeger time filter fix is automatic. Users selecting "Today", "This month", "This year", or "This day" in the time picker will now see correct trace data.

For NFW integration, the warning messages are now hidden and empty indexes display default placeholder values instead of errors.

## Limitations

- The Jaeger fix only affects Jaeger mode; Data Prepper mode time handling remains unchanged
- NFW integration default values are placeholders and should be interpreted as "no data available"

## References

### Documentation
- [Analyzing Jaeger trace data](https://docs.opensearch.org/3.1/observing-your-data/trace/trace-analytics-jaeger/): Official documentation for Jaeger trace analytics
- [Trace Analytics](https://docs.opensearch.org/3.1/observing-your-data/trace/index/): Trace Analytics overview

### Pull Requests
| PR | Description |
|----|-------------|
| [#2460](https://github.com/opensearch-project/dashboards-observability/pull/2460) | Fix Jaeger end time processing |
| [#2452](https://github.com/opensearch-project/dashboards-observability/pull/2452) | NFW Integration Vega Vis Warning Msg Fix |

## Related Feature Report

- [Full feature documentation](../../../../features/observability/trace-analytics-bug-fixes.md)
