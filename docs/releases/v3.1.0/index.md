---
tags:
  - indexing
  - observability
  - performance
  - search
  - security
---

# OpenSearch v3.1.0 Release

- Release Summary

## Features

### OpenSearch

- Approximation Framework - BKD traversal optimization for skewed datasets with DFS strategy
- Derived Source - Storage optimization by deriving _source from doc_values and stored fields
- Async Shard Batch Fetch - Enabled by default with 20s timeout for improved cluster manager resilience
- Crypto/KMS Plugin - Decoupled plugin initialization and AWS SDK v2.x dependency upgrade
- Dependency Bumps - 21 dependency updates including CVE-2025-27820 fix, Netty, Gson, Azure SDK updates
- DocRequest Refactoring - Generic interface for single-document operations
- File Cache - File pinning support and granular statistics for Writable Warm indices
- FIPS Support - Update FipsMode check for improved BC-FIPS compatibility
- Lucene Upgrade - Upgrade Apache Lucene from 10.1.0 to 10.2.1
- Network Configuration - Fix systemd seccomp filter for network.host: 0.0.0.0
- Percentiles Aggregation - Switch to MergingDigest for up to 30x performance improvement
- Plugin Installation - Fix native plugin installation error caused by PGP public key change
- Plugin Testing Framework - Enable testing for ExtensiblePlugins using classpath plugins
- Pull-based Ingestion - Lag metrics, error metrics, configurable queue, retries, create mode, write blocks, consumer reset
- Query Bug Fixes - Fixes for exists query, error handling, field validation, and IP field terms query
- Query Optimization - Automatic must_not range rewrite and sort-query performance improvements
- Remote Store - Close index rejection during migration and cluster state diff download fix
- S3 Repository Enhancements - SSE-KMS encryption support and S3 bucket owner verification
- Snapshot/Repository Fixes - Fix infinite loop during concurrent snapshot/repository update and NPE for legacy snapshots
- Star-Tree Index Enhancements - Production-ready status, date range queries, nested aggregations, index-level control
- Cluster Manager Metrics - Task execution time, node-left counter, and FS health failure metrics
- gRPC Transport - Performance optimization with pass-by-reference pattern and package reorganization
- Unified Highlighter - Add matched_fields support for blending matches from multiple fields
- System Ingest Pipeline - Automatic pipeline generation for plugin developers with bulk update support
- Query Coordinator Context - Search request access and validate API integration for index-aware query rewriting
- Composite Directory Factory - Pluggable factory for custom composite directory implementations in warm indices
- Security Manager Replacement - Enhanced Java Agent to intercept newByteChannel from FileSystemProvider
- Warm Storage Tiering - WarmDiskThresholdDecider and AutoForceMergeManager for hot-to-warm migration
- Workload Management - Paginated `/_list/wlm_stats` API with token-based pagination and sorting
- Rule-based Auto-tagging - Automatic workload group assignment based on index patterns and rules
- Parallel Shard Refresh - Shard-level refresh scheduling for improved data freshness in remote store indexes
- Platform Support - Add support for Linux riscv64 platform

### Skills

- ML Skills - Fix httpclient5 dependency version conflict and apply Spotless formatting
- ML Skills Text2Spark PPL - Add data source type parameter to PPLTool for Spark/S3 support
- Skills PPL Tool Fixes - Fix fields bug to expose multi-field mappings for aggregation queries

### Reporting

- Reporting Release Maintenance - Version increment to 3.1.0-SNAPSHOT and release notes for v3.1.0

### Security

- Resource Access Control Framework - Centralized resource sharing SPI with 1:1 backing indices and automatic access evaluation
- Security Backend Bug Fixes - Stale cache post snapshot restore, compliance audit log diff, DLS/FLS filter reader, auth header logging, password reset UI, forecasting permissions
- Security Cache Management - Selective user cache invalidation endpoint and dynamic cache TTL configuration
- Security Debugging - Enhanced error messages for "Security not initialized" with cluster manager status
- Security Dependency Updates - 24 dependency updates including Bouncy Castle 1.81, Kafka 4.0.0, and CVE-2024-52798 fix
- Security Performance Improvements - Immutable User object with serialization caching for reduced inter-node communication overhead
- Security Role Mapping - Fix mapped roles not included in ThreadContext userInfo after immutable User object change
- Security Permissions - Add forecast roles and fix missing cluster:monitor and mapping get permissions
- Security Testing Framework - Use extendedPlugins in integrationTest framework for sample resource plugin testing
- Security JWT Enhancements - Support for extracting backend roles from nested JWT claims
- Security CI/CD - Changelog verification workflow and Dependabot PR automation

### Query Insights

- Query Insights Enhancements - Metric labels for historical data, consolidated grouping settings, index exclusion, async reader, Live Queries Dashboard, WLM Dashboard
- Query Insights Release Maintenance - Fix flaky integration tests and add multi-node test infrastructure
- Query Insights Bug Fixes - Fix node-level request serialization, live query status response, and CI test stability

### Observability

- Observability Release Maintenance - Version increments, release notes, and bug fixes for trace analytics
- Observability Bug Fixes - Jaeger end time processing fix and NFW integration Vega warning fix
- Observability Trace Analytics - Merge custom source and data prepper mode, span flyout nested field support

### Neural Search

- Semantic Field - GA release with mapping transformer, ingest processor, query logic, chunking support, search analyzers, and stats tracking
- Hybrid Query Collapse - Collapse functionality for hybrid queries with 2-3x performance improvement and RRF custom weights
- Lucene Upgrade - Update hybrid query implementation for Lucene 10.2.1 API compatibility
- Neural Search Bug Fixes - 7 bug fixes for hybrid query validation, semantic field handling, radial search serialization, stats API, and stability
- Neural Search Compatibility - Update neural-search for OpenSearch 3.0 beta compatibility
- Neural Search Enhancements - Analyzer-based neural sparse query, FixedCharLengthChunker, and model_id/analyzer validation
- Neural Search Stats - Comprehensive stats API for monitoring ingest processors, search processors, hybrid queries, and semantic highlighting

### Learning to Rank

- Lucene Upgrade - Update RankerQuery for Lucene 10.2.1 DisiPriorityQueue API change

### ML Commons

- Agent Framework - Update Agent API, MCP tools persistence, function calling for LLM interfaces, custom SSE endpoint, metrics framework integration, multiple bug fixes
- Connector/Model Validation Bug Fixes - Input validation for names/descriptions, schema string type preservation, connector retry policy NPE fix, MCP tool memory fix, Bedrock DeepSeek format fix
- ML Commons Maintenance - Hidden model security, enhanced logging, HTTP client alignment, SearchIndexTool MCP compatibility, CVE fixes
- [MCP (Model Context Protocol)](features/ml-commons/mcp-(model-context-protocol).md) - MCP SDK downgrade to 0.9.0 and unit test coverage
- PlanExecuteReflect Agent - Test coverage for PlanExecuteReflect Agent runner and utilities
- ML Commons Release Notes and Documentation - Release note formatting, Maven snapshot publishing migration, README branding, Claude v4 blueprint

### Notifications

- Notifications Maintenance - Migrate from javax.mail to jakarta.mail APIs and version increment to 3.1.0-SNAPSHOT

### Job Scheduler

- Job Scheduler Maintenance - Remove Guava dependency to reduce jar hell and version increment to 3.1.0
- Job Scheduler Changelog - Add CHANGELOG and changelog_verifier workflow for iterative release notes

### Dashboards Search Relevance

- Search Relevance Dashboards Fixes - Fix schema validation in POST Query Sets endpoint

### Flow Framework

- Flow Framework Dependencies - Conditional DynamoDB client dependency and data summary with log pattern agent template
- Flow Framework Improvements - Bug fixes for RegisterAgentStep LLM field processing, exception type in error messages, and LLM spec parameter passing

### Dashboards Flow Framework

- Flow Framework UI Enhancements - Left panel navigation refactor, preview panel integration into inspector, Sparse Encoders template, configurable thread pools

### Index Management

- Notifications Improvements - Fix false positive notifications in Snapshot Management for version conflict exceptions

### Dashboards Assistant

- Dashboard Assistant (AI Chatbot) - T2viz enhancements, streaming buffer, persistent flyout state, admin UI settings
- Dashboard Assistant CI Fixes - Fix CI failures due to path alias babel configuration changes
- Security Dashboards UI Fixes - Bug fixes for embeddable dropdown, error logging, insights request timing, and conversation loading state

### Multi-Plugin

- Testing Library Updates - Update @testing-library/user-event to v14.4.3 in anomaly-detection and index-management dashboards plugins
- Version Bumps and Release Maintenance - Version increments across 11 repositories for v3.1.0 release cycle

### k-NN

- k-NN Bug Fixes - 9 bug fixes for quantization cache, rescoring, thread safety, nested queries, memory cache race conditions, backward compatibility
- k-NN Testing Infrastructure - Enable all integration tests with remote index builder and fix MockNode constructor compatibility
- k-NN Vector Search Improvements - Memory-optimized search for Faiss binary indexes, Lucene rescore support, derived source optimization, script scoring performance
- Remote Vector Index Build - GA preparation with tuned buffer sizes, segment size upper bound, renamed settings, metrics fixes

### Search Relevance

- Search Relevance Workbench - New experimental toolkit with hybrid search experiments, external judgment import, Stats API, and security integration
- Search Relevance Test Data - Add realistic ESCI-based test dataset with 150 queries and matching judgments
- Search Relevance Bug Fixes - Data model restructuring, LLM judgment improvements, search request builder fix, hybrid optimizer fix, input validation

### SQL

- SQL/PPL Calcite Engine - 15+ new commands (eventstats, flatten, expand, trendline, appendcol, grok, top, rare, fillnull, describe, patterns) and functions (coalesce, isempty, isblank, ispresent, geoip, cidrmatch) with LIMIT pushdown and ResourceMonitor
- SQL/PPL General Enhancements - JSON functions, lambda/array functions, cryptographic hashes, time conditions, approximate distinct count, match_only_text support, object field merging
- SQL/PPL Bug Fixes - 17 bug fixes including long IN-list crash, function fixes (ATAN, CONV, UNIX_TIMESTAMP), field handling, and Calcite engine stability

### Remote

- Security CVE Fixes - CVE-2025-27820 fix for Apache HttpClient in opensearch-remote-metadata-sdk

### Geospatial

- Geospatial Ip2Geo Fixes - Cache synchronization fixes for IP2Geo processor with metadata reset and retry logic

### Custom Codecs

- Build/Test Infrastructure - Fix BWC test dependency version and add java-agent plugin
- QAT-Accelerated Zstandard Compression - New `qat_zstd` codec for hardware-accelerated ZSTD compression using Intel QAT

### Anomaly Detection

- Anomaly Detection Forecasting - Bug fixes for forecasting task state handling, date format compatibility, cold-start/window delay refinements, UI validation and error display improvements

### Alerting

- Alerting Improvements - Doc-level monitor timeboxing, batch findings publishing, index pattern validation, threat intel monitor fix, dashboard alert insights
