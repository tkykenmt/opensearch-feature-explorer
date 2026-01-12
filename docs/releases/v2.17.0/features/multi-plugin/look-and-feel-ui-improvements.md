---
tags:
  - dashboards
---

# Look & Feel UI Improvements

## Summary

OpenSearch Dashboards v2.17.0 introduces comprehensive UI consistency and density improvements across multiple plugins. This coordinated effort standardizes button sizes, form components, typography, and visual hierarchy to create a more cohesive and compact user interface.

## Details

### What's New in v2.17.0

This release implements the "Look & Feel" initiative across 9 dashboard plugins, focusing on:

1. **Smaller Buttons**: Replace standard `EuiButton` with `EuiSmallButton*` variants
2. **Compressed Form Elements**: Replace `Eui<form elements>` with `EuiCompressed<form elements>` variants
3. **Consistent Typography**: Standardize paragraph sizes and header hierarchy
4. **Improved Density**: Reduce visual clutter with smaller context menus and tabs

### Technical Changes

#### Component Replacements

| Original Component | New Component | Purpose |
|-------------------|---------------|---------|
| `EuiButton` | `EuiSmallButton` | Smaller button footprint |
| `EuiButtonEmpty` | `EuiSmallButtonEmpty` | Smaller empty button |
| `EuiButtonIcon` | `EuiSmallButtonIcon` | Smaller icon button |
| `EuiFieldText` | `EuiCompressedFieldText` | Compressed text input |
| `EuiSelect` | `EuiCompressedSelect` | Compressed select dropdown |
| `EuiFieldNumber` | `EuiCompressedFieldNumber` | Compressed number input |
| `EuiTabs` | `EuiTabs size="s"` | Smaller tab navigation |
| `EuiContextMenu` | `EuiContextMenu size="s"` | Smaller context menus |

#### Typography Standards

| Element | Standard |
|---------|----------|
| Paragraph text | `<EuiText size="s">` (15.75px next theme / 14px V7 theme) |
| Main page headers | H1 wrapped in `<EuiText size="s">` |
| Modal/Flyout headers | H2 wrapped in `<EuiText size="s">` |

#### Button Usage Guidelines

- **Primary buttons**: Reserved for primary calls to action only
- **Secondary buttons**: Used for all other actions
- **One primary button per view**: Avoid multiple primary buttons on the same page

### Affected Plugins

| Plugin | Repository | PRs |
|--------|------------|-----|
| Anomaly Detection | anomaly-detection-dashboards-plugin | [#826](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/826), [#836](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/836) |
| Observability | dashboards-observability | [#2068](https://github.com/opensearch-project/dashboards-observability/pull/2068), [#2071](https://github.com/opensearch-project/dashboards-observability/pull/2071) |
| Index Management | index-management-dashboards-plugin | [#1103](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1103) |
| Notifications | dashboards-notifications | [#231](https://github.com/opensearch-project/dashboards-notifications/pull/231) |
| Reporting | dashboards-reporting | [#398](https://github.com/opensearch-project/dashboards-reporting/pull/398) |
| Search Relevance | dashboards-search-relevance | [#421](https://github.com/opensearch-project/dashboards-search-relevance/pull/421) |
| ML Commons | ml-commons-dashboards | [#349](https://github.com/opensearch-project/ml-commons-dashboards/pull/349) |

### Usage Example

Before:
```tsx
<EuiButton onClick={handleClick}>
  Submit
</EuiButton>
<EuiFieldText
  value={value}
  onChange={handleChange}
/>
```

After:
```tsx
<EuiSmallButton onClick={handleClick}>
  Submit
</EuiSmallButton>
<EuiCompressedFieldText
  value={value}
  onChange={handleChange}
/>
```

### Migration Notes

Plugin developers should:
1. Replace button components with their `EuiSmall*` equivalents
2. Replace form components with their `EuiCompressed*` equivalents
3. Add `size="s"` to `EuiTabs` and `EuiContextMenu` components
4. Wrap text content in `<EuiText size="s">`
5. Review button usage to ensure only one primary button per view

## Limitations

- Changes are primarily visual and do not affect functionality
- Some plugins may have additional Look & Feel changes in subsequent releases
- Custom components may need manual updates to match the new styling

## References

### Documentation
- [OpenSearch Dashboards Advanced Settings](https://docs.opensearch.org/2.17/dashboards/management/advanced-settings/): Customize look and feel settings

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#826](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/826) | anomaly-detection-dashboards-plugin | Smaller buttons and compressed form components |
| [#836](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/836) | anomaly-detection-dashboards-plugin | Consistency and density improvements |
| [#2068](https://github.com/opensearch-project/dashboards-observability/pull/2068) | dashboards-observability | Smaller buttons and compressed form components |
| [#2071](https://github.com/opensearch-project/dashboards-observability/pull/2071) | dashboards-observability | Integrations density and consistency improvements |
| [#1103](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1103) | index-management-dashboards-plugin | Smaller buttons and compressed form components |
| [#231](https://github.com/opensearch-project/dashboards-notifications/pull/231) | dashboards-notifications | Smaller buttons and compressed form components |
| [#398](https://github.com/opensearch-project/dashboards-reporting/pull/398) | dashboards-reporting | Smaller buttons and compressed form components |
| [#421](https://github.com/opensearch-project/dashboards-search-relevance/pull/421) | dashboards-search-relevance | Smaller buttons and compressed form components |
| [#349](https://github.com/opensearch-project/ml-commons-dashboards/pull/349) | ml-commons-dashboards | Smaller buttons and compressed form components |

## Related Feature Report

- [Full feature documentation](../../../../features/multi-plugin/multi-plugin-look-and-feel-ui-improvements.md)
