---
tags:
  - dashboards
---

# Dashboards Navigation

## Summary

This bugfix ensures that the `disabled` prop is correctly passed to `EuiSideNavItem` components for navigation links. Previously, navigation items that were registered with a disabled status (`AppNavLinkStatus.disabled`) were not visually or functionally disabled in the side navigation, causing inconsistent behavior. This fix respects the `AppNavLinkStatus` field from application registration.

## Details

### What's New in v3.4.0

The fix adds proper propagation of the `isDisabled` property from the navigation link item to the `EuiSideNavItem` component's `disabled` prop.

### Technical Changes

#### Code Change

The fix is a single-line addition in `collapsible_nav_groups.tsx`:

```typescript
// src/core/public/chrome/ui/header/collapsible_nav_groups.tsx
return {
  id: `${link.id}-${link.title}`,
  name: <EuiText>{link.title}</EuiText>,
  onClick: euiListItem.onClick,
  href: euiListItem.href,
  emphasize: euiListItem.isActive,
  className: `nav-link-item ${className || ''}`,
  buttonClassName: 'nav-link-item-btn',
  'data-test-subj': euiListItem['data-test-subj'],
  'aria-label': link.title,
  disabled: euiListItem.isDisabled,  // NEW: Pass disabled state
};
```

#### Affected Components

| Component | Change |
|-----------|--------|
| `collapsible_nav_groups.tsx` | Added `disabled` prop mapping |

### Usage Example

When registering an application with a disabled navigation link:

```typescript
// Plugin registration with disabled nav link
core.application.register({
  id: 'myPlugin',
  title: 'My Plugin',
  navLinkStatus: AppNavLinkStatus.disabled,
  mount: async (params) => {
    // ...
  }
});
```

The navigation item will now correctly appear disabled in the side navigation, preventing user interaction and displaying appropriate visual styling.

### Migration Notes

No migration required. This is a bugfix that automatically takes effect for any applications using `AppNavLinkStatus.disabled`.

## Limitations

- Only affects the collapsible navigation groups component
- Visual styling of disabled items depends on the EUI theme

## References

### Documentation
- [OpenSearch Dashboards Quickstart Guide](https://docs.opensearch.org/3.0/dashboards/quickstart/): Navigation documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#10678](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10678) | Ensure the disabled prop gets passed to the EuiSideNavItem for navlinks |

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch-dashboards/navigation.md)
