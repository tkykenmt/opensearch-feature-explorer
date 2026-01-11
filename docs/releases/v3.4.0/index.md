# OpenSearch v3.4.0 Release

## Features

### OpenSearch

- [Aggregation Optimizations](features/opensearch/aggregation-optimizations.md) - Hybrid cardinality collector, filter rewrite + skip list, MergingDigest for percentiles, matrix_stats primitive arrays
- [Filter Rewrite Optimization](features/opensearch/filter-rewrite-optimization.md) - Bulk collection APIs for filter rewrite sub-aggregation with up to 20% performance improvement
- [GRPC Transport](features/opensearch/grpc-transport.md) - Pluggable interceptors, thread context preservation, binary document formats, expanded query support
- [ApproximatePointRangeQuery Pack Method Optimization](features/opensearch/approximate-point-range-query.md) - Use Lucene's native `pack` method for `half_float` and `unsigned_long` types
- [Build Tool Upgrades](features/opensearch/build-tool-upgrades.md) - Gradle 9.1 and bundled JDK 25 updates
- [Concurrent Segment Search](features/opensearch/concurrent-segment-search.md) - Performance optimization by omitting MaxScoreCollector when sorting by score
- [Context Aware Segments](features/opensearch/context-aware-segments.md) - Collocate related documents into same segments based on grouping criteria for improved query performance
- [Index Settings](features/opensearch/index-settings.md) - Custom creation_date setting and tier-aware shard limit validation for local and remote indices
- [Segment Grouping](features/opensearch/segment-grouping.md) - Mapper for defining context-aware segment grouping criteria with Painless script support
- [Dependency Updates (OpenSearch Core)](features/opensearch/dependency-updates-opensearch-core.md) - 32 dependency updates including Netty 4.2.4 for HTTP/3 readiness
- [Engine Refactoring](features/opensearch/engine-refactoring.md) - Move prepareIndex/prepareDelete to Engine class and make NoOpResult constructors public
- [FIPS Compliance](features/opensearch/fips-compliance.md) - Test suite FIPS 140-3 compliance support with BC-FIPS provider
- [JDK 25 Support](features/opensearch/jdk-25-support.md) - Painless scripting compatibility fix for JDK 25 ClassValue behavioral change
- [Lucene Integration](features/opensearch/lucene-integration.md) - Remove MultiCollectorWrapper and use Lucene's native MultiCollector API
- [Lucene Upgrade](features/opensearch/lucene-upgrade.md) - Bump Apache Lucene from 10.3.1 to 10.3.2 with MaxScoreBulkScorer bug fix
- [Maven Snapshots Publishing](features/opensearch/maven-snapshots-publishing.md) - Migrate snapshot publishing from Sonatype to S3-backed repository at ci.opensearch.org
- [Merged Segment Warmer](features/opensearch/merged-segment-warmer.md) - GA graduation with configurable resiliency features and cluster-level merge scheduler settings
- [Node Stats Bugfixes](features/opensearch/node-stats-bugfixes.md) - Fix negative CPU usage values in node stats on certain Linux distributions
- [Normalizer Enhancements](features/opensearch/normalizer-enhancements.md) - Allow truncate token filter in normalizers for keyword field truncation
- [S3 Repository](features/opensearch/s3-repository.md) - Add LEGACY_MD5_CHECKSUM_CALCULATION to opensearch.yml settings for S3-compatible storage
- [Scroll Query Optimization](features/opensearch/scroll-query-optimization.md) - Cache StoredFieldsReader per segment for improved scroll query performance
- [Search API Tracker](features/opensearch/search-api-tracker.md) - Track search response status codes at coordinator node for observability
- [Security Kerberos Integration](features/opensearch/security-kerberos-integration.md) - Update Hadoop to 3.4.2 and enable Kerberos integration tests for JDK-24+
- [Settings Bugfixes](features/opensearch/settings-bugfixes.md) - Fix duplicate registration of dynamic settings and patch version build issues
- [Stats Builder Pattern Deprecations](features/opensearch/stats-builder-pattern-deprecations.md) - Deprecated constructors in 30+ Stats classes in favor of Builder pattern
- [Terms Query Optimization](features/opensearch/terms-query-optimization.md) - Pack terms once for keyword fields with index and docValues enabled
- [Thread Pool](features/opensearch/thread-pool.md) - ForkJoinPool thread pool type support for work-stealing parallelism
- [Transport Actions API](features/opensearch/transport-actions-api.md) - Internal API for retrieving metadata about requested indices from transport actions
- [XContent Filtering](features/opensearch/xcontent-filtering.md) - Case-insensitive filtering support for XContentMapValues.filter
- [Plugin Dependencies](features/opensearch/plugin-dependencies.md) - Range semver support for dependencies in plugin-descriptor.properties
- [Query String Monitoring](features/opensearch/query-string-monitoring.md) - Monitoring mode for query string length validation with warning logs instead of rejection
- [Repository Encryption](features/opensearch/repository-encryption.md) - Server-side encryption support for S3 remote store repositories
- [ActionPlugin Enhancements](features/opensearch/actionplugin-enhancements.md) - Pass REST header registry to getRestHandlerWrapper for efficient header access
- [WildcardFieldMapper](features/opensearch/wildcardfieldmapper.md) - Change doc_values default to true for nested query support

### Security

- [Resource Sharing](features/security/resource-sharing.md) - Multi-type index support, ResourceProvider interface, Builder pattern, REST API improvements
- [Security AccessController Migration](features/security/security-accesscontroller-migration.md) - Migrate from deprecated java.security.AccessController to org.opensearch.secure_sm.AccessController
- [Security Bugfixes](features/security/security-bugfixes.md) - Multi-tenancy `.kibana` index fix, WildcardMatcher empty string handling, DLS/FLS internal request fix, PrivilegesEvaluator modularization
- [Security Features](features/security/security-features.md) - Webhook Basic Auth, REST header propagation, system indices deprecation, static/custom config overlap, search relevance permissions
- [GitHub Actions Updates](features/security/github-actions-updates.md) - Update GitHub Actions dependencies to support Node.js 24 runtime

### Security Dashboards Plugin

- [Security Dashboards Bugfixes](features/security-dashboards-plugin/security-dashboards-bugfixes.md) - Filter blank backend roles before creating internal user

### Security Analytics Dashboards Plugin

- [Security Analytics Bugfixes](features/security-analytics-dashboards-plugin/security-analytics-bugfixes.md) - Fix correlation table rendering bug in correlations overview page

### OpenSearch Dashboards

- [Dashboards Dev Tools](features/opensearch-dashboards/dashboards-dev-tools.md) - PATCH method support for Dev Tools console
- [Dashboards Explore](features/opensearch-dashboards/dashboards-explore.md) - Histogram breakdowns, Field Statistics tab, trace flyout, correlations, cancel query, and by-value embeddables
- [Dashboards Global Search](features/opensearch-dashboards/dashboards-global-search.md) - Assets search and enhanced command system for global search
- [Dashboards CSP](features/opensearch-dashboards/dashboards-csp.md) - Dynamic configuration support for CSP report-only mode
- [Dashboards Data Connections](features/opensearch-dashboards/dashboards-data-connections.md) - Prometheus saved object support for data connections
- [Dashboards Query Action Service](features/opensearch-dashboards/dashboards-query-action-service.md) - Flyout registration support for query panel actions
- [Dashboards Visualizations](features/opensearch-dashboards/dashboards-visualizations.md) - Bar gauge, customizable legends, numerical color fields, and table column ordering
- [Dashboards Workspace](features/opensearch-dashboards/dashboards-workspace.md) - Remove restriction requiring data source for workspace creation
- [Dashboards Traces](features/opensearch-dashboards/dashboards-traces.md) - Span status filters and trace details UX improvements
- [Dashboards Dataset Management](features/opensearch-dashboards/dashboards-dataset-management.md) - Schema mapping, wildcard prefix, and enhanced dataset table

## Bug Fixes

### Alerting

- [Alerting Build](features/alerting/alerting-build.md) - Fix build script to only publish alerting plugin zip, excluding sample remote monitor plugin

### OpenSearch

- [Java Agent](features/opensearch/java-agent.md) - Fix JRT protocol URL filtering to allow MCP server connections
- [Bulk Request Bugfixes](features/opensearch/bulk-request-bugfixes.md) - Fix indices property initialization during BulkRequest deserialization
- [Bulk API Enhancements](features/opensearch/bulk-api-enhancements.md) - Implement error_trace parameter support for bulk requests
- [Cluster State & Allocation Bugfixes](features/opensearch/cluster-state-allocation-bugfixes.md) - Fix concurrent modification in allocation filters and version compatibility in remote state
- [Data Stream & Index Template Bugfixes](features/opensearch/data-stream-index-template-bugfixes.md) - Fix deletion of unused index templates matching data streams with lower priority
- [GRPC Transport Bugfixes](features/opensearch/grpc-transport-bugfixes.md) - Fix ClassCastException for large requests, Bulk API fixes, and node bootstrap with streaming transport
- [Pull-based Ingestion Bugfixes](features/opensearch/pull-based-ingestion-bugfixes.md) - Fix out-of-bounds offset handling and remove persisted pointers for at-least-once guarantees
- [Pull-based Ingestion Enhancements](features/opensearch/pull-based-ingestion-enhancements.md) - Offset-based lag metric, periodic flush, message mappers, and dynamic consumer configuration
- [Query Bugfixes](features/opensearch/query-bugfixes.md) - Fix crashes in wildcard queries, aggregations, highlighters, and script score queries
- [Reactor Netty Transport](features/opensearch/reactor-netty-transport.md) - Fix HTTP channel tracking and release during node shutdown
- [Shard Allocation](features/opensearch/shard-allocation.md) - Fix WeightFunction constraint reset when updating balance factors
- [Shard & Segment Bugfixes](features/opensearch/shard-segment-bugfixes.md) - Fix merged segment warmer exceptions, ClusterService state assertion, and EngineConfig builder
- [Snapshot & Restore Bugfixes](features/opensearch/snapshot-restore-bugfixes.md) - Fix NullPointerException when restoring remote snapshot with missing shard size information

### OpenSearch Dashboards

- [Dashboards Bugfixes](features/opensearch-dashboards/dashboards-bugfixes.md) - SQL query parser fix, Axios CVE update, DOMPurify import, dashboard utilities type checks
- [Dashboards Console](features/opensearch-dashboards/dashboards-console.md) - Fix for console_polling setting update
- [Dashboards Navigation](features/opensearch-dashboards/dashboards-navigation.md) - Fix disabled prop propagation for navigation links
- [Dashboards CI/Tests](features/opensearch-dashboards/dashboards-ci-tests.md) - Update unit test workflow to include 3.* branch support

### Dashboards Assistant

- [Dashboards Assistant Bugfixes](features/dashboards-assistant/dashboards-assistant-bugfixes.md) - Text2Viz header fix and capability services access settings fix

### Dashboards Flow Framework

- [Dashboards Flow Framework Bugfixes](features/dashboards-flow-framework/dashboards-flow-framework-bugfixes.md) - Gracefully handle workflows with no provisioned resources

### Dashboards Observability

- [Observability CI/Tests](features/dashboards-observability/observability-ci-tests.md) - CI workflow updates for 3.4.0, snapshot repository migration, test snapshot updates

### Dashboards Reporting

- [Reporting Bugfixes](features/dashboards-reporting/reporting-bugfixes.md) - Security fix for CVE-2025-57810 (jspdf bump) and null/undefined datetime handling in CSV reports

### User Behavior Insights

- [User Behavior Insights Build](features/user-behavior-insights/user-behavior-insights-build.md) - Migrate Maven snapshot publishing from Sonatype to S3-backed repository
- [User Behavior Insights Bugfixes](features/user-behavior-insights/user-behavior-insights-bugfixes.md) - ActionFilter interface adaptation, CI build script fix, plugin zip publishing fix

### Search Relevance

- [Search Relevance CI/Tests](features/search-relevance/ci-tests.md) - Test dependency fixes, JDWP debugging support, deprecated API removal, and test code cleanups
- [Search Relevance Bugfixes](features/search-relevance/search-relevance-bugfixes.md) - Fix query serialization for plugins (e.g., Learning to Rank) that extend OpenSearch's DSL
- [Hybrid Optimizer Bugfixes](features/search-relevance/hybrid-optimizer-bugfixes.md) - Fix floating-point precision in weight generation and error handling for deleted judgments
- [Security Integration Test Control](features/search-relevance/security-integ-test-control.md) - System property to control security plugin integration in tests

### SQL

- [PPL Query Optimization](features/sql/ppl-query-optimization.md) - 33 enhancements including sort pushdown, aggregation optimization, distinct count approx, case-to-range queries, fillnull command, YAML explain format
- [SQL/PPL Bugfixes](features/sql/sql-ppl-bugfixes.md) - 48 bug fixes including memory exhaustion fix, race condition fix, rex nested capture groups, filter pushdown improvements, and CVE-2025-48924
- [SQL CI/Tests](features/sql/sql-ci-tests.md) - CI/CD improvements including Gradle 9.2.0, JDK 25, BWC test splitting, query timeouts, and maven snapshots publishing
- [SQL Documentation](features/sql/sql-documentation.md) - PPL command documentation standardization, typo fixes, enhanced examples, and function documentation improvements

### Query Insights

- [Query Insights CI/Tests](features/query-insights/ci-tests.md) - Multi-node integration tests, health stats REST API tests, and flaky test fixes

### Query Insights Dashboards

- [WLM Dashboards Bugfixes](features/query-insights-dashboards/wlm-dashboards-bugfixes.md) - Fix MDS selector visibility on Workload Management pages when new home page UI is enabled
- [Query Insights Bugfixes](features/query-insights-dashboards/query-insights-bugfixes.md) - Exclude internal `top_queries-*` indices, MDS support for WLM routes, Jest test fixes

### k-NN

- [k-NN Build](features/k-nn/k-nn-build.md) - SIMD library build support and S3 snapshots migration
- [k-NN Enhancements](features/k-nn/k-nn-enhancements.md) - Native SIMD scoring for FP16, VectorSearcherHolder memory optimization, MMR rerank refactoring

### Neural Search

- [SEISMIC Bugfixes](features/neural-search/seismic-bugfixes.md) - Fix IT failures in multi-node environments, query handling without method_parameters, and disk space recovery on index deletion

### Learning to Rank

- [Learning to Rank Bugfixes](features/learning/learning-to-rank-bugfixes.md) - Legacy version ID fix, integration test stability, rescore-only SLTR logging fix

### ML Commons

- [ML Commons Bugfixes](features/ml-commons/ml-commons-bugfixes.md) - Agent type update validation, QueryPlanningTool model ID parsing, tool config empty values, agentic memory multi-node fixes

### Skills

- [Skills Log Insight](features/skills/skills-log-insight.md) - Increase max_sample_count from 2 to 5 for log insight in LogPatternAnalysisTool

### OpenSearch Remote Metadata SDK

- [Remote Model Bugfixes](features/opensearch-remote-metadata-sdk/remote-model-bugfixes.md) - Fix error when updating global model status in DynamoDB backend
- [k-NN Bugfixes](features/k-nn/k-nn-bugfixes.md) - Memory optimized search fixes, race condition in KNNQueryBuilder, Faiss inner product score calculation, and disk-based vector search BWC

### CI

- [CI/Test Infrastructure](features/ci/test-infrastructure.md) - GitHub Actions upgrades (checkout v6, github-script v8, codecov-action v5), test reliability improvements, CI disk space management, S3 snapshots integration, multi-node testing

### Multi-Repository

- [Dependency Updates](features/multi-repo/dependency-updates.md) - 28 dependency updates across 7 repositories addressing CVE-2025-11226, CVE-2025-58457, CVE-2025-41249
- [JDK 25 & Gradle 9.2 Upgrades](features/multi-plugin/jdk-25-gradle-9.2-upgrades.md) - Coordinated Gradle 9.2 and JDK 25 upgrades across 24 plugin repositories
- [Version Increments](features/multi-repo/version-increments.md) - Version bump to 3.4.0 across index-management, notifications, and dashboards-notifications

### Index Management

- [Index Management Bugfixes](features/index-management/index-management-bugfixes.md) - Fix ISM policy rebinding, SM deletion snapshot pattern parsing, ExplainSMPolicy serialization, rollup test race conditions

### Flow Framework

- [Flow Framework Bugfixes](features/flow-framework/flow-framework-bugfixes.md) - Fix incorrect output dimension default (768→384) in semantic search with local model template

### Cross-Cluster Replication

- [Cross-Cluster Replication Bugfixes](features/cross-cluster-replication/cross-cluster-replication-bugfixes.md) - Make pause replication API request body optional

### Anomaly Detection

- [Anomaly Detection Bugfixes](features/anomaly-detection/anomaly-detection-bugfixes.md) - Fix 3-AZ forecast results index creation, frequency-aware missing data detection, and data source error toast suppression
