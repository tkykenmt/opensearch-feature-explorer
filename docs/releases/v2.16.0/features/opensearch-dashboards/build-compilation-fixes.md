---
tags:
  - opensearch-dashboards
---
# Build & Compilation Fixes

## Summary

This release includes several build and compilation fixes for OpenSearch Dashboards, addressing lint checker failures, removing unused code that broke compilation, and cleaning up legacy Angular-related code.

## Details

### What's New in v2.16.0

Multiple fixes were applied to improve build stability and code quality:

1. **Lint Checker Fix**: Added `site.com` to `.lycheeignore` to resolve lint checker failures caused by example URLs in documentation.

2. **Compilation Fix**: Removed unused import (`DataSourceSelectionService`) and property from the data source view example component that was causing compilation errors.

3. **Angular Code Cleanup**: Removed legacy Angular-related comments and code from the codebase, including:
   - Removed Angular coupling comment from SCSS mixins
   - Removed `ng-bind-html` attribute from tooltip formatter JSX

### Technical Changes

| Fix | File | Change |
|-----|------|--------|
| Lint checker | `.lycheeignore` | Added `site.com` to ignore list |
| Unused import | `examples/multiple_data_source_examples/public/components/data_source_view_example.tsx` | Removed `DataSourceSelectionService` import and `dataSourceSelection` prop |
| Angular cleanup | `packages/osd-ui-framework/src/global_styling/mixins/_global_mixins.scss` | Removed Angular coupling comment |
| Angular cleanup | `src/plugins/vis_type_vislib/public/vislib/components/tooltip/_hierarchical_tooltip_formatter.js` | Removed `ng-bind-html` attribute |

## Limitations

- These are maintenance fixes with no user-facing impact
- The Angular cleanup is part of ongoing legacy code removal

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#6771](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6771) | Lint checker failure fix | - |
| [#6879](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6879) | Remove unused import and property which broke compilation | [#6878](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6878) |
| [#7087](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7087) | Remove angular related comment and code | - |
