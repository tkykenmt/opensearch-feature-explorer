---
tags:
  - opensearch
---
# Query Categorization Removal

## Summary

In v2.16.0, query categorization functionality was removed from OpenSearch core and moved to the Query Insights plugin. This change reduces overhead on the search path by moving metric counter increments to occur after request completion rather than before, enabling better correlation of query categorization data with latency, CPU, and memory metrics.

## Details

### What's New in v2.16.0

Query categorization was originally implemented in OpenSearch core to track search query metrics using the Metrics Framework. In v2.16.0, this functionality was removed from core and relocated to the Query Insights plugin for the following reasons:

1. **Performance**: Counter increments on the search path added overhead before request execution
2. **Data correlation**: Moving to the plugin enables tying query latency, CPU, and memory usage with categorization data
3. **Plugin architecture**: Query Insights plugin is the appropriate location for query analysis features

### Technical Changes

The following components were removed from OpenSearch core:

| Component | Description |
|-----------|-------------|
| `SearchQueryCategorizer` | Main class for categorizing queries and logging query shapes |
| `SearchQueryCategorizingVisitor` | Visitor pattern implementation for traversing query builder trees |
| `SearchQueryCounters` | Counter management for query type, aggregation, and sort metrics |
| `SearchQueryAggregationCategorizer` | Aggregation-specific counter incrementing |
| `QueryShapeVisitor` | Query shape extraction for logging |

### Configuration Changes

The following cluster setting was removed:

| Setting | Description |
|---------|-------------|
| `search.query.metrics.enabled` | Previously enabled/disabled query categorization in core |

Query metrics are now configured through the Query Insights plugin using `search.query.metrics.enabled` in `opensearch.yml` along with OpenTelemetry settings.

### Migration Path

Users who were using query categorization should:

1. Install the Query Insights plugin
2. Enable query metrics via `search.query.metrics.enabled: true` in `opensearch.yml`
3. Configure OpenTelemetry for metrics export (optional)

## Limitations

- Query categorization is no longer available without the Query Insights plugin installed
- Existing configurations using the removed cluster setting will have no effect

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14759](https://github.com/opensearch-project/OpenSearch/pull/14759) | Remove query categorization from core | [#14527](https://github.com/opensearch-project/OpenSearch/issues/14527) |
| [query-insights#16](https://github.com/opensearch-project/query-insights/pull/16) | Move query categorization changes to plugin | [#14527](https://github.com/opensearch-project/OpenSearch/issues/14527) |

### Related Issues
- [#11596](https://github.com/opensearch-project/OpenSearch/issues/11596): [META] Search Query Categorization
- [#14527](https://github.com/opensearch-project/OpenSearch/issues/14527): Move query categorization to query insights plugin
