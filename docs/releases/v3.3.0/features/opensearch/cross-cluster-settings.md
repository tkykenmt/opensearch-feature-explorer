---
tags:
  - domain/core
  - component/server
  - search
---
# Cross-Cluster Settings

## Summary

This release fixes a bug where the `skip_unavailable` setting for cross-cluster search (CCS) would reset to its default value when remote cluster seed nodes were updated. This fix ensures that the `skip_unavailable` setting is properly preserved during cluster configuration changes, allowing CCS to correctly return partial results when remote clusters become unavailable.

## Details

### What's New in v3.3.0

The fix addresses a critical issue in cross-cluster search where updating the `cluster.remote.<alias>.seeds` setting would cause the `skip_unavailable` setting to revert to its default value (`false`). This caused CCS queries to fail with errors instead of returning partial results when remote clusters were unavailable.

### Technical Changes

#### Root Cause

The `RemoteClusterAware.listenForUpdates()` method was not listening for changes to the `REMOTE_CLUSTER_SKIP_UNAVAILABLE` setting. When seed nodes were updated, the cluster settings update consumer would rebuild the remote cluster connection without preserving the `skip_unavailable` value.

#### Fix Implementation

Added `RemoteClusterService.REMOTE_CLUSTER_SKIP_UNAVAILABLE` to the list of settings monitored by the `listenForUpdates()` method in `RemoteClusterAware.java`:

```java
public void listenForUpdates(ClusterSettings clusterSettings) {
    List<Setting.AffixSetting<?>> remoteClusterSettings = Arrays.asList(
        RemoteClusterService.REMOTE_CLUSTER_COMPRESS,
        RemoteClusterService.REMOTE_CLUSTER_PING_SCHEDULE,
        RemoteConnectionStrategy.REMOTE_CONNECTION_MODE,
        RemoteClusterService.REMOTE_CLUSTER_SKIP_UNAVAILABLE,  // Added
        SniffConnectionStrategy.REMOTE_CLUSTERS_PROXY,
        SniffConnectionStrategy.REMOTE_CLUSTER_SEEDS,
        // ... other settings
    );
    clusterSettings.addAffixGroupUpdateConsumer(remoteClusterSettings, this::validateAndUpdateRemoteCluster);
}
```

### Usage Example

Configure cross-cluster search with `skip_unavailable` enabled:

```json
PUT _cluster/settings
{
  "persistent": {
    "cluster.remote": {
      "remote-cluster": {
        "seeds": ["172.31.0.3:9300"],
        "skip_unavailable": true
      }
    }
  }
}
```

After this fix, updating the seed nodes will preserve the `skip_unavailable` setting:

```json
PUT _cluster/settings
{
  "persistent": {
    "cluster.remote": {
      "remote-cluster": {
        "seeds": ["172.31.0.4:9300"],
        "skip_unavailable": true
      }
    }
  }
}
```

CCS queries will now correctly return partial results with `skipped: 1` when the remote cluster is unavailable, instead of failing with an error.

### Migration Notes

No migration required. This is a bug fix that improves the reliability of existing cross-cluster search configurations.

## Limitations

- The fix only affects the `skip_unavailable` setting persistence during configuration updates
- Other cross-cluster settings behavior remains unchanged

## References

### Documentation
- [Cross-cluster search documentation](https://docs.opensearch.org/3.0/search-plugins/cross-cluster-search/): Official docs

### Pull Requests
| PR | Description |
|----|-------------|
| [#18766](https://github.com/opensearch-project/OpenSearch/pull/18766) | Fix skip_unavailable setting changing to default during node drop |

### Issues (Design / RFC)
- [Issue #13798](https://github.com/opensearch-project/OpenSearch/issues/13798): Original bug report

## Related Feature Report

- Full feature documentation
