---
tags:
  - dashboards
---

# Dashboards Frontend Cleanup

## Summary

OpenSearch Dashboards v3.0.0 removes several deprecated frontend APIs and dependencies as part of a major cleanup effort. This breaking change removes `CssDistFilename` exports, the `withLongNumerals` HTTP option, the `@elastic/filesaver` dependency, and the deprecated "newExperience" Discover table option. Plugin developers and users relying on these deprecated features must update their code before upgrading to v3.0.0.

## Details

### What's New in v3.0.0

This release removes deprecated code that was marked for removal in the 3.0 major version:

1. **CssDistFilename removal**: Deprecated CSS filename exports from `osd-ui-shared-deps` package
2. **withLongNumerals removal**: Deprecated HTTP fetch option replaced by `withLongNumeralsSupport`
3. **@elastic/filesaver removal**: Replaced with the modern `file-saver` package
4. **newExperience Discover table removal**: Legacy DataGrid table implementation removed in favor of DefaultDiscoverTable

### Technical Changes

#### Removed Components

| Component | Package/Location | Replacement |
|-----------|------------------|-------------|
| `darkCssDistFilename` | `@osd/ui-shared-deps` | Use `baseCssDistFilename` with theme config |
| `darkV8CssDistFilename` | `@osd/ui-shared-deps` | Use `baseCssDistFilename` with theme config |
| `lightCssDistFilename` | `@osd/ui-shared-deps` | Use `baseCssDistFilename` with theme config |
| `lightV8CssDistFilename` | `@osd/ui-shared-deps` | Use `baseCssDistFilename` with theme config |
| `withLongNumerals` | `HttpFetchOptions` | Use `withLongNumeralsSupport` |
| `@elastic/filesaver` | `package.json` | Use `file-saver` |
| `DataGrid` component | `discover` plugin | Use `DefaultDiscoverTable` |
| `newExperience` setting | `discover` plugin | Removed (DefaultDiscoverTable is now default) |

#### Dependency Changes

| Old Dependency | New Dependency | Notes |
|----------------|----------------|-------|
| `@elastic/filesaver@1.1.2` | `file-saver@^2.0.5` | Modern, actively maintained package |
| - | `@types/file-saver@^2.0.7` | TypeScript types added |

#### Files Removed

The following files were removed from the Discover plugin:

- `data_grid.tsx` - Deprecated DataGrid component
- `data_grid_table_cell_actions.tsx` - Cell actions for deprecated grid
- `data_grid_table_cell_value.test.tsx` - Tests for deprecated component
- `data_grid_table_columns.tsx` - Column definitions for deprecated grid
- `data_grid_table_columns.test.tsx` - Tests for deprecated component
- `data_grid_table_context.tsx` - Context provider for deprecated grid
- `data_grid_table_docview_inspect_button.tsx` - Inspect button for deprecated grid
- `data_grid_table_flyout.tsx` - Flyout for deprecated grid
- `data_grid_toolbar.tsx` - Toolbar for deprecated grid
- `discover_options.tsx` - Options component for legacy toggle
- Multiple context view test files

### Migration Notes

#### For Plugin Developers

1. **CSS Filename Migration**:
   ```typescript
   // Before (deprecated)
   import { darkCssDistFilename, lightCssDistFilename } from '@osd/ui-shared-deps';
   
   // After
   import { baseCssDistFilename } from '@osd/ui-shared-deps';
   // Use theme configuration to determine styling
   ```

2. **HTTP Fetch Options Migration**:
   ```typescript
   // Before (deprecated)
   http.fetch('/api/endpoint', { withLongNumerals: true });
   
   // After
   http.fetch('/api/endpoint', { withLongNumeralsSupport: true });
   ```

3. **File Saver Migration**:
   ```typescript
   // Before
   // @ts-expect-error
   import { saveAs } from '@elastic/filesaver';
   
   // After
   import { saveAs } from 'file-saver';
   ```

#### For Users

- The Discover table now uses `DefaultDiscoverTable` exclusively
- The "Enable legacy Discover" option has been removed from Discover settings
- No user action required unless custom plugins depend on removed APIs

## Limitations

- Plugins using the deprecated `CssDistFilename` exports will fail to compile
- Plugins using `withLongNumerals` will need code changes
- Plugins importing `@elastic/filesaver` must update imports

## References

### Documentation
- [Breaking Changes Documentation](https://docs.opensearch.org/3.0/breaking-changes/): Official breaking changes for v3.0.0
- [PR #5592](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/5592): Original deprecation of withLongNumerals
- [PR #7625](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7625): Original deprecation of CssDistFilename
- [PR #9511](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9511): Deprecation of newExperience table option

### Pull Requests
| PR | Description |
|----|-------------|
| [#9446](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9446) | Remove deprecated CssDistFilename for 3.0 |
| [#9448](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9448) | Remove withLongNumerals in HttpFetchOptions |
| [#9484](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9484) | Remove @elastic/filesaver in favor of file-saver |
| [#9531](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9531) | Remove the deprecated "newExperience" table option in Discover |

### Issues (Design / RFC)
- [Issue #9253](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/9253): Planned Breaking Changes for 3.0 in OpenSearch-Dashboards
- [Issue #9341](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/9341): Remove @elastic/filesaver dependency

## Related Feature Report

- [Full feature documentation](../../../features/opensearch-dashboards/opensearch-dashboards-dashboards-frontend-cleanup.md)
