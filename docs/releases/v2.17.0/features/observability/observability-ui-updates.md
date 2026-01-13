---
tags:
  - domain/observability
  - component/server
  - dashboards
  - observability
  - search
  - sql
---
# Observability UI Updates

## Summary

OpenSearch Dashboards Observability plugin received comprehensive UI updates in v2.17.0 to improve consistency and usability across the Traces, Services, Logs, and Dashboards views. These changes align the observability interfaces with the updated header design patterns used throughout OpenSearch Dashboards.

## Details

### What's New in v2.17.0

The UI updates focus on three main areas of the Observability plugin:

1. **Traces/Services UI** - Updated header layout and improved filter button behavior
2. **Observability Dashboards UI** - Modernized dashboard listing interface
3. **Logs UI** - Refreshed log explorer with improved controls

### Technical Changes

#### Traces/Services UI Updates (PR #2078)

The Traces and Services pages received header updates to conform with the new design patterns:

| Component | Change |
|-----------|--------|
| Page Header | Updated to match new header design |
| Filter Button | Fixed double-click bug where filter would get stuck open |
| Global Filter | Separated filter components for better layout |

The filter button now properly closes when re-clicked or when an option is selected, improving the user experience.

#### Observability Dashboards UI Updates (PR #2090)

The Observability Dashboards listing page was updated with:

| Component | Change |
|-----------|--------|
| Page Header | Aligned with new header design |
| Actions Button | Repositioned next to search bar |
| Create Button | Added plus icon for visual clarity |
| Search Bar | Integrated with actions in a flex group |

#### Logs UI Updates (PR #2092)

The Logs explorer received several improvements:

| Component | Change |
|-----------|--------|
| Page Header | Updated to conform with header changes |
| Type Filter | Remade to work properly with new layout |
| PPL Button | Adjusted positioning for better alignment |
| Actions Menu | Moved from header to table toolbar |
| Search/Filter | Added inline search with type filter dropdown |

### UI Component Changes

The updates involved modifications to several React components:

| File | Purpose |
|------|---------|
| `search_bar.tsx` | Updated search bar with integrated filter button |
| `custom_panel_table.tsx` | Repositioned actions and create buttons |
| `saved_objects_table.tsx` | Added inline search and type filter |
| `home.tsx` | Simplified header, moved actions to table |

### Usage Example

The new Logs UI provides a more streamlined experience:

```
┌─────────────────────────────────────────────────────────────┐
│  Logs                                                       │
├─────────────────────────────────────────────────────────────┤
│  [🔍 Search saved queries    ] [Type ▼] [Actions ▼]        │
├─────────────────────────────────────────────────────────────┤
│  □  Name          Type           Query                      │
│  □  My Query      Query          source = logs | ...        │
│  □  CPU Metrics   Visualization  source = metrics | ...     │
└─────────────────────────────────────────────────────────────┘
```

## Limitations

- UI changes are primarily cosmetic and do not affect underlying functionality
- Some snapshot tests required updates due to component structure changes

## References

### Documentation
- [Trace Analytics Documentation](https://docs.opensearch.org/2.17/observing-your-data/trace/ta-dashboards/): Official trace analytics plugin documentation
- [Observability Overview](https://docs.opensearch.org/2.17/observing-your-data/): OpenSearch Observability documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#2078](https://github.com/opensearch-project/dashboards-observability/pull/2078) | Traces/Services UI update |
| [#2090](https://github.com/opensearch-project/dashboards-observability/pull/2090) | Observability dashboards UI update |
| [#2092](https://github.com/opensearch-project/dashboards-observability/pull/2092) | Logs UI update |

## Related Feature Report

- [Full feature documentation](../../../../features/dashboards-observability/dashboards-observability-observability-ui.md)
