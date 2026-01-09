# OpenSearch v2.18.0 Release

## Overview

This page contains feature reports for OpenSearch v2.18.0.

## Features by Repository

### OpenSearch

- [Replication](features/opensearch/replication.md) - Fix array hashCode calculation in ResyncReplicationRequest
- [Task Management](features/opensearch/task-management.md) - Fix missing fields in task index mapping for proper task result storage
- [Test Fixes](features/opensearch/test-fixes.md) - Fix flaky test in ApproximatePointRangeQueryTests by adjusting totalHits assertion logic

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
