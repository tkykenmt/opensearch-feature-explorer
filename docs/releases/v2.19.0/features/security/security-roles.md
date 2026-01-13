---
tags:
  - security
---
# Security Roles

## Summary

OpenSearch v2.19.0 adds new predefined security roles for Learning to Rank (LTR) and enhances the Anomaly Detection role with additional permissions for ingest pipelines and index settings.

## Details

### What's New in v2.19.0

#### Learning to Rank (LTR) Roles

Two new predefined roles for the Learning to Rank plugin:

| Role | Description | Permissions |
|------|-------------|-------------|
| `ltr_read_access` | Read-only access to LTR resources | Cache stats, feature store list, LTR stats |
| `ltr_full_access` | Full access to all LTR operations | All LTR cluster admin actions |

**ltr_read_access configuration:**
```yaml
ltr_read_access:
  reserved: true
  cluster_permissions:
    - cluster:admin/ltr/caches/stats
    - cluster:admin/ltr/featurestore/list
    - cluster:admin/ltr/stats
```

**ltr_full_access configuration:**
```yaml
ltr_full_access:
  reserved: true
  cluster_permissions:
    - cluster:admin/ltr/*
```

#### Anomaly Detection Role Enhancements

The `anomaly_full_access` role now includes additional permissions for ingest pipeline management and index settings:

| Permission | Type | Purpose |
|------------|------|---------|
| `cluster:admin/ingest/pipeline/delete` | Cluster | Delete ingest pipelines |
| `cluster:admin/ingest/pipeline/put` | Cluster | Create/update ingest pipelines |
| `indices:admin/setting/put` | Index | Update index settings |

These permissions enable anomaly detection workflows that require creating ingest pipelines for data preprocessing.

### Technical Changes

The changes are implemented in `config/roles.yml`:

1. **LTR roles** - Added at the end of the roles configuration file
2. **Anomaly detection enhancements** - Added to existing `anomaly_full_access` role

## Limitations

- LTR roles require the Learning to Rank plugin to be installed
- The new anomaly detection permissions apply only to `anomaly_full_access`, not `anomaly_read_access`

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#5069](https://github.com/opensearch-project/security/pull/5069) | Add ingest pipeline and indices permissions for anomaly_full_access | Backport of #5065 |
| [#5070](https://github.com/opensearch-project/security/pull/5070) | Add LTR read and full access roles | Backport of #5067 |

### Documentation

- [Predefined Roles](https://docs.opensearch.org/2.19/security/access-control/users-roles/#predefined-roles)
- [Learning to Rank](https://docs.opensearch.org/2.19/search-plugins/ltr/index/)
- [Anomaly Detection Security](https://docs.opensearch.org/2.19/observing-your-data/ad/security/)
