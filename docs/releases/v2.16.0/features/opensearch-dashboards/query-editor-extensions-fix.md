---
tags:
  - opensearch-dashboards
---
# Query Editor Extensions Fix

## Summary

This release fixes object empty check logic and render order issues in the Query Editor Extensions component, improving reliability and performance of the search bar extension system.

## Details

### What's New in v2.16.0

This bugfix addresses issues introduced in PR #7034 which added query editor extensions:

1. **Fixed Object Empty Check**: Corrected the logic for checking if `configMap` is empty. The previous implementation `!Object.keys(configMap)` always returned `false` because `Object.keys()` returns an array (truthy). Changed to `Object.keys(configMap).length === 0`.

2. **Fixed Render Order**: QueryEditorExtensions requires container divs to be mounted before extensions can render. The previous implementation mounted extensions first and relied on re-rendering of `queryEditorTopRow`. Moving the extension rendering into the QueryEditor component ensures refs are properly set before use.

3. **Improved Component Architecture**: Moved `QueryEditorExtensions` from `QueryEditorTopRow` into `QueryEditor` component, simplifying the ref management and ensuring proper render lifecycle.

### Technical Changes

#### Before (Problematic)
```typescript
// In query_editor_extensions.tsx - incorrect empty check
if (!configMap || !Object.keys(configMap)) return [];
// Object.keys() returns [], which is truthy, so this never short-circuits

// In query_editor_top_row.tsx - refs passed down
<QueryEditor
  queryEditorHeaderRef={queryEditorHeaderRef}
  queryEditorBannerRef={queryEditorBannerRef}
/>
```

#### After (Fixed)
```typescript
// In query_editor_extensions.tsx - correct empty check
if (!configMap || Object.keys(configMap).length === 0) return [];

// In query_editor.tsx - refs managed internally
private headerRef: RefObject<HTMLDivElement> = createRef();
private bannerRef: RefObject<HTMLDivElement> = createRef();
```

### Files Changed

| File | Changes |
|------|---------|
| `query_editor.tsx` | Moved extension rendering logic, internalized refs |
| `query_editor_extensions.tsx` | Fixed empty object check |
| `query_editor_top_row.tsx` | Removed extension rendering, simplified props |

## Limitations

- No behavior changes for end users; this is an internal fix
- Extensions still require proper registration through the UI Enhancements API

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#7077](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7077) | Fix object empty check and minor perf issue in query editor extensions | Follow-up to #7034 |
| [#7034](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7034) | [Discover-next] Add query editor extensions | #6077 |
