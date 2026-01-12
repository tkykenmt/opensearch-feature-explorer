---
tags:
  - dashboards
  - indexing
  - k-nn
  - ml
  - neural-search
  - performance
  - search
  - security
---

# OpenSearch v2.18.0 Release Summary

## Summary

OpenSearch 2.18.0 delivers significant enhancements for building ML-powered applications, improving search performance, and enabling better team collaboration. Key highlights include the experimental star-tree index for sub-millisecond aggregations, workload management for tenant-level resource control, enhanced workspace collaboration features in Dashboards, and major k-NN performance improvements with FAISS as the new default engine.

## Highlights

```mermaid
graph TB
    subgraph "Key Changes in v2.18.0"
        subgraph "Search & Analytics"
            ST[Star Tree Index]
            WLM[Workload Management]
            QI[Query Insights]
        end
        subgraph "ML & AI"
            T2V[Text to Visualization]
            NS[Neural Search Reranking]
            KNN[k-NN FAISS Default]
        end
        subgraph "Collaboration"
            WS[Workspace Enhancements]
            NAV[Navigation Updates]
            MDS[Multi Data Source]
        end
        subgraph "Infrastructure"
            LU[Lucene 9.12.0]
            TC[Tiered Caching]
            SEC[Security Enhancements]
        end
    end
```

## New Features

| Feature | Description | Report |
|---------|-------------|--------|
| Star Tree Index | Experimental multi-field index for sub-millisecond aggregation queries with precomputed results | [Details](features/opensearch/star-tree-index.md) |
| Workload Management | Tenant-level admission control with CPU/memory limits, query sandboxing, and QueryGroup Stats API | [Details](features/opensearch/workload-management.md) |
| Text to Visualization | AI-powered visualization generation from natural language queries using LLM agents | [Details](features/dashboards-assistant/text-to-visualization.md) |
| ByFieldRerankProcessor | Second-level reranking based on document field values for improved search relevance | [Details](features/neural-search/neural-search-reranking.md) |
| Phone Analyzers | New `phone` and `phone-search` analyzers for global phone number parsing | [Details](features/opensearch/phone-analyzer.md) |
| Paginated List APIs | New `_list/indices` and `_list/shards` APIs with pagination for large clusters | [Details](features/opensearch/list-apis-paginated.md) |
| Query Insights Health Stats API | New `/_insights/health_stats` endpoint for monitoring plugin health | [Details](features/query-insights/query-insights.md) |
| LogPatternTool | New ML skill for log pattern analysis in alerting summaries | [Details](features/skills/ml-skills-tools.md) |
| Offline Nodes Library | Core abstractions for running background tasks on dedicated offline nodes | [Details](features/opensearch/offline-nodes.md) |

## Improvements

| Area | Description | Report |
|------|-------------|--------|
| k-NN Default Engine | Changed default engine from NMSLIB to FAISS with better indexing throughput | [Details](features/k-nn/k-nn-performance-engine.md) |
| k-NN AVX512 Support | AVX512 SIMD acceleration for Faiss engine on compatible x64 processors | [Details](features/k-nn/k-nn-avx512-support.md) |
| Lucene 9.12.0 | New postings format, JDK 23 support, dynamic range facets, memory optimizations | [Details](features/opensearch/lucene-upgrade.md) |
| Tiered Caching | Segmented cache architecture for improved concurrent read/write performance | [Details](features/opensearch/tiered-caching.md) |
| Workspace Collaboration | Workspace-level UI settings, collaborator management, data connection integration, ACL auditor | [Details](features/opensearch-dashboards/workspace.md) |
| Navigation Updates | Flattened navigation, persistent state, small screen support, global search bar | [Details](features/opensearch-dashboards/navigation-updates.md) |
| Query Insights Grouping | Field name and type support for more accurate query similarity grouping | [Details](features/query-insights/query-insights.md) |
| ML Inference Processor | Search extension output support, query string in input_map, MLToolSpec config field | [Details](features/ml-commons/ml-commons-model-inference.md) |
| Batch Job Management | Rate limiting, connector credentials, model group access control for batch operations | [Details](features/ml-commons/ml-commons-batch-jobs.md) |
| Security Audit Logs | Datastream support for audit logs with better lifecycle management | [Details](features/security/security-enhancements.md) |
| Hybrid Query Rescorer | Standard OpenSearch rescore functionality now works with hybrid queries | [Details](features/neural-search/neural-search-reranking.md) |
| Doc-Level Monitor | Separate query indices for external monitors, optimized query index lifecycle | [Details](features/alerting/alerting-doc-level-monitor.md) |
| Discover Enhancements | Data summary panel, PPL/SQL query options, autocomplete improvements | [Details](features/opensearch-dashboards/discover.md) |

## Bug Fixes

| Fix | Description | PR |
|-----|-------------|-----|
| Nested Aggregations | Fix infinite loop in nested aggregations with deep-level nested objects | [Details](features/opensearch/nested-aggregations.md) |
| Wildcard Query | Fix escaped wildcard character handling and case-insensitive queries | [Details](features/opensearch/wildcard-query-fixes.md) |
| Flat Object Field | Fix infinite loop when flat_object field contains invalid token types | [Details](features/opensearch/flat-object-field.md) |
| k-NN Memory Release | Add DocValuesProducers for proper memory release when closing indexes | [Details](features/k-nn/k-nn-performance-engine.md) |
| Neural Search Order | Fix incorrect document order for nested aggregations in hybrid query | [Details](features/neural-search/neural-search-bugfixes.md) |
| ML Commons Stability | Fix model stuck in deploying state during node crash/cluster restart | [Details](features/ml-commons/ml-commons-bugfixes.md) |
| Security System Index | Fix bug where admin could read system index | [Details](features/security/security-bugfixes.md) |
| SQL Pagination | Fix SQL pagination with `pretty` parameter and PIT refactor issues | [Details](features/sql/sql-pagination.md) |
| Alerting Query Index | Fix query index shard settings and auto-expand replicas | [Details](features/alerting/alerting-bugfixes.md) |
| Workspace UI | 13 bug fixes for workspace UI/UX, page crashes, and permissions | [Details](features/opensearch-dashboards/workspace-bugfixes.md) |

## Breaking Changes

| Change | Migration | Report |
|--------|-----------|--------|
| k-NN Default Engine | New indexes use FAISS by default; specify `"engine": "nmslib"` to continue using NMSLIB | [Details](features/k-nn/k-nn-performance-engine.md) |
| Query Insights Grouping | Field name/type grouping now enabled by default; set to `false` to maintain previous behavior | [Details](features/query-insights/query-insights-settings.md) |
| Identity Feature Flag | Experimental identity feature flag removed; authentication moved to plugins | [Details](features/opensearch/identity-feature-flag-removal.md) |

## Experimental Features

| Feature | Description | Report |
|---------|-------------|--------|
| Star Tree Index | Multi-field index for accelerated aggregations (requires feature flag) | [Details](features/opensearch/star-tree-index.md) |
| Discover Updates | Enhanced query experience with PPL/SQL support, improved data selector | [Details](features/opensearch-dashboards/discover.md) |
| Text to Visualization | Natural language to visualization generation | [Details](features/dashboards-assistant/text-to-visualization.md) |
| User Personal Settings | Scoped uiSettings with User Settings page | [Details](features/opensearch-dashboards/experimental-features.md) |

## Dependencies

Notable dependency updates in this release:

| Dependency | Version | Notes |
|------------|---------|-------|
| Apache Lucene | 9.12.0 | New postings format, JDK 23 support |
| Netty | 4.1.114 | Network layer updates |
| gRPC | 1.68.0 | RPC framework update |
| Protobuf | 3.25.5 | Serialization library |
| Gradle | 8.10.2 | Build system update |
| Jackson | 2.18.0 | JSON processing |
| commons-io | 2.14.0 | CVE-2024-47554 fix |

## References

- [Official Release Notes](https://github.com/opensearch-project/opensearch-build/blob/main/release-notes/opensearch-release-notes-2.18.0.md)
- [OpenSearch 2.18.0 Release Page](https://opensearch.org/versions/opensearch-2-18-0.html)
- [Feature Reports](features/)
