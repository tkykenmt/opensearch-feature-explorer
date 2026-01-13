---
tags:
  - dashboards
  - indexing
  - ml
  - neural-search
  - performance
  - search
---

# OpenSearch v3.2.0 Release

## Overview

This page indexes all investigated release items for OpenSearch v3.2.0.

- Release Summary

## Release Reports

### OpenSearch

| Item | Category | Description |
|------|----------|-------------|
| Code Coverage (Gradle) | feature | Local code coverage generation with Gradle and JaCoCo plugin |
| Combined Fields Query | feature | New combined_fields query with BM25F scoring for multi-field text search |
| GRPC Transport | feature | GA release - module migration, plugin extensibility, proper gRPC status codes |
| Derived Source Integration | feature | Integration of derived source feature across get/search/recovery paths |
| IndexFieldDataService Async Close | bugfix | Async field data cache clearing to prevent cluster applier thread blocking |
| Staggered Merge Optimization | bugfix | Replace CPU load average with AverageTracker classes, adjust default thresholds |

### Neural Search

| Item | Category | Description |
|------|----------|-------------|
| Agentic Search | feature | [Experimental] Natural language search with agentic query clause and translator processor |
| Hybrid Query Normalization | enhancement | Upper bound for min-max normalization, inner hits with collapse, configurable collapse document storage |
| Semantic Field | enhancement | knn_vector field configuration, batch size, prune strategies, chunking, embedding reuse |

### OpenSearch Dashboards

| Item | Category | Description |
|------|----------|-------------|
| Vended Dashboard Progress | feature | Polling-based index state detection for background data sync progress |
| Explore UI Enhancements | feature | New Explore plugin with auto-visualization, multi-flavor support, and dashboard embeddable |
| Static Banner Plugin | feature | Global configurable header banner for announcements |
| Global Banner Support | feature | UI Settings integration for dynamic banner configuration |
| Discover Plugin Fixes | bugfix | Fix empty page when no index patterns, add Cypress tests |
| OUI (OpenSearch UI) Updates | bugfix | Update OUI component library from 1.19 to 1.21 |
| Query Editor UI | bugfix | Autocomplete fixes, generated query UI improvements, edit button placement |
| UI Settings & Dataset Select | bugfix | UI settings client robustness, dataset selector visual updates |
| UI Settings Backward Compatibility | feature | Restore backward compatibility for multi-scope UI settings client |
| Chart & Visualization Fixes | bugfix | Line chart legend display fix, popover toggle fix |
| Data Source Selector Scope | feature | Workspace-aware scope support for data source selector |
| Trace Details Page | feature | Dedicated trace investigation page with Gantt chart and service map |
| Bar Chart Enhancements | feature | Bar size control switch for auto/manual bar sizing |
| Dashboards CVE Fixes | deprecation | [CVE-2025-48387] tar-fs security update |
| Dashboards Code Quality & Testing | bugfix | Testing guidelines, @ts-expect-error migration, Cypress tests for Explore, component refactoring |

### OpenSearch

| Item | Category | Description |
|------|----------|-------------|
| Rule-based Auto Tagging Fix | bugfix | Fix delete rule event consumption for wildcard index based rules |
| Rule-based Auto Tagging | feature | Bug fixes and improvements: stricter attribute extraction, centralized validation, force refresh |
| Rule Cardinality Limit | feature | Configurable limit on WLM auto-tagging rule cardinality (default: 200) |
| System Ingest Pipeline Fix | bugfix | Fix system ingest pipeline to properly handle index templates |
| System Ingest Processor | feature | Pass index settings to system ingest processor factories |
| Azure Repository Fixes | bugfix | Fix SOCKS5 proxy authentication for Azure repository |
| Profiler Enhancements | bugfix | Fix concurrent timings in profiler for concurrent segment search |
| Fetch Phase Profiling | feature | Comprehensive fetch phase profiling with detailed timing breakdowns |
| Plugin Profiling | feature | Plugin profiling extensibility and multi-shard fetch phase profiling |
| Engine Optimization Fixes | bugfix | Fix leafSorter optimization for ReadOnlyEngine and NRTReplicationEngine |
| Search Preference & Awareness Fix | bugfix | Fix custom preference string to ignore awareness attributes for consistent routing |
| Settings Management | bugfix | Ignore archived settings on update to unblock settings modifications |
| SecureRandom Blocking Fix | bugfix | Fix startup freeze on low-entropy systems by reverting to non-blocking SecureRandom |
| Field Mapping Fixes | bugfix | Fix field-level ignore_malformed override and scaled_float encodePoint method |
| Search Scoring Fixes | bugfix | Fix max_score null when sorting by _score with secondary fields |
| Replication Lag Fix | bugfix | Fix segment replication lag computation using correct epoch timestamps |
| Parent-Child Query Fixes | bugfix | Fix QueryBuilderVisitor pattern for HasParentQuery and HasChildQuery |
| HTTP/2 & Reactor-Netty Fix | bugfix | Fix HTTP/2 communication when reactor-netty-secure transport is enabled |
| Query String & Regex Fixes | bugfix | Fix field alias support, COMPLEMENT flag, and TooComplexToDeterminizeException handling |
| Aggregation Task Cancellation | feature | Add task cancellation checks in aggregators to terminate long-running queries |
| Node Duress Caching | feature | Time-based caching for node duress values to reduce search latency overhead |
| Segment Concurrent Search Optimization | feature | Optimize segment grouping for concurrent search with balanced document distribution |
| Dependency Bumps (OpenSearch Core) | feature | 20 dependency updates including Lucene 10.2.2, Log4j 2.25.1, BouncyCastle, OkHttp 5.1.0 |
| Repository Rate Limiters | feature | Dynamic rate limiter settings for snapshot/restore operations |
| Secure Aux Transport Settings | feature | API update to distinguish between auxiliary transport types for SSL configuration |
| Searchable Snapshots & Writeable Warm | feature | FS stats for warm nodes based on addressable space; default remote_data_ratio changed to 5 |
| Subject Interface Update | feature | Update Subject interface to use CheckedRunnable instead of Callable |
| Numeric Terms Aggregation Optimization | feature | QuickSelect algorithm for large bucket count terms aggregations |
| Numeric Field Skip List | feature | Skip list indexing for numeric field doc values to improve range query performance |
| Scripted Metric Aggregation | feature | Support InternalScriptedMetric in InternalValueCount and InternalAvg reduce methods |
| Composite Aggregation Optimization | feature | Optimize composite aggregations by removing unnecessary object allocations |
| Remote Store Segment Warming | feature | Remote store support for merged segment warming to reduce replication lag |
| Streaming Transport & Aggregation | feature | Stream transport framework and streaming aggregation for memory-efficient high-cardinality aggregations |
| Approximation Framework Enhancements | feature | search_after support, range queries with now, multi-sort handling |
| Approximation Framework: Numeric Types | feature | Extend Approximation Framework to int, float, double, half_float, unsigned_long |
| Star Tree Index | feature | IP field search support and star-tree search statistics |
| Clusterless Mode | feature | Experimental clusterless startup mode and custom remote store path prefix |
| Cluster Info & Resource Stats | feature | Add NodeResourceUsageStats to ClusterInfo for cluster-wide resource visibility |
| BooleanQuery Rewrite Optimizations | feature | Extend must_not rewrite to numeric match, term, and terms queries (up to 54x speedup) |
| Rescore Named Queries | feature | Surface named queries from rescore contexts in matched_queries array |
| Semantic Version Field Type | feature | New `version` field type for semantic versioning with proper ordering and range queries |
| Query Phase Plugin Extension | feature | Plugin extensibility for injecting custom QueryCollectorContext during QueryPhase |
| Search Pipeline in Templates | feature | Support for search pipeline in search and msearch template APIs |
| Pull-based Ingestion | feature | File-based ingestion plugin (ingestion-fs) for local testing |
| Cat Indices API Enhancement | feature | Add last index request timestamp columns to `_cat/indices` API |
| Remote Store Metadata API | feature | New cluster-level API to fetch segment and translog metadata from remote store |
| Java Agent AccessController | feature | OpenSearch replacement for JDK's deprecated AccessController for privileged operations |
| Secure Transport Parameters | feature | SecureHttpTransportParameters API for cleaner SSL configuration in Reactor Netty 4 HTTP transport |
| Custom Index Name Resolver | feature | Plugin extensibility for custom index name expression resolvers |
| Workload Management | feature | WLM mode validation for CRUD operations, naming consistency updates, logging improvements |
| Warm Indices | feature | Write block on flood watermark, addressable space-based FS stats, resize restrictions |
| Hierarchical & ACL-aware Routing | feature | New routing processors for hierarchical paths and ACL-based document co-location |
| Terms Lookup Query Enhancement | feature | Query clause support for terms lookup enabling multi-document value extraction |

### Observability

| Item | Category | Description |
|------|----------|-------------|
| Observability Infrastructure | bugfix | Maven snapshot publishing migration, Gradle 8.14.3 upgrade, JDK24 CI support |
| Observability Service Map | enhancement | User-configurable service map max nodes and max edges settings |

### Dashboards Observability

| Item | Category | Description |
|------|----------|-------------|
| Observability Bugfixes | bugfix | Traces error display fix (nested status.code), metrics visualization fix for local cluster |

### Geospatial

| Item | Category | Description |
|------|----------|-------------|
| Geospatial Infrastructure | bugfix | Upgrade Gradle to 8.14.3 and run CI checks with JDK24 |
| Geospatial Plugin | bugfix | Block HTTP redirects in IP2Geo, migrate to PluginSubject for system index access |

### Performance Analyzer

| Item | Category | Description |
|------|----------|-------------|
| Performance Analyzer Infrastructure | bugfix | Bump SpotBugs to 6.2.2 and Checkstyle to 10.26.1 |

### Learning to Rank

| Item | Category | Description |
|------|----------|-------------|
| XGBoost Missing Values Support | feature | Proper NaN handling for XGBoost models to match native XGBoost behavior |
| OpenSearch Learning to Rank | bugfix | Gradle 8.14 upgrade, JDK24 support, flaky test fix for similarity score comparisons |

### Notifications

| Item | Category | Description |
|------|----------|-------------|
| Notifications Plugin Infrastructure | bugfix | Gradle 8.14 upgrade, JaCoCo 0.8.13, nebula.ospackage 12.0.0, JDK24 CI support |

### ML Commons

| Item | Category | Description |
|------|----------|-------------|
| ML Commons Agent Tools & Memory | bugfix | Execute Tool API, AI-oriented memory containers, QueryPlanningTool, agent enhancements, bug fixes |
| ML Commons Sparse Encoding | enhancement | TOKEN_ID format support for sparse encoding/tokenize models |
| ML Commons Model Deployment | enhancement | Auto-deploy remote models in partially deployed status |
| ML Commons Testing & Coverage | bugfix | Integration test stability fix, memory container unit tests, JaCoCo 0.8.13 upgrade |
| ML Commons Documentation & Tutorials | bugfix | Multi-modal search, semantic highlighter, neural sparse, language identification, agentic RAG tutorials |
| ML Commons Error Handling | enhancement | Proper 400 errors instead of 500 for agent execute and MCP tool registration |
| ML Commons Connectors | enhancement | Pre/post-process function validation and improved URI validation for connectors |

### Dashboards Search Relevance

| Item | Category | Description |
|------|----------|-------------|
| Search Relevance Workbench | enhancement | New default UI, dashboard visualization, polling mechanism, date filtering, task scheduling |
| Toast Notification Bugfix | bugfix | Fix error messages not rendering correctly in toast notifications |
| Repository Maintenance | bugfix | Maintainer updates, issue templates, codecov integration, GitHub Actions dependency bumps |

### Search Relevance

| Item | Category | Description |
|------|----------|-------------|
| Search Relevance Bugfixes | bugfix | 7 bug fixes: error messaging, pipeline errors, UI overflow, Venn diagram, REST API status, input validation, pipeline parameter |

### Query Insights

| Item | Category | Description |
|------|----------|-------------|
| Release Notes & Documentation | bugfix | Release notes for v3.2.0 with reader search limit increase and infrastructure updates |

### Query Insights Dashboards

| Item | Category | Description |
|------|----------|-------------|
| Query Insights Bugfixes | bugfix | react-vis migration, search bar fix, table sorting fix, UI improvements |
| Query Insights Live Queries Enhancement | enhancement | Updated default auto-refresh interval from 5s to 30s |

### SQL

| Item | Category | Description |
|------|----------|-------------|
| SQL/PPL Engine Enhancements | enhancement | Expanded pushdown (sort, aggregation, partial filter, span, relevance), RelJson security, ~30% performance improvement |
| SQL/PPL Documentation | bugfix | Update PPL documentation index and V3 engine limitations |

### Asynchronous Search

| Item | Category | Description |
|------|----------|-------------|
| Asynchronous Search Bugfix | bugfix | Gradle 8.14.3 upgrade, JDK 24 CI support, Maven snapshot endpoint migration |

### Alerting

| Item | Category | Description |
|------|----------|-------------|
| Alerting Plugin | bugfix | MGet bug fix, randomized fan-out distribution, consistent API responses |

### Index Management

| Item | Category | Description |
|------|----------|-------------|
| ISM Transitions Enhancement | bugfix | New `no_alias` and `min_state_age` transition conditions, ISM history index as System Index |

### Anomaly Detection

| Item | Category | Description |
|------|----------|-------------|
| Anomaly Detection Enhancements | enhancement | Support for >1 hour detection intervals, centralized resource access control |
| Anomaly Detection Bugfixes | bugfix | Concurrency fixes for HCAD, forecasting interval calculation, Dashboards UI improvements |

### Cross-Cluster Replication

| Item | Category | Description |
|------|----------|-------------|
| Cross-Cluster Replication | bugfix | Add missing method for RemoteClusterRepository class to fix build failure |

### k-NN

| Item | Category | Description |
|------|----------|-------------|
| k-NN Vector Search | feature | GPU indexing for FP16/Byte/Binary, ADC, random rotation, gRPC support, dynamic thread defaults |
| Lucene-on-Faiss: ADC Support | enhancement | ADC support for memory-optimized search with binary quantized indexes |
| Remote Vector Index Build | bugfix | Don't fall back to CPU on terminal failures during remote index build |

### Flow Framework

| Item | Category | Description |
|------|----------|-------------|
| Flow Framework Utilities | feature | JsonToJsonRecommender and JsonToJsonTransformer utilities for automated JSON field mapping and transformation |
| Flow Framework Bugfixes | bugfix | Memory fixes, error handling, 3.1+ API compatibility, race condition fix, default template fixes |

### Security Analytics Dashboards Plugin

| Item | Category | Description |
|------|----------|-------------|
| Security Analytics Bugfixes | bugfix | Remove Vega-based correlated findings chart, update IOC types API |

### Reporting

| Item | Category | Description |
|------|----------|-------------|
| Reporting Plugin | bugfix | System context for index creation, tenant URL parsing fix |

### Dashboards Assistant

| Item | Category | Description |
|------|----------|-------------|
| Dashboards Core Bugfixes | bugfix | Fix unit test failures due to missing Worker in Jest environment |
| Dashboards Assistant | enhancement | Support natural language visualization in new dashboard ingress (Explore UI) |

### Skills

| Item | Category | Description |
|------|----------|-------------|
| Skills Plugin Enhancements | enhancement | Index schema merging for PPLTool, error message masking, standardized parameter handling |

### Multi-Repository

| Item | Category | Description |
|------|----------|-------------|
| CVE Fixes & Dependency Updates | bugfix | CVE-2025-48734 (beanutils) and CVE-2025-7783 (form-data) security fixes |
| Version Increment (Maintenance) | bugfix | Version bumps to 3.2.0 across 14 repositories |
| Build Infrastructure (Gradle/JDK) | bugfix | Gradle 8.14/8.14.3, JDK 24 CI support, Maven endpoint updates across 17+ repositories |

### Common Utils

| Item | Category | Description |
|------|----------|-------------|
| Common Utils Bugfixes | bugfix | CVE-2025-48734 fix, PublishFindingsRequest revert, Gradle 8.14/JDK 24 upgrade |

### Security

| Item | Category | Description |
|------|----------|-------------|
| Resource Sharing | feature | Migration API, Resource Access Evaluator for automatic authorization, client accessor pattern fix |
| Permission Validation | feature | Query parameter to check API permissions without executing the request |
| Auxiliary Transport SSL | feature | TLS support for auxiliary transports (gRPC, etc.) with per-transport SSL configuration |
| Security FIPS Compliance | enhancement | Full FIPS 140-2 compliance with BC-FIPS libraries and OpenSAML shadow JAR isolation |
| Security Performance Optimization | enhancement | Precomputed privileges toggle and optimized wildcard matching |
| Star Tree Security Integration | enhancement | Disable star-tree optimization for users with DLS/FLS/Field Masking restrictions |
| Security Plugin Enhancements | enhancement | Nested JWT claims, stream transport integration, plugin permissions, tenancy access, bug fixes |

### Common (Security)

| Item | Category | Description |
|------|----------|-------------|
| Tenancy Access Control | enhancement | Add tenancy access level (READ/WRITE/NONE) to serialized user in thread context |

### Job Scheduler

| Item | Category | Description |
|------|----------|-------------|
| Job Scheduler Enhancements | feature | REST APIs for listing jobs and locks, second-level interval scheduling, LockService extensibility |

### Custom Codecs

| Item | Category | Description |
|------|----------|-------------|
| Composite Index Support | feature | Support for composite indexes (star-tree) with custom codecs |

### User Behavior Insights

| Item | Category | Description |
|------|----------|-------------|
| User Behavior Insights Data Generator | enhancement | Add search_config field for A/B TDI testing simulation |

### Security Dashboards Plugin

| Item | Category | Description |
|------|----------|-------------|
| Security Dashboards Enhancements | enhancement | Full index pattern display in role view, added missing index permissions |

### Security

| Item | Category | Description |
|------|----------|-------------|
| SPIFFE X.509 SVID Support | feature | SPIFFE-based workload identity authentication via SPIFFEPrincipalExtractor |
| Argon2 Password Hashing | feature | Argon2 password hashing algorithm support with full parameter configurability |
| Security Configuration Management | feature | Experimental versioned security configuration management with rollback/roll-forward foundation |
