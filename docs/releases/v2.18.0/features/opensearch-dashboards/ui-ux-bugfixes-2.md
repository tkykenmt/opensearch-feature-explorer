# UI/UX Bugfixes (2)

## Summary

This release item addresses multiple UI/UX issues in OpenSearch Dashboards v2.18.0, focusing on responsive design improvements for the home page, page header, recent menu, and getting started cards. These fixes enhance the user experience across different screen sizes and improve visual consistency.

## Details

### What's New in v2.18.0

Four PRs were merged to fix various UI/UX issues:

1. **Recent Menu Title Update** - Changed the header recent menu title from "Recent" to "Recent assets" for clarity
2. **Home Page Small Screen Fixes** - Added horizontal scrollbar for workspace initial page on small screens
3. **Page Header Responsive Fixes** - Fixed padding, margins, and responsive behavior of the page header
4. **Getting Started Cards Redesign** - Updated content, styling, and visual design of use case getting started cards

### Technical Changes

#### Recent Menu Title (#8529)
- Updated `recent_items.tsx` to use i18n translation for "Recent assets" title
- Improved accessibility with proper internationalization support

#### Home Page Small Screen Display (#8554)
- Added `eui-xScroll` class for horizontal scrolling on small screens
- Changed container width from fixed `1264px` to `max-width: 1264px; width: 100%`
- Fixed OpenSearch logo position with `position: fixed`
- Increased use case card minimum width from `235px` to `240px`
- Added responsive width styling to workspace initial flex group

#### Page Header Responsive Behavior (#8600)
- Fixed incorrect right/left margin on second row
- Prevented title from wrapping too quickly
- Added `eui-textBreakWord` class for proper title wrapping
- Fixed vertical alignment of title, health badge, and other elements
- Added proper spacing between left/right content on larger screens
- Reduced vertical spacing inconsistencies on smaller screens
- Updated line-height to match button size for vertical centering

#### Getting Started Cards (#8614)
- Removed card titles (hidden via CSS) for cleaner appearance
- Added icon-based visual design with `EuiIcon` components
- Updated card descriptions for consistency across use cases
- Changed footer styling to use `EuiTextColor` with subdued color
- Added new CSS class `usecaseOverviewGettingStartedCard` for consistent styling
- Removed sample data card from search overview (kept only in essentials)
- Added Discover card to search use case overview

### Components Changed

| Component | File | Changes |
|-----------|------|---------|
| Recent Items | `recent_items.tsx` | Title i18n update |
| Workspace Initial | `workspace_initial.tsx`, `workspace_initial.scss` | Responsive layout fixes |
| Header | `header.tsx`, `header.scss` | Padding and responsive fixes |
| Sample Data Card | `sample_data_card.tsx` | New card styling |
| Search Use Case | `search_use_case_setup.tsx` | Card redesign |
| Get Started Cards | `get_started_cards.tsx` | Icon and footer updates |
| Setup Overview | `setup_overview.tsx`, `setup_overview.scss` | Card styling overrides |

### Usage Example

The getting started cards now use a consistent pattern:

```tsx
{
  id: 'get_start_discover',
  icon: <EuiIcon type="compass" size="l" color="primary" />,
  title: '',  // Hidden via CSS
  description: 'Explore data to uncover and discover insights.',
  footer: (
    <EuiTextColor color="subdued">
      <EuiI18n token="workspace.essential_overview.discover.card.footer" default="Discover" />
    </EuiTextColor>
  ),
  navigateAppId: DISCOVER_APP_ID,
  order: 20,
}
```

## Limitations

- The horizontal scrollbar on small screens may not be ideal for all use cases but prevents content overflow
- Card titles are hidden via CSS rather than removed from the component structure

## Related PRs

| PR | Description |
|----|-------------|
| [#8529](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8529) | Update the title of header recent menu |
| [#8554](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8554) | Fix new home page small screen display issues |
| [#8600](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8600) | Fix padding and responsive behavior of page header |
| [#8614](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8614) | Update content and styling of use case getting started cards |

## References

- [OpenSearch Dashboards Repository](https://github.com/opensearch-project/OpenSearch-Dashboards)
