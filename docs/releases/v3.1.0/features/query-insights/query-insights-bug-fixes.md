---
tags:
  - dashboards
  - observability
  - performance
  - search
---

# Query Insights Bug Fixes

## Summary

This release includes critical bug fixes for the Query Insights plugin and its Dashboards component. The fixes address request parameter serialization issues in multi-node clusters, improve CI/CD test stability, and correct the Live Queries API response structure for accurate query status reporting.

## Details

### What's New in v3.1.0

Four bug fixes were merged across the Query Insights plugin and Query Insights Dashboards:

1. **Node-level Top Queries Request Serialization Fix** - Fixed a bug where request parameters (`from`, `to`, `id`, `verbose`) were not correctly passed to other nodes in multi-node clusters
2. **Live Query Status Response Fix** - Corrected the `is_cancelled` field location in the Live Queries API response structure
3. **Cypress Test Stability Improvements** - Enhanced CI test reliability with better timeouts, health checks, and retry logic
4. **CI Version Alignment** - Fixed version mismatch between OpenSearch and Dashboards in CI workflows

### Technical Changes

#### Request Serialization Fix (query-insights #365)

The `TopQueriesRequest` class was missing proper serialization of optional parameters when communicating between nodes:

```java
// Before: Parameters were not serialized
public TopQueriesRequest(final StreamInput in) throws IOException {
    super(in);
    this.metricType = MetricType.readFromStream(in);
    this.from = null;  // Always null on receiving node
    this.to = null;
    this.verbose = null;
    this.id = null;
}

// After: Parameters properly serialized with version check
public TopQueriesRequest(final StreamInput in) throws IOException {
    super(in);
    this.metricType = MetricType.readFromStream(in);
    if (in.getVersion().onOrAfter(Version.V_3_1_0)) {
        this.from = in.readOptionalString();
        this.to = in.readOptionalString();
        this.id = in.readOptionalString();
        this.verbose = in.readOptionalBoolean();
    }
}
```

The fix includes version compatibility checks to ensure backward compatibility with older nodes.

#### Live Query Status Fix (query-insights-dashboards #210)

The `is_cancelled` field was incorrectly nested inside `measurements` in the response. The Dashboards code was updated to read from the correct location:

```typescript
// Before: Incorrect path
item.measurements?.is_cancelled

// After: Correct path
item.is_cancelled
```

This affects:
- Query selection logic (cancelled queries cannot be selected)
- Status column rendering (shows "Cancelled" or "Running")
- Cancel action availability

#### Test Infrastructure Improvements

| Change | Description |
|--------|-------------|
| Multi-node integration tests | Default test cluster increased to 2 nodes |
| First-node targeting | Tests target specific node to avoid double-counting |
| Health check waits | Replaced fixed sleeps with health endpoint polling |
| Cypress timeouts | Increased timeouts for CI environments (up to 6 minutes) |
| Retry configuration | Added automatic retries for flaky tests |

### Configuration Changes

No new configuration options were added. Existing settings remain unchanged.

## Limitations

- The request serialization fix requires all nodes in the cluster to be on v3.1.0+ for full functionality
- Mixed-version clusters will fall back to the previous behavior (parameters not passed to older nodes)

## References

### Documentation
- [Query Insights Documentation](https://docs.opensearch.org/3.1/observing-your-data/query-insights/index/)
- [Query Insights Dashboards Documentation](https://docs.opensearch.org/3.1/observing-your-data/query-insights/query-insights-dashboard/)
- [GitHub: query-insights](https://github.com/opensearch-project/query-insights)
- [GitHub: query-insights-dashboards](https://github.com/opensearch-project/query-insights-dashboards)

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#365](https://github.com/opensearch-project/query-insights/pull/365) | query-insights | Fix node-level top queries request parameter serialization |
| [#210](https://github.com/opensearch-project/query-insights-dashboards/pull/210) | query-insights-dashboards | Fix live query status field location in response |
| [#206](https://github.com/opensearch-project/query-insights-dashboards/pull/206) | query-insights-dashboards | Fix failing Cypress tests with improved timeouts and health checks |
| [#205](https://github.com/opensearch-project/query-insights-dashboards/pull/205) | query-insights-dashboards | Fix version mismatch in CI binary installation workflow |

## Related Feature Report

- [Full feature documentation](../../../../features/query-insights/query-insights.md)
