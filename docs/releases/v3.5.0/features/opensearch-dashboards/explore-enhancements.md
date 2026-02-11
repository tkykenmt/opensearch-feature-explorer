---
tags:
  - opensearch-dashboards
---
# Explore Enhancements

## Summary

OpenSearch Dashboards v3.5.0 brings a collection of feature additions and bug fixes to the Explore plugin, focusing on improved field statistics, AI-powered visualization context awareness, a condensed Discover page UI, better logs default columns, and multiple stability fixes for patterns tables, timechart, saved search filters, and table overflow.

## Details

### What's New in v3.5.0

#### Feature Additions

- **Rare Values in Field Stats**: The Field Statistics detail view now includes a "Rare Values" section alongside the existing "Top Values", displaying infrequent values with counts and percentage calculations for string, keyword, number, IP, and boolean field types.
- **AI Context Awareness for Visualizations**: An "Ask AI" context menu action is available on Explore visualizations. Right-clicking a visualization captures it as an image using html2canvas and opens the chat window with the image and a default message for AI-assisted analysis.
- **Condensed Discover Page UI**: The Explore Discover page layout has been redesigned for a more data-focused experience. Key changes include reduced padding/margins, single-line row layout with text truncation, CSS-based `table-layout: auto` replacing a complex JS column width algorithm (~170 lines removed), inline flexbox action buttons, and `<span>`-based source field rendering for proper truncation.
- **Logs Default Columns**: Default columns are now configured for the New Discover logs experience based on common OTel logs format fields. Users can customize default columns via UI settings under `explore`. System fields (meta fields) are removed from the source column display.

#### Bug Fixes

- **Language Placeholder Fix**: The query editor placeholder now dynamically updates with the selected query language instead of showing a static placeholder. Also respects `DatasetTypeConfig.searchOnLoad` settings.
- **Patterns Table Pagination Fix**: React memoization added to patterns components (`PatternsFlyoutContext`, `PatternsContainer`, `PatternsTable`, `PatternsFlyoutEventTable`) to prevent unnecessary re-renders that caused pagination click handlers to fail due to DOM recreation race conditions in Chrome.
- **Patterns Flyout Without Timefield**: The `PatternsTableFlyout` now renders correctly for datasets without a designated time field, displaying results with only the necessary columns.
- **Null Values in Patterns Table**: Rows with null values in the Patterns Table are now filtered out to prevent table crashes.
- **Timechart Interval Change**: The `TimechartHeader` `onIntervalChange` handler now executes both histogram and data table queries, ensuring the data table updates when the timechart interval changes.
- **URL Param Filters with Saved Search**: Filters defined in URL parameters are now preserved when loading a saved search, with saved search filters used only as a fallback when no URL params exist.
- **Logs Table Overflow**: Fixed CSS overflow issue in the new Discover logs table that caused content to extend beyond its container.

## Limitations

- The "Ask AI" context menu action requires the ag-ui chatbot feature flag to be enabled in the configuration.
- Default columns for logs are based on OTel logs format and may not match all custom log schemas.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#11062](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11062) | Add rare values to field stats detail sections |  |
| [#11134](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11134) | Add context awareness for explore visualizations |  |
| [#11221](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11221) | Create a more condensed UI for the Explore Discover page |  |
| [#11203](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11203) | Add logs default columns and remove system fields from source column |  |
| [#11018](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11018) | Fix language placeholder and searchOnLoad in explore editor |  |
| [#11069](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11069) | Memoize patterns components to fix pagination in tables |  |
| [#11057](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11057) | Update PatternsTableFlyout to render without timefield |  |
| [#11182](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11182) | Filter rows with null values in Patterns Table |  |
| [#11035](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11035) | Update timechart onIntervalChange to execute data table queries | [#11021](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/11021) |
| [#11239](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11239) | Use URL param filters with saved search as fallback | [#11234](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/11234) |
| [#11310](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11310) | Fix new discover logs table overflow |  |
