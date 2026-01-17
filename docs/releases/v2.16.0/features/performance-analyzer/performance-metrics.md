---
tags:
  - performance-analyzer
---
# Performance Metrics

## Summary

Enhanced Performance Analyzer metrics collection in v2.16.0 with index UUID tagging for shard metrics and new resource utilization listeners for search and bulk operations.

## Details

### What's New in v2.16.0

Two key enhancements to the Performance Analyzer metrics framework:

1. **Index UUID Tag for Shard Metrics**: Added `index_uuid` as a dimension tag in node stats all shard metrics, enabling more precise metric identification
2. **Resource Utilization Listeners**: New RTF (Real-Time Framework) listeners for capturing CPU utilization and heap usage metrics at the task level

### Technical Changes

#### Index UUID Tag (PR #680)

Added `index_uuid` as a tag dimension in the `RTFNodeStatsAllShardsMetricsCollector` for metrics emitted by the RTF collector. This enables correlation of metrics with specific index instances.

Example metric output with new tag:
```
metric: ImmutableMetricData{
  name=cache_field_data_eviction,
  attributes={
    index_name="your-index",
    index_uuid="TxGu9noCSQKt8OE8ioR1-A",
    shard_id="0"
  },
  value=0.0
}
```

#### Resource Utilization Listeners (PR #687)

New components for capturing resource utilization metrics:

| Component | Description |
|-----------|-------------|
| `RTFPerformanceAnalyzerSearchListener` | Emits CPU_Utilization and Heap_used metrics for query and fetch phases |
| `RTFPerformanceAnalyzerTransportInterceptor` | Emits CPU_Utilization metric for BulkShardRequest operations |
| `RTFPerformanceAnalyzerTransportChannel` | Transport channel wrapper for bulk shard operations |
| `RTFPerformanceAnalyzerTransportRequestHandler` | Request handler for intercepting bulk shard requests |

##### Metrics Emitted

| Metric | Description | Unit |
|--------|-------------|------|
| `cpu_utilization` | CPU utilization per shard for search/bulk operations | rate |
| `heap_allocated` | Heap memory used per shard for search phases | bytes |

##### Metric Tags

| Tag | Description |
|-----|-------------|
| `index_name` | Name of the index |
| `index_uuid` | UUID of the index |
| `shard_id` | Shard identifier |
| `operation` | Operation type (shard_query, shard_fetch, shardbulk) |
| `failed` | Whether the operation failed |
| `shard_role` | Primary or replica (for bulk operations) |

##### Collector Mode Support

The listeners respect the collector run mode configuration:

| Mode | Search Listener | Transport Handler |
|------|-----------------|-------------------|
| RCA | Disabled | Enabled |
| TELEMETRY | Enabled | Enabled |
| DUAL | Enabled | Enabled |

## Limitations

- Resource tracking requires OpenSearch's task resource tracking to be enabled
- CPU utilization calculation uses share factor when query and fetch phases run in the same task
- Metrics are only emitted when Performance Analyzer is enabled

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#680](https://github.com/opensearch-project/performance-analyzer/pull/680) | Adds index_uuid as a tag in node stats all shard metrics | - |
| [#687](https://github.com/opensearch-project/performance-analyzer/pull/687) | Adds the listener for resource utilization metrics | - |
