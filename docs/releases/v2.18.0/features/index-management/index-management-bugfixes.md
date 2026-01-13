---
tags:
  - domain/data
  - component/server
  - dashboards
  - indexing
---
# Index Management Bugfixes

## Summary

This release includes three important bugfixes for the Index Management plugin and its Dashboards component. The fixes address issues with snapshot status detection, snapshot policy UI navigation, and data source initialization in multi-data-source environments.

## Details

### What's New in v2.18.0

Three bugfixes were merged to improve the reliability and user experience of Index Management:

1. **Snapshot Status Detection Fix** - Fixed incorrect detection of partial snapshots as successful
2. **Snapshot Policy Button Fix** - Fixed dashboard reload issue when clicking "Create snapshot policy"
3. **Data Source Initialization Fix** - Fixed initial data source being incorrectly set to local cluster

### Technical Changes

#### Snapshot Status Detection (Backend)

The `WaitForSnapshotStep` was updated to use `GetSnapshotsRequest` instead of `SnapshotsStatusRequest` for checking snapshot completion status.

**Problem**: The previous implementation using `GetSnapshotStatus` API could incorrectly report partial snapshots as successful, leading to data integrity issues.

**Solution**: Replaced with `GetSnapshots` API which provides accurate `SnapshotState` information including:
- `IN_PROGRESS` - Snapshot is still running
- `SUCCESS` - Snapshot completed successfully
- `FAILED` - Snapshot failed
- `PARTIAL` - Snapshot is partial (now correctly detected as failure)
- `INCOMPATIBLE` - Snapshot is incompatible

```kotlin
// Before: Using SnapshotsStatusRequest
val request = SnapshotsStatusRequest()
    .snapshots(arrayOf(snapshotName))
    .repository(repository)
val response: SnapshotsStatusResponse = client.admin().cluster()
    .suspendUntil { snapshotsStatus(request, it) }

// After: Using GetSnapshotsRequest
val newRequest = GetSnapshotsRequest()
    .snapshots(arrayOf(snapshotName))
    .repository(repository)
val response: GetSnapshotsResponse = client.admin().cluster()
    .suspendUntil { getSnapshots(newRequest, it) }
```

#### Snapshot Policy Button Fix (Frontend)

Changed the "Create Policy" button behavior from using `href` navigation to using the `run` callback method.

```typescript
// Before: href causes full page reload
{
  label: "Create policy",
  iconType: "plus",
  fill: true,
  href: `${PLUGIN_NAME}#${ROUTES.CREATE_SNAPSHOT_POLICY}`,
  ...
}

// After: run callback for SPA navigation
{
  label: "Create policy",
  iconType: "plus",
  fill: true,
  run: this.onClickCreate,
  ...
}
```

#### Data Source Initialization Fix (Frontend)

Fixed the initial data source selection logic to properly handle the "Local" cluster identifier.

```typescript
// Before: Only checked for undefined
dataSourceLoading: dataSourceId === undefined 
    ? props.multiDataSourceEnabled : false

// After: Also checks for "Local" identifier
dataSourceLoading: dataSourceId === undefined || dataSourceId === "Local" 
    ? props.multiDataSourceEnabled : false
```

Also added validation to prevent empty data source selection:
```typescript
onSelectedDataSources = (dataSources: DataSourceOption[]) => {
  if (dataSources.length == 0) {
    return; // No datasource selected, skip update
  }
  // ... rest of the handler
}
```

### Files Changed

| File | Changes |
|------|---------|
| `WaitForSnapshotStep.kt` | Replaced SnapshotsStatusRequest with GetSnapshotsRequest |
| `WaitForSnapshotStepTests.kt` | Updated tests for new API |
| `TestUtils.kt` | Added mockSnapshotInfo helper function |
| `SnapshotPolicies.tsx` | Changed button from href to run callback |
| `Main.tsx` | Fixed data source initialization logic |

## Limitations

- The snapshot status fix only affects new snapshot operations; existing snapshots with incorrect status are not retroactively corrected
- The data source fix requires the multi-data-source feature to be enabled

## References

### Documentation
- [Snapshot Management Documentation](https://docs.opensearch.org/2.18/dashboards/sm-dashboards/)
- [Snapshot Management API](https://docs.opensearch.org/2.18/tuning-your-cluster/availability-and-recovery/snapshots/sm-api/)
- [Index State Management](https://docs.opensearch.org/2.18/im-plugin/ism/index/)

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#1257](https://github.com/opensearch-project/index-management/pull/1257) | index-management | Fixing snapshot bug |
| [#1187](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1187) | index-management-dashboards-plugin | Create snapshot policy button reloads the dashboard |
| [#1189](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1189) | index-management-dashboards-plugin | Fixing a bug with initial data source being set to local cluster |

## Related Feature Report

- Full feature documentation
