# Input Control Visualization Bugfix

## Summary

This release fixes a visual sizing issue with disabled `ValidatedDualRange` components in Input Control visualizations. When a range slider control was disabled, it displayed with incorrect dimensions, causing visual inconsistency in dashboards.

## Details

### What's New in v2.18.0

The fix ensures that disabled range slider controls in Input Control visualizations maintain proper sizing by adding the `formRowDisplay="rowCompressed"` property to the disabled state rendering.

### Technical Changes

#### Component Fix

The `RangeControl` component in the `input_control_vis` plugin was updated to include the `formRowDisplay` property when rendering disabled `ValidatedDualRange` components.

| File | Change |
|------|--------|
| `src/plugins/input_control_vis/public/components/vis/range_control.tsx` | Added `formRowDisplay="rowCompressed"` to disabled state |

#### Code Change

Before:
```tsx
return <ValidatedDualRange disabled showInput />;
```

After:
```tsx
return <ValidatedDualRange disabled showInput formRowDisplay="rowCompressed" />;
```

### Visual Impact

The fix corrects the height and spacing of disabled range slider controls to match the enabled state, ensuring consistent visual appearance across dashboard controls.

## Limitations

- This fix only affects the visual rendering of disabled range controls
- No functional changes to the Input Control visualization behavior

## Related PRs

| PR | Description |
|----|-------------|
| [#8108](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8108) | Correct the size of disabled ValidatedDualRange components in InputControl visualizations |

## References

- [PR #8108](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8108): Main implementation
- [Building data visualizations](https://docs.opensearch.org/2.18/dashboards/visualize/viz-index/): OpenSearch Dashboards visualization documentation

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch-dashboards/input-control-visualization.md)
