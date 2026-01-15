---
tags:
  - opensearch-dashboards
---
# Discover Fixes

## Summary

Bug fixes and improvements for the Discover application in OpenSearch Dashboards v2.16.0, addressing UI layout issues, URL state migration, duplicate column handling, surrounding document view highlighting, and table column rendering.

## Details

### What's New in v2.16.0

Seven fixes were introduced to improve the Discover experience:

1. **Discover Options Location Fix** (PR #7581) - Repositioned the discover options (document table settings) to appear inline with the hits counter instead of below the time chart header, improving UI layout when query enhancements toggle is off.

2. **Legacy URL Global State Migration** (PR #6780) - Fixed migration of global state (`_g` parameter) from legacy Discover URLs. Previously, time range, filters, and refresh interval settings were lost when navigating from legacy URLs.

3. **Duplicate Timestamp Column Fix** (PR #6983) - Fixed duplicate timestamp column appearing in the document table when the time field was already included in the selected columns.

4. **Anchor Row Highlighting** (PR #7025) - Added visual highlighting for the anchor row in the surrounding documents view, making it easier to identify the context document.

5. **Wide Table Last Column Fix** (PR #7058) - Fixed the last column of tables wider than the viewport being crushed. Now all columns including the last one have fixed widths set.

6. **Styling Fixes** (PR #7546) - Corrected styling issues in the Discover 2.0 page when query enhancements toggle is enabled.

7. **Database Loading Fix** (PR #7567) - Fixed databases not being displayed in the dataset navigator after successful loading from external data sources.

### Technical Changes

#### Discover Options Location (PR #7581)

| Component | Change |
|-----------|--------|
| Chart Header | Moved `discoverOptions` from separate row to inline with `hitsCounter` |
| Toggle Button | Renamed from `queryEditorCollapseBtn` to `histogramCollapseBtn` |
| i18n Labels | Updated toggle label from `queryEditor.collapse` to `histogram.collapse` |

#### Legacy URL Migration (PR #6780)

Added global state (`_g`) extraction and migration in `migrateUrlState()` function:
- Extracts `_g` state containing time range, filters, and refresh interval
- Preserves global state when migrating from legacy `#/` or `#/view/{id}` URLs
- Added comprehensive unit tests for migration scenarios

#### Duplicate Column Prevention (PR #6983)

Modified `getLegacyDisplayedColumns()` in `helper.tsx`:
- Added check `!columns.includes(indexPattern.timeFieldName)` before prepending time column
- Prevents duplicate timestamp column when user explicitly adds time field to columns
- Added unit tests covering various column configuration scenarios

#### Anchor Row Highlighting (PR #7025)

| Change | Description |
|--------|-------------|
| Type Extension | Added `isAnchor?: boolean` property to `OpenSearchSearchHit` type |
| Row Styling | Added conditional `osdDocTable__row--highlight` class to anchor rows |
| Visual Effect | Anchor document now visually distinguished in surrounding docs view |

#### Wide Table Column Fix (PR #7058)

Changed column width calculation in `DefaultDiscoverTable`:
- Previously: Last column excluded from fixed width calculation to allow growth
- Now: All columns (except first) get fixed widths based on `getBoundingClientRect()`
- Prevents last column from being crushed when table exceeds viewport width

## Limitations

- Styling changes only apply when the query enhancements toggle is enabled
- Database loading fix specifically addresses external data source types
- Anchor row highlighting requires the `isAnchor` property to be set on the document

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#7581](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7581) | Fix discover options' location | |
| [#6780](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6780) | Migrate global state from legacy URL | [#6766](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6766) |
| [#6983](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6983) | Check if timestamp is already included to remove duplicate column | [#6982](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6982) |
| [#7025](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7025) | Highlight the anchor row in surrounding doc view | [#6457](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6457) |
| [#7058](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7058) | Allow last column of wide table to show properly | [#7056](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7056) |
| [#7546](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7546) | Fixes Discover next styling | |
| [#7567](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7567) | Fixes databases not being displayed upon success | |
