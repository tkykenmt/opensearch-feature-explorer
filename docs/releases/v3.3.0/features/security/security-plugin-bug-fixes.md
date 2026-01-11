# Security Plugin Bug Fixes

## Summary

OpenSearch v3.3.0 includes several important bug fixes across the Security plugin and related components. These fixes address issues with system index access, JWT authentication logging, user attribute handling, Job Scheduler lock management, license corrections, and a security vulnerability in the js-yaml dependency.

## Details

### What's New in v3.3.0

This release addresses multiple bug fixes that improve stability and security:

1. **System Index Access Fix**: Restored proper behavior when `plugins.security.system_indices.enabled` is set to `false`
2. **JWT Log Spam Fix**: Eliminated excessive warning logs when JWT authenticator has empty `roles_key`
3. **User Attribute Format Fix**: Ensured user attributes conform to expected `attrKey=attrVal` format
4. **Job Scheduler Lock Fix**: Removed direct reference to Job Scheduler Lock Index
5. **License Corrections**: Fixed incorrect licenses in Security Principal files
6. **js-yaml Security Fix**: Upgraded js-yaml to v4.1 to prevent code injection attacks
7. **SQL UDT Serialization Fix**: Fixed serialization/deserialization of user-defined types in pushed-down scripts

### Technical Changes

#### System Index Access Evaluator Fix

When `plugins.security.system_indices.enabled` is set to `false`, the SystemIndexAccessEvaluator was being skipped, causing plugin system requests to fail. This fix reverts to previous behavior allowing any action originating from a plugin when system indices protection is disabled.

**Affected Component**: `SystemIndexAccessEvaluator`

**Issue**: Geospatial plugin and other plugins experienced permission errors like:
```
No index-level perm match for User [name=plugin:org.opensearch.geospatial.plugin.GeospatialPlugin...]
Insufficient permissions for the referenced index [Action [indices:data/write/index]]
```

#### JWT Authentication Log Fix

The JWT authenticator was logging excessive warnings when `roles_key` was configured with an empty list:
```
[WARN] Failed to get roles from JWT claims with roles_key '[]'. Check if this key is correct...
```

The fix skips logging this warning when `roles_key` is intentionally empty.

#### User Attribute Format Standardization

The `custom_attribute_names` field in system index mappings now properly uses the `attrKey=attrVal` format. This enables proper DLS (Document Level Security) restrictions with user attribute substitutions in alerting monitors.

#### Job Scheduler Lock Management

Removed direct manipulation of the Job Scheduler Lock Index (`.scheduler-geospatial-ip2geo-datasource`). Lock management is now delegated to Job Scheduler, which handles:
- Lock expiration for long-held locks
- Automatic lock deletion when job metadata is removed

#### js-yaml Security Upgrade

Upgraded `js-yaml` from v3.x to v4.1 in security-analytics-dashboards-plugin. Version 4.x integrates `safeLoad` into the `load` function by default, preventing potential code injection attacks through malicious YAML content.

#### SQL UDT Serialization Fix

Fixed an issue where pushed-down scripts failed with user-defined types (UDTs). The Calcite `RelJson` serializer was only keeping `SqlTypeName` during serialization, causing UDTs mapped to `VARCHAR` to be incorrectly restored.

**Example affected query**:
```sql
source=bank | eval t = unix_timestamp(birthdate) | stats count() by t
```

### Configuration Changes

| Setting | Description | Default |
|---------|-------------|---------|
| `plugins.security.system_indices.enabled` | When `false`, allows plugin system requests without restrictions | `true` |

## Limitations

- The system index access fix only applies when `plugins.security.system_indices.enabled` is explicitly set to `false`
- The js-yaml upgrade may require code changes if using deprecated `safeLoad` function directly

## Related PRs

| PR | Repository | Description |
|----|------------|-------------|
| [#5579](https://github.com/opensearch-project/security/pull/5579) | security | Allow plugin system requests when system_indices.enabled is false |
| [#5640](https://github.com/opensearch-project/security/pull/5640) | security | Fix JWT log spam with empty roles_key |
| [#5675](https://github.com/opensearch-project/security/pull/5675) | security | Fix incorrect licenses in Security Principal files |
| [#1577](https://github.com/opensearch-project/security-analytics/pull/1577) | security-analytics | Remove direct reference to Job Scheduler Lock Index |
| [#1583](https://github.com/opensearch-project/security-analytics/pull/1583) | security-analytics | Ensure user attributes in expected format |
| [#1330](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1330) | security-analytics-dashboards-plugin | Upgrade js-yaml to v4.1 |
| [#4245](https://github.com/opensearch-project/sql/pull/4245) | sql | Support serializing/deserializing UDTs in pushed-down scripts |

## References

- [Issue #5634](https://github.com/opensearch-project/security/issues/5634): JWT log spam bug report
- [Issue #792](https://github.com/opensearch-project/geospatial/issues/792): Geospatial permissions issue since 3.2.0
- [Issue #1829](https://github.com/opensearch-project/alerting/issues/1829): Alerting DLS user attribute issue
- [Issue #4063](https://github.com/opensearch-project/sql/issues/4063): SQL UDT serialization issue
