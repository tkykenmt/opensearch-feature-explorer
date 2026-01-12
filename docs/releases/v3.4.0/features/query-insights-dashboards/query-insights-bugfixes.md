# Query Insights Bugfixes

## Summary

This release includes multiple bug fixes for the Query Insights plugin and dashboards, addressing issues with internal index filtering, Multi-Data Source (MDS) support for Workload Management routes, UI navigation improvements, and Jest test infrastructure fixes.

## Details

### What's New in v3.4.0

This release focuses on stability and infrastructure improvements across both the backend plugin and dashboards.

### Technical Changes

#### Backend: Exclude Internal `top_queries-*` Indices

The Query Insights plugin now properly excludes internal `top_queries-*` indices from resource tracking. Previously, when querying the Top N Queries API without time range parameters, internal indices could appear in results, causing confusion.

**Problem**: The `checkIfInternal` predicate was only applied when using `from` and `to` time range parameters, but not when querying without parameters.

**Solution**: Moved the internal index filtering logic to `QueryInsightsListener.skipSearchRequest()` method, which now checks if all search indices match the `top_queries-*` pattern and skips tracking for such requests.

```java
// New filtering logic in QueryInsightsListener
String[] searchIndices = searchRequestContext.getRequest().indices();
if (searchIndices != null
    && searchIndices.length > 0
    && Arrays.stream(searchIndices).allMatch(
        index -> index.contains(QueryInsightsSettings.TOP_QUERIES_INDEX_PREFIX))) {
    return true; // Skip tracking
}
```

#### Dashboards: MDS Support for Workload Management Routes

Fixed Multi-Data Source (MDS) support in the server-side WLM routes. The routes now properly accept and use `dataSourceId` query parameter to route requests to the correct data source.

**Changes**:
- Added `WlmPlugin` custom client for WLM API calls
- Updated all WLM routes to accept `dataSourceId` query parameter
- Routes now use data source client when `dataSourceEnabled` and `dataSourceId` is provided
- Added comprehensive test coverage for both MDS-enabled and disabled scenarios

**Affected Routes**:
| Route | Description |
|-------|-------------|
| `GET /api/_wlm/stats` | WLM stats across all nodes |
| `GET /api/_wlm/{nodeId}/stats` | WLM stats for specific node |
| `GET /api/_wlm/workload_group` | List workload groups |
| `GET /api/_wlm/workload_group/{name}` | Get specific workload group |
| `PUT /api/_wlm/workload_group` | Create workload group |
| `PUT /api/_wlm/workload_group/{name}` | Update workload group |
| `DELETE /api/_wlm/workload_group/{name}` | Delete workload group |
| `GET /api/_wlm/stats/{workloadGroupId}` | Stats for specific workload group |
| `PUT /api/_rules/workload_group` | Create index rule |
| `GET /api/_rules/workload_group` | List index rules |
| `DELETE /api/_rules/workload_group/{ruleId}` | Delete index rule |
| `PUT /api/_rules/workload_group/{ruleId}` | Update index rule |
| `GET /api/_wlm/thresholds` | Get CPU/memory rejection thresholds |

#### Dashboards: Remove "Open in Search Comparison" Button

Removed the "Open in search comparison" button from Query Details and Query Group Details pages. The button was routing to OpenSearch Playground instead of the intended Search Relevance experience.

**Affected Components**:
- `QueryDetails.tsx`
- `QueryGroupDetails.tsx`

#### Dashboards: Jest Test Infrastructure Fix

Fixed Jest test failures caused by Monaco editor ES module imports. The Monaco editor package uses ES modules which Jest cannot parse by default.

**Solution**:
- Added mock for `monaco-editor` in `test/mocks/monaco-editor.ts`
- Updated `jest.config.js` with module name mappings for Monaco-related imports
- Added `transformIgnorePatterns` to handle Monaco editor transformation

```javascript
// jest.config.js additions
moduleNameMapper: {
  '^monaco-editor/esm/vs/editor/editor.api$': '<rootDir>/test/mocks/monaco-editor.ts',
  '^monaco-editor$': '<rootDir>/test/mocks/monaco-editor.ts',
  '^@osd/monaco$': '<rootDir>/test/mocks/monaco-editor.ts',
},
transformIgnorePatterns: ['node_modules/(?!(monaco-editor)/)'],
```

### Migration Notes

No migration required. These are bug fixes with no breaking changes.

## Limitations

- The internal index exclusion only applies to requests where all indices match the `top_queries-*` pattern. Mixed queries (internal + user indices) are still tracked.

## References

### Documentation
- [Query Insights Documentation](https://docs.opensearch.org/3.0/observing-your-data/query-insights/index/)

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#481](https://github.com/opensearch-project/query-insights/pull/481) | query-insights | Exclude internal `top_queries-*` indices from tracking |
| [#411](https://github.com/opensearch-project/query-insights-dashboards/pull/411) | query-insights-dashboards | Fix MDS support in server/wlmRoutes |
| [#396](https://github.com/opensearch-project/query-insights-dashboards/pull/396) | query-insights-dashboards | Remove "Open in search comparison" button |
| [#435](https://github.com/opensearch-project/query-insights-dashboards/pull/435) | query-insights-dashboards | Fix Jest test failures due to Monaco editor imports |

### Issues (Design / RFC)
- [Issue #477](https://github.com/opensearch-project/query-insights/issues/477): `top_queries-*` indices not filtered when not using from & to parameters

## Related Feature Report

- [Full feature documentation](../../../../features/query-insights/query-insights.md)
