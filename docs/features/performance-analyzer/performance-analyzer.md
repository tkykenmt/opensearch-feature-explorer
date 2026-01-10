# Performance Analyzer

## Summary

Performance Analyzer is an OpenSearch plugin that provides detailed performance metrics from your cluster independently of the Java Virtual Machine (JVM). It includes an agent and REST API for querying cluster performance metrics, aggregations, and root cause analysis (RCA) capabilities.

## Details

### Architecture

```mermaid
graph TB
    subgraph "OpenSearch Cluster"
        OS[OpenSearch Node]
        PA[Performance Analyzer Plugin]
        RCA[RCA Agent]
    end
    
    subgraph "PA Commons Library"
        MC[Metrics Collectors]
        SC[Stats Collector]
        RTF[RTF Metrics]
    end
    
    subgraph "Storage"
        SHM[/dev/shm]
        MDB[Metrics DB]
    end
    
    OS --> PA
    PA --> MC
    MC --> SC
    SC --> RTF
    PA --> SHM
    SHM --> MDB
    RCA --> MDB
    
    API[REST API :9600] --> PA
    API --> RCA
```

### Data Flow

```mermaid
flowchart TB
    A[OpenSearch Operations] --> B[Metrics Collectors]
    B --> C[Stats Collector]
    C --> D[/dev/shm Storage]
    D --> E[Metrics DB]
    E --> F[REST API]
    F --> G[PerfTop / Custom Dashboards]
    E --> H[RCA Framework]
    H --> I[Root Cause Analysis]
```

### Components

| Component | Description |
|-----------|-------------|
| Performance Analyzer Plugin | Core plugin that collects metrics from OpenSearch |
| PA Commons Library | Shared library with metrics definitions and collectors |
| Stats Collector | Collects and aggregates statistics across collector modes |
| RTF Metrics | Real-time framework metrics constants |
| RCA Agent | Root cause analysis agent for identifying performance issues |
| Metrics DB | Temporary storage for metrics data |

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `webservice-bind-host` | Host to bind the web service | `0.0.0.0` |
| `webservice-listener-port` | Port for the web service | `9600` |
| `metrics-location` | Location for metrics data | `/dev/shm/performanceanalyzer/` |
| `metrics-deletion-interval` | Interval (minutes) for metrics cleanup | `1` |
| `cleanup-metrics-db-files` | Whether to clean up old metrics files | `true` |
| `https-enabled` | Enable HTTPS for the web service | `false` |

### Usage Example

Query available metrics:

```bash
GET localhost:9600/_plugins/_performanceanalyzer/metrics/units
```

Enable Performance Analyzer:

```bash
curl -XPOST localhost:9200/_plugins/_performanceanalyzer/cluster/config \
  -H 'Content-Type: application/json' \
  -d '{"enabled": true}'
```

Enable RCA framework:

```bash
curl -XPOST localhost:9200/_plugins/_performanceanalyzer/rca/cluster/config \
  -H 'Content-Type: application/json' \
  -d '{"enabled": true}'
```

Query RCA results:

```bash
GET localhost:9600/_plugins/_performanceanalyzer/rca?name=HighHeapUsageClusterRCA
```

## Limitations

- Requires `/dev/shm` with at least 1GB of space for heavy workloads
- Does not support client or server authentication for requests (only encryption in transit)
- RCA framework requires separate enablement

## Related PRs

| Version | PR | Description |
|---------|-----|-------------|
| v3.2.0 | [#826](https://github.com/opensearch-project/performance-analyzer/pull/826) | Bump SpotBugs to 6.2.2 and Checkstyle to 10.26.1 |
| v2.17.0 | [#690](https://github.com/opensearch-project/performance-analyzer/pull/690) | Added CacheConfig Telemetry collectors |
| v2.17.0 | [#712](https://github.com/opensearch-project/performance-analyzer/pull/712) | Bump PA to use 1.6.0 PA commons lib |

## References

- [Performance Analyzer Documentation](https://docs.opensearch.org/latest/monitoring-your-cluster/pa/index/): Official documentation
- [Performance Analyzer Repository](https://github.com/opensearch-project/performance-analyzer): Source code
- [PA Commons Repository](https://github.com/opensearch-project/performance-analyzer-commons): Commons library
- [RCA Documentation](https://docs.opensearch.org/latest/monitoring-your-cluster/pa/rca/index/): Root cause analysis

## Change History

- **v3.2.0** (2025-07-18): Build infrastructure update - SpotBugs 6.2.2, Checkstyle 10.26.1; Removed CVE-2025-27820 workaround
- **v2.17.0** (2024-09-17): Added RTFCacheConfigMetricsCollector for cache configuration telemetry; Updated PA Commons dependency to 1.6.0
