---
tags:
  - opensearch-dashboards
---
# Explore Plugin

## Summary

OpenSearch Dashboards v3.6.0 delivers significant performance improvements, a major charting library migration, and numerous bug fixes for the Explore plugin. Key changes include migrating histogram charts from elastic-charts to ECharts, moving raw search results out of Redux into a module-level cache to eliminate UI jank, optimizing initial page load by reducing redundant saved object requests by 60-80%, and fixing cross-flavor navigation state isolation between Logs, Traces, and Metrics.

## Details

### What's New in v3.6.0

#### Performance Optimizations

- **Redux results cache refactor** (PR #11478): Raw search hits (up to 10,000 documents) are moved out of Redux into a module-level `Map` cache. Redux now stores only lightweight `ResultMetadata` (total, elapsedMs, fieldSchema, hasResults) as a reactivity signal. A custom cache middleware intercepts `setResults` actions and writes full results to the cache before `next(action)`, ensuring components always read fresh data on re-render. This eliminates Immer's recursive `Object.freeze()` overhead that was causing UI jank on large result sets.

- **Initial page load optimization** (PR #11413): Added `DataViewsService.getMultiple()` for bulk fetching DataViews in a single HTTP request. Enhanced `SavedObjectsClient` batch queue deduplication within a 100ms window. Removed redundant DataView fetches from Redux persistence (reads `signalType` from Dataset object instead) and `DatasetSelectWidget`.

#### Charting Library Migration

- **Histogram migration to ECharts** (PR #11341): Migrated Explore Logs and Traces histogram charts from elastic-charts to ECharts. Introduced `echarts_histogram_utils.ts` with smart date formatting, timezone handling, tooltip formatting with partial data warnings, brush selection for time range filtering, and theme-aware styling.

- **Vega cleanup** (PR #11468): Removed all Vega-based visualization implementations from Explore. All Discover visualizations now use ECharts exclusively.

#### UI Enhancements

- **Metric visualization improvements** (PR #11452): Added "Split chart by" support for rendering multiple metrics. Refactored metric chart rendering to use ECharts + HTML/CSS combination with gradient/solid background modes and horizontal/vertical/auto layout options.

- **Discover layout density** (PR #11518): Merged the action bar into the tabs row, compacted the hits counter text format (`19 / 4,186 hits · 105 ms`), added separator between histogram and tabs, and reduced histogram paddings.

- **Patterns table improvements** (PR #11356): Added filter-for and filter-out actions, merged action icons into a single "Actions" column, formatted flyout timestamps using user's `dateFormat` setting, fixed "Update search" query to use raw query string, added PPL string escaping for pattern strings.

- **Cell text wrapping toggle** (PR #11321): Added a toggle button on the Explore data table to control cell text wrapping.

#### Bug Fixes

- **Cross-flavor navigation** (PR #11521): Fixed state bleeding between Logs, Traces, and Metrics flavors. Queries, datasets, and UI settings are now properly isolated per flavor. Also fixed RED metrics queries not executing on the Traces page.

- **Blank Discover page** (PR #11347): Fixed critical UI rendering issue when saved queries contain object-type query values (affects OSD 3.1.0 and 2.19). Added type guards and error handling.

- **Stacked bar and bar size** (PR #11460): Fixed gauge `useThresholdColor` not working, stack mode in bar charts not rendering, and removed incompatible bar gap option. Bar width UI now displays 1-100 range.

- **Histogram missing bucket** (PR #11298): Fixed histogram x-axis missing buckets by refactoring x-axis type from `category` to `number`, using `custom` series instead of `bar`.

- **Bar chart rule** (PR #11482): Fixed incorrect auto-visualization rule that made bar chart available for single metric data.

- **Visualization container height** (PR #11419): Fixed visualization container height growing when the config panel accordion expands.

- **Facet single group error** (PR #11633): Fixed error when `facetTransform` results in only a single facet group, where `createFacetLineSeries` assumed multi-facet data shape.

- **Switch styling** (PR #11409): Fixed inconsistent switch styling in the Explore visualization control panel.

## Limitations

- The ECharts migration removes Vega-based visualizations entirely; any custom Vega configurations in Explore are no longer supported
- The results cache is module-level (not persisted); browser back/forward clears the cache via `hydrateState`/`resetState`

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#11478](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11478) | Move raw hits into module-level cache to reduce Redux freeze overhead |  |
| [#11413](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11413) | Optimize initial page load by reducing redundant saved object requests |  |
| [#11341](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11341) | Migrate histogram charts from elastic-charts to ECharts |  |
| [#11468](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11468) | Clean up all Vega implementations from Explore visualizations |  |
| [#11452](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11452) | Metric visualization with split chart support and ECharts refactoring |  |
| [#11518](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11518) | Discover styles and density improvements | [#11516](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/11516) |
| [#11356](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11356) | Patterns table UI with filter actions and timestamp formatting | [#6080](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6080) |
| [#11321](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11321) | Data table cell text wrapping toggle |  |
| [#11521](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11521) | Cross-flavor navigation and state isolation fix |  |
| [#11347](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11347) | Fix blank Discover page for saved queries with object-type values | [#10883](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/10883) |
| [#11460](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11460) | Fix stacked bar display and incompatible bar size options |  |
| [#11298](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11298) | Fix histogram missing bucket by refactoring x-axis type |  |
| [#11482](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11482) | Fix bar chart incorrectly available for single metric data |  |
| [#11419](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11419) | Fix visualization container height growing with config panel |  |
| [#11633](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11633) | Fix error when faceting data into one group |  |
| [#11409](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11409) | Fix switch styling consistency in visualization control panel |  |
