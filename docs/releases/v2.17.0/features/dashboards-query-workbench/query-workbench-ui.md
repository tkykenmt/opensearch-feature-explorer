---
tags:
  - domain/core
  - component/dashboards
  - dashboards
  - indexing
  - search
  - sql
---
# Query Workbench UI Improvements

## Summary

This release item updates the Query Workbench plugin UI to use smaller and compressed variants of buttons and form components, aligning with OpenSearch Dashboards design standards for improved consistency and density.

## Details

### What's New in v2.17.0

The Query Workbench plugin received comprehensive UI refinements to improve visual consistency across OpenSearch Dashboards. The changes focus on using smaller, more compact UI components that reduce visual clutter while maintaining functionality.

### Technical Changes

#### Component Replacements

| Original Component | New Component | Purpose |
|-------------------|---------------|---------|
| `EuiButton` | `EuiSmallButton` | Smaller action buttons |
| `EuiButtonIcon` | `EuiSmallButtonIcon` | Compact icon buttons |
| `EuiButtonEmpty` | `EuiSmallButtonEmpty` | Smaller empty-style buttons |
| `EuiComboBox` | `EuiCompressedComboBox` | Compact dropdown selectors |
| `EuiFieldText` | `EuiCompressedFieldText` | Compressed text inputs |
| `EuiFieldNumber` | `EuiCompressedFieldNumber` | Compressed number inputs |
| `EuiFormRow` | `EuiCompressedFormRow` | Compact form layouts |
| `EuiRadioGroup` | `EuiCompressedRadioGroup` | Compressed radio buttons |
| `EuiSelect` | `EuiCompressedSelect` | Compact select dropdowns |

#### Affected Components

The following Query Workbench components were updated:

- **Main Page** (`main.tsx`): Documentation link button
- **SQL Page** (`SQLPage.tsx`): Run, Clear, Explain, Sample Query, and Accelerate Table buttons
- **PPL Page** (`PPLPage.tsx`): Run, Clear, Explain, and Sample Query buttons
- **Query Results** (`QueryResults.tsx`, `QueryResultsBody.tsx`): Expand/collapse icons, close buttons
- **Async Query Body** (`async_query_body.tsx`): Error modal and cancel buttons
- **Data Select** (`DataSelect.tsx`): Data source selector
- **Create Button** (`CreateButton.tsx`): Create dropdown button
- **Acceleration Index Flyout** (`acceleration_index_flyout.tsx`): Close button
- **Create Acceleration** (`create_acceleration.tsx`): Close and Copy Query buttons
- **Index Selectors**: Type selector, source selector, index options, and settings

### Usage Example

Before (v2.16.0 and earlier):
```tsx
import { EuiButton, EuiComboBox, EuiFormRow } from '@elastic/eui';

<EuiFormRow label="Data source">
  <EuiComboBox
    placeholder="Select a data source"
    options={options}
    onChange={onChange}
  />
</EuiFormRow>
<EuiButton onClick={onRun}>Run</EuiButton>
```

After (v2.17.0):
```tsx
import { EuiSmallButton, EuiCompressedComboBox, EuiCompressedFormRow } from '@elastic/eui';

<EuiCompressedFormRow label="Data source">
  <EuiCompressedComboBox
    placeholder="Select a data source"
    options={options}
    onChange={onChange}
  />
</EuiCompressedFormRow>
<EuiSmallButton onClick={onRun}>Run</EuiSmallButton>
```

### Migration Notes

This is a visual-only change with no functional impact. Users will notice:
- Smaller button sizes throughout the Query Workbench interface
- More compact form elements
- Consistent styling with other OpenSearch Dashboards plugins

No configuration changes or API modifications are required.

## Limitations

- This change only affects the Query Workbench plugin UI
- The compressed components are part of the OpenSearch UI (OUI) library and require OUI 1.10.0 or later

## References

### Documentation
- [Query Workbench Documentation](https://docs.opensearch.org/2.17/dashboards/query-workbench/)
- [OpenSearch Dashboards Design Guidelines](https://oui.opensearch.org/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#370](https://github.com/opensearch-project/dashboards-query-workbench/pull/370) | Use smaller and compressed variants of buttons and form components |

## Related Feature Report

- Full feature documentation
