---
tags:
  - dashboards
  - search
---

# Search Comparison Card for Search Use Case Overview

## Summary

This release adds a "Compare queries" card to the Search use case overview page in OpenSearch Dashboards. The card provides quick access to the Compare Search Results tool, enabling users to easily navigate to the search comparison functionality from the workspace overview.

## Details

### What's New in v2.17.0

The dashboards-search-relevance plugin now integrates with the Content Management plugin to register a service card on the Search use case overview page. This card appears when workspaces are enabled and provides a direct link to the Compare Search Results tool.

### Technical Changes

#### New Components

| Component | Description |
|-----------|-------------|
| `compare_query_card.tsx` | React component that registers the Compare Queries card with Content Management |
| `icon.svg` | Custom SVG icon for the Compare Queries card |

#### Plugin Integration

The plugin now declares `contentManagement` as an optional dependency in `opensearch_dashboards.json`:

```json
{
  "optionalPlugins": ["dataSource", "dataSourceManagement", "contentManagement"]
}
```

During the plugin start phase, if the Content Management plugin is available, the Compare Queries card is registered:

```typescript
public start(
  core: CoreStart,
  { dataSource, contentManagement }: SearchRelevanceStartDependencies
): SearchRelevancePluginStart {
  if (contentManagement) {
    registerCompareQueryCard(contentManagement, core);
  }
  return {};
}
```

#### Card Configuration

The card is registered with the following properties:

| Property | Value |
|----------|-------|
| Target Area | `search_overview/config_evaluate_search` |
| Order | 20 |
| Layout | horizontal |

### Usage Example

When users navigate to a Search workspace overview page, they will see the "Compare queries" card with:

- A custom icon representing search comparison
- Title: "Compare queries"
- Description: "The search comparison tool lets you compare the results of two different DSL queries applied to the same user query."
- A "Compare search results" button that navigates to the Search Relevance plugin

## Limitations

- The card only appears when the Content Management plugin is available
- Requires workspace feature to be enabled to see the Search use case overview page

## References

### Documentation
- [Documentation](https://docs.opensearch.org/2.17/search-plugins/search-relevance/compare-search-results/): Comparing search results

### Pull Requests
| PR | Description |
|----|-------------|
| [#427](https://github.com/opensearch-project/dashboards-search-relevance/pull/427) | Add compare queries card to search use case overview page |

### Issues (Design / RFC)
- [Issue #7807](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7807): Search use case overview page

## Related Feature Report

- [Full feature documentation](../../../../features/dashboards-search-relevance/dashboards-search-relevance-search-comparison.md)
