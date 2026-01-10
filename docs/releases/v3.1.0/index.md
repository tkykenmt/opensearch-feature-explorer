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

### Reporting

- [Reporting Release Maintenance](features/reporting/reporting-release-maintenance.md) - Version increment to 3.1.0-SNAPSHOT and release notes for v3.1.0

### Security

- [Security Dependency Updates](features/security/security-dependency-updates.md) - 24 dependency updates including Bouncy Castle 1.81, Kafka 4.0.0, and CVE-2024-52798 fix
- [Security Permissions](features/security/security-permissions.md) - Add forecast roles and fix missing cluster:monitor and mapping get permissions

### Query Insights

- [Query Insights Release Maintenance](features/query-insights/query-insights-release-maintenance.md) - Fix flaky integration tests and add multi-node test infrastructure

### Observability

- [Observability Release Maintenance](features/observability/observability-release-maintenance.md) - Version increments, release notes, and bug fixes for trace analytics

### Neural Search

- [Lucene Upgrade](features/neural-search/lucene-upgrade.md) - Update hybrid query implementation for Lucene 10.2.1 API compatibility
- [Neural Search Compatibility](features/neural-search/neural-search-compatibility.md) - Update neural-search for OpenSearch 3.0 beta compatibility

### Learning to Rank

- [Lucene Upgrade](features/learning/lucene-upgrade.md) - Update RankerQuery for Lucene 10.2.1 DisiPriorityQueue API change

### ML Commons

- [ML Commons Maintenance](features/ml-commons/ml-commons-maintenance.md) - Hidden model security, enhanced logging, HTTP client alignment, SearchIndexTool MCP compatibility, CVE fixes
- [MCP (Model Context Protocol)](features/ml-commons/mcp-(model-context-protocol).md) - MCP SDK downgrade to 0.9.0 and unit test coverage
- [PlanExecuteReflect Agent](features/ml-commons/planexecutereflect-agent.md) - Test coverage for PlanExecuteReflect Agent runner and utilities

### Notifications

- [Notifications Maintenance](features/notifications/notifications-maintenance.md) - Migrate from javax.mail to jakarta.mail APIs and version increment to 3.1.0-SNAPSHOT

### Job Scheduler

- [Job Scheduler Maintenance](features/job-scheduler/job-scheduler-maintenance.md) - Remove Guava dependency to reduce jar hell and version increment to 3.1.0
- [Job Scheduler Changelog](features/job-scheduler/job-scheduler-changelog.md) - Add CHANGELOG and changelog_verifier workflow for iterative release notes

### Dashboards Search Relevance

- [Search Relevance Dashboards Fixes](features/dashboards-search-relevance/search-relevance-dashboards-fixes.md) - Fix schema validation in POST Query Sets endpoint

### Flow Framework

- [Flow Framework Dependencies](features/flow-framework/flow-framework-dependencies.md) - Conditional DynamoDB client dependency and data summary with log pattern agent template

### Dashboards Assistant

- [Dashboard Assistant CI Fixes](features/dashboards-assistant/dashboard-assistant-ci-fixes.md) - Fix CI failures due to path alias babel configuration changes

### Multi-Plugin

- [Testing Library Updates](features/multi-plugin/testing-library-updates.md) - Update @testing-library/user-event to v14.4.3 in anomaly-detection and index-management dashboards plugins

### k-NN

- [k-NN Testing Infrastructure](features/k-nn/k-nn-testing-infrastructure.md) - Enable all integration tests with remote index builder and fix MockNode constructor compatibility

### Search Relevance

- [Search Relevance Test Data](features/search-relevance/search-relevance-test-data.md) - Add realistic ESCI-based test dataset with 150 queries and matching judgments

### Remote

- [Security CVE Fixes](features/remote/security-cve-fixes.md) - CVE-2025-27820 fix for Apache HttpClient in opensearch-remote-metadata-sdk
