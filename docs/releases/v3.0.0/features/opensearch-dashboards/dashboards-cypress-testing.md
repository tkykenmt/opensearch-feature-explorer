---
tags:
  - domain/core
  - component/dashboards
  - dashboards
  - search
---
# Dashboards Cypress Testing

## Summary

OpenSearch Dashboards v3.0.0 includes significant improvements to Cypress end-to-end testing coverage. This release adds 18 PRs focused on expanding test coverage for Discover 2.0 features, fixing flaky tests, and improving test infrastructure reliability.

## Details

### What's New in v3.0.0

This release introduces comprehensive Cypress test coverage for key Dashboards functionality:

- **Discover Page Testing**: New tests for sidebar functionality, top values, field filtering by type, and table canvas
- **Dashboard Integration**: Tests for saved searches in dashboards
- **Inspect Functionality**: Integration tests for inspect feature in Discover and Dashboards pages
- **Query Features**: Tests for recent queries, query editor display, and auto query updates on dataset switch
- **Test Reliability**: Fixes for flaky tests, retry mechanisms, and improved test data handling

### Technical Changes

#### New Test Suites

| Test Suite | Description | PR |
|------------|-------------|----|
| Sidebar Tests | Top values, field filtering by type | [#9386](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9386) |
| Saved Search Tests | Saved searches in dashboards | [#9288](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9288) |
| Inspect Tests | Inspect functionality for Discover/Dashboards | [#9292](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9292), [#9331](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9331) |
| Histogram Tests | Histogram interaction tests | [#9290](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9290) |
| Recent Queries Tests | All recent queries functionality | [#9307](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9307) |
| Table Canvas Tests | Table canvas in discover | [#9285](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9285) |
| Query Editor Tests | Query editor display | [#9398](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9398) |
| Dataset Switch Tests | Auto query updates on dataset switch | [#9322](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9322) |

#### Test Infrastructure Improvements

| Improvement | Description | PR |
|-------------|-------------|----|
| Flaky Test Fixes | General flakiness fixes | [#9433](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9433) |
| Retry Mechanism | Retry for flaky share menu test | [#9352](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9352) |
| Test Data Updates | Random IDs, missing value fields, unique fields | [#9321](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9321) |
| Performance | Use before/after hooks to speed up tests | [#9439](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9439) |
| Cleanup | Remove unnecessary reload in saved_search test | [#9396](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9396) |
| S3 Integration | Clear session storage in S3 integ test | [#9490](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9490) |
| Re-enabled Tests | Re-enable saved search cypress tests | [#9628](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9628) |

### Usage Example

Run Cypress tests with:

```bash
# Open Cypress test runner
yarn run cypress open

# Run specific test spec
yarn run cypress run --spec "cypress/integration/discover/sidebar.spec.js"
```

## Limitations

- Some tests may require specific test data setup
- Tests are designed for Discover 2.0 features and may not cover legacy Discover

## References

### Pull Requests
| PR | Description |
|----|-------------|
| [#9154](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9154) | Refactor TESTID-140 sidebar spec and clean up |
| [#9285](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9285) | Add tests for table canvas in discover |
| [#9288](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9288) | Add tests for saved searches in dashboards |
| [#9290](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9290) | Add histogram interaction tests |
| [#9292](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9292) | Add inspect functionality tests |
| [#9307](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9307) | Add all recent queries tests |
| [#9314](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9314) | Test sort in language_specific_display |
| [#9321](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9321) | Update cypress data |
| [#9322](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9322) | Add cypress test for auto query updates |
| [#9331](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9331) | Add inspect functionality tests |
| [#9352](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9352) | Add retry mechanism for flaky share menu test |
| [#9386](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9386) | Add Top Values and Filter Sidebar Fields testing |
| [#9396](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9396) | Remove unnecessary reload in saved_search test |
| [#9398](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9398) | Add tests for query editor display |
| [#9433](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9433) | Fix flakiness in cypress tests |
| [#9439](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9439) | Use before/after to speed up test |
| [#9490](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9490) | Clear session storage in S3 integ test |
| [#9628](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9628) | Reenable saved search cypress tests |

### Issues (Design / RFC)
- [Issue #8946](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/8946): TESTID-140 Sidebar testing
- [Issue #8954](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/8954): Sharing spec testing
- [Issue #8955](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/8955): Inspect functionality testing
- [Issue #8959](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/8959): Saved searches testing

## Related Feature Report

- Full feature documentation
