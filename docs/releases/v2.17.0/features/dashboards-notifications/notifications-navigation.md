# Notifications Navigation

## Summary

This enhancement updates the navigation display name for the Notifications plugin in OpenSearch Dashboards. When the new navigation system is enabled, the plugin now appears as "Notification channels" instead of "Notifications" in the Settings and Setup navigation group. Additionally, a description has been added to help users understand the plugin's purpose.

## Details

### What's New in v2.17.0

The PR introduces two key changes to improve the navigation experience:

1. **Renamed navigation item**: The parent item name in the Settings and Setup nav group is changed from "Notifications" to "Notification channels" for better clarity
2. **Added description**: A new description "Configure and organize notification channels" is displayed in the left navigation panel

### Technical Changes

#### Navigation Registration Changes

The plugin registration now includes a description for the left navigation:

```typescript
core.application.register({
  id: PLUGIN_NAME,
  title: this.title,
  category: core.chrome?.navGroup?.getNavGroupEnabled() ? undefined : DEFAULT_APP_CATEGORIES.management,
  order: 9060,
  description: i18n.translate('dashboards-notifications.leftNav.notifications.description', {
    defaultMessage: 'Configure and organize notification channels.'
  }),
  // ...
});
```

When adding nav links to the Settings and Setup group, the title is now explicitly set:

```typescript
core.chrome.navGroup.addNavLinksToGroup(DEFAULT_NAV_GROUPS.settingsAndSetup, [
  {
    id: PLUGIN_NAME,
    title: 'Notification channels'
  }
]);
```

### Usage Example

When the new navigation is enabled (`navGroup.getNavGroupEnabled()` returns `true`), users will see:

- **Settings and Setup** (nav group)
  - **Notification channels** (parent item with description)
    - Channels
    - Email senders
    - Email recipient groups

### Migration Notes

No migration required. This is a UI-only change that takes effect automatically when using the new navigation system.

## Limitations

- The renamed navigation item only appears when the new navigation system is enabled
- Legacy navigation continues to show "Notifications" under the Management category

## Related PRs

| PR | Description |
|----|-------------|
| [#234](https://github.com/opensearch-project/dashboards-notifications/pull/234) | Change parent item name for new navigation |

## References

- [OpenSearch Notifications Documentation](https://docs.opensearch.org/2.17/observing-your-data/notifications/index/)
- [dashboards-notifications Repository](https://github.com/opensearch-project/dashboards-notifications)

## Related Feature Report

- [Full feature documentation](../../../../features/dashboards-notifications/dashboards-notifications.md)
