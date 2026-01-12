# AI Search Flows Dashboards Bug Fixes

## Summary

Bug fixes for the AI Search Flows Dashboards plugin (dashboards-flow-framework) in OpenSearch 3.0.0. These changes improve the quick configure modal UX, enhance processor error handling, and add version compatibility for the search query section.

## Details

### What's New in v3.0.0

This release includes two key bug fixes that improve the user experience and version compatibility of the AI Search Flows plugin.

### Technical Changes

#### Quick Configure Component Refactoring (PR #604)

The quick configure modal has been completely refactored to improve form management and validation:

| Change | Description |
|--------|-------------|
| Formik Integration | Quick configure components now use Formik for form state management |
| Required Model Selection | Models are now required for applicable presets (semantic search, hybrid search, RAG) |
| Component Rename | `QuickConfigureInputs` renamed to `QuickConfigureOptionalFields` for clarity |
| ModelField Reusability | `ModelField` component cleaned up and made reusable across the plugin |
| Error Modal Improvement | "No model found" modal now shows once even for presets with multiple models |

#### Processor Error Handling Improvements (PR #604)

Enhanced error display for ingest and search pipeline processors:

| Feature | Description |
|---------|-------------|
| Dynamic Error Messages | Processor-level errors shown dynamically in accordion header when closed |
| Error Callout | Detailed error callout displayed when processor accordion is opened |
| Multiple Error Support | Inspector's errors tab now supports rendering multiple errors |
| State Management | Accordion open/closed state now persisted for better UX |

#### Version Compatibility for Search Query Section (PR #605)

Added version checking to hide the search query section for older OpenSearch versions:

| Behavior | Description |
|----------|-------------|
| Version Check | Search query section hidden when OpenSearch version < 2.19.0 |
| UI Cleanup | Removed unnecessary spacing between search_query and search_response sections |
| Graceful Fallback | Defaults to showing the section if version check fails |

### Code Changes

#### Modified Components

| File | Changes |
|------|---------|
| `quick_configure_modal.tsx` | Refactored to use Formik, added model validation |
| `quick_configure_optional_fields.tsx` | New component for optional configuration fields |
| `processors_list.tsx` | Added error display in accordion headers and callouts |
| `tools.tsx` | Updated to support multiple error messages |
| `errors.tsx` | Changed from single `errorMessage` to `errorMessages` array |
| `search_inputs.tsx` | Added version check to conditionally show search query section |
| `model_field.tsx` | Enhanced with additional props for reusability |
| `workflow_inputs.tsx` | Added toast dismissal on "Test flow" button click |

#### Removed Components

| File | Reason |
|------|--------|
| `quick_configure_inputs.tsx` | Replaced by `quick_configure_optional_fields.tsx` |

### Usage Example

The improved quick configure modal now validates model selection:

```typescript
// Models are now required for non-custom presets
const formSchemaObj = {
  name: yup.string().required('Required'),
  description: yup.string().optional(),
  embeddingModel: yup.object({
    id: yup.string().required('Required')
  }),
  llm: yup.object({
    id: yup.string().required('Required')
  })
};
```

### Migration Notes

- No migration required for end users
- Plugin developers using `QuickConfigureInputs` should update to `QuickConfigureOptionalFields`
- Error handling components now expect `errorMessages` array instead of single `errorMessage` string

## Limitations

- Version check for search query section requires async call to get effective version
- Model selection is now mandatory for non-custom presets (previously optional)
- Error display limited to processor-level errors; form validation errors shown separately

## References

### Documentation
- [AI Search Flows Documentation](https://docs.opensearch.org/3.0/vector-search/ai-search/workflow-builder/)
- [PR #586](https://github.com/opensearch-project/dashboards-flow-framework/pull/586): Previous UX updates (continuation)
- [dashboards-flow-framework Repository](https://github.com/opensearch-project/dashboards-flow-framework)

### Pull Requests
| PR | Description |
|----|-------------|
| [#604](https://github.com/opensearch-project/dashboards-flow-framework/pull/604) | Refactor quick configure components; improve processor error handling |
| [#605](https://github.com/opensearch-project/dashboards-flow-framework/pull/605) | Hide search query section when version is less than 2.19 |

### Issues (Design / RFC)
- [Issue #550](https://github.com/opensearch-project/dashboards-flow-framework/issues/550): Hide ProcessorList component for SEARCH_REQUEST when version < 2.19.0

## Related Feature Report

- [Full feature documentation](../../../../features/dashboards-flow-framework/ai-search-flows.md)
