---
tags:
  - opensearch-dashboards
---
# Explore & Dataset Management

## Summary

In v3.6.0, the Explore plugin and Dataset Management plugin are now enabled in analytics (all use case) workspaces, in addition to the existing observability workspace support. A related bugfix aligns dataset index queries with index pattern wildcard behavior by removing the explicit `expand_wildcards: 'all'` parameter.

## Details

### What's New in v3.6.0

#### Explore in Analytics Workspaces

The Explore plugin previously only registered navigation links for the observability workspace. In v3.6.0, nav links are now also registered for the `all` (analytics) workspace nav group, making Explore accessible from analytics workspaces.

Key changes in `src/plugins/explore/public/plugin.ts`:
- Nav links (Explore, Logs, Traces, Metrics) are registered for both `DEFAULT_NAV_GROUPS.observability` and `DEFAULT_NAV_GROUPS.all`
- In analytics workspaces, the Explore entry appears as "Explorer" (distinct title) while retaining "Explore" in observability workspaces
- Workspace feature check now accepts both `observability` and `all` use case IDs

#### Dataset Management in Analytics Workspaces

The Dataset Management plugin previously restricted access to observability workspaces only. In v3.6.0:
- Access is now allowed in analytics workspaces (identified by `ALL_USE_CASE_ID` in workspace features)
- Nav link visibility is updated to show in both observability and analytics workspaces
- Users outside these workspace types are still redirected to the index patterns management page

#### Navigation Fixes

- Parent nav links in collapsible nav groups are now always collapsible, fixing a bug where `categoryCollapsible` incorrectly inverted the collapsible behavior
- The Explore app's nav link alias mapping was corrected from `data-explorer` to `explore`, ensuring proper active state highlighting

#### Dataset Query Wildcard Behavior Fix

The `expand_wildcards: 'all'` parameter was removed from dataset index resolution queries in both `use_index_fetcher.ts` and `index_type.ts`. Previously, dataset queries explicitly requested all index types (including hidden indices starting with `.`), which differed from index pattern behavior. The fix aligns both code paths to use the OpenSearch default (`open` indices only).

### Technical Changes

| File | Change |
|------|--------|
| `src/plugins/explore/public/plugin.ts` | Register nav links for `DEFAULT_NAV_GROUPS.all`; accept `all` use case in workspace check |
| `src/plugins/dataset_management/public/plugin.ts` | Add `ALL_USE_CASE_ID` check for workspace access and nav link visibility |
| `src/core/public/chrome/ui/header/collapsible_nav_groups.tsx` | Fix collapsible prop to always be `true` for parent nav links |
| `src/core/public/chrome/ui/header/nav_link.tsx` | Fix explore alias from `data-explorer` to `explore` |
| `src/plugins/data/public/query/query_string/dataset_service/lib/index_data_structure_creator/use_index_fetcher.ts` | Remove `expand_wildcards: 'all'` from index resolution query |
| `src/plugins/data/public/query/query_string/dataset_service/lib/index_type.ts` | Remove `expand_wildcards: 'all'` from `fetchIndices` query |

## Limitations

- The Explore plugin remains experimental; APIs and behavior may change
- The "Explorer" title in analytics workspaces differs from "Explore" in observability workspaces, which may cause user confusion

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#11444](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11444) | Enable Explore and dataset management plugins in analytics workspaces |  |
| [#11571](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11571) | Update dataset query to match index pattern wildcard behavior |  |
