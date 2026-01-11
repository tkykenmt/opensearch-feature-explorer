# OpenSearch v3.4.0 Release

## Features

### OpenSearch

- [Build Tool Upgrades](features/opensearch/build-tool-upgrades.md) - Gradle 9.1 and bundled JDK 25 updates
- [Dependency Updates (OpenSearch Core)](features/opensearch/dependency-updates-opensearch-core.md) - 32 dependency updates including Netty 4.2.4 for HTTP/3 readiness
- [Lucene Upgrade](features/opensearch/lucene-upgrade.md) - Bump Apache Lucene from 10.3.1 to 10.3.2 with MaxScoreBulkScorer bug fix
- [Security Kerberos Integration](features/opensearch/security-kerberos-integration.md) - Update Hadoop to 3.4.2 and enable Kerberos integration tests for JDK-24+
- [Settings Bugfixes](features/opensearch/settings-bugfixes.md) - Fix duplicate registration of dynamic settings and patch version build issues
- [Stats Builder Pattern Deprecations](features/opensearch/stats-builder-pattern-deprecations.md) - Deprecated constructors in 30+ Stats classes in favor of Builder pattern

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

### OpenSearch Dashboards

- [Dashboards Console](features/opensearch-dashboards/dashboards-console.md) - Fix for console_polling setting update
- [Dashboards Navigation](features/opensearch-dashboards/dashboards-navigation.md) - Fix disabled prop propagation for navigation links
