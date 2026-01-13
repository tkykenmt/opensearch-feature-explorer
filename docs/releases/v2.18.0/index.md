---
tags:
  - indexing
  - observability
  - performance
  - search
---

# OpenSearch v2.18.0 Release

## Overview

This page contains feature reports for OpenSearch v2.18.0.

- Release Summary

## Features by Repository

### OpenSearch

- Lucene 9.12.0 Upgrade - Upgrade Apache Lucene from 9.11.1 to 9.12.0 with new postings format, JDK 23 support, and performance optimizations
- List APIs (Paginated) - New `_list/indices` and `_list/shards` APIs with pagination support, plus cat API response limits
- Cluster Stats API - URI path filtering support for selective metric retrieval
- OpenSearch Core Dependencies - 26 dependency updates including Lucene 9.12.0, Netty 4.1.114, gRPC 1.68.0, Protobuf 3.25.5
- Cluster State Management - Fix voting configuration mismatch by updating lastSeenClusterState in commit phase
- Remote Cluster State - Fallback to remote cluster state on term-version check mismatch for improved performance in large clusters
- Dynamic Settings - Make multiple cluster settings dynamic for tuning on larger clusters
- Wildcard Query Fixes - Fix escaped wildcard character handling and case-insensitive query on wildcard field
- Flat Object Field - Fix infinite loop when flat_object field contains invalid token types
- Flat Object Query Optimization - Use IndexOrDocValuesQuery to optimize query performance, enable wildcard queries
- Index Settings - Fix default value handling when setting index.number_of_replicas and index.number_of_routing_shards to null
- Multi-Search API - Fix multi-search with template doesn't return status code
- Node Join/Leave - Fix race condition in node-join and node-left loop
- Search Backpressure - Add validation for cancellation settings to prevent cluster crashes
- Search Pipeline - Add support for msearch API to pass search pipeline name
- Star Tree Index - Initial experimental release with metric aggregations (sum, min, max, avg, value_count)
- Tiered Caching - Segmented cache architecture for improved concurrency and performance
- Streaming Indexing - Bug fixes for streaming bulk request hangs and newline termination errors
- Replication - Fix array hashCode calculation in ResyncReplicationRequest
- Task Management - Fix missing fields in task index mapping for proper task result storage
- Test Fixes - Fix flaky test in ApproximatePointRangeQueryTests by adjusting totalHits assertion logic
- Nested Aggregations - Fix infinite loop in nested aggregations with deep-level nested objects
- Phone Analyzer - New `phone` and `phone-search` analyzers for phone number indexing and search
- Code Cleanup - Query approximation simplification, Stream API optimization, typo fix
- Search Request Stats - Enable coordinator search.request_stats_enabled by default
- Secure Transport Settings - Add dynamic SecureTransportParameters to fix SSL dual mode regression
- Identity Feature Flag Removal - Remove experimental identity feature flag, move authentication to plugins
- Docker Compose v2 Support - Add support for Docker Compose v2 in TestFixturesPlugin for modern Docker installations
- Snapshot Restore Enhancements - Alias renaming during restore and clone operation optimization for doc-rep clusters
- Remote Store Metrics - New REMOTE_STORE metric in Node Stats API for monitoring pinned timestamp fetch operations
- S3 Repository - Standard retry mode for S3 clients and SLF4J warning fix
- S3 Async Deletion - Async deletion support for S3 repository using S3 async client
- Dynamic Threadpool Resize - Runtime thread pool size adjustment via cluster settings API
- Async Shard Fetch Metrics - OTel counter metrics for async shard fetch success and failure tracking
- Search API Enhancements - WithFieldName interface for aggregation/sort builders and successfulSearchShardIndices in SearchRequestContext
- Offline Nodes - New offline-tasks library with core abstractions for running background tasks on dedicated offline nodes
- Workload Management - Query sandboxing with tenant-level admission control, resource limits (CPU/memory), QueryGroup Stats API, and persistence

### OpenSearch Dashboards

- Dev Tools Modal - Dev Tools console rendered as a modal overlay for improved workflow
- Navigation Updates - Flattened navigation, persistent state, small screen support, border style updates
- Content Management - Add Page API to allow remove section
- Discover - Data summary panel, updated appearance, cache management, and bug fixes
- CI/CD & Build Improvements - Switch OSD Optimizer to content-based hashing for CI compatibility
- Input Control Visualization - Fix disabled ValidatedDualRange component sizing
- Data Source Permissions - Fix missing functions in data source permission saved object wrapper
- Dynamic Config - Bugfixes for config saved objects, global config discovery, and index/alias validation
- i18n & Localization - i18n validation workflows, precommit hook, translation fixes, language selection fix
- Data Connections - Dataset picker support for data connections with multi-select table, pagination, and search
- Data Connections Bugfixes - MDS endpoint unification, tabs navigation, type display, auto-complete MDS support
- Dependency Updates - JSON11 upgrade for UTF-8 safety, chokidar bump
- Discover Bugfixes (2) - S3 fields support, deleted index pattern handling, time field display, saved query loading
- Maintainers - Add Hailong-am as maintainer
- OUI Updates - Updates to OpenSearch UI component library (1.13 → 1.15)
- Query Enhancements (2) - Async polling, error handling, language compatibility, saved query fixes
- Query Enhancements Bugfixes - Search strategy extensibility, recent query fix, module exports, keyboard shortcuts
- Sample Data - Updated UI for new UX, OTEL sample data support for traces, metrics, and logs
- Sample Data Bugfixes - Update OTEL sample data description with compatible OS version
- Saved Query UX - New flyout-based UI for saved queries, sample queries on no results page
- TSVB Visualization - Hidden axis option, per-axis scale setting, compressed input fields
- UI/UX Bugfixes - Sidebar tooltips, initial page fixes, overlay positioning, Chrome 129 workaround, OUI breakpoints, HeaderControl rendering
- UI/UX Bugfixes (2) - Responsive design fixes for home page, page header, recent menu, and getting started cards
- UI/UX Improvements - Page title semantic improvements (h1 + xs size) for accessibility
- Workspace - Workspace-level UI settings, collaborator management, data connection integration, global search bar, ACL auditor
- Workspace Bugfixes - 13 bug fixes for workspace UI/UX, page crashes, permissions, and navigation
- Dashboards Maintenance - Version bump post 2.17, enhanced search API cleanup
- Query Editor - Footer bar for single-line editor, extension ordering fix, PPL autocomplete improvements
- Async Query - Frontend polling for async search, async PPL support for S3 datasets
- Dashboards Improvements - Loading indicator with time counter for query results
- MDS Integration Support - Multi Data Source support for Integration feature
- Experimental Features - User personal settings with scoped uiSettings and User Settings page
- Security CVE Fixes - Security updates for dns-sync, axios, path-to-regexp, dompurify, elliptic, micromatch

### Multi-Plugin

- Dependency Updates - 19 dependency updates including CVE-2024-7254 fix, Gradle 8.10.2, upload-artifact v4
- Search Autocomplete - Fix search_as_you_type multi-fields support and enhanced Dashboards autocomplete UX
- Release Notes - v2.18.0 release notes added across alerting, common-utils, notifications, query-insights, and security repositories

### Flow Framework

- Flow Framework - Add optional config field to tool step, incremental resource removal during deprovisioning
- Flow Framework Workflow State - Remove Painless scripts for workflow state updates, implement optimistic locking
- Flow Framework Bugfixes - Fix template update location in ReprovisionWorkflowTransportAction, improved logger statements
- Query Assist Data Summary Agent - Add sample template for Query Assist Data Summary Agent using Claude on Bedrock

### Alerting

- Alerting Doc-Level Monitor - Doc-level monitor improvements including comments system indices, remote monitor logging, separate query indices for external monitors, and query index lifecycle optimization
- Alerting Bugfixes - Query index management fixes, bucket-level monitor optimization, dashboard UX improvements, MDS compatibility fixes

### Alerting Dashboards Plugin

- Alerting Summary & Insights - AI-powered alert insights with context-aware analysis, LLM-generated summaries, and log pattern detection for visual editor monitors

### Common Utils

- Doc-Level Monitor Query Indices - New `delete_query_index_in_every_run` flag for dynamic deletion of doc-level monitor query indices, designed for externally defined monitors

### SQL

- SQL Error Handling - Improved error handling for malformed cursors and edge cases in query parsing
- SQL Pagination - Bug fixes for SQL pagination with `pretty` parameter and PIT refactor issues
- SQL PIT Refactor - Refactor SQL plugin to use Point in Time (PIT) API instead of Scroll API for joins and pagination
- SQL Plugin Maintenance - Security fix for CVE-2024-47554 (commons-io upgrade to 2.14.0) and test fixes for 2.18 branch
- SQL Query Fixes - Fix alias resolution in legacy SQL with filters, correct regex character range in Grok compiler
- SQL Scheduler - Bugfix to remove scheduler index from SystemIndexDescriptor to prevent conflicts with Job Scheduler plugin

### k-NN

- k-NN AVX512 Support - AVX512 SIMD support for Faiss engine, accelerating vector search and indexing on compatible x64 processors
- k-NN Performance & Engine - Default engine changed to FAISS, approximate threshold updated to 15K, rescoring improvements, memory management enhancements
- k-NN Documentation - JavaDoc cleanup for RescoreContext class
- k-NN Maintenance - Lucene 9.12 codec compatibility, force merge performance optimization, benchmark folder removal, code refactoring

### Neural Search

- Neural Search Reranking - ByFieldRerankProcessor for field-based reranking and hybrid query rescorer support
- Neural Search Text Chunking - Add `ignore_missing` parameter to text chunking processors for flexible handling of optional fields
- Neural Search Bugfixes - Fixed incorrect document order for nested aggregations in hybrid query

### ML Commons

- ML Commons Batch Jobs - Rate limiting, connector credential support, model group access control, and default action types for batch inference/ingestion
- ML Commons Model & Inference - Remote model auto-redeployment filtering, optional llmQuestion for RAG, search extension output support, query string in input_map, MLToolSpec config field, AWS Textract/Comprehend trusted endpoints
- ML Commons Bugfixes - 11 bug fixes for RAG pipelines, ML inference processors, connector time fields, model deployment stability, master key race condition, Bedrock BWC, and agent logging
- ML Commons Configuration - Change `.plugins-ml-config` index to use `auto_expand_replicas: 0-all` for maximum availability
- ML Commons Connectors & Blueprints - Bedrock Converse blueprint, cross-account model invocation tutorial, role temporary credential support, Titan Embedding V2 blueprint
- ML Commons CI/CD - Workflow approval system for external contributors, artifact actions upgrade to v4, developer guide updates

### Query Insights

- Query Insights Enhancements - Health Stats API, OpenTelemetry error metrics, field name/type grouping support, historical query time range parameters, cache management improvements
- Query Insights Settings - Change default values for grouping attribute settings (field_name, field_type) from false to true
- Query CI/CD - Upgrade deprecated actions/upload-artifact from v1/v2 to v3

### Anomaly Detection

- Anomaly Detection Enhancements - Suppression rule validation in AnomalyDetector constructor, default rules bug fix for empty rulesets, RCF version upgrade to 4.2.0
- Anomaly Detection Dependencies - Dependency updates (Jackson 2.18.0, JUnit Jupiter 5.11.2, Mockito 5.14.1) and removal of unused javassist dependency

### Anomaly Detection Dashboards

- Anomaly Detection Bugfixes - Bug fixes for custom result index rendering, historical analysis route, and preview support for rules and imputation

### Security Analytics

- Security Analytics System Indices - Standardized system index settings (1 primary shard, 1-20 replicas), dedicated query indices option, correlation alert refresh policy fix
- Security Analytics Correlation - Bug fixes for threat intel monitor alias resolution and REFRESHING state enum query
- Threat Intel Bug Fixes - Notification listener leak fix, duplicate findings prevention, source config validation, improved error handling
- Security Analytics IOC - IOC bug fixes: null check for multi-indicator scans, ListIOCs API count limits removed, index exists check for large IOC batches

### Security Analytics Dashboards

- Security Analytics UX - Comprehensive UX improvements including navigation menu restructuring, standardized UI spacing and typography, compressed search bars and filters, and context-aware page titles
- Security Analytics Data Source - Data source handling bug fixes including picker remount optimization, error toast suppression, default data source selection, and getting started cards visual redesign
- Security Analytics Findings - Fix findings page crash when custom rules are deleted and correct rule severity display for multi-rule findings

### Dashboards Query Workbench

- Query Workbench Bugfixes - Bug fixes for modal mounting support and MDS error handling

### Dashboards Assistant

- Assistant Capabilities - Capability-based UI rendering control, new API to check agent config existence, agentName renamed to agentConfigName
- Text to Visualization (t2viz) - AI-powered visualization generation from natural language queries using LLM agents

### Dashboards Maps

- Dashboards Maps Bugfix - Fix flyout overlay issue with new application header

### Dashboards Reporting

- Reporting Bugfixes - Fix missing EUI component imports in report_settings component

### Dashboards Notifications

- Notifications Bugfixes - Fix default data source selection, typo fixes, CI workflow updates
- Notifications Fit & Finish - UX improvements: semantic headers, consistent text sizes, smaller context menus, spacing standardization, full-width content

### Job Scheduler

- Job Scheduler - Return LockService from createComponents for Guice injection

### Index Management

- Index Management Bugfixes - Snapshot status detection fix, snapshot policy button reload fix, data source initialization fix
- Index Management Enhancements - Mixed rollup/non-rollup index search, UX improvements, transform API validation

### Observability

- Observability UI Improvements - Services data picker fix, header control styling, custom traces table filters, Getting Started workflow restructure, CI build cache optimization
- Observability Bugfixes - Multiple bug fixes including navigation fixes, workspace compatibility, MDS support improvements, and UI/UX enhancements

### Dashboards Observability

- Observability Get Started - Major restructure of Getting Started workflows into Logs/Metrics/Traces signal types, telemetry source dropdown, Self Managed/AWS tabs, auto index template creation

### Security

- Security Enhancements - Datastream support for audit logs, auto-convert V6 to V7 configuration, circuit breaker override, improved certificate error messages, JWT in MultipleAuthentication
- Security Bugfixes - Multiple bug fixes including system index access control, SAML audit logging, demo config detection, SSL dual mode propagation, stored field handling, and closed index mappings
- Security Plugin Maintenance - Cache endpoint deprecation warning, securityadmin script undeprecation, ASN1 refactoring for FIPS, CVE-2024-47554 fix, BWC test fixes

### Skills

- Skills Plugin Dependencies - Dependency updates (Mockito 5.14.2, JUnit5 5.11.2, ByteBuddy 1.15.4, Gradle 8.10.2) and test fix for AnomalyDetector API changes
- ML Skills & Tools - New LogPatternTool for log pattern analysis, customizable prompt support for CreateAnomalyDetectorTool

### CI/CD

- CI/CD & Build Improvements - JDK-21 baseline updates, CI workflow fixes, test security improvements, backport process enhancements across index-management, ml-commons, notifications, and observability

### Maintenance

- Version Bumps & Maintenance - Routine version increment PRs across 12 plugin repositories for v2.18.0 release preparation
