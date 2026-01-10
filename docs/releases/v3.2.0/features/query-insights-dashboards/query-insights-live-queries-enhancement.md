# Query Insights Live Queries Enhancement

## Summary

This release item improves the Live Queries page in the Query Insights Dashboards plugin by changing the default auto-refresh interval from 5 seconds to 30 seconds. This change reduces unnecessary API calls and improves dashboard performance while still providing timely updates for monitoring in-flight queries.

## Details

### What's New in v3.2.0

The Live Queries page now uses a 30-second default auto-refresh interval instead of 5 seconds, providing a better balance between real-time monitoring and system resource usage.

### Technical Changes

#### Auto-Refresh Interval Update (PR #304)

**Before:**
```typescript
export const DEFAULT_REFRESH_INTERVAL = 5000; // 5 seconds
```

**After:**
```typescript
export const DEFAULT_REFRESH_INTERVAL = 30000; // 30 seconds
```

The change was made in `InflightQueries.tsx` and affects the default polling behavior of the Live Queries dashboard component.

#### Rationale

- **Reduced API Load**: Decreases the frequency of `/_insights/live_queries` API calls by 6x
- **Better Resource Usage**: Less network traffic and server-side processing
- **Appropriate Granularity**: 30 seconds is sufficient for most monitoring use cases
- **User Configurable**: Users can still adjust the refresh interval as needed

### Usage

The Live Queries page can be accessed via:
- **Standard**: OpenSearch Plugins > Query insights > Live Queries tab
- **Multi-Data Source**: Data administration > Performance > Query insights > Live Queries tab

Users can manually refresh or adjust the auto-refresh interval through the UI controls.

## Limitations

- The 30-second interval may not be suitable for time-critical monitoring scenarios
- Users requiring faster updates should manually adjust the refresh interval

## Related PRs

| PR | Description |
|----|-------------|
| [#304](https://github.com/opensearch-project/query-insights-dashboards/pull/304) | Updated Autorefresh 30s |

## References

- [Issue #152](https://github.com/opensearch-project/query-insights-dashboards/issues/152): Feature request for In-Flight Query Tracking
- [Live Queries Documentation](https://docs.opensearch.org/3.0/observing-your-data/query-insights/live-queries/)
- [Query Insights Dashboards Documentation](https://docs.opensearch.org/3.0/observing-your-data/query-insights/query-insights-dashboard/)

## Related Feature Report

- [Full feature documentation](../../../features/query-insights/query-insights.md)
