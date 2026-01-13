---
tags:
  - domain/core
  - component/server
  - indexing
  - ml
  - security
---
# Cluster Permissions

## Summary

OpenSearch 3.0.0 includes a breaking change to the `_cat/shards` API permission model. The `CatShardsAction` permission has been changed from `cluster:monitor/shards` to `internal:monitor/shards`, restoring the pre-2.17 behavior where non-admin users can call the `_cat/shards` API without requiring explicit cluster-level permissions.

## Details

### What's New in v3.0.0

The `CatShardsAction` class has been modified to use an internal permission instead of a cluster-level permission:

```java
// Before (v2.17 - v2.x)
public static final String NAME = "cluster:monitor/shards";

// After (v3.0.0)
public static final String NAME = "internal:monitor/shards";
```

### Background

In OpenSearch 2.17, the `CatShardsAction` was introduced to support pagination and cancellation for the `_cat/shards` API. This action was registered with the permission `cluster:monitor/shards`, which inadvertently required non-admin users to have explicit cluster-level permissions to call the API.

Prior to 2.17, the `_cat/shards` API only required index-level permissions (`indices:monitor/stats`), allowing users with read access to specific indexes to view shard information for those indexes.

### Technical Changes

#### Permission Change

| Version | Permission | Type |
|---------|------------|------|
| < 2.17 | `indices:monitor/stats` | Index-level |
| 2.17 - 2.x | `cluster:monitor/shards` | Cluster-level |
| 3.0.0+ | `internal:monitor/shards` | Internal |

#### Impact

- **Non-admin users**: Can now call `_cat/shards` without explicit `cluster:monitor/shards` permission
- **Security configurations**: The `cluster:monitor/shards` permission is no longer required and can be removed from role definitions

### Migration Notes

If you added `cluster:monitor/shards` to your role definitions after upgrading to 2.17, you can safely remove this permission when upgrading to 3.0.0. The permission will be ignored but removing it keeps your security configuration clean.

**Before (2.17+):**
```yaml
my_role:
  cluster_permissions:
    - 'cluster:monitor/shards'  # Can be removed
  index_permissions:
    - index_patterns:
        - 'my-index-*'
      allowed_actions:
        - 'indices:data/read/*'
        - 'indices:monitor/stats'
```

**After (3.0.0):**
```yaml
my_role:
  index_permissions:
    - index_patterns:
        - 'my-index-*'
      allowed_actions:
        - 'indices:data/read/*'
        - 'indices:monitor/stats'
```

## Limitations

- This change only affects the `_cat/shards` API
- Other CAT APIs may still require their respective permissions
- The change is backward compatible for users who already have the `cluster:monitor/shards` permission configured

## References

### Documentation
- [CAT shards API](https://docs.opensearch.org/3.0/api-reference/cat/cat-shards/): Official documentation
- [Permissions](https://docs.opensearch.org/3.0/security/access-control/permissions/): Security permissions reference

### Pull Requests
| PR | Description |
|----|-------------|
| [#17203](https://github.com/opensearch-project/OpenSearch/pull/17203) | Changed CatShardsAction to internal to allow non-admin users |
| [#18185](https://github.com/opensearch-project/OpenSearch/pull/18185) | Adding new permission for _cat/shard action to 3.0 release notes |

### Issues (Design / RFC)
- [Issue #17199](https://github.com/opensearch-project/OpenSearch/issues/17199): Bug report - Make CatShardsAction internal

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/opensearch-cluster-permissions.md)
