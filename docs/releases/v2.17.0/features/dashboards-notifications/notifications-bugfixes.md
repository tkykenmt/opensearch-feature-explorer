# Notifications Bugfixes

## Summary

This release includes two bugfixes for the OpenSearch Dashboards Notifications plugin: fixing the link checker CI workflow and persisting the dataSourceId across applications when using the new navigation.

## Details

### What's New in v2.17.0

Two bugfixes were introduced to improve the stability and usability of the Notifications plugin:

1. **Link Checker Fix**: Added missing files (CONTRIBUTING.md, NOTICE) to fix the link checker CI check that was failing due to broken internal links.

2. **DataSourceId Persistence**: Fixed an issue where the selected data source was not persisted when navigating between different Notifications pages (Channels, Email Senders, Email Recipient Groups) under the new navigation system.

### Technical Changes

#### DataSourceId Persistence Implementation

The fix introduces a new hook `useUpdateUrlWithDataSourceProperties` that automatically updates the URL with the current `dataSourceId` when multi-data-source (MDS) is enabled:

```typescript
export function useUpdateUrlWithDataSourceProperties() {
  const dataSourceMenuProps = useContext(DataSourceMenuContext);
  const { dataSourceId, multiDataSourceEnabled } = dataSourceMenuProps;
  const history = useHistory();
  
  useEffect(() => {
    if (multiDataSourceEnabled) {
      history.replace({
        search: queryString.stringify({
          ...currentQuery,
          dataSourceId,
        }),
      });
    }
  }, [dataSourceId, multiDataSourceEnabled]);
}
```

#### New Components

| Component | Description |
|-----------|-------------|
| `useUpdateUrlWithDataSourceProperties` | React hook to persist dataSourceId in URL |
| `dataSourceObservable` | BehaviorSubject to share data source state across the plugin |

#### Modified Files

| File | Changes |
|------|---------|
| `MDSEnabledComponent.tsx` | Added `useUpdateUrlWithDataSourceProperties` hook |
| `PageHeader.tsx` | Integrated URL update hook |
| `EmailSenders.tsx` | Added hook for data source persistence |
| `Main.tsx` | Enhanced data source initialization and state management |
| `plugin.ts` | Added app state updater for default routes with dataSourceId |
| `constants.ts` | Added `dataSourceObservable` for cross-component state |

### Usage Example

When MDS is enabled, navigating to the Channels page will now include the dataSourceId in the URL:

```
/app/notifications-dashboards#/channels?dataSourceId=abc123
```

This ensures that when users navigate between Channels, Email Senders, and Email Recipient Groups, the selected data source is preserved.

## Limitations

- The dataSourceId persistence only applies when multi-data-source is enabled
- URL-based state management may cause issues with very long dataSourceId values

## Related PRs

| PR | Description |
|----|-------------|
| [#242](https://github.com/opensearch-project/dashboards-notifications/pull/242) | Fix link checker - Added missing CONTRIBUTING.md and NOTICE files |
| [#244](https://github.com/opensearch-project/dashboards-notifications/pull/244) | Persist dataSourceId across applications under new Nav change |

## References

- [OpenSearch Notifications Documentation](https://docs.opensearch.org/2.17/observing-your-data/notifications/index/)
- [Backport PR #249 (2.x)](https://github.com/opensearch-project/dashboards-notifications/pull/249)
- [Backport PR #255 (2.17)](https://github.com/opensearch-project/dashboards-notifications/pull/255)

## Related Feature Report

- [Full feature documentation](../../../../features/dashboards-notifications/dashboards-notifications.md)
