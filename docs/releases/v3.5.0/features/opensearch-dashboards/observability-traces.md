---
tags:
  - opensearch-dashboards
---
# Observability Traces

## Summary

OpenSearch Dashboards v3.5.0 introduces RED metrics charts (Rate, Errors, Duration) for the Discover:Traces experience, adds dynamic configuration flags for Traces and Metrics features via the DynamicConfigService, implements dataset UI and observability workspace with trace automation in the observability plugin, and delivers multiple bug fixes for trace auto-detection, redirection, naming conventions, correlation types, sample data index naming, and correlations saved object search.

## Details

### What's New in v3.5.0

#### RED Metrics Charts for Discover:Traces
PR [#11030](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11030) adds RED metrics (Request, Error, Latency) charts to the Discover:Traces experience. Three PPL query calls generate the visualizations with per-chart headers, per-chart cache keys, improved interval options, and configurable bucket targeting. Currently compatible with the Data Prepper schema. PR [#11063](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11063) follows up by fixing the RED metric query to sort after buckets are formed rather than before, improving performance and backward compatibility with older PPL versions.

#### Dynamic Setting Flags for Explore Traces + Metrics
PR [#11220](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11220) refactors the Explore plugin to use `DynamicConfigService` for managing feature flags (`discoverTraces.enabled` and `discoverMetrics.enabled`). This enables dynamic configuration without restarts. Feature flags are exposed as capabilities that other plugins can consume via `request.getCapabilities()` on the server side or `useCapabilities()` on the browser side. Configuration in `opensearch_dashboards.yml`:

```yaml
explore:
  discoverTraces:
    enabled: true
  discoverMetrics:
    enabled: false
```

#### Dataset UI and Observability Workspace + Trace Automation
PR [#11096](https://github.com/opensearch-project/dashboards-observability/pull/11096) adds dataset UI and observability workspace integration with trace automation support.

### Bug Fixes

| Fix | PR | Description |
|-----|-----|-------------|
| Traces redirection | [#11068](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11068) | Fixed URL redirection bug based on timestamp, improved field-resolution fallbacks for trace details and span durations, added caching for histogram config lookups |
| Trace automation naming | [#11174](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11174) | Fixed mis-named field in auto-creation that prevented UI from picking up registered timefield; corrected to use "timestamp" field name |
| Auto detect bug | [#11191](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11191) | Stopped trace auto-detection from running when a trace dataset already exists; removed creation flow from log page; added empty state for datasource select |
| OTel sample data index names | [#11208](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11208) | Updated OTEL sample data index naming to avoid conflicts with Data Prepper production data |
| Correlation type naming | [#11215](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11215) | Changed correlationType from static `APM-Correlation` to dynamic `trace-to-logs-<trace-dataset-title>` for unique identification in Assets page |
| Correlations saved object search | [#11256](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11256) | Added `title` field (text type) to correlations saved object for search support; fixed broken search in Saved Objects Management UI caused by keyword-type `correlationType` field |

## Limitations

- RED metrics charts are currently only compatible with the Data Prepper schema
- Dynamic feature flags for Traces and Metrics default to `false` (disabled)

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#11030](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11030) | Add RED metrics charts for Discover:Traces |  |
| [#11096](https://github.com/opensearch-project/dashboards-observability/pull/11096) | Dataset UI and observability workspace + Trace automation |  |
| [#11063](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11063) | Fix RED metric query for Discover:Traces |  |
| [#11068](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11068) | Discover:Traces redirection fix + testing improvement |  |
| [#11220](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11220) | Add dynamic setting flag for Explore Traces + Metrics |  |
| [#11174](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11174) | Fix trace automation naming convention |  |
| [#11191](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11191) | Fix Traces: Auto detect bug |  |
| [#11208](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11208) | Update the OTel sample data index names |  |
| [#11215](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11215) | Update correlationType for trace-to-logs objects | [#2545](https://github.com/opensearch-project/dashboards-observability/issues/2545) |
| [#11256](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11256) | Add title field to correlations saved object | [#11133](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/11133) |
