# OpenSearch v3.1.0 Release

## Features

### OpenSearch

- [Dependency Bumps](features/opensearch/dependency-bumps.md) - 21 dependency updates including CVE-2025-27820 fix, Netty, Gson, Azure SDK updates
- [DocRequest Refactoring](features/opensearch/docrequest-refactoring.md) - Generic interface for single-document operations
- [FIPS Support](features/opensearch/fips-support.md) - Update FipsMode check for improved BC-FIPS compatibility
- [Lucene Upgrade](features/opensearch/lucene-upgrade.md) - Upgrade Apache Lucene from 10.1.0 to 10.2.1
- [Network Configuration](features/opensearch/network-configuration.md) - Fix systemd seccomp filter for network.host: 0.0.0.0
- [Percentiles Aggregation](features/opensearch/percentiles-aggregation.md) - Switch to MergingDigest for up to 30x performance improvement
- [Plugin Installation](features/opensearch/plugin-installation.md) - Fix native plugin installation error caused by PGP public key change
- [Query Bug Fixes](features/opensearch/query-bug-fixes.md) - Fixes for exists query, error handling, field validation, and IP field terms query
- [Snapshot/Repository Fixes](features/opensearch/repository-fixes.md) - Fix infinite loop during concurrent snapshot/repository update and NPE for legacy snapshots
