# Dashboards Visualizations

## Summary

OpenSearch Dashboards v3.4.0 introduces significant enhancements to the Explore plugin's visualization capabilities, including a new bar gauge visualization type, customizable legend names, numerical field support for color mapping, customized column ordering for table visualizations, and improved threshold logic for gauge visualizations. These improvements provide users with more flexible and powerful data visualization options.

## Details

### What's New in v3.4.0

#### New Bar Gauge Visualization
A new bar gauge visualization type has been added to the Explore plugin, providing an alternative way to display metric values with threshold-based coloring. Bar gauges display values as horizontal bars with configurable thresholds.

#### Customizable Legend Names
Users can now customize legend names in visualizations, allowing for more descriptive and user-friendly chart legends. This works for both single and multiple legend scenarios.

#### Numerical Field as Color Field
The color field in visualizations now supports numerical fields in addition to categorical fields, enabling gradient-based color mapping for continuous data values.

#### Table Visualization Column Ordering
Table visualizations now support customized column ordering with proper persistence in dashboards. Users can:
- Enable "Customized column order" toggle in settings
- Drag columns to reorder using the columns selector or header actions
- Hide columns while maintaining order
- Save column configurations to dashboards

#### Improved Gauge Threshold Logic
The threshold logic for gauge and bar gauge visualizations has been refactored:
- Text color now always reflects threshold color
- MinBase serves as a cutoff line with last threshold color applied to values below
- Negative values are now supported for min/max controls
- Debounce added when adding/updating/deleting thresholds

### Technical Changes

#### New Components

| Component | Description |
|-----------|-------------|
| Bar Gauge | New visualization type displaying metrics as horizontal bars |
| Legend Name Editor | UI for customizing legend display names |
| Numerical Color Field | Support for numerical fields in color mapping |
| Column Order Toggle | Toggle for enabling customized column ordering |
| Column Drag Handler | Drag-and-drop column reordering functionality |

#### Configuration Changes

| Setting | Description | Default |
|---------|-------------|---------|
| `customizedColumnOrder` | Enable customized column ordering for tables | `false` |
| `legendName` | Custom legend name for visualizations | Field name |

### Usage Example

```yaml
# Enable customized column order in table visualization
1. Create a table visualization in Explore
2. Open Settings panel
3. Enable "Customized column order" toggle
4. Drag columns to desired order
5. Save to dashboard

# Customize legend name
1. Create a chart visualization
2. Click on legend settings
3. Enter custom legend name
4. Apply changes

# Use numerical field for color
1. Create a visualization with color field
2. Select a numerical field for color
3. Configure color gradient range
```

### Migration Notes

No migration required. New features are additive and backward compatible.

## Limitations

- Column order customization is only available when the toggle is enabled
- In dashboard mode, column selector and density options are hidden
- Numerical color fields require appropriate data ranges for effective visualization

## References

### Documentation
- [Building data visualizations](https://docs.opensearch.org/3.4/dashboards/visualize/viz-index/): Official documentation
- [OpenSearch Dashboards Repository](https://github.com/opensearch-project/OpenSearch-Dashboards)

### Pull Requests
| PR | Description |
|----|-------------|
| [#10604](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10604) | Allow customizing legend name |
| [#10697](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10697) | Add bar gauge visualization |
| [#10808](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10808) | Support numerical field as color field |
| [#10868](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10868) | Refactor threshold logic of gauge and bar gauge |
| [#10894](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10894) | Add tests for gauge and bar gauge |
| [#10896](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10896) | Add tests for table visualization |
| [#10898](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10898) | Add customized column order toggle for table visualization |
| [#10599](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10599) | Fix breadcrumb floating issue |
| [#10657](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10657) | Fix tabs length and scroll persistence |

## Related Feature Report

- [Full feature documentation](../../../features/opensearch-dashboards/explore.md)
