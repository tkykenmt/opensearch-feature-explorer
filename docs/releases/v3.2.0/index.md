# OpenSearch v3.2.0 Release

## Overview

This page indexes all investigated release items for OpenSearch v3.2.0.

## Release Reports

### OpenSearch

| Item | Category | Description |
|------|----------|-------------|
| [Code Coverage (Gradle)](features/opensearch/code-coverage-gradle.md) | feature | Local code coverage generation with Gradle and JaCoCo plugin |
| [Combined Fields Query](features/opensearch/combined-fields-query.md) | feature | New combined_fields query with BM25F scoring for multi-field text search |
| [GRPC Transport](features/opensearch/grpc-transport.md) | feature | GA release - module migration, plugin extensibility, proper gRPC status codes |
| [Derived Source Integration](features/opensearch/derived-source.md) | feature | Integration of derived source feature across get/search/recovery paths |
| [IndexFieldDataService Async Close](features/opensearch/indexfielddataservice-async-close.md) | bugfix | Async field data cache clearing to prevent cluster applier thread blocking |
| [Staggered Merge Optimization](features/opensearch/staggered-merge-optimization.md) | bugfix | Replace CPU load average with AverageTracker classes, adjust default thresholds |

### Neural Search

| Item | Category | Description |
|------|----------|-------------|
| [Agentic Search](features/neural-search/agentic-search.md) | feature | [Experimental] Natural language search with agentic query clause and translator processor |
| [Hybrid Query Normalization](features/neural-search/hybrid-query-normalization.md) | enhancement | Upper bound for min-max normalization, inner hits with collapse, configurable collapse document storage |
| [Semantic Field](features/neural-search/semantic-field.md) | enhancement | knn_vector field configuration, batch size, prune strategies, chunking, embedding reuse |

### OpenSearch Dashboards

| Item | Category | Description |
|------|----------|-------------|
| [Vended Dashboard Progress](features/opensearch-dashboards/vended-dashboard-progress.md) | feature | Polling-based index state detection for background data sync progress |
| [Explore UI Enhancements](features/opensearch-dashboards/explore-ui-enhancements.md) | feature | New Explore plugin with auto-visualization, multi-flavor support, and dashboard embeddable |
| [Static Banner Plugin](features/opensearch-dashboards/static-banner-plugin.md) | feature | Global configurable header banner for announcements |
| [Global Banner Support](features/opensearch-dashboards/global-banner-support.md) | feature | UI Settings integration for dynamic banner configuration |
| [Discover Plugin Fixes](features/opensearch-dashboards/discover-plugin-fixes.md) | bugfix | Fix empty page when no index patterns, add Cypress tests |
| [OUI (OpenSearch UI) Updates](features/opensearch-dashboards/oui-updates.md) | bugfix | Update OUI component library from 1.19 to 1.21 |
| [Query Editor UI](features/opensearch-dashboards/query-editor-ui.md) | bugfix | Autocomplete fixes, generated query UI improvements, edit button placement |
| [UI Settings & Dataset Select](features/opensearch-dashboards/ui-settings-dataset-select.md) | bugfix | UI settings client robustness, dataset selector visual updates |
| [UI Settings Backward Compatibility](features/opensearch-dashboards/ui-settings-backward-compatibility.md) | feature | Restore backward compatibility for multi-scope UI settings client |
| [Chart & Visualization Fixes](features/opensearch-dashboards/chart-visualization-fixes.md) | bugfix | Line chart legend display fix, popover toggle fix |
| [Data Source Selector Scope](features/opensearch-dashboards/data-source-selector-scope.md) | feature | Workspace-aware scope support for data source selector |
| [Trace Details Page](features/opensearch-dashboards/trace-details-page.md) | feature | Dedicated trace investigation page with Gantt chart and service map |
| [Bar Chart Enhancements](features/opensearch-dashboards/bar-chart-enhancements.md) | feature | Bar size control switch for auto/manual bar sizing |
| [Dashboards CVE Fixes](features/opensearch-dashboards/dashboards-cve-fixes.md) | deprecation | [CVE-2025-48387] tar-fs security update |

### OpenSearch

| Item | Category | Description |
|------|----------|-------------|
| [Rule-based Auto Tagging Fix](features/opensearch/rule-based-auto-tagging-fix.md) | bugfix | Fix delete rule event consumption for wildcard index based rules |
| [Rule-based Auto Tagging](features/opensearch/rule-based-auto-tagging.md) | feature | Bug fixes and improvements: stricter attribute extraction, centralized validation, force refresh |
| [Rule Cardinality Limit](features/opensearch/rule-cardinality-limit.md) | feature | Configurable limit on WLM auto-tagging rule cardinality (default: 200) |
| [System Ingest Pipeline Fix](features/opensearch/system-ingest-pipeline-fix.md) | bugfix | Fix system ingest pipeline to properly handle index templates |
| [System Ingest Processor](features/opensearch/system-ingest-processor.md) | feature | Pass index settings to system ingest processor factories |
| [Azure Repository Fixes](features/opensearch/azure-repository-fixes.md) | bugfix | Fix SOCKS5 proxy authentication for Azure repository |
| [Profiler Enhancements](features/opensearch/profiler-enhancements.md) | bugfix | Fix concurrent timings in profiler for concurrent segment search |
| [Fetch Phase Profiling](features/opensearch/fetch-phase-profiling.md) | feature | Comprehensive fetch phase profiling with detailed timing breakdowns |
| [Plugin Profiling](features/opensearch/plugin-profiling.md) | feature | Plugin profiling extensibility and multi-shard fetch phase profiling |
| [Engine Optimization Fixes](features/opensearch/engine-optimization-fixes.md) | bugfix | Fix leafSorter optimization for ReadOnlyEngine and NRTReplicationEngine |
| [Search Preference & Awareness Fix](features/opensearch/search-preference-awareness-fix.md) | bugfix | Fix custom preference string to ignore awareness attributes for consistent routing |
| [Settings Management](features/opensearch/settings-management.md) | bugfix | Ignore archived settings on update to unblock settings modifications |
| [SecureRandom Blocking Fix](features/opensearch/securerandom-blocking-fix.md) | bugfix | Fix startup freeze on low-entropy systems by reverting to non-blocking SecureRandom |
| [Field Mapping Fixes](features/opensearch/field-mapping-fixes.md) | bugfix | Fix field-level ignore_malformed override and scaled_float encodePoint method |
| [Search Scoring Fixes](features/opensearch/search-scoring-fixes.md) | bugfix | Fix max_score null when sorting by _score with secondary fields |
| [Replication Lag Fix](features/opensearch/replication-lag-fix.md) | bugfix | Fix segment replication lag computation using correct epoch timestamps |
| [Parent-Child Query Fixes](features/opensearch/parent-child-query-fixes.md) | bugfix | Fix QueryBuilderVisitor pattern for HasParentQuery and HasChildQuery |
| [HTTP/2 & Reactor-Netty Fix](features/opensearch/http2-reactor-netty-fix.md) | bugfix | Fix HTTP/2 communication when reactor-netty-secure transport is enabled |
| [Query String & Regex Fixes](features/opensearch/query-string-regex-fixes.md) | bugfix | Fix field alias support, COMPLEMENT flag, and TooComplexToDeterminizeException handling |
| [Aggregation Task Cancellation](features/opensearch/aggregation-task-cancellation.md) | feature | Add task cancellation checks in aggregators to terminate long-running queries |
| [Node Duress Caching](features/opensearch/node-duress-caching.md) | feature | Time-based caching for node duress values to reduce search latency overhead |
| [Segment Concurrent Search Optimization](features/opensearch/segment-concurrent-search-optimization.md) | feature | Optimize segment grouping for concurrent search with balanced document distribution |
| [Dependency Bumps (OpenSearch Core)](features/opensearch/dependency-bumps-opensearch-core.md) | feature | 20 dependency updates including Lucene 10.2.2, Log4j 2.25.1, BouncyCastle, OkHttp 5.1.0 |
| [Repository Rate Limiters](features/opensearch/repository-rate-limiters.md) | feature | Dynamic rate limiter settings for snapshot/restore operations |
| [Secure Aux Transport Settings](features/opensearch/secure-aux-transport-settings.md) | feature | API update to distinguish between auxiliary transport types for SSL configuration |
| [Searchable Snapshots & Writeable Warm](features/opensearch/searchable-snapshots-writeable-warm.md) | feature | FS stats for warm nodes based on addressable space; default remote_data_ratio changed to 5 |
| [Subject Interface Update](features/opensearch/subject-interface-update.md) | feature | Update Subject interface to use CheckedRunnable instead of Callable |
| [Numeric Terms Aggregation Optimization](features/opensearch/numeric-terms-aggregation-optimization.md) | feature | QuickSelect algorithm for large bucket count terms aggregations |
| [Numeric Field Skip List](features/opensearch/numeric-field-skip-list.md) | feature | Skip list indexing for numeric field doc values to improve range query performance |
| [Scripted Metric Aggregation](features/opensearch/scripted-metric-aggregation.md) | feature | Support InternalScriptedMetric in InternalValueCount and InternalAvg reduce methods |
| [Composite Aggregation Optimization](features/opensearch/composite-aggregation-optimization.md) | feature | Optimize composite aggregations by removing unnecessary object allocations |
| [Remote Store Segment Warming](features/opensearch/remote-store-segment-warming.md) | feature | Remote store support for merged segment warming to reduce replication lag |
| [Streaming Transport & Aggregation](features/opensearch/streaming-transport-aggregation.md) | feature | Stream transport framework and streaming aggregation for memory-efficient high-cardinality aggregations |
| [Approximation Framework Enhancements](features/opensearch/approximation-framework-enhancements.md) | feature | search_after support, range queries with now, multi-sort handling |
| [Approximation Framework: Numeric Types](features/opensearch/approximation-framework-numeric-types.md) | feature | Extend Approximation Framework to int, float, double, half_float, unsigned_long |
| [Star Tree Index](features/opensearch/star-tree-index.md) | feature | IP field search support and star-tree search statistics |
| [Clusterless Mode](features/opensearch/clusterless-mode.md) | feature | Experimental clusterless startup mode and custom remote store path prefix |
| [Cluster Info & Resource Stats](features/opensearch/cluster-info-resource-stats.md) | feature | Add NodeResourceUsageStats to ClusterInfo for cluster-wide resource visibility |
| [BooleanQuery Rewrite Optimizations](features/opensearch/booleanquery-rewrite-optimizations.md) | feature | Extend must_not rewrite to numeric match, term, and terms queries (up to 54x speedup) |
| [Rescore Named Queries](features/opensearch/rescore-named-queries.md) | feature | Surface named queries from rescore contexts in matched_queries array |
| [Semantic Version Field Type](features/opensearch/semantic-version-field-type.md) | feature | New `version` field type for semantic versioning with proper ordering and range queries |
| [Query Phase Plugin Extension](features/opensearch/query-phase-plugin-extension.md) | feature | Plugin extensibility for injecting custom QueryCollectorContext during QueryPhase |
| [Search Pipeline in Templates](features/opensearch/search-pipeline-in-templates.md) | feature | Support for search pipeline in search and msearch template APIs |
| [Pull-based Ingestion](features/opensearch/pull-based-ingestion.md) | feature | File-based ingestion plugin (ingestion-fs) for local testing |
| [Cat Indices API Enhancement](features/opensearch/cat-indices-api-enhancement.md) | feature | Add last index request timestamp columns to `_cat/indices` API |
| [Remote Store Metadata API](features/opensearch/remote-store-metadata-api.md) | feature | New cluster-level API to fetch segment and translog metadata from remote store |
| [Java Agent AccessController](features/opensearch/java-agent-accesscontroller.md) | feature | OpenSearch replacement for JDK's deprecated AccessController for privileged operations |
| [Secure Transport Parameters](features/opensearch/secure-transport-parameters.md) | feature | SecureHttpTransportParameters API for cleaner SSL configuration in Reactor Netty 4 HTTP transport |
| [Custom Index Name Resolver](features/opensearch/custom-index-name-resolver.md) | feature | Plugin extensibility for custom index name expression resolvers |
| [Workload Management](features/opensearch/workload-management.md) | feature | WLM mode validation for CRUD operations, naming consistency updates, logging improvements |
| [Warm Indices](features/opensearch/warm-indices.md) | feature | Write block on flood watermark, addressable space-based FS stats, resize restrictions |
| [Hierarchical & ACL-aware Routing](features/opensearch/hierarchical-acl-aware-routing.md) | feature | New routing processors for hierarchical paths and ACL-based document co-location |
| [Terms Lookup Query Enhancement](features/opensearch/terms-lookup-query-enhancement.md) | feature | Query clause support for terms lookup enabling multi-document value extraction |

### Observability

| Item | Category | Description |
|------|----------|-------------|
| [Observability Infrastructure](features/observability/observability-infrastructure.md) | bugfix | Maven snapshot publishing migration, Gradle 8.14.3 upgrade, JDK24 CI support |
| [Observability Service Map](features/observability/observability-service-map.md) | enhancement | User-configurable service map max nodes and max edges settings |

### Dashboards Observability

| Item | Category | Description |
|------|----------|-------------|
| [Observability Bugfixes](features/dashboards-observability/observability-bugfixes.md) | bugfix | Traces error display fix (nested status.code), metrics visualization fix for local cluster |

### Geospatial

| Item | Category | Description |
|------|----------|-------------|
| [Geospatial Infrastructure](features/geospatial/geospatial-infrastructure.md) | bugfix | Upgrade Gradle to 8.14.3 and run CI checks with JDK24 |
| [Geospatial Plugin](features/geospatial/geospatial-plugin.md) | bugfix | Block HTTP redirects in IP2Geo, migrate to PluginSubject for system index access |

### Performance Analyzer

| Item | Category | Description |
|------|----------|-------------|
| [Performance Analyzer Infrastructure](features/performance-analyzer/performance-analyzer-infrastructure.md) | bugfix | Bump SpotBugs to 6.2.2 and Checkstyle to 10.26.1 |

### Learning to Rank

| Item | Category | Description |
|------|----------|-------------|
| [XGBoost Missing Values Support](features/opensearch-learning-to-rank-base/xgboost-missing-values-support.md) | feature | Proper NaN handling for XGBoost models to match native XGBoost behavior |
| [OpenSearch Learning to Rank](features/opensearch-learning-to-rank-base/opensearch-learning-to-rank.md) | bugfix | Gradle 8.14 upgrade, JDK24 support, flaky test fix for similarity score comparisons |

### Notifications

| Item | Category | Description |
|------|----------|-------------|
| [Notifications Plugin Infrastructure](features/notifications/notifications-plugin-infrastructure.md) | bugfix | Gradle 8.14 upgrade, JaCoCo 0.8.13, nebula.ospackage 12.0.0, JDK24 CI support |

### ML Commons

| Item | Category | Description |
|------|----------|-------------|
| [ML Commons Agent Tools & Memory](features/ml-commons/ml-commons-agent-tools-memory.md) | bugfix | Execute Tool API, AI-oriented memory containers, QueryPlanningTool, agent enhancements, bug fixes |
| [ML Commons Sparse Encoding](features/ml-commons/ml-commons-sparse-encoding.md) | enhancement | TOKEN_ID format support for sparse encoding/tokenize models |
| [ML Commons Model Deployment](features/ml-commons/ml-commons-model-deployment.md) | enhancement | Auto-deploy remote models in partially deployed status |
| [ML Commons Testing & Coverage](features/ml-commons/ml-commons-testing-coverage.md) | bugfix | Integration test stability fix, memory container unit tests, JaCoCo 0.8.13 upgrade |
| [ML Commons Documentation & Tutorials](features/ml-commons/ml-commons-documentation-tutorials.md) | bugfix | Multi-modal search, semantic highlighter, neural sparse, language identification, agentic RAG tutorials |
| [ML Commons Error Handling](features/ml-commons/ml-commons-error-handling.md) | enhancement | Proper 400 errors instead of 500 for agent execute and MCP tool registration |
| [ML Commons Connectors](features/ml-commons/ml-commons-connectors.md) | enhancement | Pre/post-process function validation and improved URI validation for connectors |

### Dashboards Search Relevance

| Item | Category | Description |
|------|----------|-------------|
| [Toast Notification Bugfix](features/dashboards-search-relevance/toast-notification-bugfix.md) | bugfix | Fix error messages not rendering correctly in toast notifications |
| [Repository Maintenance](features/dashboards-search-relevance/repository-maintenance.md) | bugfix | Maintainer updates, issue templates, codecov integration, GitHub Actions dependency bumps |

### Search Relevance

| Item | Category | Description |
|------|----------|-------------|
| [Search Relevance Bugfixes](features/search-relevance/search-relevance-bugfixes.md) | bugfix | 7 bug fixes: error messaging, pipeline errors, UI overflow, Venn diagram, REST API status, input validation, pipeline parameter |

### Query Insights

| Item | Category | Description |
|------|----------|-------------|
| [Release Notes & Documentation](features/query-insights/release-notes-documentation.md) | bugfix | Release notes for v3.2.0 with reader search limit increase and infrastructure updates |

### Query Insights Dashboards

| Item | Category | Description |
|------|----------|-------------|
| [Query Insights Bugfixes](features/query-insights-dashboards/query-insights-bugfixes.md) | bugfix | react-vis migration, search bar fix, table sorting fix, UI improvements |
| [Query Insights Live Queries Enhancement](features/query-insights-dashboards/query-insights-live-queries-enhancement.md) | enhancement | Updated default auto-refresh interval from 5s to 30s |

### SQL

| Item | Category | Description |
|------|----------|-------------|
| [SQL/PPL Engine Enhancements](features/sql/ppl-engine.md) | enhancement | Expanded pushdown (sort, aggregation, partial filter, span, relevance), RelJson security, ~30% performance improvement |
| [SQL/PPL Documentation](features/sql/ppl-documentation.md) | bugfix | Update PPL documentation index and V3 engine limitations |

### Asynchronous Search

| Item | Category | Description |
|------|----------|-------------|
| [Asynchronous Search Bugfix](features/asynchronous-search/asynchronous-search-bugfix.md) | bugfix | Gradle 8.14.3 upgrade, JDK 24 CI support, Maven snapshot endpoint migration |

### Alerting

| Item | Category | Description |
|------|----------|-------------|
| [Alerting Plugin](features/alerting/alerting-plugin.md) | bugfix | MGet bug fix, randomized fan-out distribution, consistent API responses |

### Anomaly Detection

| Item | Category | Description |
|------|----------|-------------|
| [Anomaly Detection Enhancements](features/anomaly-detection/anomaly-detection-enhancements.md) | enhancement | Support for >1 hour detection intervals, centralized resource access control |
| [Anomaly Detection Bugfixes](features/anomaly-detection/anomaly-detection-bugfixes.md) | bugfix | Concurrency fixes for HCAD, forecasting interval calculation, Dashboards UI improvements |

### Cross-Cluster Replication

| Item | Category | Description |
|------|----------|-------------|
| [Cross-Cluster Replication](features/cross-cluster-replication/cross-cluster-replication.md) | bugfix | Add missing method for RemoteClusterRepository class to fix build failure |

### k-NN

| Item | Category | Description |
|------|----------|-------------|
| [k-NN Vector Search](features/k-nn/k-nn-vector-search.md) | feature | GPU indexing for FP16/Byte/Binary, ADC, random rotation, gRPC support, dynamic thread defaults |
| [Lucene-on-Faiss: ADC Support](features/k-nn/lucene-on-faiss.md) | enhancement | ADC support for memory-optimized search with binary quantized indexes |
| [Remote Vector Index Build](features/k-nn/remote-vector-index-build.md) | bugfix | Don't fall back to CPU on terminal failures during remote index build |

### Flow Framework

| Item | Category | Description |
|------|----------|-------------|
| [Flow Framework Bugfixes](features/flow-framework/flow-framework-bugfixes.md) | bugfix | Memory fixes, error handling, 3.1+ API compatibility, race condition fix, default template fixes |

### Security Analytics Dashboards Plugin

| Item | Category | Description |
|------|----------|-------------|
| [Security Analytics Bugfixes](features/security-analytics-dashboards-plugin/security-analytics-bugfixes.md) | bugfix | Remove Vega-based correlated findings chart, update IOC types API |

### Reporting

| Item | Category | Description |
|------|----------|-------------|
| [Reporting Plugin](features/reporting/reporting-plugin.md) | bugfix | System context for index creation, tenant URL parsing fix |

### Dashboards Assistant

| Item | Category | Description |
|------|----------|-------------|
| [Dashboards Core Bugfixes](features/dashboards-assistant/dashboards-core-bugfixes.md) | bugfix | Fix unit test failures due to missing Worker in Jest environment |
| [Dashboards Assistant](features/dashboards-assistant/dashboards-assistant.md) | enhancement | Support natural language visualization in new dashboard ingress (Explore UI) |

### Skills

| Item | Category | Description |
|------|----------|-------------|
| [Skills Plugin Enhancements](features/skills/skills-plugin-enhancements.md) | enhancement | Index schema merging for PPLTool, error message masking, standardized parameter handling |

### Multi-Repository

| Item | Category | Description |
|------|----------|-------------|
| [CVE Fixes & Dependency Updates](features/multi-repo/cve-fixes-dependency-updates.md) | bugfix | CVE-2025-48734 (beanutils) and CVE-2025-7783 (form-data) security fixes |
| [Version Increment (Maintenance)](features/multi-plugin/version-increment-maintenance.md) | bugfix | Version bumps to 3.2.0 across 14 repositories |
| [Build Infrastructure (Gradle/JDK)](features/multi-plugin/build-infrastructure-gradle-jdk.md) | bugfix | Gradle 8.14/8.14.3, JDK 24 CI support, Maven endpoint updates across 17+ repositories |

### Common Utils

| Item | Category | Description |
|------|----------|-------------|
| [Common Utils Bugfixes](features/common-utils/common-utils-bugfixes.md) | bugfix | CVE-2025-48734 fix, PublishFindingsRequest revert, Gradle 8.14/JDK 24 upgrade |

### Security

| Item | Category | Description |
|------|----------|-------------|
| [Resource Sharing](features/security/resource-sharing.md) | feature | Migration API, Resource Access Evaluator for automatic authorization, client accessor pattern fix |
| [Permission Validation](features/security/permission-validation.md) | feature | Query parameter to check API permissions without executing the request |
| [Auxiliary Transport SSL](features/security/auxiliary-transport-ssl.md) | feature | TLS support for auxiliary transports (gRPC, etc.) with per-transport SSL configuration |
| [Security FIPS Compliance](features/security/security-fips-compliance.md) | enhancement | Full FIPS 140-2 compliance with BC-FIPS libraries and OpenSAML shadow JAR isolation |
| [Security Performance Optimization](features/security/security-performance-optimization.md) | enhancement | Precomputed privileges toggle and optimized wildcard matching |
| [Star Tree Security Integration](features/security/star-tree-security-integration.md) | enhancement | Disable star-tree optimization for users with DLS/FLS/Field Masking restrictions |
| [Security Plugin Enhancements](features/security/security-plugin-enhancements.md) | enhancement | Nested JWT claims, stream transport integration, plugin permissions, tenancy access, bug fixes |

### Common (Security)

| Item | Category | Description |
|------|----------|-------------|
| [Tenancy Access Control](features/common/tenancy-access-control.md) | enhancement | Add tenancy access level (READ/WRITE/NONE) to serialized user in thread context |

### Custom Codecs

| Item | Category | Description |
|------|----------|-------------|
| [Composite Index Support](features/custom-codecs/composite-index-support.md) | feature | Support for composite indexes (star-tree) with custom codecs |

### User Behavior Insights

| Item | Category | Description |
|------|----------|-------------|
| [User Behavior Insights Data Generator](features/user-behavior-insights/user-behavior-insights-data-generator.md) | enhancement | Add search_config field for A/B TDI testing simulation |

### Security Dashboards Plugin

| Item | Category | Description |
|------|----------|-------------|
| [Security Dashboards Enhancements](features/security-dashboards-plugin/security-dashboards-enhancements.md) | enhancement | Full index pattern display in role view, added missing index permissions |

### Security

| Item | Category | Description |
|------|----------|-------------|
| [SPIFFE X.509 SVID Support](features/security/spiffe-x.509-svid-support.md) | feature | SPIFFE-based workload identity authentication via SPIFFEPrincipalExtractor |
| [Argon2 Password Hashing](features/security/argon2-password-hashing.md) | feature | Argon2 password hashing algorithm support with full parameter configurability |
| [Security Configuration Management](features/security/security-configuration-management.md) | feature | Experimental versioned security configuration management with rollback/roll-forward foundation |
