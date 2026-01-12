---
tags:
  - dashboards
---

# Global Banner Support via UI Settings

## Summary

OpenSearch Dashboards v3.2.0 enhances the Banner Plugin with UI Settings integration, enabling administrators to configure and update the global banner dynamically through the Advanced Settings interface without requiring server restarts. Changes take effect in real-time, providing a more flexible and user-friendly banner management experience.

## Details

### What's New in v3.2.0

This release adds UI Settings support to the Banner Plugin, allowing banner configuration through the Dashboards Management interface:

- Server-side registration of banner settings as UI Settings
- Client-side subscription to setting changes for live updates
- Real-time banner updates without page reload
- YAML configuration values used as default values for UI Settings
- New banner settings category in Advanced Settings

### Technical Changes

#### Architecture Changes

```mermaid
graph TB
    subgraph Configuration
        YML[opensearch_dashboards.yml]
        UISettings[UI Settings / Advanced Settings]
    end
    
    subgraph Server["Server Side"]
        ServerPlugin[BannerPlugin Server]
        UISettingsReg[UI Settings Registration]
        GetConfigRoute[/api/_plugins/_banner/content]
    end
    
    subgraph Browser["Browser Side"]
        ClientPlugin[BannerPlugin Client]
        GlobalBanner[GlobalBanner Component]
    end
    
    YML -->|default values| UISettingsReg
    UISettings -->|user overrides| UISettingsReg
    UISettingsReg --> ServerPlugin
    ServerPlugin --> GetConfigRoute
    GetConfigRoute -->|reads from UI Settings| ClientPlugin
    ClientPlugin --> GlobalBanner
```

#### New Components

| Component | Description |
|-----------|-------------|
| `ui_settings.ts` | Defines banner UI settings with schema validation |
| `getDefaultBannerSettings()` | Returns UI settings configuration for banner |

#### New Configuration (UI Settings)

| Setting | Type | Description | Default |
|---------|------|-------------|---------|
| `banner:active` | boolean | Controls banner visibility | `true` |
| `banner:content` | markdown | Banner message content | `''` |
| `banner:color` | select | Color scheme: `primary`, `warning`, `danger` | `primary` |
| `banner:iconType` | select | Icon: `iInCircle`, `help`, `alert`, `warning`, `check`, `bell` | `iInCircle` |
| `banner:useMarkdown` | boolean | Enable Markdown rendering | `true` |

### Usage Example

1. Navigate to **Dashboards Management** > **Advanced Settings**
2. Search for `banner:` to find banner settings
3. Modify settings:

```
banner:active = true
banner:content = **Maintenance Notice:** System upgrade scheduled for Saturday 2AM UTC
banner:color = warning
banner:iconType = alert
banner:useMarkdown = true
```

4. Save changes - banner updates immediately

### Configuration Priority

Settings are resolved in the following order:
1. User-modified UI Settings (highest priority)
2. YAML configuration values (used as defaults)
3. Built-in defaults (lowest priority)

```yaml
# opensearch_dashboards.yml - sets default values
banner.enabled: true
banner.content: "Default announcement"
banner.color: primary
```

### API Changes

The `/api/_plugins/_banner/content` endpoint now reads from UI Settings instead of directly from YAML configuration:

```typescript
// Server reads from UI Settings client
const uiSettingsClient = context.core.uiSettings.client;
const settings = await uiSettingsClient.getAll();

const config: BannerConfig = {
  content: settings['banner:content'],
  color: settings['banner:color'],
  iconType: settings['banner:iconType'],
  isVisible: Boolean(settings['banner:active']),
  useMarkdown: Boolean(settings['banner:useMarkdown']),
  size: settings['banner:size'],
};
```

### Migration Notes

- Existing YAML configurations continue to work as default values
- UI Settings overrides take precedence over YAML values
- No breaking changes to existing deployments
- Page reload required after changing settings (indicated in UI)

## Limitations

- Settings require page reload to take effect (`requiresPageReload: true`)
- No `banner:size` setting exposed in UI (uses default)
- Settings are global (no per-workspace or per-user configuration)

## References

### Documentation
- [Advanced Settings Documentation](https://docs.opensearch.org/3.0/dashboards/management/advanced-settings/): OpenSearch Dashboards Advanced Settings

### Pull Requests
| PR | Description |
|----|-------------|
| [#10264](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10264) | Add global banner support via UI settings with live updates |

### Issues (Design / RFC)
- [Issue #9861](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/9861): RFC - OpenSearch Dashboards Banner Plugin
- [Issue #9990](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/9990): Meta issue tracking banner plugin development

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch-dashboards/banner-plugin.md)
