---
tags:
  - opensearch-dashboards
---
# OUI Bump

## Summary

OpenSearch Dashboards v2.16.0 updates the OpenSearch UI (OUI) component library from version 1.7.0 to 1.8.0. This update brings UI improvements including a new Split Button component, enhanced accessibility, faster animations, and various bug fixes.

## Details

### What's New in v2.16.0

The OUI 1.8.0 update includes:

| Category | Changes |
|----------|---------|
| New Components | Split Button component for combined action/dropdown buttons |
| Accessibility | Improved screenreader support for data grid copy/paste |
| UI Polish | Faster animations for modals, popovers, and tooltips |
| Typography | Base font size set to 18px in Next Theme |
| Buttons | Consistent font sizes, reverted font-weight to normal |
| Forms | Compressed form components, color-picker, and combobox |
| Bug Fixes | Breadcrumb alignment, data grid lines, resizable panel collapse button |

### Technical Changes

The update modifies the `@opensearch-project/oui` dependency across multiple packages:

| Package | Change |
|---------|--------|
| `package.json` | `1.7.0` → `1.8.0` |
| `packages/osd-ui-framework/package.json` | `1.7.0` → `1.8.0` |
| `packages/osd-ui-shared-deps/package.json` | `1.7.0` → `1.8.0` |
| Test plugin packages | `1.7.0` → `1.8.0` |

### Key OUI 1.8.0 Features

**Split Button Component**
A new component combining a primary action button with a dropdown for additional options.

**Accessibility Improvements**
- Eliminated screenreader content when copying/pasting data grid tables
- Fixed info tooltip display on icon-only buttons

**Animation Performance**
Faster animations for modals, popovers, and tooltips improve perceived responsiveness.

**Form Component Updates**
- Compressed variants for form components
- Updated color-picker and combobox components
- Filter button improvements

## Limitations

- This is a dependency update; no new APIs are exposed directly to plugins
- The PR was labeled "Skip-Changelog" indicating minimal user-facing impact

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#7363](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7363) | Bump OUI to 1.8.0 | - |

### OUI Release
- [OUI 1.8.0 Release Notes](https://github.com/opensearch-project/oui/releases/tag/1.8.0)
