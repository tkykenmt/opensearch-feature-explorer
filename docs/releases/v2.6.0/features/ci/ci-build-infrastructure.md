---
tags:
  - ci
---
# CI/Build Infrastructure

## Summary

OpenSearch 2.6.0 includes 8 bug fixes for CI/Build Infrastructure.

## Details

### Bug Fixes

- Added maven-publish.yml to decouple publishing of snapshots to Maven via Github Actions
- Fix Node.js and Yarn installation in CI
- Fix Node.js and Yarn installation in CI
- Bump version to 2.6.0
- Updating CODEOWNERS as per issue by @macohen in https://github.com/opensearch-project/dashboards-search-relevance/pull/148
- Fix detection of Chrome's version on Darwin during CI
- [BWC Tests] Add BWC tests for `2.6.0`
- Prevent primitive linting limitations from being applied to unit tests found under `src/setup_node_env`

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#320](https://github.com/opensearch-project/job/pull/320) | Added maven-publish.yml to decouple publishing of snapshots to Maven via Github Actions | job |
| [#166](https://github.com/opensearch-project/dashboards-maps/pull/166) | Fix Node.js and Yarn installation in CI | dashboards-maps |
| [#46](https://github.com/opensearch-project/dashboards-query-workbench/pull/46) | Fix Node.js and Yarn installation in CI | dashboards-query-workbench |
| [#160](https://github.com/opensearch-project/dashboards-maps/pull/160) | Bump version to 2.6.0 | dashboards-maps |
| [#146](https://github.com/opensearch-project/dashboards-maps/pull/146) | Updating CODEOWNERS as per issue by @macohen in https://github.com/opensearch-project/dashboards-search-relevance/pull/148 | dashboards-maps |
| [#3296](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/3296) | Fix detection of Chrome's version on Darwin during CI | OpenSearch-Dashboards |
| [#3356](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/3356) | [BWC Tests] Add BWC tests for `2.6.0` | OpenSearch-Dashboards |
| [#3403](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/3403) | Prevent primitive linting limitations from being applied to unit tests found under `src/setup_node_env` | OpenSearch-Dashboards |
