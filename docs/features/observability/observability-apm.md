---
tags:
  - observability
---
# Application Performance Monitoring (APM)

## Summary

OpenSearch APM (Application Performance Monitoring) provides comprehensive observability capabilities for distributed systems built on open-source technologies. It enables monitoring of service health, performance metrics, and dependencies through an integrated dashboard experience in OpenSearch Dashboards.

## Details

### Architecture

APM employs a hybrid architecture leveraging different storage systems for optimal performance:

```mermaid
graph TB
    subgraph "Data Collection"
        App[Application] --> OTel[OTel SDK]
        OTel --> Collector[OTel Collector]
        Collector --> DataPrepper[Data Prepper]
    end
    
    subgraph "Storage Layer"
        DataPrepper --> OS[OpenSearch<br/>Topology & Traces]
        DataPrepper --> Prom[Prometheus<br/>RED Metrics]
    end
    
    subgraph "Visualization"
        OS --> Dashboard[OpenSearch Dashboards]
        Prom --> Dashboard
    end
    
    subgraph "APM Features"
        Dashboard --> Services[Services Home]
        Dashboard --> Map[Application Map]
        Dashboard --> Details[Service Details]
        Dashboard --> Correlations[Correlations]
    end
```

### Key Capabilities

| Capability | Description |
|------------|-------------|
| RED Metrics | Rate, Errors, and Duration metrics for services and operations |
| Service Maps | Interactive topology visualization showing service dependencies |
| Service-Level Monitoring | Detailed performance metrics at service and operation levels |
| Trace Exploration | Deep dive into distributed traces with log correlation |

### Components

#### Services Home Page

Interactive landing page displaying all monitored services with:
- Services table with columns: Service Name, Environment, Latency (P95), Throughput, Failure Ratio
- Sparkline visualizations for metric trends
- Resizable filter sidebar with environment, latency, throughput, and failure ratio filters
- Top Services by Fault Rate widget
- Top Dependencies by Fault Rate widget

#### Application Map

Interactive service topology visualization featuring:
- CelestialMap-based graph visualization
- Group By functionality (environment, deployment, namespace)
- Service Details Panel with RED metrics on node click
- Edge Metrics Flyout for dependency metrics
- Sidebar navigation with service list and search

#### Service Details Pages

Comprehensive drill-down views with three tabs:
- **Overview Tab**: Key metric cards (Requests, Faults, Errors, Availability, P99 Latency) and time-series charts
- **Operations Tab**: All operations with sortable/filterable metrics and expandable detail charts
- **Dependencies Tab**: Outbound service dependencies with metrics

#### Correlations Flyout

Quick view panel for:
- Correlated spans with status code filtering
- Associated logs with log level filtering
- Expandable rows showing raw logs and spans
- Navigation links to Explore traces and logs

### Configuration

APM configuration is stored as a saved object containing:

| Setting | Description |
|---------|-------------|
| Trace Dataset | OpenSearch index pattern for trace data |
| Service Map Dataset | OpenSearch index pattern for service topology |
| Prometheus Connection | Saved object reference for Prometheus data source |

### Query Languages

| Language | Use Case |
|----------|----------|
| PPL | Querying OpenSearch for topology, operations, and trace data |
| PromQL | Querying Prometheus for RED metrics and time-series data |

### Data Flow

1. Applications instrumented with OpenTelemetry SDK emit traces and metrics
2. OTel Collector receives and processes telemetry data
3. Data Prepper routes data to appropriate backends:
   - Topology and trace data → OpenSearch
   - Time-series metrics → Prometheus
4. APM UI queries both backends to display unified observability views

## Limitations

- Requires hybrid backend setup (OpenSearch + Prometheus)
- Service map visualization depends on CelestialMap library
- Metrics accuracy depends on proper OpenTelemetry instrumentation
- High-cardinality data may impact Prometheus performance
- Throughput normalization depends on correctly configured Window Duration matching the Data Prepper `window_duration` setting (default 60s)

## Change History

- **v3.6.0** (2026-04): Fixed APM metrics accuracy (server-side filtering, chart-total consistency, throughput as req/s), updated PromQL queries with time-range aggregation and custom step sizes, updated service map PPL queries for Data Prepper v2 index mappings, fixed UI pagination reset and chart rendering, fixed logs correlation dataSource for external datasources, replaced deprecated ad command with MLCommons RCF service, migrated to OSD core APM topology package, fixed span flyout race condition, added Prometheus instant query support, updated lodash for CVE-2026-4800
- **v3.5.0** (2026-02): Initial implementation with Services Home, Application Map, Service Details, and Correlations Flyout

## References

### Documentation

- [RFC: OpenSearch Application Performance Monitoring](https://github.com/opensearch-project/dashboards-observability/issues/2545)

### Pull Requests

| Version | PR | Description |
|---------|-----|-------------|
| v3.6.0 | [#2596](https://github.com/opensearch-project/dashboards-observability/pull/2596) | Update service map PPL queries for Data Prepper v2 mappings |
| v3.6.0 | [#2601](https://github.com/opensearch-project/dashboards-observability/pull/2601) | Replace deprecated ad command with MLCommons RCF service |
| v3.6.0 | [#2611](https://github.com/opensearch-project/dashboards-observability/pull/2611) | Use OSD core APM topology package |
| v3.6.0 | [#2618](https://github.com/opensearch-project/dashboards-observability/pull/2618) | Fix UI pagination, settings modal, chart rendering |
| v3.6.0 | [#2621](https://github.com/opensearch-project/dashboards-observability/pull/2621) | Update PromQL queries with time-range aggregation |
| v3.6.0 | [#2623](https://github.com/opensearch-project/dashboards-observability/pull/2623) | Fix metrics accuracy: server-side filtering, throughput normalization |
| v3.6.0 | [#2624](https://github.com/opensearch-project/dashboards-observability/pull/2624) | Fix metric card calculations |
| v3.6.0 | [#2625](https://github.com/opensearch-project/dashboards-observability/pull/2625) | Fix logs correlation dataSource for external datasources |
| v3.6.0 | [#2636](https://github.com/opensearch-project/dashboards-observability/pull/2636) | Update lodash to 4.18.1 (CVE-2026-4800) |
| v3.6.0 | [#11554](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11554) | Support Prometheus instant query API |
| v3.6.0 | [#11654](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11654) | Fix span flyout race condition |
| v3.5.0 | [#2556](https://github.com/opensearch-project/dashboards-observability/pull/2556) | APM Configuration page and server components |
| v3.5.0 | [#2557](https://github.com/opensearch-project/dashboards-observability/pull/2557) | APM config and context provider |
| v3.5.0 | [#2558](https://github.com/opensearch-project/dashboards-observability/pull/2558) | Services landing page |
| v3.5.0 | [#2561](https://github.com/opensearch-project/dashboards-observability/pull/2561) | Correlations flyout support |
| v3.5.0 | [#2565](https://github.com/opensearch-project/dashboards-observability/pull/2565) | Service details hooks and utilities |
| v3.5.0 | [#2566](https://github.com/opensearch-project/dashboards-observability/pull/2566) | Service details pages |
| v3.5.0 | [#2574](https://github.com/opensearch-project/dashboards-observability/pull/2574) | Application Map with topology visualization |
