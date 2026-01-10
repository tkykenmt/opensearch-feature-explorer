# OpenSearch v2.18.0 Release

## Overview

This page contains feature reports for OpenSearch v2.18.0.

## Features by Repository

### OpenSearch

- [List APIs (Paginated)](features/opensearch/list-apis-paginated.md) - New `_list/indices` and `_list/shards` APIs with pagination support, plus cat API response limits
- [Cluster Stats API](features/opensearch/cluster-stats-api.md) - URI path filtering support for selective metric retrieval
- [OpenSearch Core Dependencies](features/opensearch/opensearch-core-dependencies.md) - 26 dependency updates including Lucene 9.12.0, Netty 4.1.114, gRPC 1.68.0, Protobuf 3.25.5
- [Cluster State Management](features/opensearch/cluster-state-management.md) - Fix voting configuration mismatch by updating lastSeenClusterState in commit phase
- [Remote Cluster State](features/opensearch/remote-cluster-state.md) - Fallback to remote cluster state on term-version check mismatch for improved performance in large clusters
- [Dynamic Settings](features/opensearch/dynamic-settings.md) - Make multiple cluster settings dynamic for tuning on larger clusters
- [Wildcard Query Fixes](features/opensearch/wildcard-query-fixes.md) - Fix escaped wildcard character handling and case-insensitive query on wildcard field
- [Flat Object Field](features/opensearch/flat-object-field.md) - Fix infinite loop when flat_object field contains invalid token types
- [Flat Object Query Optimization](features/opensearch/flat-object-query-optimization.md) - Use IndexOrDocValuesQuery to optimize query performance, enable wildcard queries
- [Index Settings](features/opensearch/index-settings.md) - Fix default value handling when setting index.number_of_replicas and index.number_of_routing_shards to null
- [Multi-Search API](features/opensearch/multi-search-api.md) - Fix multi-search with template doesn't return status code
- [Node Join/Leave](features/opensearch/node-join-leave.md) - Fix race condition in node-join and node-left loop
- [Search Backpressure](features/opensearch/search-backpressure.md) - Add validation for cancellation settings to prevent cluster crashes
- [Search Pipeline](features/opensearch/search-pipeline.md) - Add support for msearch API to pass search pipeline name
- [Star Tree Index](features/opensearch/star-tree-index.md) - Initial experimental release with metric aggregations (sum, min, max, avg, value_count)
- [Tiered Caching](features/opensearch/tiered-caching.md) - Segmented cache architecture for improved concurrency and performance
- [Streaming Indexing](features/opensearch/streaming-indexing.md) - Bug fixes for streaming bulk request hangs and newline termination errors
- [Replication](features/opensearch/replication.md) - Fix array hashCode calculation in ResyncReplicationRequest
- [Task Management](features/opensearch/task-management.md) - Fix missing fields in task index mapping for proper task result storage
- [Test Fixes](features/opensearch/test-fixes.md) - Fix flaky test in ApproximatePointRangeQueryTests by adjusting totalHits assertion logic
- [Nested Aggregations](features/opensearch/nested-aggregations.md) - Fix infinite loop in nested aggregations with deep-level nested objects
- [Phone Analyzer](features/opensearch/phone-analyzer.md) - New `phone` and `phone-search` analyzers for phone number indexing and search
- [Code Cleanup](features/opensearch/code-cleanup.md) - Query approximation simplification, Stream API optimization, typo fix
- [Search Request Stats](features/opensearch/search-request-stats.md) - Enable coordinator search.request_stats_enabled by default
- [Secure Transport Settings](features/opensearch/secure-transport-settings.md) - Add dynamic SecureTransportParameters to fix SSL dual mode regression
- [Identity Feature Flag Removal](features/opensearch/identity-feature-flag-removal.md) - Remove experimental identity feature flag, move authentication to plugins
- [Docker Compose v2 Support](features/opensearch/docker-compose-v2-support.md) - Add support for Docker Compose v2 in TestFixturesPlugin for modern Docker installations
- [Snapshot Restore Enhancements](features/opensearch/snapshot-restore-enhancements.md) - Alias renaming during restore and clone operation optimization for doc-rep clusters
- [Remote Store Metrics](features/opensearch/remote-store-metrics.md) - New REMOTE_STORE metric in Node Stats API for monitoring pinned timestamp fetch operations
- [S3 Repository](features/opensearch/s3-repository.md) - Standard retry mode for S3 clients and SLF4J warning fix
- [S3 Async Deletion](features/opensearch/s3-async-deletion.md) - Async deletion support for S3 repository using S3 async client
- [Dynamic Threadpool Resize](features/opensearch/dynamic-threadpool-resize.md) - Runtime thread pool size adjustment via cluster settings API
- [Async Shard Fetch Metrics](features/opensearch/async-shard-fetch-metrics.md) - OTel counter metrics for async shard fetch success and failure tracking
- [Search API Enhancements](features/opensearch/search-api-enhancements.md) - WithFieldName interface for aggregation/sort builders and successfulSearchShardIndices in SearchRequestContext
- [Offline Nodes](features/opensearch/offline-nodes.md) - New offline-tasks library with core abstractions for running background tasks on dedicated offline nodes
- [Workload Management](features/opensearch/workload-management.md) - Query sandboxing with tenant-level admission control, resource limits (CPU/memory), QueryGroup Stats API, and persistence

### OpenSearch Dashboards

- [Dev Tools Modal](features/opensearch-dashboards/dev-tools.md) - Dev Tools console rendered as a modal overlay for improved workflow
- [Navigation Updates](features/opensearch-dashboards/navigation-updates.md) - Flattened navigation, persistent state, small screen support, border style updates
- [Content Management](features/opensearch-dashboards/content-management.md) - Add Page API to allow remove section
- [Discover](features/opensearch-dashboards/discover.md) - Data summary panel, updated appearance, cache management, and bug fixes
- [CI/CD & Build Improvements](features/opensearch-dashboards/cicd-build-dashboards.md) - Switch OSD Optimizer to content-based hashing for CI compatibility
- [Input Control Visualization](features/opensearch-dashboards/input-control-visualization.md) - Fix disabled ValidatedDualRange component sizing
- [Data Source Permissions](features/opensearch-dashboards/data-source-permissions.md) - Fix missing functions in data source permission saved object wrapper
- [Dynamic Config](features/opensearch-dashboards/dynamic-config.md) - Bugfixes for config saved objects, global config discovery, and index/alias validation
- [i18n & Localization](features/opensearch-dashboards/i18n-localization.md) - i18n validation workflows, precommit hook, translation fixes, language selection fix
- [Data Connections](features/opensearch-dashboards/data-connections.md) - Dataset picker support for data connections with multi-select table, pagination, and search
- [Data Connections Bugfixes](features/opensearch-dashboards/data-connections-bugfixes.md) - MDS endpoint unification, tabs navigation, type display, auto-complete MDS support
- [Dependency Updates](features/opensearch-dashboards/dependency-updates-dashboards.md) - JSON11 upgrade for UTF-8 safety, chokidar bump
- [Discover Bugfixes (2)](features/opensearch-dashboards/discover-bugfixes-2.md) - S3 fields support, deleted index pattern handling, time field display, saved query loading
- [Maintainers](features/opensearch-dashboards/maintainers.md) - Add Hailong-am as maintainer
- [OUI Updates](features/opensearch-dashboards/oui-updates.md) - Updates to OpenSearch UI component library (1.13 → 1.15)
- [Query Enhancements (2)](features/opensearch-dashboards/query-enhancements-2.md) - Async polling, error handling, language compatibility, saved query fixes
- [Query Enhancements Bugfixes](features/opensearch-dashboards/query-enhancements-bugfixes.md) - Search strategy extensibility, recent query fix, module exports, keyboard shortcuts
- [Sample Data](features/opensearch-dashboards/sample-data.md) - Updated UI for new UX, OTEL sample data support for traces, metrics, and logs
- [Sample Data Bugfixes](features/opensearch-dashboards/sample-data-bugfixes.md) - Update OTEL sample data description with compatible OS version
- [Saved Query UX](features/opensearch-dashboards/saved-query-ux.md) - New flyout-based UI for saved queries, sample queries on no results page
- [TSVB Visualization](features/opensearch-dashboards/tsvb-visualization-bugfixes.md) - Hidden axis option, per-axis scale setting, compressed input fields
- [UI/UX Bugfixes](features/opensearch-dashboards/ui-ux-bugfixes.md) - Sidebar tooltips, initial page fixes, overlay positioning, Chrome 129 workaround, OUI breakpoints, HeaderControl rendering
- [UI/UX Bugfixes (2)](features/opensearch-dashboards/ui-ux-bugfixes-2.md) - Responsive design fixes for home page, page header, recent menu, and getting started cards
- [UI/UX Improvements](features/opensearch-dashboards/ui-ux-improvements.md) - Page title semantic improvements (h1 + xs size) for accessibility
- [Workspace](features/opensearch-dashboards/workspace.md) - Workspace-level UI settings, collaborator management, data connection integration, global search bar, ACL auditor
- [Workspace Bugfixes](features/opensearch-dashboards/workspace-bugfixes.md) - 13 bug fixes for workspace UI/UX, page crashes, permissions, and navigation
- [Dashboards Maintenance](features/opensearch-dashboards/dashboards-maintenance.md) - Version bump post 2.17, enhanced search API cleanup
- [Query Editor](features/opensearch-dashboards/query-editor.md) - Footer bar for single-line editor, extension ordering fix, PPL autocomplete improvements
- [Async Query](features/opensearch-dashboards/async-query.md) - Frontend polling for async search, async PPL support for S3 datasets
- [Dashboards Improvements](features/opensearch-dashboards/dashboards-improvements.md) - Loading indicator with time counter for query results
- [MDS Integration Support](features/opensearch-dashboards/mds-integration-support.md) - Multi Data Source support for Integration feature
- [Experimental Features](features/opensearch-dashboards/experimental-features.md) - User personal settings with scoped uiSettings and User Settings page
- [Security CVE Fixes](features/opensearch-dashboards/security-cve-fixes.md) - Security updates for dns-sync, axios, path-to-regexp, dompurify, elliptic, micromatch

### Multi-Plugin

- [Dependency Updates](features/multi-plugin/dependency-updates.md) - 19 dependency updates including CVE-2024-7254 fix, Gradle 8.10.2, upload-artifact v4
- [Search Autocomplete](features/multi-plugin/search-autocomplete.md) - Fix search_as_you_type multi-fields support and enhanced Dashboards autocomplete UX
- [Release Notes](features/multi-plugin/release-notes.md) - v2.18.0 release notes added across alerting, common-utils, notifications, query-insights, and security repositories

### Flow Framework

- [Flow Framework Workflow State](features/flow-framework/flow-framework-workflow-state.md) - Remove Painless scripts for workflow state updates, implement optimistic locking
- [Query Assist Data Summary Agent](features/flow-framework/query-assist.md) - Add sample template for Query Assist Data Summary Agent using Claude on Bedrock

### Alerting

- [Alerting Doc-Level Monitor](features/alerting/alerting-doc-level-monitor.md) - Doc-level monitor improvements including comments system indices, remote monitor logging, separate query indices for external monitors, and query index lifecycle optimization

### SQL

- [SQL Plugin Maintenance](features/sql/sql-plugin-maintenance.md) - Security fix for CVE-2024-47554 (commons-io upgrade to 2.14.0) and test fixes for 2.18 branch

### k-NN

- [k-NN Maintenance](features/k-nn/k-nn-maintenance.md) - Lucene 9.12 codec compatibility, force merge performance optimization, benchmark folder removal, code refactoring

### ML Commons

- [ML Commons Connectors & Blueprints](features/ml-commons/ml-commons-connectors-blueprints.md) - Bedrock Converse blueprint, cross-account model invocation tutorial, role temporary credential support, Titan Embedding V2 blueprint

### Query Insights

- [Query Insights Settings](features/query-insights/query-insights-settings.md) - Change default values for grouping attribute settings (field_name, field_type) from false to true
- [Query CI/CD](features/query-insights/query-ci-cd.md) - Upgrade deprecated actions/upload-artifact from v1/v2 to v3

### Security Analytics

- [Security Analytics System Indices](features/security-analytics/security-analytics-system-indices.md) - Standardized system index settings (1 primary shard, 1-20 replicas), dedicated query indices option, correlation alert refresh policy fix

### Security

- [Security Plugin Maintenance](features/security/security-plugin-maintenance.md) - Cache endpoint deprecation warning, securityadmin script undeprecation, ASN1 refactoring for FIPS, CVE-2024-47554 fix, BWC test fixes

### Skills

- [Skills Plugin Dependencies](features/skills/skills-plugin-dependencies.md) - Dependency updates (Mockito 5.14.2, JUnit5 5.11.2, ByteBuddy 1.15.4, Gradle 8.10.2) and test fix for AnomalyDetector API changes

### CI/CD

- [CI/CD & Build Improvements](features/ci/cd-build-improvements.md) - JDK-21 baseline updates, CI workflow fixes, test security improvements, backport process enhancements across index-management, ml-commons, notifications, and observability

### Maintenance

- [Version Bumps & Maintenance](features/maintenance/version-bumps-maintenance.md) - Routine version increment PRs across 12 plugin repositories for v2.18.0 release preparation
