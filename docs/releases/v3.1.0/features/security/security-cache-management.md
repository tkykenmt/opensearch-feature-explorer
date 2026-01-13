---
tags:
  - domain/security
  - component/server
  - performance
  - security
---
# Security Cache Management

## Summary

OpenSearch v3.1.0 introduces enhanced security cache management capabilities, allowing administrators to invalidate authentication cache entries for individual users and dynamically update cache TTL settings without restarting the cluster. These improvements address the inefficiency of global cache invalidation when only specific user entries become stale, particularly useful for LDAP environments where user backend roles may change.

## Details

### What's New in v3.1.0

This release adds two key enhancements to security cache management:

1. **Selective User Cache Invalidation**: A new REST endpoint to flush cache entries for individual users
2. **Dynamic Cache TTL Configuration**: The `plugins.security.cache.ttl_minutes` setting can now be updated dynamically via cluster settings API

### Technical Changes

#### Architecture Changes

```mermaid
graph TB
    subgraph "Security Cache Management"
        API[REST API]
        BR[BackendRegistry]
        UC[User Cache]
        RIC[REST Impersonation Cache]
        RRC[REST Role Cache]
    end
    
    subgraph "New Endpoints"
        FC[DELETE /cache]
        FU[DELETE /cache/user/{username}]
    end
    
    subgraph "Dynamic Settings"
        CS[Cluster Settings API]
        TTL[TTL Setting Listener]
    end
    
    FC --> API
    FU --> API
    API --> BR
    BR --> UC
    BR --> RIC
    BR --> RRC
    
    CS --> TTL
    TTL --> BR
    BR -.->|Recreate| UC
    BR -.->|Recreate| RIC
    BR -.->|Recreate| RRC
```

#### New Components

| Component | Description |
|-----------|-------------|
| `FlushCacheApiAction` | Extended REST handler supporting user-specific cache invalidation |
| `BackendRegistry.invalidateUserCache()` | New method for selective cache invalidation by username |
| `SecuritySettings.CACHE_TTL_SETTING` | Dynamic cluster setting for cache TTL |

#### New Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `plugins.security.cache.ttl_minutes` | Authentication cache TTL (now dynamic) | 60 |

#### API Changes

**New Endpoint: Flush Individual User Cache**

```
DELETE /_plugins/_security/api/cache/user/{username}
```

Response:
```json
{
  "message": "Cache invalidated for user: {username}"
}
```

**Existing Endpoint: Flush All Cache (unchanged)**

```
DELETE /_plugins/_security/api/cache
```

Response:
```json
{
  "message": "Cache flushed successfully."
}
```

**Dynamic TTL Update via Cluster Settings**

```
PUT /_cluster/settings
{
  "transient": {
    "plugins.security.cache.ttl_minutes": "1440"
  }
}
```

### Usage Example

```bash
# Invalidate cache for a specific user after LDAP role change
curl -X DELETE "https://localhost:9200/_plugins/_security/api/cache/user/john_doe" \
  -H "Content-Type: application/json" \
  --cert admin.pem --key admin-key.pem --cacert root-ca.pem

# Update cache TTL dynamically (24 hours)
curl -X PUT "https://localhost:9200/_cluster/settings" \
  -H "Content-Type: application/json" \
  -d '{
    "transient": {
      "plugins.security.cache.ttl_minutes": "1440"
    }
  }' \
  --cert admin.pem --key admin-key.pem --cacert root-ca.pem
```

### Migration Notes

- The new user-specific cache invalidation endpoint requires admin privileges
- Dynamic TTL changes via cluster settings are transient and do not persist across restarts
- For permanent TTL changes, update `opensearch.yml` with `plugins.security.cache.ttl_minutes`

## Limitations

- User-specific cache invalidation requires knowing the exact username
- Dynamic TTL changes recreate all caches, temporarily affecting performance
- The endpoint does not validate if the user exists before invalidation

## References

### Documentation
- [Security Settings Documentation](https://docs.opensearch.org/3.0/install-and-configure/configuring-opensearch/security-settings/): Official security configuration docs

### Pull Requests
| PR | Description |
|----|-------------|
| [#5337](https://github.com/opensearch-project/security/pull/5337) | Add flush cache endpoint for individual user |
| [#5324](https://github.com/opensearch-project/security/pull/5324) | Register cluster settings listener for `plugins.security.cache.ttl_minutes` |

### Issues (Design / RFC)
- [Issue #2829](https://github.com/opensearch-project/security/issues/2829): Feature request for per-user cache invalidation

## Related Feature Report

- Full feature documentation
