# OpenSearch v3.1.0 Release

## Features

### OpenSearch

- [Approximation Framework](features/opensearch/approximation-framework.md) - BKD traversal optimization for skewed datasets with DFS strategy
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
