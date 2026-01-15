---
tags:
  - opensearch-dashboards
---
# Look & Feel UI Improvements

## Summary

OpenSearch Dashboards v2.16.0 introduces comprehensive UI consistency improvements as part of the "Look & Feel" initiative. These changes standardize component usage across the application, including semantic headers, consistent icon usage, OUI tooltips, small popover padding, and density improvements for Discover and query bar components.

## Details

### What's New in v2.16.0

The Look & Feel improvements in v2.16.0 focus on visual consistency and user experience refinements across multiple areas:

#### Semantic Headers
- Refactored page, modal, and flyout components to use semantic headers for better accessibility and consistent styling

#### Icon Consistency
- Standardized plus icons: replaced `plusInCircle` with `plus` icon for add/create use cases
- Updated recent items icon from SVG to React component for dark mode support
- Migrated recent items icon to OUI library for theme compatibility

#### Tooltip Standardization
- Replaced browser native tooltips with OUI tooltips across header icons (menu, home, dev tools, help, appearance)
- Added OUI tooltips to data components (change filters, saved queries)
- Added tooltips to Discover field icons and visualization toggle legend
- Added tooltips to index pattern source filters table (edit/delete icons)

#### Popover Padding
- Applied small padding (`panelPaddingSize="s"`) to non-context menu popovers
- Updated popovers in: Appearance, Discover Field, Help, Syntax, Visualize, Saved Objects Export, Vis Augmenter, Recent Items

#### Tab Sizing
- Standardized `EuiTabs` and `EuiTabbedContent` to use small size across the application

#### Discover & Query Bar Density
- Updated filter context menu and add filter button styling
- Fixed padding on add/edit filter popovers
- Made data table denser with 6px padding (matching Data Grid medium cell spacing)
- Adjusted field section headers to match field font size
- Fixed doc details flyout link sizes and JSON font size
- Fixed inspector flyout title display and selected view size

#### VisBuilder Improvements
- Applied semantic headers to modals
- Updated flyover icons
- Added tooltips to field detail icons

#### Bug Fixes
- Fixed wrapping of labels in filter by type popover
- Fixed saved query management button alignment and removed erroneous down arrow icon
- Fixed Discover sidebar field icon spacing
- Fixed visualization legend button tooltip positioning

## Limitations

- CSS `:has()` selector used in some styles may not work in older browsers
- Some tooltip changes may require snapshot test updates

## References

### Pull Requests
| PR | Description |
|----|-------------|
| [#7192](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7192) | Refactor to use semantic headers for page, modal & flyout |
| [#7195](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7195) | Consistency of Plus Icons |
| [#7200](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7200) | Update Popover Padding Size |
| [#7231](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7231) | Replace browser tooltip usage with OUI tooltip |
| [#7232](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7232) | Use small EuiTabs and EuiTabbedContent across the board |
| [#7299](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7299) | Density and consistency changes for discover and query bar |
| [#7327](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7327) | Fix wrapping of labels in filter by type popover |
| [#7341](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7341) | Apply missing guidance for visBuilder |
| [#7478](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7478) | Update recent items icon from SVG to react component |
| [#7508](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7508) | Update icon of recent items from OUI library to enable dark mode |
| [#7523](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7523) | Apply small popover padding and add OUI tooltips |
| [#7530](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7530) | Discover and Query Management fix |
