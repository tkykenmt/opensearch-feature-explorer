---
tags:
  - opensearch-dashboards
---
# Discover Fixes

## Summary

Bug fixes for the Discover Next (Discover 2.0) feature in OpenSearch Dashboards v2.16.0, addressing styling issues and database loading display problems when query enhancements are enabled.

## Details

### What's New in v2.16.0

Two bug fixes were introduced to improve the Discover Next experience:

1. **Styling Fixes** - Corrected styling issues in the Discover 2.0 page when the query enhancements toggle is enabled, including:
   - Query bar styling improvements
   - Dataset navigator styling updates with database icon and tooltip
   - Language selector with arrow down icon
   - Query editor layout restructuring with collapsible sections
   - Sidebar field search styling improvements
   - Histogram chart wrapper styling

2. **Database Loading Fix** - Fixed an issue where databases were not being displayed in the dataset navigator after successful loading from external data sources.

### Technical Changes

#### Styling Changes (PR #7546)

| Component | Change |
|-----------|--------|
| Dataset Navigator | Added database icon, tooltip, and updated CSS class naming |
| Query Editor | Restructured layout with collapsible top bar and body sections |
| Language Selector | Added arrow down icon, sorted language options alphabetically |
| Field Search | Updated styling for query enhancements mode |
| Chart Wrapper | Added border and padding styling for histogram |
| App Container | Added height calculations for `dsc--next` class |

#### Database Loading Fix (PR #7567)

Added `useEffect` hook in `DataSetNavigator` component to properly handle the `SUCCESS` status from `databasesLoadStatus`, ensuring databases are displayed after successful loading from external data sources.

## Limitations

- Styling changes only apply when the query enhancements toggle is enabled
- Database loading fix specifically addresses external data source types (`SIMPLE_DATA_SOURCE_TYPES.EXTERNAL`)

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#7546](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7546) | Fixes Discover next styling |  |
| [#7567](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7567) | Fixes databases not being displayed upon success |  |
