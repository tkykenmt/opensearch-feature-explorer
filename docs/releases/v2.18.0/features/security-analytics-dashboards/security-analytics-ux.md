---
tags:
  - domain/security
  - component/dashboards
  - dashboards
  - search
  - security
---
# Security Analytics UX

## Summary

OpenSearch v2.18.0 introduces comprehensive UX improvements to the Security Analytics Dashboards plugin as part of the "Fit and Finish" initiative. These changes enhance the visual consistency, navigation, and usability of the Security Analytics interface, including updated page layouts, compressed UI elements, improved navigation menu structure, and context-aware page titles.

## Details

### What's New in v2.18.0

The Security Analytics UX improvements in v2.18.0 focus on three main areas:

1. **Navigation and Menu Structure**: Updated category labels to flatten menus in the Analytics (All) use case, improving discoverability of Security Analytics features
2. **Visual Consistency**: Standardized spacing, padding, and typography across all Security Analytics pages
3. **Usability Enhancements**: Added compressed search bars and filters, improved button placement, and context-aware page titles

### Technical Changes

#### Navigation Updates

The navigation structure was updated to show Security Analytics features in the Analytics (All) use case:

| Application | Order | Category | Visibility |
|-------------|-------|----------|------------|
| Threat alerts | 300 | investigate | All nav groups |
| Findings | 400 | investigate | All nav groups |
| Correlations | 500 | investigate | All nav groups |
| Threat detectors | 600 | configure | All nav groups |
| Detection rules | 700 | configure | All nav groups |
| Correlation rules | 800 | configure | All nav groups |
| Threat intelligence | 900 | configure | All nav groups |
| Log types | 1000 | configure | All nav groups |

#### UI Component Changes

| Component | Change | Impact |
|-----------|--------|--------|
| ContentPanel title | Changed from H2 to H3 | Improved visual hierarchy |
| ContentPanel padding | Standardized to 16px | Consistent spacing |
| Search bars | Added `compressed: true` | Smaller, cleaner appearance |
| Filter buttons | Added `compressed: true` | Consistent with search bars |
| Page gutters | Changed to `gutterSize='m'` | Consistent 16px spacing |
| Create detector button | Added plus icon | Better visual affordance |
| Delete button | Moved to left of search bar | Improved bulk action visibility |

#### Overview Page Enhancements

- Context-aware page title based on current navigation group
- Updated Getting Started card with smaller title element (`h4` with `titleSize='s'`)
- Removed hover state from empty message widgets
- Changed "total active alerts" to "total active threat alerts"
- Added period to "Correlate events" description

#### Alerts and Findings Pages

- Moved tabs to the top of the page
- Moved refresh and action buttons inside the table
- Added alerts graph above the table in each tab
- Compressed search and filter components

#### Detectors Page

- Added bulk delete button to the left of the search bar
- Moved Actions dropdown to require single selection
- Added plus icon to "Create detector" button

### Usage Example

The navigation category update ensures Security Analytics appears in the Analytics (All) use case:

```typescript
// Navigation links configuration
const navlinks = [
  { id: GETTING_STARTED_NAV_ID, showInAllNavGroup: true },
  { id: THREAT_ALERTS_NAV_ID, showInAllNavGroup: true },
  { id: FINDINGS_NAV_ID, showInAllNavGroup: true },
  { id: CORRELATIONS_NAV_ID, showInAllNavGroup: true },
  { id: PLUGIN_NAME, category: DEFAULT_APP_CATEGORIES.configure, 
    title: 'Threat detection', showInAllNavGroup: true, order: 600 },
  { id: DETECTORS_NAV_ID, parentNavLinkId: PLUGIN_NAME, showInAllNavGroup: true },
  // ... additional nav links
];
```

### Source Refresh Interval Enhancement

Added HOURS option for source refresh interval in threat intelligence configuration, providing more flexibility for data source refresh scheduling.

## Limitations

- The context-aware page title requires the new navigation group feature to be enabled
- Some visual changes may appear different when `newHomePage` feature flag is disabled

## References

### Documentation
- [Security Analytics Documentation](https://docs.opensearch.org/2.18/security-analytics/): Official documentation
- [OpenSearch-Dashboards PR #8332](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8332): Related navigation changes in core Dashboards

### Pull Requests
| PR | Description |
|----|-------------|
| [#1169](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1169) | Update category to flatten menus in analytics(all) use case |
| [#1174](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1174) | Fit and Finish UX Fixes |
| [#1175](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1175) | Security analytics overview page improvements |
| [#1197](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1197) | Added HOURS option for source refresh interval |
| [#2121](https://github.com/opensearch-project/security-dashboards-plugin/pull/2121) | Update category label for security plugin |
| [#2130](https://github.com/opensearch-project/security-dashboards-plugin/pull/2130) | Fix button label |

## Related Feature Report

- Full feature documentation
