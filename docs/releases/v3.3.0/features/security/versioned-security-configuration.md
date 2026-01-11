# Versioned Security Configuration

## Summary

OpenSearch v3.3.0 introduces the View API and Rollback API for the experimental versioned security configuration feature. These APIs enable administrators to view the complete history of security configuration changes and roll back to any previous configuration version, providing operational safety and disaster recovery capabilities for security settings.

## Details

### What's New in v3.3.0

This release adds REST APIs for viewing and rolling back security configuration versions:

- **View API**: Retrieve all versions or a specific version of security configurations
- **Rollback API**: Restore security configurations to the immediately preceding version or any specific version

### Technical Changes

#### New REST Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/_plugins/_security/api/versions` | GET | View all configuration versions |
| `/_plugins/_security/api/version/{versionId}` | GET | View a specific version |
| `/_plugins/_security/api/version/rollback` | POST | Roll back to the preceding version |
| `/_plugins/_security/api/version/rollback/{versionId}` | POST | Roll back to a specific version |

#### New Permissions

| Permission | Description |
|------------|-------------|
| `restapi:admin/view_version` | Required to view configuration versions |
| `restapi:admin/rollback_version` | Required to roll back configurations |

These permissions are included in the default `security_manager` and `all_access` roles.

### Usage Example

#### View All Versions

```bash
curl -XGET "https://localhost:9200/_plugins/_security/api/versions?pretty" \
  -u 'admin:admin' --insecure
```

Response:
```json
{
  "versions": [
    {
      "version_id": "v1",
      "timestamp": "2025-05-22T08:46:11.887620466Z",
      "modified_by": "system",
      "security_configs": { ... }
    },
    {
      "version_id": "v2",
      "timestamp": "2025-05-23T06:56:20.081933886Z",
      "modified_by": "admin",
      "security_configs": { ... }
    }
  ]
}
```

#### View Specific Version

```bash
curl -XGET "https://localhost:9200/_plugins/_security/api/version/v2?pretty" \
  -u 'admin:admin' --insecure
```

#### Roll Back to Preceding Version

```bash
curl -XPOST "https://localhost:9200/_plugins/_security/api/version/rollback" \
  -u 'admin:admin' --insecure
```

Response:
```json
{
  "status": "OK",
  "message": "config rolled back to version v4"
}
```

#### Roll Back to Specific Version

```bash
curl -XPOST "https://localhost:9200/_plugins/_security/api/version/rollback/v2" \
  -u 'admin:admin' --insecure
```

### Multi-Node Behavior

Rollback operations work correctly in multi-node clusters:
- Rollback can be initiated from any node
- The cluster manager node handles the actual configuration update
- A new version is created after rollback to maintain audit trail

### Migration Notes

1. Enable the feature in `opensearch.yml`:
   ```yaml
   plugins.security.configurations_versions.enabled: true
   ```
2. Restart the cluster for changes to take effect
3. The View and Rollback APIs require admin permissions

## Limitations

- **Experimental Status**: Feature remains experimental and disabled by default
- **Admin Access Required**: Only users with admin/security manager roles can access these APIs
- **Rollback Creates New Version**: Rolling back creates a new version entry (e.g., rolling back from v5 to v3 creates v6 with v3's content)
- **Version Not Found**: Returns 404 if the specified version doesn't exist

## Related PRs

| PR | Description |
|----|-------------|
| [#5357](https://github.com/opensearch-project/security/pull/5357) | Initial versioned security configuration management (v3.2.0) |
| [#5431](https://github.com/opensearch-project/security/pull/5431) | View API and Rollback API implementation (closed without merge - functionality included in #5357) |

## References

- [Issue #5093](https://github.com/opensearch-project/security/issues/5093): Original feature request
- [Security Configuration Versioning Documentation](https://docs.opensearch.org/3.3/security/configuration/versioning/): Official documentation

## Related Feature Report

- [Full feature documentation](../../../features/security/security-configuration-versioning.md)
