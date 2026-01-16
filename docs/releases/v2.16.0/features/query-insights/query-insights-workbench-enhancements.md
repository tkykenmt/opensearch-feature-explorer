---
tags:
  - query-insights
---
# Query Insights & Workbench Enhancements

## Summary

OpenSearch v2.16.0 enhances Query Insights with improved query categorization metrics, adding latency, CPU, and memory histograms for different query types. Resource usage metrics are now always populated for categorization purposes, improving the accuracy of query performance analysis.

## Details

### What's New in v2.16.0

#### Query Categorization Metrics Enhancement
The Query Insights plugin now increments histograms for latency, CPU, and memory usage for each query type, aggregation type, and sort order. This provides more granular performance data for query analysis.

**Metrics tracked per query type:**
- Latency histograms
- CPU usage histograms  
- Memory usage histograms

**Query categorization dimensions:**
- Query types (match, term, range, etc.)
- Aggregation types (terms, date_histogram, etc.)
- Sort orders

#### Resource Usage Metrics Population
Resource usage metrics are now always populated for categorization, regardless of whether Top N queries feature is enabled. This ensures consistent data collection for query performance analysis.

### Technical Changes

| Change | Description |
|--------|-------------|
| Histogram integration | Latency and resource usage data integrated with query categorization |
| Metric population | Resource usage metrics always collected for categorization |
| Linting fixes | Code quality improvements and Java documentation fixes |

## Limitations

- Query categorization adds minimal overhead to query processing
- Histogram data is collected in-memory and may increase memory usage with high query volumes

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#30](https://github.com/opensearch-project/query-insights/pull/30) | Increment latency, cpu and memory histograms for query/aggregation/sort query types | [#14588](https://github.com/opensearch-project/OpenSearch/issues/14588) |
| [#41](https://github.com/opensearch-project/query-insights/pull/41) | Always populate resource usage metrics for categorization | [#40](https://github.com/opensearch-project/query-insights/issues/40) |
