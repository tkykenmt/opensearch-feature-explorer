# OUI Updates

## Summary

OpenSearch Dashboards v2.18.0 includes a series of updates to the OpenSearch UI (OUI) component library, upgrading from version 1.12 to 1.15. These updates bring visual improvements, font changes, and new SCSS variables for better theming consistency across the dashboard interface.

## Details

### What's New in v2.18.0

The OUI library was incrementally updated through three PRs:

1. **OUI 1.13** - Initial update with general improvements
2. **OUI 1.14** - Removed Fira Code font in favor of Source Code Pro for the v9 theme
3. **OUI 1.15** - Introduced official `$euiSideNavBackgroundColor` SCSS variable

### Technical Changes

#### Font Changes

OUI 1.14 replaced the Fira Code monospace font with Source Code Pro as part of the v9 theme standardization. This change affects code blocks, console output, and other monospace text throughout the dashboard.

#### New SCSS Variables

OUI 1.15 introduced the `$euiSideNavBackgroundColor` variable, replacing the temporary `$ouiSideNavBackgroundColorTemp` variable that was previously defined locally in OpenSearch Dashboards.

| Old Variable | New Variable | Purpose |
|--------------|--------------|---------|
| `$ouiSideNavBackgroundColorTemp` | `$euiSideNavBackgroundColor` | Side navigation background color |

#### Files Updated

The following components were updated to use the new official OUI variable:

- `src/core/public/chrome/ui/header/collapsible_nav_group_enabled.scss` - Main navigation styling
- `src/plugins/workspace/public/components/workspace_selector/workspace_selector.scss` - Workspace selector styling

#### Package Updates

All OUI package references were updated across multiple `package.json` files:

```json
"@elastic/eui": "npm:@opensearch-project/oui@1.15.0"
```

### Usage Example

The side navigation background color is now applied using the official OUI variable:

```scss
.context-nav-wrapper {
  background-color: $euiSideNavBackgroundColor;
}
```

### Migration Notes

If you have custom plugins or themes that reference `$ouiSideNavBackgroundColorTemp`, update them to use `$euiSideNavBackgroundColor` instead.

## Limitations

- These are maintenance updates with no new UI components
- Font changes may affect the visual appearance of code blocks in existing dashboards

## References

### Documentation
- [OUI Repository](https://github.com/opensearch-project/oui): OpenSearch UI component library

### Pull Requests
| PR | Description |
|----|-------------|
| [#8246](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8246) | Update OUI to 1.13 |
| [#8372](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8372) | Update OUI to 1.14 (font changes) |
| [#8480](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8480) | Update OUI to 1.15 and consume $euiSideNavBackgroundColor |

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch-dashboards/oui.md)
