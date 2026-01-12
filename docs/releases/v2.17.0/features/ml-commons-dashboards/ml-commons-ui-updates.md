---
tags:
  - dashboards
  - indexing
  - ml
---

# ML Commons UI Updates

## Summary

This release aligns the ML Commons Dashboards UI with OpenSearch UX guidelines by standardizing font sizes and styles across the plugin. The changes ensure visual consistency with other OpenSearch Dashboards plugins.

## Details

### What's New in v2.17.0

The ML Commons Dashboards plugin received UI refinements to align with the OpenSearch UX design guidelines. These changes standardize the typography across the deployed models dashboard and model preview panels.

### Technical Changes

#### Component Updates

| Component | Change | Description |
|-----------|--------|-------------|
| `model_deployment_table.tsx` | `<>` → `<EuiText size="s">` | Wrapped empty prompt body content with small text styling |
| `connector_details.tsx` | `EuiTitle` → `EuiText size="s"` | Changed section header from title to small text |
| `preview_panel/index.tsx` | `EuiTitle size="m"` → `EuiText size="s"` | Changed flyout header from medium title to small text |
| `nodes_table.tsx` | `EuiTitle` → `EuiText size="s"` | Changed "Status by node" header to small text |

#### Files Changed

| File | Additions | Deletions |
|------|-----------|-----------|
| `public/components/monitoring/model_deployment_table.tsx` | 6 | 6 |
| `public/components/preview_panel/connector_details.tsx` | 3 | 3 |
| `public/components/preview_panel/index.tsx` | 3 | 3 |
| `public/components/preview_panel/nodes_table.tsx` | 8 | 4 |

### Usage Example

The changes affect the visual presentation of the ML Commons Dashboards UI. No configuration changes are required.

Before (using `EuiTitle`):
```tsx
<EuiFlyoutHeader hasBorder>
  <EuiTitle size="m">
    <h2>{name}</h2>
  </EuiTitle>
</EuiFlyoutHeader>
```

After (using `EuiText size="s"`):
```tsx
<EuiFlyoutHeader hasBorder>
  <EuiText size="s">
    <h2>{name}</h2>
  </EuiText>
</EuiFlyoutHeader>
```

## Limitations

- This is a visual-only change with no functional impact
- The changes apply only to the ML Commons Dashboards plugin UI

## References

### Documentation
- [Managing ML models in OpenSearch Dashboards](https://docs.opensearch.org/2.17/ml-commons-plugin/ml-dashboard/): Official documentation for ML Commons Dashboards

### Pull Requests
| PR | Description |
|----|-------------|
| [#355](https://github.com/opensearch-project/ml-commons-dashboards/pull/355) | Align font size and style with UX guideline |

## Related Feature Report

- [Full feature documentation](../../../../features/ml-commons-dashboards/ml-commons-dashboards.md)
