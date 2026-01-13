---
tags:
  - domain/core
  - component/dashboards
  - dashboards
  - neural-search
---
# Dashboards UI Updates

## Summary

OpenSearch Dashboards v2.17.0 includes UI updates focused on header spacing improvements and OUI (OpenSearch UI) library upgrade to version 1.10.0. These changes enhance the visual consistency and user experience of the application header and navigation components.

## Details

### What's New in v2.17.0

This release updates the OpenSearch UI (OUI) component library from version 1.9.0 to 1.10.0 and refines header spacing throughout the application.

### Technical Changes

#### OUI Library Upgrade

The `@opensearch-project/oui` package was upgraded from 1.9.0 to 1.10.0 across multiple packages:

| Package | Change |
|---------|--------|
| `package.json` | OUI 1.9.0 → 1.10.0 |
| `packages/osd-ui-framework/package.json` | OUI 1.9.0 → 1.10.0 |
| `packages/osd-ui-shared-deps/package.json` | OUI 1.9.0 → 1.10.0 |
| Test plugin packages | OUI 1.9.0 → 1.10.0 |

#### Header Spacing Improvements

The new top navigation header received significant styling updates:

| Component | Change |
|-----------|--------|
| `.newTopNavHeader` | Added padding, gap spacing, and border-bottom for application header |
| `.newTopNavHeaderTitle` | New class for consistent title styling with `font-size: 2rem` |
| `.headerAppActionMenu` | Improved gap spacing for action menu items |
| `.headerRecentItemsButton` | Simplified styling with margin adjustments |

#### Recent Items Button Refactoring

The recent items button was refactored from `EuiHeaderSectionItemButton` to `EuiButtonIcon` with `EuiToolTip`:

- Changed icon from `recentlyViewedApp` to `recent`
- Added tooltip with "Recents" label
- Improved accessibility with `aria-label` and `aria-expanded` attributes
- Consistent button sizing with `size="xs"`

#### Application Title Changes

The application title in the header was updated:

- Changed from `EuiText` with `<h2>` to `EuiTitle` with `<h1>`
- Added `newTopNavHeaderTitle` class for consistent styling
- Improved semantic HTML structure

### Usage Example

The header changes are automatically applied when using the new top navigation. No configuration changes are required.

```typescript
// The header automatically uses the updated styling
// when useNewHomePage is enabled
```

### Migration Notes

- No breaking changes for existing implementations
- Snapshot tests may need updating due to component structure changes
- Custom CSS targeting old header classes may need adjustment

## Limitations

- Header spacing changes are specific to the new top navigation design
- Some styling uses CSS `:has()` selector which may not work in older browsers

## References

### Documentation
- [OUI 1.10.0 Release](https://github.com/opensearch-project/oui/releases)
- [OpenSearch Dashboards Repository](https://github.com/opensearch-project/OpenSearch-Dashboards)

### Pull Requests
| PR | Description |
|----|-------------|
| [#7741](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7741) | Revisit updated header spacing, bump OUI to 1.10.0 |

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch-dashboards/opensearch-dashboards-dashboards-ui-updates.md)
