---
tags:
  - dashboards
---

# Notifications Bugfixes

## Summary

OpenSearch Dashboards Notifications v2.18.0 includes several bug fixes focused on improving the Multi-Data-Source (MDS) experience and fixing UI typos. The key fix addresses an issue where the plugin incorrectly defaulted to the local cluster instead of the configured default data source during initial page load.

## Details

### What's New in v2.18.0

This release contains bug fixes for the Dashboards Notifications plugin, primarily addressing data source selection behavior and minor UI improvements.

### Technical Changes

#### Data Source Selection Fix (PR #290)

The main bug fix addresses incorrect data source initialization behavior:

**Problem**: When MDS was enabled and local cluster was disabled, the plugin would still try to use the local cluster as the default, causing errors.

**Solution**: 
- Changed `dataSourceObservable` default value from `LocalCluster` to an empty object `{}`
- Added guard clause in `onSelectedDataSources` to handle empty data source arrays
- Modified `updateDefaultRouteOfManagementApplications` to only append `dataSourceId` to the hash when the value is defined

```typescript
// Before: Always defaulted to local cluster
export const dataSourceObservable = new BehaviorSubject<DataSourceOption>(LocalCluster);

// After: Use empty object to let data source picker determine the default
export const dataSourceObservable = new BehaviorSubject<DataSourceOption>({});
```

#### Route Handling Improvement

The plugin now properly handles undefined data source values:

```typescript
const dataSourceValue = dataSourceObservable.value?.id;
let hash = `#/`;
// Only append dataSourceId when it's defined
if (dataSourceValue !== undefined) {
  hash = `#/?dataSourceId=${dataSourceValue}`;
}
```

#### Error Response Code Fix

Changed error response status codes from 500 to 404 for missing resources in `configRoutes.ts`, providing more accurate HTTP semantics.

#### UI Typo Fix (PR #287)

Fixed typo in the Email Recipient Groups UI:
- Changed `recepient` to `recipient` in button variable name
- Fixed application title from "Email recepient groups" to "Email recipient groups"

#### CI/CD Improvements

- Updated Java version from 11 to 21 in GitHub Actions workflows
- Ensures compatibility with newer OpenSearch versions

### Files Changed

| File | Changes |
|------|---------|
| `public/pages/Main/Main.tsx` | Data source initialization logic |
| `public/plugin.ts` | Route hash handling, typo fix |
| `public/utils/constants.ts` | Default data source observable |
| `server/routes/configRoutes.ts` | Error status codes, validation |
| `public/pages/Emails/components/tables/RecipientGroupsTable.tsx` | Typo fix |
| `.github/workflows/*.yml` | Java version update |

## Limitations

- These fixes are specific to MDS-enabled deployments
- Users with local cluster disabled must ensure a default data source is configured

## References

### Documentation
- [dashboards-notifications Repository](https://github.com/opensearch-project/dashboards-notifications)
- [PR #290 Video Demo](https://github.com/user-attachments/assets/71861be4-3f4f-4cdf-a0cf-9d79bf8b5780)

### Pull Requests
| PR | Description |
|----|-------------|
| [#287](https://github.com/opensearch-project/dashboards-notifications/pull/287) | Fix typo in recipient |
| [#290](https://github.com/opensearch-project/dashboards-notifications/pull/290) | Bug fix to switch to default datasource instead of local cluster |
| [#271](https://github.com/opensearch-project/dashboards-notifications/pull/271) | Fix CI workflow for windows |
| [#280](https://github.com/opensearch-project/dashboards-notifications/pull/280) | Fix cache cypress hashfile path |

## Related Feature Report

- [Full feature documentation](../../../../features/dashboards-notifications/dashboards-notifications.md)
