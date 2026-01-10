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
| [Rescore Named Queries](features/opensearch/rescore-named-queries.md) | feature | Surface named queries from rescore contexts in matched_queries array |
| [Semantic Version Field Type](features/opensearch/semantic-version-field-type.md) | feature | New `version` field type for semantic versioning with proper ordering and range queries |
| [Query Phase Plugin Extension](features/opensearch/query-phase-plugin-extension.md) | feature | Plugin extensibility for injecting custom QueryCollectorContext during QueryPhase |
| [Search Pipeline in Templates](features/opensearch/search-pipeline-in-templates.md) | feature | Support for search pipeline in search and msearch template APIs |
| [Pull-based Ingestion](features/opensearch/pull-based-ingestion.md) | feature | File-based ingestion plugin (ingestion-fs) for local testing |
| [Cat Indices API Enhancement](features/opensearch/cat-indices-api-enhancement.md) | feature | Add last index request timestamp columns to `_cat/indices` API |
| [Remote Store Metadata API](features/opensearch/remote-store-metadata-api.md) | feature | New cluster-level API to fetch segment and translog metadata from remote store |
| [Java Agent AccessController](features/opensearch/java-agent-accesscontroller.md) | feature | OpenSearch replacement for JDK's deprecated AccessController for privileged operations |
