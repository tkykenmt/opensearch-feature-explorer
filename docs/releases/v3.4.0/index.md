# OpenSearch v3.4.0 Release

## Features

### OpenSearch

- [Aggregation Optimizations](features/opensearch/aggregation-optimizations.md) - Hybrid cardinality collector, filter rewrite + skip list, MergingDigest for percentiles, matrix_stats primitive arrays
- [Build Tool Upgrades](features/opensearch/build-tool-upgrades.md) - Gradle 9.1 and bundled JDK 25 updates
- [Concurrent Segment Search](features/opensearch/concurrent-segment-search.md) - Performance optimization by omitting MaxScoreCollector when sorting by score
- [Dependency Updates (OpenSearch Core)](features/opensearch/dependency-updates-opensearch-core.md) - 32 dependency updates including Netty 4.2.4 for HTTP/3 readiness
- [Engine Refactoring](features/opensearch/engine-refactoring.md) - Move prepareIndex/prepareDelete to Engine class and make NoOpResult constructors public
- [JDK 25 Support](features/opensearch/jdk-25-support.md) - Painless scripting compatibility fix for JDK 25 ClassValue behavioral change
- [Lucene Integration](features/opensearch/lucene-integration.md) - Remove MultiCollectorWrapper and use Lucene's native MultiCollector API
- [Lucene Upgrade](features/opensearch/lucene-upgrade.md) - Bump Apache Lucene from 10.3.1 to 10.3.2 with MaxScoreBulkScorer bug fix
- [Maven Snapshots Publishing](features/opensearch/maven-snapshots-publishing.md) - Migrate snapshot publishing from Sonatype to S3-backed repository at ci.opensearch.org
- [Node Stats Bugfixes](features/opensearch/node-stats-bugfixes.md) - Fix negative CPU usage values in node stats on certain Linux distributions
- [S3 Repository](features/opensearch/s3-repository.md) - Add LEGACY_MD5_CHECKSUM_CALCULATION to opensearch.yml settings for S3-compatible storage
- [Security Kerberos Integration](features/opensearch/security-kerberos-integration.md) - Update Hadoop to 3.4.2 and enable Kerberos integration tests for JDK-24+
- [Settings Bugfixes](features/opensearch/settings-bugfixes.md) - Fix duplicate registration of dynamic settings and patch version build issues
- [Stats Builder Pattern Deprecations](features/opensearch/stats-builder-pattern-deprecations.md) - Deprecated constructors in 30+ Stats classes in favor of Builder pattern
- [Terms Query Optimization](features/opensearch/terms-query-optimization.md) - Pack terms once for keyword fields with index and docValues enabled
- [XContent Filtering](features/opensearch/xcontent-filtering.md) - Case-insensitive filtering support for XContentMapValues.filter
- [Plugin Dependencies](features/opensearch/plugin-dependencies.md) - Range semver support for dependencies in plugin-descriptor.properties
- [ActionPlugin Enhancements](features/opensearch/actionplugin-enhancements.md) - Pass REST header registry to getRestHandlerWrapper for efficient header access
- [WildcardFieldMapper](features/opensearch/wildcardfieldmapper.md) - Change doc_values default to true for nested query support

### Security

- [Security AccessController Migration](features/security/security-accesscontroller-migration.md) - Migrate from deprecated java.security.AccessController to org.opensearch.secure_sm.AccessController

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

### OpenSearch

- [Java Agent](features/opensearch/java-agent.md) - Fix JRT protocol URL filtering to allow MCP server connections
- [Bulk Request Bugfixes](features/opensearch/bulk-request-bugfixes.md) - Fix indices property initialization during BulkRequest deserialization
- [Cluster State & Allocation Bugfixes](features/opensearch/cluster-state-allocation-bugfixes.md) - Fix concurrent modification in allocation filters and version compatibility in remote state
- [Data Stream & Index Template Bugfixes](features/opensearch/data-stream-index-template-bugfixes.md) - Fix deletion of unused index templates matching data streams with lower priority
- [GRPC Transport Bugfixes](features/opensearch/grpc-transport-bugfixes.md) - Fix ClassCastException for large requests, Bulk API fixes, and node bootstrap with streaming transport
- [Pull-based Ingestion Bugfixes](features/opensearch/pull-based-ingestion-bugfixes.md) - Fix out-of-bounds offset handling and remove persisted pointers for at-least-once guarantees
- [Query Bugfixes](features/opensearch/query-bugfixes.md) - Fix crashes in wildcard queries, aggregations, highlighters, and script score queries
- [Reactor Netty Transport](features/opensearch/reactor-netty-transport.md) - Fix HTTP channel tracking and release during node shutdown
- [Shard Allocation](features/opensearch/shard-allocation.md) - Fix WeightFunction constraint reset when updating balance factors
- [Shard & Segment Bugfixes](features/opensearch/shard-segment-bugfixes.md) - Fix merged segment warmer exceptions, ClusterService state assertion, and EngineConfig builder
- [Snapshot & Restore Bugfixes](features/opensearch/snapshot-restore-bugfixes.md) - Fix NullPointerException when restoring remote snapshot with missing shard size information

### OpenSearch Dashboards

- [Dashboards Console](features/opensearch-dashboards/dashboards-console.md) - Fix for console_polling setting update
- [Dashboards Navigation](features/opensearch-dashboards/dashboards-navigation.md) - Fix disabled prop propagation for navigation links
