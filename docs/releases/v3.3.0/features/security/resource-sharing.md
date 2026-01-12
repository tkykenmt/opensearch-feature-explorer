---
tags:
  - dashboards
  - performance
  - search
  - security
---

# Resource Sharing Bug Fixes and Enhancements

## Summary

OpenSearch v3.3.0 includes significant improvements to the Resource Sharing framework, introducing DLS-based automatic filtering, multi-tenancy support, and new APIs for dashboard integration. These changes improve search performance, enable tenant-aware resource management, and provide better UI support for resource access control.

## Details

### What's New in v3.3.0

This release focuses on three key areas:

1. **DLS-Based Automatic Filtering**: Resources are now automatically filtered using Document Level Security (DLS) based on `all_shared_principals`, eliminating the need for plugins to make separate queries for accessible resource IDs.

2. **Multi-Tenancy Support**: Resource sharing now tracks tenant information when multi-tenancy is enabled, allowing resources to be associated with specific tenants.

3. **Dashboard API Support**: New REST APIs enable OpenSearch Dashboards to provide a UI for managing resource access.

### Technical Changes

#### New Field: `all_shared_principals`

A new field `all_shared_principals` is now stored directly in resource documents to enable efficient DLS filtering:

```json
{
  "name": "sharedDashboard",
  "description": "A dashboard resource shared with multiple principals",
  "all_shared_principals": [
    "user:resource_sharing_test_user_alice",
    "user:resource_sharing_test_user_bob",
    "role:analytics_team",
    "role:all_access",
    "backend_role:Developers"
  ]
}
```

The security plugin automatically applies a DLS filter to limit search results:

```json
{
  "terms": {
    "all_shared_principals.keyword": [
      "user:resource_sharing_test_user_alice",
      "user:*",
      "role:all_access",
      "role:analytics_team",
      "backend_role:Developers"
    ]
  }
}
```

#### Tenant Tracking

When multi-tenancy is enabled, the `created_by` field now includes tenant information:

```json
{
  "sharing_info": {
    "resource_id": "0syx4pgBAqFBFKRNT2SD",
    "created_by": {
      "user": "admin",
      "tenant": "customtenant"
    },
    "share_with": {
      "sample_plugin_index_all_access": {
        "users": ["resource_sharing_test_user_all_access"]
      }
    }
  }
}
```

#### New REST APIs

| API | Method | Description |
|-----|--------|-------------|
| `/_plugins/_security/api/resource/types` | GET | List resource types and their action groups |
| `/_plugins/_security/api/resource/list?resource_type=<index>` | GET | List accessible resources with sharing info |

**Example Response for `/resource/types`:**

```json
{
  "types": [
    {
      "type": "org.opensearch.sample.SampleResource",
      "index": ".sample_resource",
      "action_groups": ["sample_read_only", "sample_read_write", "sample_full_access"]
    }
  ]
}
```

**Example Response for `/resource/list`:**

```json
{
  "resources": [
    {
      "resource_id": "1",
      "created_by": {
        "user": "darshit",
        "tenant": "some-tenant"
      },
      "share_with": {
        "sample_read_only": {
          "users": ["craig"]
        }
      },
      "can_share": true
    }
  ]
}
```

### Bug Fixes

| Issue | Fix |
|-------|-----|
| Case-sensitive user search | Changed `created_by.user` to use keyword search instead of text for exact case-sensitive matching |
| Cluster bootstrap failure | Reverted `@Inject` pattern to client accessor pattern to prevent `NoClassDefFoundError` when security plugin is absent |
| GET _doc authorization | GET _doc requests on sharable resource indices are now correctly treated as index requests for privilege evaluation |
| PATCH visibility update | Resource visibility (`all_shared_principals`) is now properly updated when using PATCH API |
| Update wipes principals | Resource updates no longer wipe out `all_shared_principals` field |
| Multiple shares blocked | Initial share map is now mutable to allow sharing with multiple access roles at once |
| Index settings mismatch | Resource sharing indices now match `.kibana*` index settings for consistency |

### Usage Example

**Searching resources with automatic DLS filtering:**

```bash
# As user 'alice' - only sees resources shared with her
GET /.sample_resource/_search
{
  "query": {
    "match_all": {}
  }
}
```

The security plugin automatically injects a DLS filter, so the response only includes resources where:
- `alice` is the owner
- Resource is public (`user:*`)
- Resource is explicitly shared with `alice` or one of her roles/backend_roles

## Limitations

- DLS filtering requires the `all_shared_principals` field to be properly maintained
- Tenant tracking only works when multi-tenancy is enabled (`user.getRequestedTenant() != null`)
- Dashboard APIs require the resource plugin to supply action groups via `resource-action-groups.yml`

## References

### Documentation
- [RESOURCE_SHARING_AND_ACCESS_CONTROL.md](https://github.com/opensearch-project/security/blob/main/RESOURCE_SHARING_AND_ACCESS_CONTROL.md): Developer guide

### Pull Requests
| PR | Description |
|----|-------------|
| [#5600](https://github.com/opensearch-project/security/pull/5600) | Use DLS to automatically filter sharable resources based on `all_shared_principals` |
| [#5596](https://github.com/opensearch-project/security/pull/5596) | Keep track of `all_shared_principals` for searchability |
| [#5588](https://github.com/opensearch-project/security/pull/5588) | Track tenant for sharable resources with multi-tenancy |
| [#5597](https://github.com/opensearch-project/security/pull/5597) | Add APIs for dashboards support for resource access management |
| [#5574](https://github.com/opensearch-project/security/pull/5574) | Fix case-sensitive user search with keyword field |
| [#5576](https://github.com/opensearch-project/security/pull/5576) | Revert @Inject pattern to client accessor pattern |
| [#5631](https://github.com/opensearch-project/security/pull/5631) | Treat GET _doc as indices request on sharable resource index |
| [#5654](https://github.com/opensearch-project/security/pull/5654) | Update resource visibility on PATCH API |
| [#5658](https://github.com/opensearch-project/security/pull/5658) | Handle resource updates to preserve `all_shared_principals` |
| [#5666](https://github.com/opensearch-project/security/pull/5666) | Make initial share map mutable for multiple shares |
| [#5605](https://github.com/opensearch-project/security/pull/5605) | Match index settings of `.kibana` indices |

### Issues (Design / RFC)
- [Issue #4500](https://github.com/opensearch-project/security/issues/4500): Resource Permissions and Sharing proposal

## Related Feature Report

- [Full feature documentation](../../../../features/security/resource-access-control-framework.md)
