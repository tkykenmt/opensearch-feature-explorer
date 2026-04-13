---
tags:
  - opensearch
---
# Star Tree Index

## Summary

In v3.6.0, the Star Tree Index feature gains intra-segment search support for all single-value metric aggregation factories. This enables metric aggregations (sum, min, max, avg, stats, cardinality, value_count) to be parallelized within individual segments, improving aggregation performance on large segments when concurrent segment search is enabled.

## Key Changes

### Intra-Segment Search for Metric Aggregations

Seven metric aggregation factories now declare support for intra-segment search by overriding `supportsIntraSegmentSearch()` to return `true`:

| Aggregation Factory | Description |
|---------------------|-------------|
| `SumAggregatorFactory` | Sum of numeric values |
| `MinAggregatorFactory` | Minimum value |
| `MaxAggregatorFactory` | Maximum value |
| `AvgAggregatorFactory` | Average value |
| `StatsAggregatorFactory` | Combined min/max/sum/count/avg |
| `CardinalityAggregatorFactory` | Approximate distinct count (HyperLogLog++) |
| `ValueCountAggregatorFactory` | Count of values |

### How It Works

Intra-segment search partitions large segments into smaller document ranges that can be processed concurrently. When enabled:

1. The intra-segment decider evaluates whether the query and aggregations support partitioning
2. If all aggregation factories return `supportsIntraSegmentSearch() == true`, the segment is split into partitions
3. Each partition is assigned to a different search slice for parallel execution
4. Results are merged across partitions

### Prerequisites

- Concurrent segment search must be enabled
- Intra-segment search must be enabled (`search.intra_segment_search.enabled: true`)
- Segment must exceed minimum size threshold (`search.intra_segment_search.min_segment_size`, default: 500,000 docs)

### Test Infrastructure

A new `indexBulkWithSegments()` helper method was added to `OpenSearchIntegTestCase` to support creating indexes with a specific number of segments for testing intra-segment partitioning behavior.

## References

- PR: `https://github.com/opensearch-project/OpenSearch/pull/20503`
- Related initial PR: `https://github.com/opensearch-project/OpenSearch/pull/19704`
- Related issue: `https://github.com/opensearch-project/OpenSearch/issues/19694`
- Meta issue: `https://github.com/opensearch-project/OpenSearch/issues/18852`
