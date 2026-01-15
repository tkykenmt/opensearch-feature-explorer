---
tags:
  - opensearch-dashboards
---
# Visualization Color Fix

## Summary

Fixed an issue where visualizations with more than 10 items displayed incorrect colors. The color palette rotation logic was updated to ensure consistent color ordering regardless of the number of data items.

## Details

### What's New in v2.16.0

This bug fix addresses a color display issue in OpenSearch Dashboards visualizations that occurred when displaying more than 10 data items.

### Problem

When a visualization contained more than 10 items, the `euiPaletteColorBlind` function would rotate through colors in an inconsistent manner, causing:
- Colors to appear in unexpected order
- Visual inconsistency between visualizations with different item counts
- Difficulty distinguishing data series in charts

### Technical Changes

The fix modifies the `MappedColors` class in `src/plugins/charts/public/services/colors/mapped_colors.ts`:

| Parameter | Before | After |
|-----------|--------|-------|
| `rotations` | Calculated inline | Extracted to variable for reuse |
| `direction` | `'both'` (always) | `'lighter'` when rotations=2, `'both'` otherwise |
| `order` | Not specified | `'middle-out'` when rotations>2, `'append'` otherwise |

```typescript
// Updated color palette configuration
const rotations = Math.ceil(keys.length / 10);
const colorPalette = euiPaletteColorBlind({
  rotations,
  direction: rotations === 2 ? 'lighter' : 'both',
  order: rotations > 2 ? 'middle-out' : 'append',
})
```

This ensures that:
1. Original colors are always used first
2. Color rotation maintains visual consistency
3. The palette expands predictably as more items are added

## Limitations

- This fix applies only to visualizations using the default color palette
- Custom color mappings configured via `visualization:colorMapping` setting are not affected

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#7051](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7051) | Fix colors of visualizations with more than 10 items | [#5422](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/5422) |
