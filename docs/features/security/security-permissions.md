---
tags:
  - security
---
# Security Permissions

## Summary

OpenSearch Security plugin provides predefined roles for various features including Forecasting, Anomaly Detection, Machine Learning, and more. These roles define cluster-level and index-level permissions that control access to plugin functionality. The Security plugin's `roles.yml` configuration file contains reserved roles that are automatically available after installation.

## Details

### Architecture

```mermaid
graph TB
    subgraph "Security Plugin"
        RolesYml[roles.yml]
        RolesMapping[roles_mapping.yml]
    end
    
    subgraph "Predefined Roles"
        ForecastRead[forecast_read_access]
        ForecastFull[forecast_full_access]
        AnomalyRead[anomaly_read_access]
        AnomalyFull[anomaly_full_access]
        MLRead[ml_read_access]
        MLFull[ml_full_access]
    end
    
    subgraph "Permission Types"
        ClusterPerm[Cluster Permissions]
        IndexPerm[Index Permissions]
    end
    
    RolesYml --> ForecastRead
    RolesYml --> ForecastFull
    RolesYml --> AnomalyRead
    RolesYml --> AnomalyFull
    RolesYml --> MLRead
    RolesYml --> MLFull
    
    ForecastRead --> ClusterPerm
    ForecastRead --> IndexPerm
    ForecastFull --> ClusterPerm
    ForecastFull --> IndexPerm
    
    RolesMapping --> Users[Users/Backend Roles]
```

### Components

| Component | Description |
|-----------|-------------|
| `roles.yml` | Defines predefined roles with cluster and index permissions |
| `roles_mapping.yml` | Maps users and backend roles to security roles |
| Cluster Permissions | Control access to cluster-wide operations |
| Index Permissions | Control access to specific indices and operations |

### Forecast Roles Configuration

#### forecast_read_access

Provides read-only access to forecast resources:

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

#### forecast_full_access

Provides full access to all forecasting functionality:

```yaml
forecast_full_access:
  reserved: true
  cluster_permissions:
    - 'cluster:admin/plugin/forecast/*'
    - 'cluster:admin/settings/update'
    - 'cluster_monitor'
  index_permissions:
    - index_patterns:
        - '*'
      allowed_actions:
        - 'indices:admin/aliases/get'
        - 'indices:admin/mapping/get'
        - 'indices:admin/mapping/put'
        - 'indices:admin/mappings/fields/get*'
        - 'indices:admin/mappings/get'
        - 'indices:admin/resolve/index'
        - 'indices:data/read*'
        - 'indices:data/read/field_caps*'
        - 'indices:data/read/search'
        - 'indices:data/write*'
        - 'indices_monitor'
```

### Usage Example

Map roles to users in `roles_mapping.yml`:

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

## Limitations

- Forecast roles are separate from Anomaly Detection roles (`anomaly_read_access`, `anomaly_full_access`)
- Cross-cluster forecasting requires `cluster_monitor` permission and proper cluster connectivity
- Reserved roles cannot be modified through the API; changes require editing `roles.yml` directly

## Change History

- **v3.1.0** (2025-06): Added `forecast_read_access` and `forecast_full_access` roles with complete permissions for forecasting feature including `cluster_monitor` and `indices:admin/mappings/get`


## References

### Documentation
- [OpenSearch Security Permissions Documentation](https://docs.opensearch.org/3.0/security/access-control/permissions/)
- [Defining Users and Roles](https://docs.opensearch.org/3.0/security/access-control/users-roles/)
- [Security Dashboards Plugin PR #2253](https://github.com/opensearch-project/security-dashboards-plugin/pull/2253): Frontend dropdown update

### Pull Requests
| Version | PR | Description | Related Issue |
|---------|-----|-------------|---------------|
| v3.1.0 | [#5386](https://github.com/opensearch-project/security/pull/5386) | Add forecast roles and permissions |   |
| v3.1.0 | [#5405](https://github.com/opensearch-project/security/pull/5405) | Add missing cluster:monitor permission |   |
| v3.1.0 | [#5412](https://github.com/opensearch-project/security/pull/5412) | Add missing mapping get permission |   |
