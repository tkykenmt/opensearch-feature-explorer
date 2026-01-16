---
tags:
  - query-insights
---
# Query Insights Plugin Setup

## Summary

OpenSearch v2.16.0 marks the initial release of the Query Insights plugin as a standalone repository. This release includes the bootstrap of the plugin repository, comprehensive CI/CD infrastructure setup, build system configuration, and several bug fixes to ensure proper build and integration with OpenSearch.

## Details

### What's New in v2.16.0

The Query Insights plugin was extracted from OpenSearch core and established as an independent plugin repository. Key changes include:

1. **Repository Bootstrap**: Initial setup of the query-insights plugin repository with maintainers and project structure
2. **Query Categorization Migration**: Moved query categorization functionality from OpenSearch core to the plugin, reducing search path overhead
3. **CI/CD Infrastructure**: Complete CI/CD pipeline setup including Gradle configuration, GitHub Actions workflows, and build scripts
4. **Security Scanning**: Configured Mend (WhiteSource) for automated security vulnerability scanning
5. **Build System**: Added build scripts for artifact generation and Maven publish workflow for dependency distribution
6. **Code Quality**: Added code hygiene checks including Spotless and Checkstyle for consistent code formatting
7. **Backport Support**: Added GitHub Actions for automated backporting to release branches
8. **Documentation**: Updated README with user guide

### Technical Changes

#### Query Categorization Migration

The query categorization changes were moved from OpenSearch core to the Query Insights plugin:

- Removed `SearchQueryCategorizer`, `SearchQueryCategorizingVisitor`, `SearchQueryCounters`, `SearchQueryAggregationCategorizer`, and `QueryShapeVisitor` classes from core
- Removed `search.query.metrics.enabled` cluster setting from core
- Query metrics now configured through plugin settings with OpenTelemetry integration
- Counter increments now occur after request completion rather than on the search path

#### Build System Updates

- Added build script (`scripts/build.sh`) for artifact generation following opensearch-build onboarding guide
- Fixed NodeRequest class to use `BaseNodeRequest` (deprecated) for 2.x compatibility instead of `TransportRequest` used in 3.0
- Added correct version variable setup in build script for proper zip file naming
- Updated GitHub Actions workflow for Node 20 compatibility
- Added Maven publish workflow for snapshot and release publishing

#### Code Quality Infrastructure

- Added Spotless plugin for automatic code formatting
- Added Checkstyle for code style enforcement
- Configured code hygiene checks in CI pipeline

## Limitations

- This is the initial plugin release; some features are still being developed
- Query categorization requires the plugin to be installed separately

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1](https://github.com/opensearch-project/query-insights/pull/1) | Configure Mend for GitHub.com (security scanning) | - |
| [#2](https://github.com/opensearch-project/query-insights/pull/2) | Bootstrap query insights plugin repo with maintainers | - |
| [#14](https://github.com/opensearch-project/query-insights/pull/14) | Add build script to query insights plugin | - |
| [#15](https://github.com/opensearch-project/query-insights/pull/15) | Fix linux CI build failure when upgrade Actions runner to Node 20 | - |
| [#16](https://github.com/opensearch-project/query-insights/pull/16) | Move query categorization changes to plugin | [#14527](https://github.com/opensearch-project/OpenSearch/issues/14527) |
| [#17](https://github.com/opensearch-project/query-insights/pull/17) | Add backport GitHub actions | [#7](https://github.com/opensearch-project/query-insights/issues/7) |
| [#18](https://github.com/opensearch-project/query-insights/pull/18) | Fix build error in NodeRequest class for 2.x | - |
| [#24](https://github.com/opensearch-project/query-insights/pull/24) | Add maven publish workflow | - |
| [#34](https://github.com/opensearch-project/query-insights/pull/34) | Fix query insights zip versioning | [#33](https://github.com/opensearch-project/query-insights/issues/33) |
| [#51](https://github.com/opensearch-project/query-insights/pull/51) | Add code hygiene checks (Spotless, Checkstyle) | [#7](https://github.com/opensearch-project/query-insights/issues/7) |
| [#52](https://github.com/opensearch-project/query-insights/pull/52) | Added 2.16 release notes | [#32](https://github.com/opensearch-project/query-insights/issues/32) |
