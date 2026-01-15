---
tags:
  - query-insights
---
# Query Insights Plugin Setup

## Summary

OpenSearch v2.16.0 marks the initial release of the Query Insights plugin as a standalone repository. This release includes the bootstrap of the plugin repository, CI/CD infrastructure setup, and several bug fixes to ensure proper build and integration with OpenSearch.

## Details

### What's New in v2.16.0

The Query Insights plugin was extracted from OpenSearch core and established as an independent plugin repository. Key changes include:

1. **Repository Bootstrap**: Initial setup of the query-insights plugin repository with maintainers and project structure
2. **Query Categorization Migration**: Moved query categorization functionality from OpenSearch core to the plugin, reducing search path overhead
3. **CI/CD Fixes**: Fixed Linux CI build failures caused by GitHub Actions runner upgrade to Node 20
4. **Build Compatibility**: Fixed build errors in NodeRequest class for 2.x branch compatibility
5. **Versioning Fix**: Corrected query insights zip file versioning for proper artifact naming

### Technical Changes

#### Query Categorization Migration

The query categorization changes were moved from OpenSearch core to the Query Insights plugin:

- Removed `SearchQueryCategorizer`, `SearchQueryCategorizingVisitor`, `SearchQueryCounters`, `SearchQueryAggregationCategorizer`, and `QueryShapeVisitor` classes from core
- Removed `search.query.metrics.enabled` cluster setting from core
- Query metrics now configured through plugin settings with OpenTelemetry integration
- Counter increments now occur after request completion rather than on the search path

#### Build System Updates

- Fixed NodeRequest class to use `BaseNodeRequest` (deprecated) for 2.x compatibility instead of `TransportRequest` used in 3.0
- Added correct version variable setup in build script for proper zip file naming
- Updated GitHub Actions workflow for Node 20 compatibility

## Limitations

- This is the initial plugin release; some features are still being developed
- Query categorization requires the plugin to be installed separately

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#2](https://github.com/opensearch-project/query-insights/pull/2) | Bootstrap query insights plugin repo with maintainers | - |
| [#15](https://github.com/opensearch-project/query-insights/pull/15) | Fix linux CI build failure when upgrade Actions runner to Node 20 | - |
| [#16](https://github.com/opensearch-project/query-insights/pull/16) | Move query categorization changes to plugin | [#14527](https://github.com/opensearch-project/OpenSearch/issues/14527) |
| [#18](https://github.com/opensearch-project/query-insights/pull/18) | Fix build error in NodeRequest class for 2.x | - |
| [#34](https://github.com/opensearch-project/query-insights/pull/34) | Fix query insights zip versioning | [#33](https://github.com/opensearch-project/query-insights/issues/33) |
