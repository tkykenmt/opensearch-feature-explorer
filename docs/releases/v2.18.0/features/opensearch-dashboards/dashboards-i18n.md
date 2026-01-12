---
tags:
  - dashboards
  - search
---

# Dashboards i18n

## Summary

This release fixes dynamic uses of i18n and corrects unprefixed and duplicate i18n identifiers in the dataSourceManagement plugin. These fixes ensure proper internationalization support and enable translation validation in CI/CD workflows.

## Details

### What's New in v2.18.0

The dataSourceManagement plugin had several i18n issues that prevented proper translation validation:

1. **Dynamic i18n usage**: Some code used dynamic string construction for i18n keys, which breaks static analysis
2. **Unprefixed identifiers**: Some i18n keys lacked the required plugin prefix
3. **Duplicate identifiers**: Some i18n keys were reused with different default messages

### Technical Changes

#### Fixed Dynamic i18n Patterns

Before (problematic):
```typescript
// Dynamic default message - breaks translation extraction
i18n.translate('dataSourceManagement.createDataSource.description', {
  defaultMessage: useNewUX ? 'Connect OpenSearch Cluster' : 'Open Search',
})
```

After (fixed):
```typescript
// Separate static translations
useNewUX
  ? i18n.translate('dataSourcesManagement.dataSources.createOpenSearchDataSourceBreadcrumbs', {
      defaultMessage: 'Connect OpenSearch Cluster',
    })
  : i18n.translate('dataSourcesManagement.legacyUX.dataSources.createOpenSearchDataSourceBreadcrumbs', {
      defaultMessage: 'Open Search',
    })
```

#### Fixed Unprefixed Identifiers

| Before | After |
|--------|-------|
| `dataSource.localCluster` | `dataSourcesManagement.localCluster` |
| `dataSource.fetchDataSourceError` | `dataSourcesManagement.error.fetchDataSourceById` |
| `dataSource.management.dataSourceColumn` | `dataSourcesManagement.dataSourceColumn` |
| `dataSourceError.dataSourceErrorMenuHeaderLink` | `dataSourcesManagement.dataSourceError.dataSourceErrorMenuHeaderLink` |
| `datasources.associatedObjectsTab.*` | `dataSourcesManagement.associatedObjectsTab.*` |

#### New Components

| Component | Description |
|-----------|-------------|
| `DataSourceOptionalLabelSuffix` | Reusable component for optional field labels with proper i18n |

#### Refactored Toast Messages

Changed from dynamic i18n in toast handlers to pre-translated messages:

```typescript
// Before
handleDisplayToastMessage({
  id: 'dataSourcesManagement.createDataSource.existingDatasourceNames',
  defaultMessage: 'Unable to fetch some resources.',
});

// After
handleDisplayToastMessage({
  message: i18n.translate('dataSourcesManagement.createDataSource.existingDatasourceNames', {
    defaultMessage: 'Unable to fetch some resources.',
  }),
});
```

### Files Changed

| File | Changes |
|------|---------|
| `breadcrumbs.ts` | Fixed dynamic breadcrumb text |
| `constants.tsx` | Fixed unprefixed LocalCluster identifier |
| `create_button.tsx` | Split dynamic button text into separate translations |
| `create_data_source_form.tsx` | Refactored section headers and optional labels |
| `create_data_source_wizard.tsx` | Changed toast message handling |
| `data_source_selectable.tsx` | Fixed error message i18n |
| `data_source_selector.tsx` | Fixed placeholder and prepend text |
| `data_source_table.tsx` | Changed toast message handling |
| `associated_objects_*.tsx` | Fixed unprefixed identifiers |

### Migration Notes

No migration required. This is a bugfix that improves i18n compliance without changing functionality.

## Limitations

- This fix is specific to the dataSourceManagement plugin
- Other plugins received similar fixes in separate PRs

## References

### Documentation
- [i18n Framework Documentation](https://github.com/opensearch-project/OpenSearch-Dashboards/tree/main/packages/osd-i18n)

### Pull Requests
| PR | Description |
|----|-------------|
| [#8394](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8394) | Main implementation (merged to main) |
| [#8516](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8516) | Backport to 2.x branch |

### Issues (Design / RFC)
- [Issue #8394](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8394): Original PR

## Related Feature Report

- [Full feature documentation](../../../features/opensearch-dashboards/i18n-localization.md)
