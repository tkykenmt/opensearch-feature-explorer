---
tags:
  - domain/core
  - component/dashboards
  - dashboards
---
# TSVB Visualization

## Summary

This release improves the Time-Series Visual Builder (TSVB) in OpenSearch Dashboards with enhanced axis control options and UI consistency fixes. Users can now hide axes, set per-axis scale (normal/log), and benefit from compressed input fields that match the OUI design system.

## Details

### What's New in v2.18.0

PR #8504 introduces three changes to TSVB time series visualizations:

1. **Hide Axis Option**: New "Hidden" position option for the separate axis setting, allowing users to completely hide the Y-axis while maintaining data visualization
2. **Per-Axis Scale Setting**: Each series with a separate axis can now have its own scale (Normal or Log), fixing a long-standing bug where enabling separate axis would override the global axis scale setting
3. **Compressed Input Fields**: Non-OUI input fields now use `EuiFormControlLayout` with compressed styling for visual consistency

### Technical Changes

#### New Axis Position Option

```javascript
export const AXIS_POSITION = {
  LEFT: 'left',
  RIGHT: 'right',
  HIDDEN: 'hidden',  // New in v2.18.0
};
```

When axis position is set to "Hidden":
- The axis is internally positioned to the left but rendered with `hide: true`
- Data series continue to render normally
- Useful for dashboard layouts where axis labels are not needed

#### New Axis Scale Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `axis_scale` | Scale type for the series axis | `normal` |

Available scale options:
- `normal` - Linear scale
- `log` - Logarithmic scale

This fixes [Issue #1929](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/1929) where enabling "Separate Axis" would force the scale to "Normal" regardless of the Panel Options setting.

#### UI Component Updates

Input fields in the following components now use compressed EUI styling:

| Component | Field | Change |
|-----------|-------|--------|
| Moving Average Agg | Window | Wrapped with `EuiFormControlLayout` |
| Serial Diff Agg | Lag | Wrapped with `EuiFormControlLayout` |
| Top Hit Agg | Size | Wrapped with `EuiFormControlLayout` |
| Gauge Panel | Max | Wrapped with `EuiFormControlLayout` |
| Table Panel | Pivot Rows | Wrapped with `EuiFormControlLayout` |
| Timeseries Config | Axis Min/Max | Wrapped with `EuiFormControlLayout` |

The custom `.tvbAgg__input` CSS class was removed in favor of standard EUI classes.

### Usage Example

To configure a time series with a hidden axis and log scale:

1. Navigate to **Visualize** → **Create Visualization** → **TSVB**
2. Select **Time Series** visualization type
3. Under **Data** tab, select a series and go to **Options**
4. Set **Separate Axis** to **Yes**
5. Set **Axis Position** to **Hidden** (new option)
6. Set **Axis Scale** to **Log** (new option)

### Migration Notes

No migration required. Existing TSVB visualizations will continue to work. The new axis scale setting defaults to "normal" for backward compatibility.

## Limitations

- The "Hidden" axis position is only available for time series visualizations with separate axis enabled
- Axis scale setting is per-series, not global (this is intentional to allow mixed scales)

## References

### Documentation
- [TSVB Documentation](https://docs.opensearch.org/2.18/dashboards/visualize/tsvb/): Official TSVB documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#8504](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8504) | Allow hiding the TSVB axis for time series, compress non-OUI input fields, allow setting scale of each axis |

### Issues (Design / RFC)
- [Issue #1929](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/1929): Bug report - Separate axis overrides axis scale setting

## Related Feature Report

- Full feature documentation
