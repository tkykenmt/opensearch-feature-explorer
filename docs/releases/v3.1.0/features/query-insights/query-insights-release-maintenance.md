# Query Insights Release Maintenance

## Summary

This release includes bug fixes for flaky integration tests in the Query Insights plugin. The changes improve test reliability by addressing timing issues, adding proper test infrastructure for multi-node scenarios, and fixing window boundary calculations.

## Details

### What's New in v3.1.0

This release focuses on test stability improvements rather than new features. The changes ensure more reliable CI/CD pipelines by fixing intermittent test failures.

### Technical Changes

#### Test Infrastructure Improvements

| Change | Description |
|--------|-------------|
| Multi-node test support | Added `getNodeClient(int nodeIndex)` method for targeting specific nodes |
| Index creation consistency | Added `createIndexWithSettings()` to ensure consistent shard counts |
| Retry logic | Added retry mechanisms for index discovery and cluster health checks |
| Time buffer | Added 10-second buffer to timestamp queries to handle processing delays |

#### Fixed Flaky Tests

| Test Class | Fix Applied |
|------------|-------------|
| `QueryInsightsRestTestCase` | Added index creation with default settings, retry logic for top_queries index discovery |
| `QueryInsightsExporterIT` | Increased search iterations and added delays between searches |
| `TopQueriesServiceTests` | Set reasonable window size (1 hour) instead of `Long.MAX_VALUE` |
| `LiveQueriesRestIT` | Added proper index mapping for aggregations and sorting |
| `MinMaxQueryGrouperBySimilarityIT` | Added settings propagation delays and state clearing |

#### New Test Classes (PR #482)

| Test Class | Description |
|------------|-------------|
| `QueryInsightsClusterIT` | Multi-node integration tests for data collection and aggregation |
| `HealthStatsRestIT` | Integration tests for health stats REST API |

#### Window Size Changes

Default window size increased from 1 minute to 5 minutes in test settings to prevent queries from being lost during window rotation:

```java
// Before
"search.insights.top_queries.latency.window_size" : "1m"

// After  
"search.insights.top_queries.latency.window_size" : "5m"
```

### Migration Notes

No migration required. These are internal test improvements only.

## Limitations

- `QueryInsightsClusterIT` is excluded from security integration tests due to SSL certificate limitations with multi-node setups in Java 21

## Related PRs

| PR | Description |
|----|-------------|
| [#364](https://github.com/opensearch-project/query-insights/pull/364) | Fix flaky integration tests |
| [#482](https://github.com/opensearch-project/query-insights/pull/482) | Add multi-node and health stats integration tests, fix additional flaky tests |

## References

- [Query Insights Documentation](https://docs.opensearch.org/3.1/observing-your-data/query-insights/index/)
- [Query Insights Health Documentation](https://docs.opensearch.org/3.1/observing-your-data/query-insights/health/)

## Related Feature Report

- [Full feature documentation](../../../../features/query-insights/query-insights.md)
