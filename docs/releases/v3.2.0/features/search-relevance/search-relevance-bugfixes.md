---
tags:
  - dashboards
  - search
---

# Search Relevance Bugfixes

## Summary

This release includes 7 bug fixes across the Search Relevance Workbench components (both dashboards-search-relevance and search-relevance repositories). The fixes improve error handling, UI stability, and input validation for the experimental Search Relevance Workbench feature.

## Details

### What's New in v3.2.0

This release focuses on improving the user experience and stability of the Search Relevance Workbench through targeted bug fixes in both the frontend (dashboards-search-relevance) and backend (search-relevance) components.

### Bug Fixes

#### Dashboards Search Relevance (Frontend)

| PR | Fix | Description |
|----|-----|-------------|
| [#578](https://github.com/opensearch-project/dashboards-search-relevance/pull/578) | Backend plugin disabled messaging | Improved error messaging when the backend plugin is not enabled, helping users identify configuration issues |
| [#582](https://github.com/opensearch-project/dashboards-search-relevance/pull/582) | Pipeline error suppression | Suppress false 404 errors when no pipelines exist yet (OpenSearch returns 404 for empty pipeline searches) |
| [#585](https://github.com/opensearch-project/dashboards-search-relevance/pull/585) | Validation results overflow | Fix horizontal overflow in the validation results table during Search Configuration creation |
| [#586](https://github.com/opensearch-project/dashboards-search-relevance/pull/586) | Venn diagram statistics | Fix incorrect unique result counts in the eyeballing tool's Venn diagram when switching between queries |

#### Search Relevance (Backend)

| PR | Fix | Description |
|----|-----|-------------|
| [#176](https://github.com/opensearch-project/search-relevance/pull/176) | REST API error status | Return proper 4xx status codes instead of 500 for validation errors (e.g., duplicate search configurations in PAIRWISE_COMPARISON) |
| [#177](https://github.com/opensearch-project/search-relevance/pull/177) | Input validation | Add text validation for queryText and referenceAnswer fields with character limits (name: 50, description: 250, queryText/referenceAnswer: 2000) |
| [#187](https://github.com/opensearch-project/search-relevance/pull/187) | Pipeline parameter fix | Fix missing pipeline name in pointwise experiments when using hybrid queries with search configurations |

### Technical Changes

#### Frontend Fixes

The Venn diagram fix (#586) addresses a React state synchronization issue where `result1`, `result2`, and `statistics` were updated in separate `useEffect` blocks, causing stale data to be displayed during query transitions. The fix consolidates these updates into a single effect.

#### Backend Fixes

The REST API error status fix (#176) ensures proper HTTP status codes are returned:
- `BAD_REQUEST (400)` for validation errors like duplicate search configurations
- Previously returned `INTERNAL_SERVER_ERROR (500)` for these cases

Input validation (#177) adds JSON parsing validation and length checks:
```java
// Validation limits
name: max 50 characters
description: max 250 characters  
queryText: max 2000 characters
referenceAnswer: max 2000 characters
```

## Limitations

- These fixes are part of the experimental Search Relevance Workbench feature
- Backend plugin must be enabled via cluster settings for full functionality

## References

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#578](https://github.com/opensearch-project/dashboards-search-relevance/pull/578) | dashboards-search-relevance | Improve messaging when backend plugin is disabled |
| [#582](https://github.com/opensearch-project/dashboards-search-relevance/pull/582) | dashboards-search-relevance | Do not show Pipeline error if there are no pipelines yet |
| [#585](https://github.com/opensearch-project/dashboards-search-relevance/pull/585) | dashboards-search-relevance | Avoid validation results overflow in Search Configuration creation |
| [#586](https://github.com/opensearch-project/dashboards-search-relevance/pull/586) | dashboards-search-relevance | Fix wrong unique number of results in Venn diagram |
| [#176](https://github.com/opensearch-project/search-relevance/pull/176) | search-relevance | Bug fix on REST APIs error status for creations |
| [#177](https://github.com/opensearch-project/search-relevance/pull/177) | search-relevance | Added queryText and referenceAnswer text validation from manual input |
| [#187](https://github.com/opensearch-project/search-relevance/pull/187) | search-relevance | Fixed pipeline parameter being ignored in pairwise metrics processing for hybrid |

### Issues (Design / RFC)
- [Issue #543](https://github.com/opensearch-project/dashboards-search-relevance/issues/543): Backend plugin disabled messaging
- [Issue #557](https://github.com/opensearch-project/dashboards-search-relevance/issues/557): Pipeline error when no pipelines exist
- [Issue #584](https://github.com/opensearch-project/dashboards-search-relevance/issues/584): Validation results overflow
- [Issue #529](https://github.com/opensearch-project/dashboards-search-relevance/issues/529): Venn diagram incorrect counts
- [Issue #186](https://github.com/opensearch-project/search-relevance/issues/186): Input validation for query sets
- [Issue #170](https://github.com/opensearch-project/search-relevance/issues/170): Missing pipeline name in experiments
- [OpenSearch Issue #15917](https://github.com/opensearch-project/OpenSearch/issues/15917): 404 when searching for pipelines when none exist

## Related Feature Report

- [Search Relevance Workbench](../../../features/search-relevance/search-relevance-workbench.md)
