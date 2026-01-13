---
tags:
  - dashboards
  - ml
  - performance
  - search
  - sql
---

# OpenSearch v3.4.0 Release Summary

## Summary

OpenSearch 3.4.0 delivers significant performance improvements, expanded PPL functionality, and a redesigned agentic search experience. Key highlights include up to 40% faster aggregation workloads through Lucene's bulk collection API, ~19% improvement in scroll query performance, enhanced gRPC transport with expanded query support, and new PPL commands for data exploration. The release also introduces a no-code agentic search UI with MCP integration and comprehensive infrastructure upgrades to JDK 25 and Gradle 9.2 across all plugins.

## Highlights

```mermaid
graph TB
    subgraph "Performance"
        A[Aggregation Optimizations<br/>5-40% faster]
        B[Scroll Query Caching<br/>~19% improvement]
        C[Percentiles MergingDigest<br/>Low-cardinality boost]
    end
    
    subgraph "Query & Analytics"
        D[New PPL Commands<br/>chart, streamstats, multisearch]
        E[gRPC Query Support<br/>6 new query types]
        F[Filter Rewrite<br/>Sub-aggregation optimization]
    end
    
    subgraph "AI & Search"
        G[Agentic Search UX<br/>No-code agent builder]
        H[MCP Integration<br/>External tool support]
        I[Scheduled Experiments<br/>Cron-based execution]
    end
    
    subgraph "Infrastructure"
        J[JDK 25 Support]
        K[Gradle 9.2 Upgrade]
        L[24 Plugin Updates]
    end
```

## New Features

| Feature | Description | Report |
|---------|-------------|--------|
| PPL Alerting | V2 alerting API with PPL query support, stateless alerts, per-result and result-set trigger modes | Details |
| Agentic Search UX | No-code agent builder with MCP server support, conversational memory, and simplified configuration | Details |
| Scheduled Experiments | Cron-based scheduling for recurring search relevance experiments with historical tracking | Details |
| ISM Exclusion Pattern | Support exclusion patterns in ISM templates using `-` prefix for selective index management | Details |
| k-NN Memory Optimized Warmup | Optimized warmup procedure for memory-optimized search with page cache pre-loading | Details |
| Query Version-Aware Settings | Dynamic feature detection based on cluster version for Query Insights Dashboards | Details |
| WLM Security Attributes | Security attribute extraction for WLM rule-based auto-tagging (username, roles) | Details |
| Anomaly Detection Daily Insights | AI-powered anomaly correlation with automated detector creation via ML agents | Details |
| Remote Store CMK Support | Customer-managed key encryption/decryption with STS role assumption for cross-account access | Details |
| Flow Framework Access Control | Integration with centralized Resource Sharing and Access Control framework | Details |

## Improvements

| Area | Description | Report |
|------|-------------|--------|
| Aggregation Performance | Hybrid cardinality collector, filter rewrite + skip list (up to 10x), MergingDigest for percentiles, matrix_stats 5x speedup | Details |
| Scroll Query Performance | Cache StoredFieldsReader per segment for ~19% improvement | Details |
| gRPC Transport | Support for ConstantScoreQuery, FuzzyQuery, MatchBoolPrefixQuery, MatchPhrasePrefix, PrefixQuery, MatchQuery; CBOR/SMILE/YAML formats | Details |
| PPL Commands | New chart, streamstats, multisearch, replace, appendpipe commands; bucket_nullable, usenull options | Details |
| PPL Functions | New mvindex, mvdedup, mvappend, tostring functions; per_second/minute/hour/day for timechart | Details |
| PPL Query Optimization | 33 enhancements including sort pushdown, distinct count approx, case-to-range queries | Details |
| Security Configuration | Dedicated config reloading thread, dynamic resource settings, X509v3 SAN authentication, securityadmin timeout | Details |
| Resource Sharing | Multi-type index support, ResourceProvider interface, Builder pattern, REST API improvements | Details |
| Dashboards Explore | Histogram breakdowns, Field Statistics tab, trace flyout, correlations, cancel query | Details |
| Dashboards Chat | Global search integration, suggestion system, state persistence, session storage | Details |
| ML Commons | Sensitive parameter filtering, resource type support, increased batch task limits (max: 10,000) | Details |
| k-NN Enhancements | Native SIMD scoring for FP16, VectorSearcherHolder memory optimization | Details |
| SEISMIC Nested Field | Support nested field ingestion and query for text chunking workflows | Details |

## Bug Fixes

| Area | Description | PR |
|------|-------------|-----|
| SQL/PPL | 48 bug fixes including memory exhaustion, race conditions, rex nested capture groups | Details |
| Security | Multi-tenancy `.kibana` index fix, WildcardMatcher empty string handling, DLS/FLS internal request fix | Details |
| k-NN | Memory optimized search fixes, race condition in KNNQueryBuilder, Faiss inner product score calculation | Details |
| Query Bugfixes | Fix crashes in wildcard queries, aggregations, highlighters, script score queries | Details |
| gRPC Transport | Fix ClassCastException for large requests, Bulk API fixes, node bootstrap with streaming transport | Details |
| Index Management | Fix ISM policy rebinding, SM deletion snapshot pattern parsing, rollup test race conditions | Details |
| ML Commons | Agent type update validation, QueryPlanningTool model ID parsing, agentic memory multi-node fixes | Details |
| Neural Search | SEISMIC IT failures, query handling without method_parameters, disk space recovery | Details |
| Anomaly Detection | 3-AZ forecast results index creation, frequency-aware missing data detection | Details |
| Search Relevance | Hybrid optimizer floating-point precision, query serialization for LTR plugins | Details |

## Breaking Changes

| Change | Migration | Report |
|--------|-----------|--------|
| Stats Builder Pattern | 30+ Stats classes deprecated constructors in favor of Builder pattern | Details |
| System Indices Deprecation | `plugins.security.system_indices.indices` setting deprecated | Details |
| AccessController Migration | Migrate from `java.security.AccessController` to `org.opensearch.secure_sm.AccessController` | Details |

## Dependencies

Notable dependency updates in this release:

- **Lucene**: 10.3.1 → 10.3.2 (MaxScoreBulkScorer bug fix)
- **Gradle**: 9.2.0 across all plugins
- **JDK**: 25 support across all plugins
- **Netty**: 4.2.4 (HTTP/3 readiness)
- **Calcite**: 1.41.0 for SQL plugin
- **Security**: 28 dependency updates addressing CVE-2025-11226, CVE-2025-58457, CVE-2025-41249

See Dependency Updates and JDK 25 & Gradle 9.2 Upgrades for details.

## References

- [Official Release Notes](https://github.com/opensearch-project/opensearch-build/blob/main/release-notes/opensearch-release-notes-3.4.0.md)
- [OpenSearch Core Release Notes](https://github.com/opensearch-project/OpenSearch/blob/main/release-notes/opensearch.release-notes-3.4.0.md)
- [OpenSearch Dashboards Release Notes](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/release-notes/opensearch-dashboards.release-notes-3.4.0.md)
- [Feature Reports](features/)
