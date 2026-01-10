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
| [OpenSearch Learning to Rank](features/opensearch-learning-to-rank-base/opensearch-learning-to-rank.md) | bugfix | Gradle 8.14 upgrade, JDK24 support, flaky test fix for similarity score comparisons |

### Notifications

| Item | Category | Description |
|------|----------|-------------|
| [Notifications Plugin Infrastructure](features/notifications/notifications-plugin-infrastructure.md) | bugfix | Gradle 8.14 upgrade, JaCoCo 0.8.13, nebula.ospackage 12.0.0, JDK24 CI support |

### ML Commons

| Item | Category | Description |
|------|----------|-------------|
| [ML Commons Testing & Coverage](features/ml-commons/ml-commons-testing-coverage.md) | bugfix | Integration test stability fix, memory container unit tests, JaCoCo 0.8.13 upgrade |
| [ML Commons Documentation & Tutorials](features/ml-commons/ml-commons-documentation-tutorials.md) | bugfix | Multi-modal search, semantic highlighter, neural sparse, language identification, agentic RAG tutorials |

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

### SQL

| Item | Category | Description |
|------|----------|-------------|
| [SQL/PPL Documentation](features/sql/ppl-documentation.md) | bugfix | Update PPL documentation index and V3 engine limitations |

### Asynchronous Search

| Item | Category | Description |
|------|----------|-------------|
| [Asynchronous Search Bugfix](features/asynchronous-search/asynchronous-search-bugfix.md) | bugfix | Gradle 8.14.3 upgrade, JDK 24 CI support, Maven snapshot endpoint migration |

### k-NN

| Item | Category | Description |
|------|----------|-------------|
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

### Multi-Repository

| Item | Category | Description |
|------|----------|-------------|
| [CVE Fixes & Dependency Updates](features/multi-repo/cve-fixes-dependency-updates.md) | bugfix | CVE-2025-48734 (beanutils) and CVE-2025-7783 (form-data) security fixes |
| [Version Increment (Maintenance)](features/multi-plugin/version-increment-maintenance.md) | bugfix | Version bumps to 3.2.0 across 14 repositories |
| [Build Infrastructure (Gradle/JDK)](features/multi-plugin/build-infrastructure-gradle-jdk.md) | bugfix | Gradle 8.14/8.14.3, JDK 24 CI support, Maven endpoint updates across 17+ repositories |
