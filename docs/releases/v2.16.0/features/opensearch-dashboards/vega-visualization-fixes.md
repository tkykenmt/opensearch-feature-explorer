---
tags:
  - opensearch-dashboards
---
# Vega Visualization Fixes

## Summary

This release fixes an error message formatting issue in the Vega visualization URL parser. When users specified an unsupported query type (such as `ppl`), the error message displayed template placeholders instead of the actual type value.

## Details

### What's New in v2.16.0

The fix corrects string interpolation in the error message generation for unsupported URL types in Vega visualizations.

### Technical Changes

**Before (broken):**
```
url: {"%type%": "${type}"} is not supported
```

**After (fixed):**
```
url: {"%type%": "ppl"} is not supported
```

The issue was caused by using single quotes instead of template literals (backticks) for string interpolation in the `vega_parser.ts` file:

```typescript
// Before (incorrect - no interpolation)
urlObject: 'url: {"%type%": "${type}"}'

// After (correct - template literal with interpolation)
urlObject: `url: {"%type%": "${type}"}`
```

### Affected Component

| Component | File | Change |
|-----------|------|--------|
| vis_type_vega | `src/plugins/vis_type_vega/public/data_model/vega_parser.ts` | Fixed string interpolation |

## Limitations

None.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#6777](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6777) | Fix vega visualization error message not been formatted | - |
