---
tags:
  - indexing
  - k-nn
  - neural-search
  - observability
  - performance
  - search
  - security
  - sql
---

# OpenSearch v3.2.0 Release Summary

## Summary

OpenSearch 3.2.0 delivers major advancements in search performance, AI capabilities, and security. Key highlights include gRPC Transport reaching GA status, expanded GPU support for vector search, experimental Agentic Search for natural language queries, streaming aggregation for memory-efficient high-cardinality workloads, and enhanced semantic field configuration. The release also brings significant PPL/SQL engine improvements, new security features including Argon2 password hashing and SPIFFE authentication, and comprehensive infrastructure updates across the ecosystem.

## Highlights

```mermaid
graph TB
    subgraph "Key Changes in v3.2.0"
        subgraph "Performance"
            GRPC[gRPC Transport GA]
            STREAM[Streaming Aggregation]
            APPROX[Approximation Framework<br/>All Numeric Types]
            PPL[PPL Calcite ~30%<br/>Performance Boost]
        end
        
        subgraph "AI & Search"
            AGENTIC[Agentic Search<br/>Experimental]
            SEMANTIC[Semantic Field<br/>Enhancements]
            GPU[GPU Indexing<br/>FP16/Byte/Binary]
            ADC[ADC & Random Rotation<br/>for Binary Quantization]
        end
        
        subgraph "Security"
            ARGON2[Argon2 Password<br/>Hashing]
            SPIFFE[SPIFFE X.509<br/>SVID Support]
            FIPS[FIPS 140-2<br/>Compliance]
        end
        
        subgraph "Observability"
            STARTREE[Star-tree IP Field<br/>& Statistics]
            TRACE[Trace Details Page]
            EXPLORE[Explore UI]
        end
    end
```

## New Features

| Feature | Description | Report |
|---------|-------------|--------|
| gRPC Transport GA | Production-ready gRPC transport with plugin extensibility and proper status codes | [Details](features/opensearch/grpc-transport.md) |
| Agentic Search | [Experimental] Natural language search with LLM-powered query translation | [Details](features/neural-search/neural-search-agentic-search.md) |
| Streaming Aggregation | Memory-efficient aggregation via segment-level streaming to coordinator | [Details](features/opensearch/opensearch-streaming-transport-aggregation.md) |
| GPU Indexing (FP16/Byte/Binary) | Extended GPU acceleration for additional vector types | [Details](features/k-nn/k-nn-vector-search.md) |
| ADC & Random Rotation | Improved recall for binary quantized indices | [Details](features/k-nn/k-nn-vector-search.md) |
| Argon2 Password Hashing | Modern memory-hard password hashing algorithm | [Details](features/security/security-argon2-password-hashing.md) |
| SPIFFE X.509 SVID Support | Workload identity authentication via SPIFFE | [Details](features/security/security-spiffe-x.509-svid-support.md) |
| Semantic Version Field Type | New `version` field type for semantic versioning | [Details](features/opensearch/opensearch-semantic-version-field-type.md) |
| Combined Fields Query | BM25F scoring for multi-field text search | [Details](features/opensearch/opensearch-combined-fields-query.md) |
| Execute Tool API | Direct tool execution without agent orchestration | [Details](features/ml-commons/ml-commons-agent-tools-memory.md) |
| Memory Container APIs | AI-oriented persistent memory for agents | [Details](features/ml-commons/ml-commons-agent-tools-memory.md) |
| Job Scheduler REST APIs | List jobs and locks via REST endpoints | [Details](features/job-scheduler/job-scheduler-enhancements.md) |
| Explore UI | New data exploration plugin with auto-visualization | [Details](features/opensearch-dashboards/explore-ui-enhancements.md) |
| Trace Details Page | Dedicated trace investigation with Gantt chart | [Details](features/opensearch-dashboards/trace-details-page.md) |
| Flow Framework Utilities | JsonToJson Recommender and Transformer | [Details](features/flow-framework/flow-framework-utilities.md) |

## Improvements

| Area | Description | Report |
|------|-------------|--------|
| Semantic Field | knn_vector config, batch size, prune strategies, chunking, embedding reuse | [Details](features/neural-search/neural-search-semantic-field.md) |
| Hybrid Query | Upper bound for min-max normalization, inner hits with collapse | [Details](features/neural-search/hybrid-query-normalization.md) |
| Approximation Framework | Extended to all numeric types (int, float, double, half_float, unsigned_long) | [Details](features/opensearch/approximation-framework-numeric-types.md) |
| PPL/SQL Engine | Expanded pushdown, RelJson security, ~30% performance improvement | [Details](features/sql/ppl-engine.md) |
| Star-tree Index | IP field search support and query statistics | [Details](features/opensearch/opensearch-star-tree-index.md) |
| Security Performance | Precomputed privileges toggle, optimized wildcard matching | [Details](features/security/security-performance-optimization.md) |
| FIPS Compliance | BC-FIPS libraries, OpenSAML shadow JAR isolation | [Details](features/security/security-opensearch-fips-compliance.md) |
| Anomaly Detection | Support for >1 hour intervals, centralized resource access control | [Details](features/anomaly-detection/anomaly-detection-enhancements.md) |
| ML Commons Connectors | Pre/post-process validation, improved URI validation | [Details](features/ml-commons/ml-commons-connectors.md) |
| Search Relevance Workbench | New default UI, dashboard visualization, task scheduling | [Details](features/dashboards-search-relevance/search-relevance-workbench.md) |
| Query Insights | MDS support for inflight queries, 30s default auto-refresh | [Details](features/query-insights-dashboards/query-insights-live-queries-enhancement.md) |
| Lucene-on-Faiss | ADC support for memory-optimized binary quantized search | [Details](features/k-nn/k-nn-lucene-on-faiss.md) |

## Bug Fixes

| Fix | Description | PR |
|-----|-------------|-----|
| SecureRandom Blocking | Fix startup freeze on low-entropy systems | [#18xxx](https://github.com/opensearch-project/OpenSearch/pull/18xxx) |
| HTTP/2 Reactor-Netty | Fix communication when secure transport enabled | [Details](features/opensearch/http2-reactor-netty-fix.md) |
| Replication Lag | Fix segment replication lag computation | [Details](features/opensearch/replication-lag-fix.md) |
| Search Scoring | Fix max_score null when sorting by _score | [Details](features/opensearch/search-scoring-fixes.md) |
| Field Mapping | Fix ignore_malformed override and scaled_float | [Details](features/opensearch/field-mapping-fixes.md) |
| Query String | Fix field alias, COMPLEMENT flag, regex handling | [Details](features/opensearch/query-string-regex-fixes.md) |
| Alerting MGet | Fix MGet bug, randomize fan-out distribution | [Details](features/alerting/alerting-plugin.md) |
| Flow Framework | Memory fixes, error handling, race condition fix | [Details](features/flow-framework/flow-framework-bugfixes.md) |
| Neural Search Collapse | Fix collapse bug with knn query deduplication | [#1413](https://github.com/opensearch-project/neural-search/pull/1413) |
| CVE-2025-48734 | commons-beanutils security fix | [Details](features/multi-repo/cve-fixes-opensearch-dashboards-dependency-updates.md) |

## Breaking Changes

| Change | Migration | Report |
|--------|-----------|--------|
| PPL v2 Fallback Disabled | Set `plugins.calcite.fallback.allowed=true` to re-enable | [Details](features/sql/ppl-engine.md) |
| gRPC Package Rename | Update imports from `org.opensearch.plugin.transport.grpc` to `org.opensearch.transport.grpc` | [Details](features/opensearch/grpc-transport.md) |

## Experimental Features

| Feature | Description | Enable Setting |
|---------|-------------|----------------|
| Agentic Search | Natural language query translation | `plugins.neural_search.agentic_search_enabled` |
| Streaming Aggregation | Memory-efficient high-cardinality aggregations | `opensearch.experimental.feature.transport.stream.enabled` |
| Clusterless Mode | Startup without cluster coordination | Experimental flag |
| Security Config Management | Versioned security configuration | Experimental flag |
| Agentic Memory | AI-oriented memory containers | `plugins.ml_commons.agentic_memory.enabled` |

## Infrastructure Updates

Notable infrastructure changes across the ecosystem:

- **Gradle**: Upgraded to 8.14/8.14.3 across 17+ repositories
- **JDK**: CI support for JDK 24
- **Lucene**: Updated to 10.2.2
- **Log4j**: Updated to 2.25.1
- **BouncyCastle**: Replaced with BC-FIPS for FIPS compliance
- **Maven**: Snapshot publishing endpoint migration

## Dependencies

Notable dependency updates from the official release notes:

- Lucene 10.2.2
- Log4j 2.25.1
- BouncyCastle (BC-FIPS)
- OkHttp 5.1.0
- commons-beanutils 1.11.0 (CVE fix)
- commons-lang3 3.18.0 (CVE fix)

## References

- [Official Release Notes](https://github.com/opensearch-project/opensearch-build/blob/main/release-notes/opensearch-release-notes-3.2.0.md)
- [OpenSearch Core Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-3.2.0.md)
- [OpenSearch Dashboards Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-3.2.0.md)
- [Release Artifacts](https://opensearch.org/artifacts/by-version/#release-3-2-0)
- [Feature Reports](features/)
