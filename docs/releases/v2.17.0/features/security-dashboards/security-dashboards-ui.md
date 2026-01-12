---
tags:
  - dashboards
  - neural-search
  - security
---

# Security Dashboards UI Enhancements

## Summary

OpenSearch v2.17.0 introduces significant UI/UX improvements to the Security Dashboards Plugin as part of the "Look & Feel" initiative. These changes modernize the interface with smaller, compressed UI components, updated page headers, improved avatar placement, and consistent density across all security-related pages.

## Details

### What's New in v2.17.0

This release focuses on visual consistency and density improvements across the Security Dashboards Plugin:

1. **Smaller and Compressed Components**: Replaced standard EUI components with their smaller/compressed variants
2. **Updated Page Headers**: New page header system supporting the updated UX when `home:useNewHomePage` is enabled
3. **Avatar Relocation**: Account avatar conditionally moves to the left navigation when the new home page layout is active
4. **Consistency and Density Improvements**: Standardized font sizes, semantic headers, smaller tabs, and context menus

### Technical Changes

#### Component Migration

The following EUI components were migrated to their smaller/compressed variants:

| Original Component | New Component |
|-------------------|---------------|
| `EuiButton` | `EuiSmallButton` |
| `EuiButtonEmpty` | `EuiSmallButtonEmpty` |
| `EuiButtonIcon` | `EuiSmallButtonIcon` |
| `EuiFieldText` | `EuiCompressedFieldText` |
| `EuiFieldPassword` | `EuiCompressedFieldPassword` |
| `EuiComboBox` | `EuiCompressedComboBox` |
| `EuiFormRow` | `EuiCompressedFormRow` |
| `EuiSwitch` | `EuiCompressedSwitch` |
| `EuiRadioGroup` | `EuiCompressedRadioGroup` |
| `EuiSuperSelect` | `EuiCompressedSuperSelect` |
| `EuiTextArea` | `EuiCompressedTextArea` |

#### New Header Components

New header components were introduced to support the updated UX:

```typescript
// public/apps/configuration/header/header-components.tsx
export const PageHeader = (props: HeaderProps & DescriptionProps & ControlProps) => {
  const useNewUx = props.coreStart.uiSettings.get('home:useNewHomePage');
  // Conditionally renders new header controls or fallback component
};

export const HeaderButtonOrLink = React.memo((props: HeaderProps & ControlProps) => {
  // Renders header controls in the app right controls area
});
```

#### Avatar Placement Logic

The account avatar now conditionally appears in the left navigation:

```typescript
// public/apps/account/account-app.tsx
const isPlacedInLeftNav = coreStart.uiSettings.get('home:useNewHomePage');

coreStart.chrome.navControls[isPlacedInLeftNav ? 'registerLeftBottom' : 'registerRight']({
  order: isPlacedInLeftNav ? 10000 : 2000,
  mount: (element: HTMLElement) => { /* ... */ }
});
```

#### Density Improvements

| Area | Change |
|------|--------|
| Context Menus | Removed popover padding, using `panelPaddingSize="none"` and `size="s"` |
| Paragraph Font Size | Standardized to 15.75px (next theme) / 14px (V7 theme) via `EuiText size="s"` |
| Headers | Semantic headers (H1 on main pages, H2 on modals/flyouts) |
| Tabs | Using small tabs via `size="s"` |
| Popovers | Small padding on popovers |

### Affected Pages

All security-related pages received UI updates:

- Get Started
- Authentication and Authorization
- Internal Users (list and edit)
- Roles (list, create, edit, view)
- Role Mapping
- Permissions
- Tenants (manage and configure)
- Audit Logs (view and edit settings)
- Account modals (password reset, tenant switch, role info)

### Usage Example

The new page header pattern:

```tsx
<PageHeader
  navigation={props.depsStart.navigation}
  coreStart={props.coreStart}
  descriptionControls={descriptionData}
  appRightControls={buttonData}
  fallBackComponent={
    <EuiPageHeader>
      <EuiText size="s">
        <h1>Page Title</h1>
      </EuiText>
    </EuiPageHeader>
  }
  resourceType={ResourceType.roles}
/>
```

### Migration Notes

These changes are backward compatible. The UI automatically adapts based on the `home:useNewHomePage` setting:

- **New UX enabled**: Uses new header controls, avatar in left nav, updated styling
- **New UX disabled**: Falls back to previous UI patterns

## Limitations

- The new header controls require the navigation plugin's `HeaderControl` component
- Avatar placement in left nav requires `home:useNewHomePage` to be enabled
- Some visual changes may require theme updates to fully take effect

## References

### Documentation
- [Security Dashboards Plugin Repository](https://github.com/opensearch-project/security-dashboards-plugin)
- [OpenSearch Dashboards Look & Feel Guidelines](https://github.com/AMoo-Miki/OpenSearch-Dashboards/tree/header-collective)

### Pull Requests
| PR | Description |
|----|-------------|
| [#2079](https://github.com/opensearch-project/security-dashboards-plugin/pull/2079) | Use smaller and compressed variants of buttons and form components |
| [#2082](https://github.com/opensearch-project/security-dashboards-plugin/pull/2082) | Conditionally change where avatar shows up |
| [#2083](https://github.com/opensearch-project/security-dashboards-plugin/pull/2083) | Adds page headers for updated UX |
| [#2101](https://github.com/opensearch-project/security-dashboards-plugin/pull/2101) | Consistency and density improvements |

## Related Feature Report

- [Full feature documentation](../../../features/security-dashboards/security-dashboards-plugin.md)
