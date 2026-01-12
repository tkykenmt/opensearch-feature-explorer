---
tags:
  - dashboards
  - search
---

# Data Source Permissions Bugfix

## Summary

This bugfix resolves a critical issue where OpenSearch Dashboards would fail to start with an internal server error due to missing functions in the Data Source Permission saved object client wrapper. The error occurred because the wrapper did not properly expose all required saved object client functions.

## Details

### What's New in v2.18.0

Fixed the `DataSourcePermissionClientWrapper` to include all necessary saved object client functions that were previously missing.

### Technical Changes

#### Root Cause

The `DataSourcePermissionClientWrapper` class wraps the saved object client to enforce permission checks for data source operations. However, when returning the wrapped client, it only included custom implementations for `create`, `bulkCreate`, `delete`, `update`, and `bulkUpdate` methods, while omitting other essential client functions.

This caused the following error when accessing OpenSearch Dashboards:

```
TypeError: this.savedObjectsClient.get is not a function
    at UiSettingsClient.read
```

#### Fix Applied

Added the missing saved object client functions to the wrapper return object:

| Function | Description |
|----------|-------------|
| `get` | Retrieve a single saved object |
| `checkConflicts` | Check for conflicts before operations |
| `errors` | Access error utilities |
| `addToNamespaces` | Add saved object to namespaces |
| `deleteFromNamespaces` | Remove saved object from namespaces |
| `find` | Search for saved objects |
| `bulkGet` | Retrieve multiple saved objects |
| `deleteByWorkspace` | Delete saved objects by workspace |

#### Code Change

```typescript
return {
  ...wrapperOptions.client,
  create: createWithManageableBy,
  bulkCreate: bulkCreateWithManageableBy,
  delete: deleteWithManageableBy,
  update: updateWithManageableBy,
  bulkUpdate: bulkUpdateWithManageableBy,
  // Added missing functions
  get: wrapperOptions.client.get,
  checkConflicts: wrapperOptions.client.checkConflicts,
  errors: wrapperOptions.client.errors,
  addToNamespaces: wrapperOptions.client.addToNamespaces,
  deleteFromNamespaces: wrapperOptions.client.deleteFromNamespaces,
  find: wrapperOptions.client.find,
  bulkGet: wrapperOptions.client.bulkGet,
  deleteByWorkspace: wrapperOptions.client.deleteByWorkspace,
};
```

### Impact

Without this fix, OpenSearch Dashboards would display an "Internal Server Error" and fail to load properly when the data source permission feature was enabled.

## Limitations

None specific to this fix.

## References

### Documentation
- [Data Sources Documentation](https://docs.opensearch.org/2.18/dashboards/management/data-sources/): Official documentation for data sources
- [Data Source Permissions](https://docs.opensearch.org/2.18/security/access-control/permissions/#data-source-permissions): Permission configuration

### Pull Requests
| PR | Description |
|----|-------------|
| [#8118](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8118) | Fix data source permission client wrapper error |

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch-dashboards/opensearch-dashboards-data-source-permissions.md)
