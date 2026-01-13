---
tags:
  - indexing
  - performance
  - search
  - security
---

# OpenSearch v3.4.0 Release

- Release Summary

## Features

### OpenSearch

- Aggregation Optimizations - Hybrid cardinality collector, filter rewrite + skip list, MergingDigest for percentiles, matrix_stats primitive arrays
- Filter Rewrite Optimization - Bulk collection APIs for filter rewrite sub-aggregation with up to 20% performance improvement
- GRPC Transport - Pluggable interceptors, thread context preservation, binary document formats, expanded query support
- ApproximatePointRangeQuery Pack Method Optimization - Use Lucene's native `pack` method for `half_float` and `unsigned_long` types
- Build Tool Upgrades - Gradle 9.1 and bundled JDK 25 updates
- Concurrent Segment Search - Performance optimization by omitting MaxScoreCollector when sorting by score
- Context Aware Segments - Collocate related documents into same segments based on grouping criteria for improved query performance
- Index Settings - Custom creation_date setting and tier-aware shard limit validation for local and remote indices
- Segment Grouping - Mapper for defining context-aware segment grouping criteria with Painless script support
- Dependency Updates (OpenSearch Core) - 32 dependency updates including Netty 4.2.4 for HTTP/3 readiness
- Engine Refactoring - Move prepareIndex/prepareDelete to Engine class and make NoOpResult constructors public
- FIPS Compliance - Test suite FIPS 140-3 compliance support with BC-FIPS provider
- JDK 25 Support - Painless scripting compatibility fix for JDK 25 ClassValue behavioral change
- Lucene Integration - Remove MultiCollectorWrapper and use Lucene's native MultiCollector API
- Lucene Upgrade - Bump Apache Lucene from 10.3.1 to 10.3.2 with MaxScoreBulkScorer bug fix
- Maven Snapshots Publishing - Migrate snapshot publishing from Sonatype to S3-backed repository at ci.opensearch.org
- Merged Segment Warmer - GA graduation with configurable resiliency features and cluster-level merge scheduler settings
- Node Stats Bugfixes - Fix negative CPU usage values in node stats on certain Linux distributions
- Normalizer Enhancements - Allow truncate token filter in normalizers for keyword field truncation
- S3 Repository - Add LEGACY_MD5_CHECKSUM_CALCULATION to opensearch.yml settings for S3-compatible storage
- Scroll Query Optimization - Cache StoredFieldsReader per segment for improved scroll query performance
- Search API Tracker - Track search response status codes at coordinator node for observability
- Security Kerberos Integration - Update Hadoop to 3.4.2 and enable Kerberos integration tests for JDK-24+
- Settings Bugfixes - Fix duplicate registration of dynamic settings and patch version build issues
- Stats Builder Pattern Deprecations - Deprecated constructors in 30+ Stats classes in favor of Builder pattern
- Terms Query Optimization - Pack terms once for keyword fields with index and docValues enabled
- Thread Pool - ForkJoinPool thread pool type support for work-stealing parallelism
- Transport Actions API - Internal API for retrieving metadata about requested indices from transport actions
- XContent Filtering - Case-insensitive filtering support for XContentMapValues.filter
- Plugin Dependencies - Range semver support for dependencies in plugin-descriptor.properties
- Query String Monitoring - Monitoring mode for query string length validation with warning logs instead of rejection
- Repository Encryption - Server-side encryption support for S3 remote store repositories
- ActionPlugin Enhancements - Pass REST header registry to getRestHandlerWrapper for efficient header access
- WildcardFieldMapper - Change doc_values default to true for nested query support

### Security

- Resource Sharing - Multi-type index support, ResourceProvider interface, Builder pattern, REST API improvements
- Security AccessController Migration - Migrate from deprecated java.security.AccessController to org.opensearch.secure_sm.AccessController
- Security Bugfixes - Multi-tenancy `.kibana` index fix, WildcardMatcher empty string handling, DLS/FLS internal request fix, PrivilegesEvaluator modularization
- Security Configuration - Dedicated config reloading thread, dynamic resource settings, X509v3 SAN authentication, performance optimizations, securityadmin timeout
- Security Features - Webhook Basic Auth, REST header propagation, system indices deprecation, static/custom config overlap, search relevance permissions
- WLM Security Attributes - Security attribute extraction for WLM rule-based auto-tagging (username, roles)
- GitHub Actions Updates - Update GitHub Actions dependencies to support Node.js 24 runtime

### Security Dashboards Plugin

- Security Dashboards Bugfixes - Filter blank backend roles before creating internal user

### Security Analytics Dashboards Plugin

- Security Analytics Bugfixes - Fix correlation table rendering bug in correlations overview page

### Alerting

- PPL Alerting - V2 alerting API with PPL query support, stateless alerts with automatic expiration, per-result and result-set trigger modes

### OpenSearch Dashboards

- Dashboards AI Insights - Detection Insights workspace category and log pattern agent support for Discover Summary
- Dashboards Chat - Global search integration, suggestion system, state persistence, session storage, Explore integration
- Dashboards Dev Tools - PATCH method support for Dev Tools console
- Dashboards Explore - Histogram breakdowns, Field Statistics tab, trace flyout, correlations, cancel query, and by-value embeddables
- Dashboards Global Search - Assets search and enhanced command system for global search
- Dashboards CSP - Dynamic configuration support for CSP report-only mode
- Dashboards Data Connections - Prometheus saved object support for data connections
- Dashboards Query Action Service - Flyout registration support for query panel actions
- Dashboards Visualizations - Bar gauge, customizable legends, numerical color fields, and table column ordering
- Dashboards Workspace - Remove restriction requiring data source for workspace creation
- Dashboards Traces - Span status filters and trace details UX improvements
- Dashboards Dataset Management - Schema mapping, wildcard prefix, and enhanced dataset table

## Bug Fixes

### Alerting

- Alerting Build - Fix build script to only publish alerting plugin zip, excluding sample remote monitor plugin

### Alerting Dashboards Plugin

- Alerting Enhancements - Keyword filter support for bucket-level monitor triggers and MDS client fix for OpenSearch API calls

### OpenSearch

- Java Agent - Fix JRT protocol URL filtering to allow MCP server connections
- Bulk Request Bugfixes - Fix indices property initialization during BulkRequest deserialization
- Bulk API Enhancements - Implement error_trace parameter support for bulk requests
- Cluster State & Allocation Bugfixes - Fix concurrent modification in allocation filters and version compatibility in remote state
- Data Stream & Index Template Bugfixes - Fix deletion of unused index templates matching data streams with lower priority
- GRPC Transport Bugfixes - Fix ClassCastException for large requests, Bulk API fixes, and node bootstrap with streaming transport
- Pull-based Ingestion Bugfixes - Fix out-of-bounds offset handling and remove persisted pointers for at-least-once guarantees
- Pull-based Ingestion Enhancements - Offset-based lag metric, periodic flush, message mappers, and dynamic consumer configuration
- Query Bugfixes - Fix crashes in wildcard queries, aggregations, highlighters, and script score queries
- Reactor Netty Transport - Fix HTTP channel tracking and release during node shutdown
- Shard Allocation - Fix WeightFunction constraint reset when updating balance factors
- Shard & Segment Bugfixes - Fix merged segment warmer exceptions, ClusterService state assertion, and EngineConfig builder
- Snapshot & Restore Bugfixes - Fix NullPointerException when restoring remote snapshot with missing shard size information

### OpenSearch Dashboards

- Dashboards Bugfixes - SQL query parser fix, Axios CVE update, DOMPurify import, dashboard utilities type checks
- Dashboards Console - Fix for console_polling setting update
- Dashboards Navigation - Fix disabled prop propagation for navigation links
- Dashboards CI/Tests - Update unit test workflow to include 3.* branch support

### Dashboards Assistant

- Discover Summary - Log pattern detection for Discover Summary with specialized agent selection
- Dashboards Assistant Bugfixes - Text2Viz header fix and capability services access settings fix

### Dashboards Flow Framework

- Dashboards Agent & Assistant - Agent summary visualization, memory integration, simplified configuration, automatic response filters
- Dashboards Flow Framework Bugfixes - Gracefully handle workflows with no provisioned resources

### Dashboards Observability

- Observability CI/Tests - CI workflow updates for 3.4.0, snapshot repository migration, test snapshot updates
- Observability Integrations - Static file serving cleanup with image type validation and SVG sanitization

### Dashboards Reporting

- Reporting Bugfixes - Security fix for CVE-2025-57810 (jspdf bump) and null/undefined datetime handling in CSV reports

### Dashboards Notifications

- Notifications UX - Fix channel name edit refetching on every keystroke

### User Behavior Insights

- User Behavior Insights Build - Migrate Maven snapshot publishing from Sonatype to S3-backed repository
- User Behavior Insights Bugfixes - ActionFilter interface adaptation, CI build script fix, plugin zip publishing fix

### Search Relevance

- Agentic Search - Pairwise comparison support, MCP server integration, conversational search UI, source parameter preservation
- Scheduled Experiments - Cron-based scheduling for recurring experiment execution with historical results tracking
- Query Sets & Judgment Lists - GUID filtering support for Query Sets with strongly typed QuerySetItem interface
- Search Relevance CI/Tests - Test dependency fixes, JDWP debugging support, deprecated API removal, and test code cleanups
- Search Relevance Bugfixes - Fix query serialization for plugins (e.g., Learning to Rank) that extend OpenSearch's DSL
- Hybrid Optimizer Bugfixes - Fix floating-point precision in weight generation and error handling for deleted judgments
- Security Integration Test Control - System property to control security plugin integration in tests

### SQL

- PPL Eval Functions - New multivalue functions (mvappend, mvindex, mvdedup), tostring conversion function, and regexp_replace alias
- PPL Timechart Functions - Rate-based aggregation functions (per_second, per_minute, per_hour, per_day), millisecond span support, custom timefield option, merged timechart/chart implementation
- PPL Query Optimization - 33 enhancements including sort pushdown, aggregation optimization, distinct count approx, case-to-range queries, fillnull command, YAML explain format
- SQL/PPL Bugfixes - 48 bug fixes including memory exhaustion fix, race condition fix, rex nested capture groups, filter pushdown improvements, and CVE-2025-48924
- SQL CI/Tests - CI/CD improvements including Gradle 9.2.0, JDK 25, BWC test splitting, query timeouts, and maven snapshots publishing
- SQL Documentation - PPL command documentation standardization, typo fixes, enhanced examples, and function documentation improvements
- PPL Commands (Calcite) - New PPL commands (chart, streamstats, multisearch, replace, appendpipe) and enhancements (bucket_nullable, usenull, pushdown optimizations)

### Query Insights

- Query Insights CI/Tests - Multi-node integration tests, health stats REST API tests, and flaky test fixes

### Query Insights Dashboards

- Query Version-Aware Settings - Version-aware settings support for dynamic feature detection based on cluster version
- WLM Dashboards Bugfixes - Fix MDS selector visibility on Workload Management pages when new home page UI is enabled
- Query Insights Bugfixes - Exclude internal `top_queries-*` indices, MDS support for WLM routes, Jest test fixes

### k-NN

- k-NN Build - SIMD library build support and S3 snapshots migration
- k-NN Enhancements - Native SIMD scoring for FP16, VectorSearcherHolder memory optimization, MMR rerank refactoring
- k-NN Memory Optimized Warmup - Optimized warmup procedure for memory-optimized search with page cache pre-loading

### Neural Search

- SEISMIC Bugfixes - Fix IT failures in multi-node environments, query handling without method_parameters, and disk space recovery on index deletion
- SEISMIC Nested Field - Support nested field ingestion and query for text chunking workflows with SEISMIC sparse ANN

### Performance Analyzer

- Performance Analyzer - Restore Java 21 minimum compatibility and remove Java 24 from CI matrix

### Learning to Rank

- Learning to Rank Bugfixes - Legacy version ID fix, integration test stability, rescore-only SLTR logging fix
- Learning to Rank Enhancements - Test infrastructure improvements, narrowed index cleanup scope for better test isolation

### ML Commons

- ML Commons Enhancements - Sensitive parameter filtering for connector APIs, resource type support for resource sharing, increased batch task limits (default: 100, max: 10,000)
- ML Commons Bugfixes - Agent type update validation, QueryPlanningTool model ID parsing, tool config empty values, agentic memory multi-node fixes

### Skills

- Skills Log Insight - Increase max_sample_count from 2 to 5 for log insight in LogPatternAnalysisTool

### OpenSearch Remote Metadata SDK

- Remote Store CMK Support - CMK encryption/decryption support for customer data with STS role assumption for cross-account access
- Remote Model Bugfixes - Fix error when updating global model status in DynamoDB backend
- k-NN Bugfixes - Memory optimized search fixes, race condition in KNNQueryBuilder, Faiss inner product score calculation, and disk-based vector search BWC

### CI

- CI/Test Infrastructure - GitHub Actions upgrades (checkout v6, github-script v8, codecov-action v5), test reliability improvements, CI disk space management, S3 snapshots integration, multi-node testing

### Multi-Repository

- Dependency Updates - 28 dependency updates across 7 repositories addressing CVE-2025-11226, CVE-2025-58457, CVE-2025-41249
- JDK 25 & Gradle 9.2 Upgrades - Coordinated Gradle 9.2 and JDK 25 upgrades across 24 plugin repositories
- Version Increments - Version bump to 3.4.0 across index-management, notifications, and dashboards-notifications

### Index Management

- ISM Exclusion Pattern - Support exclusion patterns in ISM template index patterns using `-` prefix for selective index management
- Index Management Bugfixes - Fix ISM policy rebinding, SM deletion snapshot pattern parsing, ExplainSMPolicy serialization, rollup test race conditions

### Flow Framework

- Flow Framework Access Control - Integration with centralized Resource Sharing and Access Control framework
- Flow Framework Bugfixes - Fix incorrect output dimension default (768→384) in semantic search with local model template

### Cross-Cluster Replication

- Cross-Cluster Replication Bugfixes - Make pause replication API request body optional

### Anomaly Detection

- Anomaly Detection Enhancements - Conditional resource sharing fallback, client API extensions for validate/suggest, auto_create field, suggest API read access
- Anomaly Detection Bugfixes - Fix 3-AZ forecast results index creation, frequency-aware missing data detection, and data source error toast suppression

### Anomaly Detection Dashboards Plugin

- Anomaly Detection Daily Insights - New Daily Insights page with AI-powered anomaly correlation, automated detector creation via ML agents, and multi-cluster index management
