---
tags:
  - domain/search
  - component/dashboards
  - dashboards
  - performance
  - search
---
# Toast Notification Error Message Bug Fix

## Summary

This bug fix resolves an issue where error messages were not rendering correctly in toast notifications within the Search Relevance Workbench plugin. Previously, when API calls failed, users would see generic error messages instead of the actual error details from the backend, making it difficult to diagnose issues.

## Details

### What's New in v3.2.0

The fix ensures that error messages from backend API responses are properly extracted and displayed in toast notifications across multiple components of the Search Relevance Workbench.

### Technical Changes

#### Root Cause

When the OpenSearch Dashboards HTTP client encounters an error, the actual error message is nested within the `body` property of the error object. The previous implementation passed the entire error object to `notifications.toasts.addError()`, which couldn't properly extract the nested message.

#### Fix Implementation

The fix modifies error handling across 9 files to use optional chaining to extract the error body:

```typescript
// Before
notifications.toasts.addError(err, {
  title: 'Failed to create experiment',
});

// After
notifications.toasts.addError(err?.body || err, {
  title: 'Failed to create experiment',
});
```

#### Affected Components

| Component | File | Description |
|-----------|------|-------------|
| Template Configuration | `experiment_create/configuration/template_configuration.tsx` | Experiment creation |
| Evaluation Experiment View | `experiment_view/evaluation_experiment_view.tsx` | Document score processing |
| Hybrid Optimizer View | `experiment_view/hybrid_optimizer_experiment_view.tsx` | Variant details loading |
| Judgment Form | `judgment/hooks/use_judgment_form.ts` | Judgment creation |
| Query Set Table | `query_set/components/query_set_table.tsx` | Pagination options |
| Query Set Create | `query_set/views/query_set_create.tsx` | Query set creation |
| Search Configuration Form | `search_configuration/hooks/use_search_configuration_form.ts` | Index fetching and config creation |
| Search Configuration Listing | `search_configuration/views/search_configuration_listing.tsx` | Pagination options |

### Usage Example

When an error occurs (e.g., authorization failure), users now see the actual error message:

**Before:**
```
Error: [object Object]
```

**After:**
```
Error: Search Relevance Workbench is disabled
```

### Migration Notes

No migration required. This is a transparent bug fix that improves error message visibility.

## Limitations

- The fix relies on the error object having a `body` property containing the error message
- If the backend returns errors in a different format, the fallback to the original error object is used

## References

### Pull Requests
| PR | Description |
|----|-------------|
| [#612](https://github.com/opensearch-project/dashboards-search-relevance/pull/612) | Bug fixes for error messages not render correctly for toast notifications |

### Issues (Design / RFC)
- [Issue #547](https://github.com/opensearch-project/dashboards-search-relevance/issues/547): Error messages are not surfaced to search relevance workbench

## Related Feature Report

- [Full feature documentation](../../../../features/dashboards-search-relevance/search-relevance-workbench.md)
