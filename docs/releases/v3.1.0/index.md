# OpenSearch v3.1.0 Release

## Features

### OpenSearch

- [Approximation Framework](features/opensearch/approximation-framework.md) - BKD traversal optimization for skewed datasets with DFS strategy
- [Derived Source](features/opensearch/derived-source.md) - Storage optimization by deriving _source from doc_values and stored fields
- [Async Shard Batch Fetch](features/opensearch/async-shard-batch-fetch.md) - Enabled by default with 20s timeout for improved cluster manager resilience
- [Crypto/KMS Plugin](features/opensearch/crypto-kms-plugin.md) - Decoupled plugin initialization and AWS SDK v2.x dependency upgrade
- [Dependency Bumps](features/opensearch/dependency-bumps.md) - 21 dependency updates including CVE-2025-27820 fix, Netty, Gson, Azure SDK updates
- [DocRequest Refactoring](features/opensearch/docrequest-refactoring.md) - Generic interface for single-document operations
- [File Cache](features/opensearch/file-cache.md) - File pinning support and granular statistics for Writable Warm indices
- [FIPS Support](features/opensearch/fips-support.md) - Update FipsMode check for improved BC-FIPS compatibility
- [Lucene Upgrade](features/opensearch/lucene-upgrade.md) - Upgrade Apache Lucene from 10.1.0 to 10.2.1
- [Network Configuration](features/opensearch/network-configuration.md) - Fix systemd seccomp filter for network.host: 0.0.0.0
- [Percentiles Aggregation](features/opensearch/percentiles-aggregation.md) - Switch to MergingDigest for up to 30x performance improvement
- [Plugin Installation](features/opensearch/plugin-installation.md) - Fix native plugin installation error caused by PGP public key change
- [Plugin Testing Framework](features/opensearch/plugin-testing-framework.md) - Enable testing for ExtensiblePlugins using classpath plugins
- [Pull-based Ingestion](features/opensearch/pull-based-ingestion.md) - Lag metrics, error metrics, configurable queue, retries, create mode, write blocks, consumer reset
- [Query Bug Fixes](features/opensearch/query-bug-fixes.md) - Fixes for exists query, error handling, field validation, and IP field terms query
- [Query Optimization](features/opensearch/query-optimization.md) - Automatic must_not range rewrite and sort-query performance improvements
- [Remote Store](features/opensearch/remote-store.md) - Close index rejection during migration and cluster state diff download fix
- [S3 Repository Enhancements](features/opensearch/s3-repository-enhancements.md) - SSE-KMS encryption support and S3 bucket owner verification
- [Snapshot/Repository Fixes](features/opensearch/repository-fixes.md) - Fix infinite loop during concurrent snapshot/repository update and NPE for legacy snapshots
- [Star-Tree Index Enhancements](features/opensearch/star-tree-index.md) - Production-ready status, date range queries, nested aggregations, index-level control
- [Cluster Manager Metrics](features/opensearch/cluster-manager-metrics.md) - Task execution time, node-left counter, and FS health failure metrics
- [gRPC Transport](features/opensearch/grpc-transport.md) - Performance optimization with pass-by-reference pattern and package reorganization
- [Unified Highlighter](features/opensearch/unified-highlighter.md) - Add matched_fields support for blending matches from multiple fields
- [System Ingest Pipeline](features/opensearch/system-ingest-pipeline.md) - Automatic pipeline generation for plugin developers with bulk update support
- [Query Coordinator Context](features/opensearch/query-coordinator-context.md) - Search request access and validate API integration for index-aware query rewriting
- [Composite Directory Factory](features/opensearch/composite-directory-factory.md) - Pluggable factory for custom composite directory implementations in warm indices
- [Security Manager Replacement](features/opensearch/security-manager-replacement.md) - Enhanced Java Agent to intercept newByteChannel from FileSystemProvider
- [Warm Storage Tiering](features/opensearch/warm-storage-tiering.md) - WarmDiskThresholdDecider and AutoForceMergeManager for hot-to-warm migration
- [Workload Management](features/opensearch/workload-management.md) - Paginated `/_list/wlm_stats` API with token-based pagination and sorting
- [Rule-based Auto-tagging](features/opensearch/rule-based-auto-tagging.md) - Automatic workload group assignment based on index patterns and rules
- [Parallel Shard Refresh](features/opensearch/parallel-shard-refresh.md) - Shard-level refresh scheduling for improved data freshness in remote store indexes
- [Platform Support](features/opensearch/platform-support.md) - Add support for Linux riscv64 platform

### Skills

- [ML Skills](features/skills/ml-skills.md) - Fix httpclient5 dependency version conflict and apply Spotless formatting
- [Skills PPL Tool Fixes](features/skills/skills-ppl-tool-fixes.md) - Fix fields bug to expose multi-field mappings for aggregation queries

### Reporting

- [Reporting Release Maintenance](features/reporting/reporting-release-maintenance.md) - Version increment to 3.1.0-SNAPSHOT and release notes for v3.1.0

### Security

- [Security Backend Bug Fixes](features/security/security-backend-bug-fixes.md) - Stale cache post snapshot restore, compliance audit log diff, DLS/FLS filter reader, auth header logging, password reset UI, forecasting permissions
- [Security Cache Management](features/security/security-cache-management.md) - Selective user cache invalidation endpoint and dynamic cache TTL configuration
- [Security Debugging](features/security/security-debugging.md) - Enhanced error messages for "Security not initialized" with cluster manager status
- [Security Dependency Updates](features/security/security-dependency-updates.md) - 24 dependency updates including Bouncy Castle 1.81, Kafka 4.0.0, and CVE-2024-52798 fix
- [Security Performance Improvements](features/security/security-performance-improvements.md) - Immutable User object with serialization caching for reduced inter-node communication overhead
- [Security Role Mapping](features/security/security-role-mapping.md) - Fix mapped roles not included in ThreadContext userInfo after immutable User object change
- [Security Permissions](features/security/security-permissions.md) - Add forecast roles and fix missing cluster:monitor and mapping get permissions
- [Security Testing Framework](features/security/security-testing-framework.md) - Use extendedPlugins in integrationTest framework for sample resource plugin testing
- [Security JWT Enhancements](features/security/security-jwt-enhancements.md) - Support for extracting backend roles from nested JWT claims
- [Security CI/CD](features/security/security-ci-cd.md) - Changelog verification workflow and Dependabot PR automation

### Query Insights

- [Query Insights Enhancements](features/query-insights/query-insights-enhancements.md) - Metric labels for historical data, consolidated grouping settings, index exclusion, async reader, Live Queries Dashboard, WLM Dashboard
- [Query Insights Release Maintenance](features/query-insights/query-insights-release-maintenance.md) - Fix flaky integration tests and add multi-node test infrastructure
- [Query Insights Bug Fixes](features/query-insights/query-insights-bug-fixes.md) - Fix node-level request serialization, live query status response, and CI test stability

### Observability

- [Observability Release Maintenance](features/observability/observability-release-maintenance.md) - Version increments, release notes, and bug fixes for trace analytics
- [Observability Bug Fixes](features/observability/observability-bug-fixes.md) - Jaeger end time processing fix and NFW integration Vega warning fix
- [Observability Trace Analytics](features/dashboards-observability/observability-trace-analytics.md) - Merge custom source and data prepper mode, span flyout nested field support

### Neural Search

- [Lucene Upgrade](features/neural-search/lucene-upgrade.md) - Update hybrid query implementation for Lucene 10.2.1 API compatibility
- [Neural Search Bug Fixes](features/neural-search/neural-search-bug-fixes.md) - 7 bug fixes for hybrid query validation, semantic field handling, radial search serialization, stats API, and stability
- [Neural Search Compatibility](features/neural-search/neural-search-compatibility.md) - Update neural-search for OpenSearch 3.0 beta compatibility
- [Neural Search Stats](features/neural-search/neural-search-stats.md) - Comprehensive stats API for monitoring ingest processors, search processors, hybrid queries, and semantic highlighting

### Learning to Rank

- [Lucene Upgrade](features/learning/lucene-upgrade.md) - Update RankerQuery for Lucene 10.2.1 DisiPriorityQueue API change

### ML Commons

- [Agent Framework](features/ml-commons/ml-commons-agent-framework.md) - Update Agent API, MCP tools persistence, function calling for LLM interfaces, custom SSE endpoint, metrics framework integration, multiple bug fixes
- [Connector/Model Validation Bug Fixes](features/ml-commons/connector-model-validation.md) - Input validation for names/descriptions, schema string type preservation, connector retry policy NPE fix, MCP tool memory fix, Bedrock DeepSeek format fix
- [ML Commons Maintenance](features/ml-commons/ml-commons-maintenance.md) - Hidden model security, enhanced logging, HTTP client alignment, SearchIndexTool MCP compatibility, CVE fixes
- [MCP (Model Context Protocol)](features/ml-commons/mcp-(model-context-protocol).md) - MCP SDK downgrade to 0.9.0 and unit test coverage
- [PlanExecuteReflect Agent](features/ml-commons/planexecutereflect-agent.md) - Test coverage for PlanExecuteReflect Agent runner and utilities
- [ML Commons Release Notes and Documentation](features/ml-commons/ml-commons-release-notes-and-documentation.md) - Release note formatting, Maven snapshot publishing migration, README branding, Claude v4 blueprint

### Notifications

- [Notifications Maintenance](features/notifications/notifications-maintenance.md) - Migrate from javax.mail to jakarta.mail APIs and version increment to 3.1.0-SNAPSHOT

### Job Scheduler

- [Job Scheduler Maintenance](features/job-scheduler/job-scheduler-maintenance.md) - Remove Guava dependency to reduce jar hell and version increment to 3.1.0
- [Job Scheduler Changelog](features/job-scheduler/job-scheduler-changelog.md) - Add CHANGELOG and changelog_verifier workflow for iterative release notes

### Dashboards Search Relevance

- [Search Relevance Dashboards Fixes](features/dashboards-search-relevance/search-relevance-dashboards-fixes.md) - Fix schema validation in POST Query Sets endpoint

### Flow Framework

- [Flow Framework Dependencies](features/flow-framework/flow-framework-dependencies.md) - Conditional DynamoDB client dependency and data summary with log pattern agent template
- [Flow Framework Improvements](features/flow-framework/flow-framework-improvements.md) - Bug fixes for RegisterAgentStep LLM field processing, exception type in error messages, and LLM spec parameter passing

### Index Management

- [Notifications Improvements](features/index-management/notifications-improvements.md) - Fix false positive notifications in Snapshot Management for version conflict exceptions

### Dashboards Assistant

- [Dashboard Assistant CI Fixes](features/dashboards-assistant/dashboard-assistant-ci-fixes.md) - Fix CI failures due to path alias babel configuration changes
- [Security Dashboards UI Fixes](features/dashboards-assistant/security-dashboards-ui-fixes.md) - Bug fixes for embeddable dropdown, error logging, insights request timing, and conversation loading state

### Multi-Plugin

- [Testing Library Updates](features/multi-plugin/testing-library-updates.md) - Update @testing-library/user-event to v14.4.3 in anomaly-detection and index-management dashboards plugins
- [Version Bumps and Release Maintenance](features/multi-plugin/version-bumps-and-release-maintenance.md) - Version increments across 11 repositories for v3.1.0 release cycle

### k-NN

- [k-NN Bug Fixes](features/k-nn/k-nn-bug-fixes.md) - 9 bug fixes for quantization cache, rescoring, thread safety, nested queries, memory cache race conditions, backward compatibility
- [k-NN Testing Infrastructure](features/k-nn/k-nn-testing-infrastructure.md) - Enable all integration tests with remote index builder and fix MockNode constructor compatibility
- [Remote Vector Index Build](features/k-nn/remote-vector-index-build.md) - GA preparation with tuned buffer sizes, segment size upper bound, renamed settings, metrics fixes

### Search Relevance

- [Search Relevance Test Data](features/search-relevance/search-relevance-test-data.md) - Add realistic ESCI-based test dataset with 150 queries and matching judgments
- [Search Relevance Bug Fixes](features/search-relevance/search-relevance-bug-fixes.md) - Data model restructuring, LLM judgment improvements, search request builder fix, hybrid optimizer fix, input validation

### SQL

- [SQL/PPL Bug Fixes](features/sql/sql-ppl-bug-fixes.md) - 17 bug fixes including long IN-list crash, function fixes (ATAN, CONV, UNIX_TIMESTAMP), field handling, and Calcite engine stability

### Remote

- [Security CVE Fixes](features/remote/security-cve-fixes.md) - CVE-2025-27820 fix for Apache HttpClient in opensearch-remote-metadata-sdk

### Geospatial

- [Geospatial Ip2Geo Fixes](features/geospatial/geospatial-ip2geo-fixes.md) - Cache synchronization fixes for IP2Geo processor with metadata reset and retry logic

### Custom Codecs

- [Build/Test Infrastructure](features/custom-codecs/test-infrastructure.md) - Fix BWC test dependency version and add java-agent plugin
