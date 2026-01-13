---
tags:
  - release
---
# OpenSearch v2.19.0 Release Summary

## Summary

OpenSearch 2.19.0 delivers significant enhancements for ML-powered applications, vector search performance, security, and observability. Key highlights include multi-tenancy support for ML Commons and Flow Framework, binary vector support in Lucene, cosine similarity for Faiss, hybrid search pagination, and a new Query Insights dashboard. The release also introduces the Learning to Rank plugin, enhanced security privilege evaluation with O(1) performance, and automatic TLS certificate hot reloading.

## Highlights

```mermaid
graph TB
    subgraph "ML & AI"
        MT[Multi-tenancy]
        FF[Flow Framework]
        LTR[Learning to Rank]
        AI[AI Assistant]
    end
    subgraph "Vector Search"
        BV[Binary Vectors - Lucene]
        CS[Cosine Similarity - Faiss]
        AVX[AVX-512 SIMD]
        DV[Derived Source]
    end
    subgraph "Search"
        HQ[Hybrid Query Pagination]
        RRF[Reciprocal Rank Fusion]
        TQ[Template Query]
        BF[Bitmap Filtering]
    end
    subgraph "Security"
        PE[O(1) Privilege Evaluation]
        TLS[TLS Hot Reload]
        IP[Identity Plugin]
    end
    subgraph "Observability"
        QI[Query Insights Dashboard]
        GC[Gantt Chart Redesign]
        SM[Service Map Updates]
    end
```

## New Features

| Feature | Repository | Description |
|---------|------------|-------------|
| Multi-tenancy | ml-commons | Logical resource separation by tenant ID for scalable multi-tenant ML solutions |
| Flow Framework Multi-tenancy | flow-framework | Remote metadata client and synchronous provisioning with tenant support |
| Learning to Rank | learning | New plugin with XGBoost/RankLib models, circuit breaker, stats API |
| Binary Vectors (Lucene) | k-nn | Binary index support for Lucene engine with 90%+ memory reduction |
| Cosine Similarity (Faiss) | k-nn | Native cosine similarity without manual normalization |
| AVX-512 SIMD | k-nn | Advanced instructions for Intel Sapphire Rapids processors |
| Hybrid Query Pagination | neural-search | `pagination_depth` parameter for large result set management |
| Reciprocal Rank Fusion | neural-search | Alternative score combination using document ranks |
| Template Query | opensearch | Dynamic placeholder substitution with `${variable_name}` syntax |
| Query Insights Dashboard | query-insights-dashboards | New UI for monitoring top N queries with drill-down analysis |
| CreateAlertTool | skills | AI-powered natural language alert creation |
| Geospatial Client | geospatial | New Java artifact for cross-plugin IP enrichment |
| Feature Direction Rules | anomaly-detection | Precise spike/dip detection for individual metrics |

## Improvements

| Improvement | Repository | Description |
|-------------|------------|-------------|
| O(1) Privilege Evaluation | security | Hash-table-based checks with 79% performance improvement |
| TLS Certificate Hot Reload | security | Automatic certificate reloading without restart |
| Identity Plugin Extension | security | ContextProvidingPluginSubject for secure system index access |
| Bitmap Filtering | opensearch | Cost-based selection for optimal filter performance |
| Flat Object Field | opensearch | DocValues-based term queries with 1.6-2.1% throughput improvement |
| Neural Sparse Pruning | neural-search | Configurable pruning for ingestion and two-phase search |
| Hybrid Query Explainability | neural-search | `hybrid_score_explanation` processor for debugging |
| Verbose Pipeline | opensearch | Detailed processor debugging with execution time tracking |
| Star Tree Index | opensearch | Keyword, IP, and object field support with metric aggregations |
| Concurrency Optimizations | k-nn | Parallel graph file downloads for remote storage |
| Gantt Chart Redesign | dashboards-observability | Zoom, minimap, and improved span visualization |
| Service Map Updates | dashboards-observability | Enhanced topology visualization |
| Discover Enhancements | opensearch-dashboards | Indexed views, banner framework, data2summary validation |
| Workspace Enhancements | opensearch-dashboards | Dismissible sections, recent items optimization |

## Bug Fixes

| Fix | Repository | Description |
|-----|------------|-------------|
| Deprecation Logger Memory Leak | opensearch | Bounded cache to 16,384 entries to prevent OOM |
| Searchable Snapshot | opensearch | Alias rollover, scripted query permissions, shallow copy fixes |
| Tiered Caching Stats | opensearch | Accurate cache statistics and maximum size settings |
| Remote State Manifest | opensearch | Fixed deserialization for cluster upgrades |
| k-NN Filter Rewrite | k-nn | Consistent results across filter queries |
| k-NN index.knn Setting | k-nn | Prevent modification after index creation |
| Hybrid Query Scoring | neural-search | Consistent scoring in sorted hybrid queries |
| JWT Attribute Parsing | security | Fixed list parsing in JWT attributes |
| OpenID Connect Redirect | security-dashboards | Preserve query in login redirect URL |
| Aggregation Rule Detector | security-analytics | Fixed trigger conditions for aggregation rules |
| OCSF 1.1 Field Mapping | security-analytics | Improved field mapping for OCSF 1.1 |

## Breaking Changes

None in this release.

## Deprecation Notices

| Deprecation | Target Version | Details |
|-------------|----------------|---------|
| Ubuntu Linux 20.04 | Upcoming | End-of-life April 2025 |
| Amazon Linux 2 (Dashboards) | Upcoming | Node.js 18 EOL April 2025 |
| NMSLIB Engine | 3.0.0 | Use Faiss or Lucene engines instead |
| Performance-Analyzer-Rca | 3.0.0 | Replaced by Telemetry plugin |
| Dashboards-Visualizations (ganttCharts) | 3.0.0 | Plugin removal |
| Legacy Notebooks | 3.0.0 | Observability indexes support removal |
| SQL DSL Format | 3.0.0 | Various settings deprecated |

## Experimental Features

| Feature | Description |
|---------|-------------|
| Star Tree Aggregation | Metric aggregations and date histograms with up to 100x query reduction |
| Disk-Tiered Cache | Partitioned cache with concurrent read/write access |
| Derived Source for k-NN | Storage optimization by removing vectors from JSON source |
| Discover SQL/PPL | SQL and PPL query language support in Discover view |

## References

- [OpenSearch 2.19.0 Release Page](https://opensearch.org/versions/opensearch-2-19-0.html)
- [OpenSearch Release Notes](https://github.com/opensearch-project/OpenSearch/blob/2.19/release-notes/opensearch.release-notes-2.19.0.md)
- [OpenSearch Dashboards Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/2.19/release-notes/opensearch-dashboards.release-notes-2.19.0.md)
- [Consolidated Release Notes](https://github.com/opensearch-project/opensearch-build/blob/main/release-notes/opensearch-release-notes-2.19.0.md)
