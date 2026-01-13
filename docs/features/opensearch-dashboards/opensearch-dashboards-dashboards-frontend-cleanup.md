---
tags:
  - opensearch-dashboards
---
# Dashboards Frontend Cleanup

## Summary

OpenSearch Dashboards periodically removes deprecated frontend APIs and dependencies to maintain code quality and reduce technical debt. This feature tracks the cleanup of deprecated exports, HTTP options, third-party dependencies, and UI components that have been superseded by newer implementations.

## Details

### Architecture

```mermaid
graph TB
    subgraph "Removed in v3.0.0"
        CSS[CssDistFilename exports]
        LN[withLongNumerals option]
        FS[@elastic/filesaver]
        DG[DataGrid / newExperience]
    end
    
    subgraph "Replacements"
        BASE[baseCssDistFilename + theme config]
        LNS[withLongNumeralsSupport]
        FSN[file-saver package]
        DDT[DefaultDiscoverTable]
    end
    
    CSS --> BASE
    LN --> LNS
    FS --> FSN
    DG --> DDT
```

### Components

| Component | Status | Replacement | Deprecated In | Removed In |
|-----------|--------|-------------|---------------|------------|
| `darkCssDistFilename` | Removed | `baseCssDistFilename` | v2.x | v3.0.0 |
| `darkV8CssDistFilename` | Removed | `baseCssDistFilename` | v2.x | v3.0.0 |
| `lightCssDistFilename` | Removed | `baseCssDistFilename` | v2.x | v3.0.0 |
| `lightV8CssDistFilename` | Removed | `baseCssDistFilename` | v2.x | v3.0.0 |
| `withLongNumerals` | Removed | `withLongNumeralsSupport` | v2.x | v3.0.0 |
| `@elastic/filesaver` | Removed | `file-saver` | v2.x | v3.0.0 |
| `DataGrid` component | Removed | `DefaultDiscoverTable` | v2.x | v3.0.0 |
| `newExperience` setting | Removed | N/A (default behavior) | v2.x | v3.0.0 |

### Migration Guide

#### CssDistFilename Migration

The theme-specific CSS filename exports were deprecated in favor of a unified approach using `baseCssDistFilename` combined with theme configuration.

```typescript
// Before (deprecated)
import { 
  darkCssDistFilename, 
  lightCssDistFilename,
  darkV8CssDistFilename,
  lightV8CssDistFilename 
} from '@osd/ui-shared-deps';

// After
import { baseCssDistFilename } from '@osd/ui-shared-deps';
// Theme selection is handled through theme configuration
```

#### HTTP Fetch Options Migration

The `withLongNumerals` option was renamed to `withLongNumeralsSupport` for clarity.

```typescript
// Before (deprecated)
const response = await http.fetch('/api/data', {
  withLongNumerals: true
});

// After
const response = await http.fetch('/api/data', {
  withLongNumeralsSupport: true
});
```

#### File Saver Migration

The `@elastic/filesaver` package (last published 7 years ago) was replaced with the actively maintained `file-saver` package.

```typescript
// Before
// @ts-expect-error - no types available
import { saveAs } from '@elastic/filesaver';

// After
import { saveAs } from 'file-saver';
// TypeScript types available via @types/file-saver
```

Affected files:
- `src/plugins/console/public/application/containers/main/main.tsx`
- `src/plugins/inspector/public/views/data/lib/export_csv.ts`
- `src/plugins/saved_objects_management/public/management_section/objects_table/saved_objects_table.tsx`
- `src/plugins/vis_type_table/public/utils/convert_to_csv_data.ts`

#### Discover Table Migration

The `newExperience` DataGrid table option was removed. The `DefaultDiscoverTable` is now the only supported table implementation.

```typescript
// Before - DataGrid was available via newExperience setting
// The DiscoverOptions component allowed toggling between tables

// After - DefaultDiscoverTable is used exclusively
// No configuration needed
```

## Limitations

- Breaking change: Plugins using deprecated APIs will fail to compile against v3.0.0
- No automatic migration path for custom plugins
- Plugins must be updated before upgrading to v3.0.0

## Change History

- **v3.0.0** (2025-05-06): Removed deprecated CssDistFilename exports, withLongNumerals option, @elastic/filesaver dependency, and newExperience Discover table option


## References

### Documentation
- [Breaking Changes Documentation](https://docs.opensearch.org/3.0/breaking-changes/): Official v3.0.0 breaking changes
- [file-saver npm package](https://www.npmjs.com/package/file-saver): Replacement for @elastic/filesaver

### Pull Requests
| Version | PR | Description | Related Issue |
|---------|-----|-------------|---------------|
| v3.0.0 | [#9446](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9446) | Remove deprecated CssDistFilename | [#9253](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/9253) |
| v3.0.0 | [#9448](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9448) | Remove withLongNumerals in HttpFetchOptions | [#9253](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/9253) |
| v3.0.0 | [#9484](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9484) | Remove @elastic/filesaver | [#9341](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/9341) |
| v3.0.0 | [#9531](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9531) | Remove newExperience table option | [#9253](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/9253) |
| v2.x | [#5592](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/5592) | Deprecate withLongNumerals |   |
| v2.x | [#7625](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7625) | Deprecate CssDistFilename |   |
| v2.x | [#9511](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9511) | Deprecate newExperience table option |   |

### Issues (Design / RFC)
- [Issue #9253](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/9253): Planned Breaking Changes for 3.0
- [Issue #9341](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/9341): Remove @elastic/filesaver dependency
