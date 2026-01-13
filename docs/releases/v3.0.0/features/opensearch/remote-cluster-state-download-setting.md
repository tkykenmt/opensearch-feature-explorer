---
tags:
  - domain/core
  - component/server
  - performance
---
# Remote Cluster State Download Setting

## Summary

Introduces a new cluster setting `cluster.remote_state.download.serve_read_api.enabled` to disable downloading full cluster state from remote storage on term mismatch. This prevents performance degradation in clusters with large numbers of indices where full cluster state downloads can occupy remote threadpools and delay cluster state update propagation.

## Details

### What's New in v3.0.0

A new dynamic cluster setting allows operators to control whether nodes download full cluster state from remote storage when a term mismatch is detected.

### Technical Changes

#### Problem Addressed

In clusters with large numbers of indices, fetching full cluster state on term mismatch causes:
- Downloading too many files from remote storage
- Remote threadpool saturation
- Delayed cluster state update propagation from cluster manager
- Node lag due to occupied threadpools

#### New Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `cluster.remote_state.download.serve_read_api.enabled` | Controls whether full cluster state download from remote is enabled on term mismatch | `true` |

### Usage Example

```bash
# Disable full cluster state download on term mismatch
PUT /_cluster/settings
{
  "persistent": {
    "cluster.remote_state.download.serve_read_api.enabled": false
  }
}
```

### Migration Notes

- This setting is dynamic and can be changed without cluster restart
- Consider disabling in clusters with large numbers of indices experiencing cluster state propagation delays
- Monitor remote threadpool utilization before and after changing this setting

## Limitations

- When disabled, nodes may have stale cluster state until the next successful cluster state update from the cluster manager
- Only applicable to remote cluster state enabled clusters

## References

### Documentation
- [Remote cluster state](https://docs.opensearch.org/3.0/tuning-your-cluster/availability-and-recovery/remote-store/remote-cluster-state/): Official documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#16798](https://github.com/opensearch-project/OpenSearch/pull/16798) | Introduce a setting to disable download of full cluster state from remote on term mismatch |

### Issues (Design / RFC)
- [Documentation Issue #8957](https://github.com/opensearch-project/documentation-website/issues/8957): Public documentation request

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/opensearch-remote-store.md)
