---
tags:
  - indexing
  - performance
  - search
---

# Query Insights CI/Tests

## Summary

This release improves the test infrastructure for the Query Insights plugin by adding comprehensive multi-node integration tests and health stats REST API tests. The changes also fix several flaky tests by addressing timing issues related to settings propagation and window rotation in multi-node environments.

## Details

### What's New in v3.4.0

This bugfix release focuses on improving test reliability and coverage for the Query Insights plugin:

1. **New Multi-Node Integration Tests**: Added `QueryInsightsClusterIT` with 6 test methods covering multi-node data collection, aggregation, and consistency validation
2. **Health Stats REST API Tests**: Added `HealthStatsRestIT` for comprehensive health stats endpoint testing
3. **Flaky Test Fixes**: Fixed timing issues in existing tests by adding settings propagation delays and increasing window sizes

### Technical Changes

#### New Test Classes

| Test Class | Description |
|------------|-------------|
| `QueryInsightsClusterIT` | Multi-node cluster integration tests for query insights data collection and aggregation |
| `HealthStatsRestIT` | REST API integration tests for the `/_insights/health_stats` endpoint |

#### Test Infrastructure Improvements

| Change | Description |
|--------|-------------|
| `getNodeClient(int nodeIndex)` | New helper method to target specific nodes by index for explicit node targeting in tests |
| `getClusterNodeCount()` | New helper method to get the number of nodes in the cluster |
| `waitForExpectedNodes(int)` | New helper method to wait for expected number of nodes before running tests |
| `verifyMultiNodeClusterSetup()` | New helper method to verify cluster health and node count |

#### Flaky Test Fixes

| Test | Fix Applied |
|------|-------------|
| `MinMaxQueryGrouperBySimilarityIT` | Added settings propagation delays (`Thread.sleep(2000)`) and explicit disable/enable cycle to prevent test interference |
| `QueryInsightsClusterIT` | Increased window size from 1m to 5m to prevent queries from being lost during window rotation |
| `TopQueriesServiceTests.testTimeFilterIncludesSomeRecords` | Fixed timing issue by including both current and history windows in query results |
| `fetchHistoricalTopQueries` | Added 10-second buffer to 'to' time to account for processing delays and clock skew |

#### CI Configuration Updates

| File | Change |
|------|--------|
| `.github/workflows/integ-tests-with-security.yml` | Updated macOS runner from `macos-13` to `macos-15` |
| `build.gradle` | Excluded `QueryInsightsClusterIT` from security integration tests (requires 2+ nodes, incompatible with demo SSL certs in Java 21) |

### Usage Example

The new multi-node tests validate query insights functionality across cluster nodes:

```java
// Test multi-node data collection
@Test
public void testMultiNodeDataCollectionAndAggregation() {
    waitForExpectedNodes(2);
    verifyMultiNodeClusterSetup();
    
    // Send queries to different nodes
    try (RestClient node1Client = getNodeClient(0)) {
        // Execute queries on node 1
    }
    try (RestClient node2Client = getNodeClient(1)) {
        // Execute queries on node 2
    }
    
    // Verify aggregated data from all nodes
    assertTopQueriesCount(4, "latency");
}
```

## Limitations

- `QueryInsightsClusterIT` is excluded from security integration tests because multi-node clusters with demo SSL certificates are not supported in Java 21
- Tests require increased window sizes (5 minutes instead of 1 minute) to prevent timing-related failures

## References

### Documentation
- [Query Insights Documentation](https://docs.opensearch.org/3.0/observing-your-data/query-insights/index/)
- [Health Stats API Documentation](https://docs.opensearch.org/3.0/observing-your-data/query-insights/health/)
- [GitHub Repository](https://github.com/opensearch-project/query-insights)

### Pull Requests
| PR | Description |
|----|-------------|
| [#482](https://github.com/opensearch-project/query-insights/pull/482) | Add multi-node, healthstats integration tests and fix flaky tests |

## Related Feature Report

- [Full feature documentation](../../../../features/query-insights/query-insights.md)
