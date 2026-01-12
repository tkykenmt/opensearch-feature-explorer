---
tags:
  - indexing
  - observability
  - search
---

# Nodes Info API Changes

## Summary

OpenSearch 3.0.0 introduces a breaking change to the Nodes Info API: the `search_pipelines` metric is no longer included in the default set of metrics returned by `NodesInfoRequest`. This change reduces the default response size by excluding metrics that are typically only needed for specific use cases.

## Details

### What's New in v3.0.0

The `NodesInfoRequest` class now uses a "default metrics" set instead of "all metrics" by default. The `search_pipelines` metric is excluded from this default set, meaning clients must explicitly request it when needed.

### Technical Changes

#### API Behavior Change

| Aspect | Before v3.0.0 | v3.0.0+ |
|--------|---------------|---------|
| Default metrics | All 12 metrics | 11 metrics (excludes `search_pipelines`) |
| `GET /_nodes` response | Includes `search_pipelines` | Does NOT include `search_pipelines` |
| Explicit request required | No | Yes, for `search_pipelines` |

#### New Methods in NodesInfoRequest

| Method | Description |
|--------|-------------|
| `defaultMetrics()` | Returns the default set of metrics (excludes `search_pipelines`) |
| `all()` | Returns all available metrics (includes `search_pipelines`) |

#### Available Metrics

The Nodes Info API supports the following metrics:

| Metric | Included in Default | Description |
|--------|---------------------|-------------|
| `settings` | ✓ | Node settings |
| `os` | ✓ | Operating system info |
| `process` | ✓ | Process information |
| `jvm` | ✓ | JVM details |
| `thread_pool` | ✓ | Thread pool settings |
| `transport` | ✓ | Transport layer info |
| `http` | ✓ | HTTP layer info |
| `plugins` | ✓ | Installed plugins |
| `ingest` | ✓ | Ingest pipelines info |
| `aggregations` | ✓ | Available aggregations |
| `indices` | ✓ | Index settings |
| `search_pipelines` | ✗ | Search pipelines info |

### Usage Example

To explicitly request `search_pipelines` metrics:

```bash
# Request only search_pipelines metric
GET /_nodes/search_pipelines

# Request all metrics including search_pipelines
GET /_nodes/_all
```

For Java clients:

```java
// Default request (excludes search_pipelines)
NodesInfoRequest request = new NodesInfoRequest();

// Request all metrics including search_pipelines
NodesInfoRequest allRequest = new NodesInfoRequest().all();

// Request only search_pipelines
NodesInfoRequest pipelinesRequest = new NodesInfoRequest()
    .clear()
    .addMetric(NodesInfoRequest.Metric.SEARCH_PIPELINES.metricName());
```

### Migration Notes

If your application relies on `search_pipelines` information from the Nodes Info API:

1. Update API calls to explicitly request the `search_pipelines` metric
2. Use `GET /_nodes/search_pipelines` for REST API calls
3. For Java clients, use `.all()` or explicitly add the metric

## Limitations

- This is a **breaking change** - existing clients expecting `search_pipelines` in default responses will need updates
- The change affects both REST API and Java transport client behavior

## References

### Documentation
- [Nodes Info API Documentation](https://docs.opensearch.org/3.0/api-reference/nodes-apis/nodes-info/): Official documentation
- [PR #12497](https://github.com/opensearch-project/OpenSearch/pull/12497): Main implementation
- [PR #10296](https://github.com/opensearch-project/OpenSearch/pull/10296): Related - Add optional section of node analyzers into NodeInfo

### Pull Requests
| PR | Description |
|----|-------------|
| [#12497](https://github.com/opensearch-project/OpenSearch/pull/12497) | Do not request "search_pipelines" metrics by default in NodesInfoRequest |

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/nodes-info-api.md)
