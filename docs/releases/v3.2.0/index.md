# OpenSearch v3.2.0 Release

## Overview

This page indexes all investigated release items for OpenSearch v3.2.0.

## Release Reports

### OpenSearch

| Item | Category | Description |
|------|----------|-------------|
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
| [System Ingest Pipeline Fix](features/opensearch/system-ingest-pipeline-fix.md) | bugfix | Fix system ingest pipeline to properly handle index templates |
| [Azure Repository Fixes](features/opensearch/azure-repository-fixes.md) | bugfix | Fix SOCKS5 proxy authentication for Azure repository |
| [Profiler Enhancements](features/opensearch/profiler-enhancements.md) | bugfix | Fix concurrent timings in profiler for concurrent segment search |
| [Engine Optimization Fixes](features/opensearch/engine-optimization-fixes.md) | bugfix | Fix leafSorter optimization for ReadOnlyEngine and NRTReplicationEngine |
| [Search Preference & Awareness Fix](features/opensearch/search-preference-awareness-fix.md) | bugfix | Fix custom preference string to ignore awareness attributes for consistent routing |
| [Settings Management](features/opensearch/settings-management.md) | bugfix | Ignore archived settings on update to unblock settings modifications |
| [SecureRandom Blocking Fix](features/opensearch/securerandom-blocking-fix.md) | bugfix | Fix startup freeze on low-entropy systems by reverting to non-blocking SecureRandom |
| [Field Mapping Fixes](features/opensearch/field-mapping-fixes.md) | bugfix | Fix field-level ignore_malformed override and scaled_float encodePoint method |
| [Search Scoring Fixes](features/opensearch/search-scoring-fixes.md) | bugfix | Fix max_score null when sorting by _score with secondary fields |
| [Replication Lag Fix](features/opensearch/replication-lag-fix.md) | bugfix | Fix segment replication lag computation using correct epoch timestamps |
| [Parent-Child Query Fixes](features/opensearch/parent-child-query-fixes.md) | bugfix | Fix QueryBuilderVisitor pattern for HasParentQuery and HasChildQuery |
