# Security Permissions

## Summary

This release fixes missing security permissions for the Forecasting plugin, ensuring users with `forecast_full_access` role can properly create and manage forecasters, including cross-cluster forecasters. Three permissions were added: `cluster_monitor` for cluster monitoring, `indices:admin/mappings/get` for mapping retrieval, and the complete forecast roles configuration.

## Details

### What's New in v3.1.0

Three PRs addressed permission gaps in the Security plugin's predefined roles for the Forecasting feature:

1. **New Forecast Roles** (PR #5386): Added `forecast_read_access` and `forecast_full_access` roles to support the forecasting feature
2. **Cluster Monitor Permission** (PR #5405): Added missing `cluster_monitor` permission for cross-cluster forecaster creation
3. **Mapping Get Permission** (PR #5412): Added missing `indices:admin/mappings/get` permission for index mapping retrieval

### Technical Changes

#### New Roles Added

| Role | Description |
|------|-------------|
| `forecast_read_access` | Read-only access to forecast resources |
| `forecast_full_access` | Full access to all forecasting functionality |

#### forecast_read_access Permissions

```yaml
forecast_read_access:
  reserved: true
  cluster_permissions:
    - 'cluster:admin/plugin/forecast/forecaster/info'
    - 'cluster:admin/plugin/forecast/forecaster/stats'
    - 'cluster:admin/plugin/forecast/forecaster/suggest'
    - 'cluster:admin/plugin/forecast/forecaster/validate'
    - 'cluster:admin/plugin/forecast/forecasters/get'
    - 'cluster:admin/plugin/forecast/forecasters/info'
    - 'cluster:admin/plugin/forecast/forecasters/search'
    - 'cluster:admin/plugin/forecast/result/topForecasts'
    - 'cluster:admin/plugin/forecast/tasks/search'
  index_permissions:
    - index_patterns:
        - 'opensearch-forecast-result*'
      allowed_actions:
        - 'indices:admin/mappings/fields/get*'
        - 'indices:admin/resolve/index'
        - 'indices:data/read*'
```

#### forecast_full_access Permissions

```yaml
forecast_full_access:
  reserved: true
  cluster_permissions:
    - 'cluster:admin/plugin/forecast/*'
    - 'cluster:admin/settings/update'
    - 'cluster_monitor'  # Added in PR #5405
  index_permissions:
    - index_patterns:
        - '*'
      allowed_actions:
        - 'indices:admin/aliases/get'
        - 'indices:admin/mapping/get'
        - 'indices:admin/mapping/put'
        - 'indices:admin/mappings/fields/get*'
        - 'indices:admin/mappings/get'  # Added in PR #5412
        - 'indices:admin/resolve/index'
        - 'indices:data/read*'
        - 'indices:data/read/field_caps*'
        - 'indices:data/read/search'
        - 'indices:data/write*'
        - 'indices_monitor'
```

### Usage Example

To assign forecast access to a user, map the role in `roles_mapping.yml`:

```yaml
forecast_full_access:
  reserved: false
  users:
    - "forecast_admin"
  backend_roles:
    - "forecast_admins"

forecast_read_access:
  reserved: false
  users:
    - "forecast_viewer"
  backend_roles:
    - "forecast_viewers"
```

### Migration Notes

- Users upgrading from previous versions need to update their `roles.yml` configuration to include the new forecast roles
- Existing anomaly detection users can use similar role patterns for forecasting
- The `cluster_monitor` permission is required for cross-cluster forecaster operations

## Limitations

- The forecast roles are specific to the Forecasting plugin and do not cover Anomaly Detection (which has separate `anomaly_read_access` and `anomaly_full_access` roles)
- Cross-cluster forecasting requires additional cluster connectivity configuration

## References

### Documentation
- [OpenSearch Security Permissions Documentation](https://docs.opensearch.org/3.0/security/access-control/permissions/)
- [Defining Users and Roles](https://docs.opensearch.org/3.0/security/access-control/users-roles/)
- [Security Dashboards Plugin PR #2253](https://github.com/opensearch-project/security-dashboards-plugin/pull/2253): Frontend dropdown update for forecast permissions

### Pull Requests
| PR | Description |
|----|-------------|
| [#5386](https://github.com/opensearch-project/security/pull/5386) | Add forecast roles and permissions |
| [#5405](https://github.com/opensearch-project/security/pull/5405) | Add missing cluster:monitor permission |
| [#5412](https://github.com/opensearch-project/security/pull/5412) | Add missing mapping get permission |

## Related Feature Report

- [Full feature documentation](../../../features/security/security-permissions.md)
