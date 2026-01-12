---
tags:
  - dashboards
  - indexing
  - search
---

# Discover Plugin Fixes

## Summary

This release includes two bug fixes for the Discover plugin in OpenSearch Dashboards: a critical fix for the empty page issue when no index patterns exist, and new Cypress tests for discover visualization functionality.

## Details

### What's New in v3.2.0

Two improvements to the Discover plugin:

1. **Empty Page Fix**: Fixed an issue where the Discover plugin showed an empty page instead of the "no index patterns" UI when users had no index patterns configured
2. **Cypress Tests**: Added comprehensive Cypress tests for discover visualization functionality

### Technical Changes

#### Bug Fix: Empty Page Issue

The root cause was in the data-explorer's `metadata_slice.ts`. When no index patterns exist, `data.indexPatterns.getDefault()` threw an error instead of returning undefined. This error occurred during the preload phase, preventing the application from loading and stopping the discover plugin from showing the `DiscoverNoIndexPatterns` component.

**Before (problematic code):**
```typescript
const defaultIndexPattern = isQueryEnhancementEnabled
  ? undefined
  : await data.indexPatterns.getDefault();
```

**After (fixed code):**
```typescript
let defaultIndexPattern;
if (!isQueryEnhancementEnabled) {
  try {
    defaultIndexPattern = await data.indexPatterns.getDefault();
  } catch (error) {
    defaultIndexPattern = undefined;
  }
} else {
  defaultIndexPattern = undefined;
}
```

The fix wraps the `getDefault()` call in a try-catch block, allowing the application to continue with `undefined` instead of crashing. This ensures the discover plugin can properly render the `DiscoverNoIndexPatterns` component.

#### New Cypress Tests

Added comprehensive Cypress tests for discover visualization:

| Test | Description |
|------|-------------|
| Saved search in dashboards | Tests loading saved searches into dashboards |
| Time range updates | Verifies changing time range updates saved search results |
| Visualization rule matching | Tests metric, line, bar, scatter, heatmap, and facet visualizations |
| Chart type switching | Tests switching between chart types and table view |

**Key test improvements:**
- Added `data-test-subj` attributes to UI components for better test targeting
- Tests cover PPL queries with various aggregation patterns
- Validates correct axis assignments for different visualization types

### Files Changed

| File | Change |
|------|--------|
| `src/plugins/data_explorer/public/utils/state_management/metadata_slice.ts` | Added try-catch for getDefault() |
| `cypress/.../saved_search_in_dashboards.spec.js` | Rewrote saved search tests |
| `cypress/.../rule_matching_vis.spec.js` | Added visualization tests |
| `src/plugins/dashboard/.../show_add_panel_popover.tsx` | Added test-subj attribute |
| `src/plugins/explore/.../chart_type_selector.tsx` | Added test-subj attributes |
| `src/plugins/explore/.../axes_selector.tsx` | Added test-subj attribute |

## Limitations

- The fix only addresses the case where `getDefault()` throws an error; other index pattern loading issues may still occur
- Cypress tests require workspace and data source setup

## References

### Documentation
- [Index patterns documentation](https://docs.opensearch.org/3.2/dashboards/management/index-patterns/): Official docs on index patterns

### Pull Requests
| PR | Description |
|----|-------------|
| [#10345](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10345) | Fix: Discover plugin shows empty page instead of no-index-patterns UI |
| [#10315](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10315) | Add cypress tests for discover visualization |

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch-dashboards/opensearch-dashboards-discover.md)
