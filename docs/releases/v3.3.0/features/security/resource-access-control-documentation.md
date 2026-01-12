---
tags:
  - security
---

# Resource Access Control Documentation

## Summary

This release item adds comprehensive documentation for the Resource Sharing and Access Control feature in the OpenSearch Security plugin. The documentation provides guidance for both plugin developers and cluster administrators/users, covering the complete lifecycle of resource sharing from implementation to usage.

## Details

### What's New in v3.3.0

PR [#5540](https://github.com/opensearch-project/security/pull/5540) introduces a complete documentation overhaul for the Resource Access Control feature, restructuring the existing documentation into two distinct parts:

1. **Part 1: Plugin Developer Guide** - Technical implementation details for plugin developers
2. **Part 2: Cluster-admin and User Guide** - Operational guidance for administrators and end users

### Documentation Structure

```mermaid
graph TB
    subgraph Documentation["RESOURCE_SHARING_AND_ACCESS_CONTROL.md"]
        subgraph Part1["Part 1: Plugin Developer Guide"]
            P1A[Feature Overview]
            P1B[Components & SPI]
            P1C[Resource Sharing API Design]
            P1D[Using ResourceSharingClient]
            P1E[ActionGroups]
            P1F[Restrictions & Best Practices]
        end
        
        subgraph Part2["Part 2: Cluster-admin & User Guide"]
            P2A[Feature Flag Setup]
            P2B[Dynamic Settings]
            P2C[User Setup & Permissions]
            P2D[Migration API]
            P2E[Resource Sharing REST API]
            P2F[Best Practices]
        end
    end
    
    Part1 --> Part2
```

### Key Documentation Additions

#### For Plugin Developers

| Section | Description |
|---------|-------------|
| DocRequest Interface | New requirement for ActionRequests to implement DocRequest for resource access control |
| resource-action-groups.yml | Configuration file format for declaring action groups per resource type |
| Filtering Results | Automatic result filtering based on authenticated user via `all_shared_principals` field |
| isFeatureEnabledForType | New API method to check if feature is enabled for a specific resource type |

#### For Administrators and Users

| Section | Description |
|---------|-------------|
| Dynamic Settings | Runtime configuration via `_cluster/settings` API |
| Protected Types | New setting `plugins.security.experimental.resource_sharing.protected_types` |
| Migration API | Complete documentation for migrating legacy sharing metadata |
| REST API Reference | Full API documentation for PUT, PATCH, POST, GET operations |

### New REST API Documentation

The documentation now includes complete REST API reference:

| API | Method | Description |
|-----|--------|-------------|
| `/_plugins/_security/api/resource/share` | PUT | Create/replace sharing settings |
| `/_plugins/_security/api/resource/share` | PATCH/POST | Add or revoke recipients (non-destructive) |
| `/_plugins/_security/api/resource/share` | GET | Retrieve current sharing configuration |
| `/_plugins/_security/api/resource/types` | GET | List available resource types and action groups |
| `/_plugins/_security/api/resource/list` | GET | List accessible resources for current user |
| `/_plugins/_security/api/resources/migrate` | POST | Migrate legacy sharing metadata |

### Configuration Updates

New dynamic settings documented:

```yaml
# Enable resource sharing
plugins.security.experimental.resource_sharing.enabled: true

# Specify protected resource types
plugins.security.experimental.resource_sharing.protected_types: ["anomaly-detector", "forecaster", "ml-model"]
```

These settings can now be updated at runtime:

```json
PUT _cluster/settings
{
  "persistent": {
    "plugins.security.experimental.resource_sharing.enabled": "true",
    "plugins.security.experimental.resource_sharing.protected_types": ["anomaly-detector", "forecaster", "ml-model"]
  }
}
```

## Limitations

- Documentation is specific to the experimental resource sharing feature
- Feature must be explicitly enabled via configuration
- Protected types must be declared for resource-level authorization to take effect

## References

### Documentation
- [RESOURCE_SHARING_AND_ACCESS_CONTROL.md](https://github.com/opensearch-project/security/blob/main/RESOURCE_SHARING_AND_ACCESS_CONTROL.md): Full documentation
- [spi/README.md](https://github.com/opensearch-project/security/blob/main/spi/README.md): SPI implementation guide

### Blog Posts
- [Blog: Introducing resource sharing](https://opensearch.org/blog/introducing-resource-sharing-a-new-access-control-model-for-opensearch/): Official announcement

### Pull Requests
| PR | Description |
|----|-------------|
| [#5540](https://github.com/opensearch-project/security/pull/5540) | Adds comprehensive documentation for Resource Access Control feature |

## Related Feature Report

- [Full feature documentation](../../../../features/security/resource-access-control-framework.md)
