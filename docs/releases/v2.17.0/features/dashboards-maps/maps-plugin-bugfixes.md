---
tags:
  - dashboards
---

# Maps Plugin Bugfixes

## Summary

This release includes two bugfixes for the OpenSearch Dashboards Maps plugin: deprecation of multi-data source display in the UI and migration of integration tests to the centralized functional test repository.

## Details

### What's New in v2.17.0

#### 1. Deprecated Multi-Data Source Display

The multi-data source display feature in Maps has been deprecated when `data_source` is enabled. This change aligns with the Trineo Maps UX design and simplifies the user interface.

**Changes:**
- Removed `dataSource` and `dataSourceManagement` from optional plugins
- Removed data source reference tracking from layer management
- Simplified the top navigation menu by removing data source aggregated view
- Removed data source menu from maps listing page

**UI Impact:**
- Before: Maps displayed a data source selector in the header when multi-data source was enabled
- After: Data source selector is no longer shown in Maps UI

#### 2. Integration Test Migration to FTR Repository

The Cypress integration tests have been migrated from the dashboards-maps repository to the centralized [opensearch-dashboards-functional-test](https://github.com/opensearch-project/opensearch-dashboards-functional-test) repository.

**Changes:**
- Removed local Cypress test files and configuration
- Added new GitHub Actions workflow `FTR E2E Dashboards Maps Test` that runs tests from the FTR repository
- Updated developer guide to reference the new test location

### Technical Changes

#### Removed Components

| Component | Description |
|-----------|-------------|
| `dataSourceManagement` | Plugin dependency for data source UI |
| `dataSourceRefIds` state | Tracking of data source references |
| `DataSourceAggregatedView` | Header component showing active data sources |

#### Removed Files (Test Migration)

| File | Description |
|------|-------------|
| `.github/workflows/cypress-workflow.yml` | Old Cypress CI workflow |
| `cypress/` directory | All local Cypress tests |
| `cypress.config.js` | Cypress configuration |

#### New Workflow

The new `remote-ftr-integ-test-workflow.yml` workflow:
- Runs on pull requests and pushes
- Downloads OpenSearch with geospatial plugin
- Bootstraps OpenSearch Dashboards with Maps plugin
- Runs Cypress tests from `opensearch-dashboards-functional-test` repository

### Migration Notes

For developers:
- Integration tests are now located in `cypress/fixtures/plugins/custom-import-map-dashboards` in the FTR repository
- Follow the [FTR Developer Guide](https://github.com/opensearch-project/opensearch-dashboards-functional-test/blob/main/DEVELOPER_GUIDE.md) to run tests locally

## Limitations

- Multi-data source display is no longer available in Maps when data source feature is enabled
- This is a UX simplification, not a removal of multi-data source support for data layers

## References

### Documentation
- [FTR PR #1540](https://github.com/opensearch-project/opensearch-dashboards-functional-test/pull/1540): Move maps integration tests to FTR repo

### Pull Requests
| PR | Description |
|----|-------------|
| [#651](https://github.com/opensearch-project/dashboards-maps/pull/651) | Deprecate maps multi data source display |
| [#664](https://github.com/opensearch-project/dashboards-maps/pull/664) | Use functional test repo to run maps integration test workflow |

### Issues (Design / RFC)
- [Issue #649](https://github.com/opensearch-project/dashboards-maps/issues/649): Support Trineo new headers change in maps
- [Issue #592](https://github.com/opensearch-project/dashboards-maps/issues/592): Cypress CI failed with Electron Renderer crash

## Related Feature Report

- [Full feature documentation](../../../../features/dashboards-maps/dashboards-maps-maps-geospatial.md)
