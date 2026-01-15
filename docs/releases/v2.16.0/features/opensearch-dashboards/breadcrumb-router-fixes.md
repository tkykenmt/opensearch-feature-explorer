---
tags:
  - opensearch-dashboards
---
# Breadcrumb & Router Fixes

## Summary

Fixed breadcrumb navigation issues for four applications (Assets, Index Pattern Management, Data Sources Management, Application Settings) when the new navigation feature flag is enabled. These applications were migrated from sub-applications within Dashboard Management to standalone applications in the left navigation, which broke their breadcrumb functionality with BrowserRouter.

## Details

### What's New in v2.16.0

This fix addresses breadcrumb navigation issues that occurred when the `navGroupEnabled` feature flag is turned on. The changes ensure breadcrumbs work correctly with BrowserRouter for migrated applications.

### Technical Changes

#### Problem
When new navigation is enabled, four applications were added to the left navigation as standalone apps:
- Assets (Saved Objects Management)
- Index Pattern Management
- Data Sources Management
- Application Settings (Advanced Settings)

Previously, these worked as sub-applications within Dashboard Management, which intercepted `setBreadCrumbs` calls to make breadcrumbs compatible with BrowserRouter and inherit the parent history from OSD core.

After migration to standalone applications, they used `core.chrome.setBreadCrumbs` directly, which doesn't support BrowserRouter.

#### Solution
A new utility function `getScopedBreadcrumbs` was introduced to wrap breadcrumb items with proper router navigation:

```typescript
export const getScopedBreadcrumbs = (
  crumbs: ChromeBreadcrumb[] = [],
  appHistory: ScopedHistory
) => {
  const wrapBreadcrumb = (item: ChromeBreadcrumb, scopedHistory: ScopedHistory) => ({
    ...item,
    ...(item.href ? reactRouterNavigate(scopedHistory, item.href) : {}),
  });
  return crumbs.map((item) => wrapBreadcrumb(item, appHistory));
};
```

#### Updated Plugins
Each affected plugin now wraps breadcrumbs using `getScopedBreadcrumbs`:

| Plugin | File |
|--------|------|
| Advanced Settings | `src/plugins/advanced_settings/public/plugin.ts` |
| Data Source Management | `src/plugins/data_source_management/public/plugin.ts` |
| Index Pattern Management | `src/plugins/index_pattern_management/public/plugin.ts` |
| Saved Objects Management | `src/plugins/saved_objects_management/public/plugin.ts` |

#### Additional Fixes
- Left navigation now shows expandable menu on home page when workspace is enabled
- Workspace overview is now visible in all use cases
- Fixed navigation group display when current nav group is "all"
- Hidden nav links no longer show in navigation groups

## Limitations

- Changes only take effect when the `navGroupEnabled` feature flag is enabled
- No impact on existing application behavior when feature flag is disabled

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#7401](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7401) | Fix breadcrumb issue for 4 new added applications with BrowserRouter | - |
