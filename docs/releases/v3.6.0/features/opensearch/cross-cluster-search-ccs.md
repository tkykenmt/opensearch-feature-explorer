---
tags:
  - opensearch
---
# Cross-Cluster Search (CCS)

## Summary

OpenSearch v3.6.0 adds an optional `cluster_name` setting for CCS sniff mode that validates the remote cluster's name during the transport handshake. This prevents coordinator nodes from accidentally routing search traffic to the wrong cluster when seed hosts become stale or are recycled.

## Details

### What's New in v3.6.0

A new cluster setting `cluster.remote.<alias>.cluster_name` allows users to specify the expected name of a remote cluster. When configured, the sniff connection strategy validates the remote cluster's name during the initial handshake. If the name does not match, the connection attempt for that seed is rejected and the strategy moves on to the next available seed.

### Problem

In environments where hosts are recycled across multiple use cases, configured seed addresses can become stale. A different OpenSearch cluster may start running on the same host and port. Combined with a coordinator node restart, this can cause some coordinator nodes to unknowingly forward search traffic to an unintended cluster.

Previously, CCS sniff mode only validated that subsequent connections went to the same cluster as the first successful handshake. There was no way to enforce that the initial connection itself reached the correct cluster.

### Technical Changes

#### New Cluster Setting

| Setting | Description | Default |
|---------|-------------|---------|
| `cluster.remote.<alias>.cluster_name` | Expected remote cluster name for sniff mode validation | (empty — no validation) |

The setting is:
- Dynamic (`Setting.Property.Dynamic`)
- Node-scoped (`Setting.Property.NodeScope`)
- Only supported in sniff mode (enforced by `StrategyValidator`)

#### Validation Logic

The `getRemoteClusterNamePredicate()` method in `SniffConnectionStrategy` was updated:

1. If `expectedClusterName` is set, the predicate checks the remote cluster name against it
2. If not set, the existing behavior is preserved (accept any cluster on first connect, then enforce consistency)

When validation fails, the error message is:
```
handshake with [<node>] failed: remote cluster name [<actual>] does not match expected remote cluster name [<expected>]
```

The strategy continues to the next seed node, allowing graceful fallback when some seeds are stale.

#### Strategy Rebuild

Changing the `cluster_name` setting triggers a connection strategy rebuild, similar to changing seeds or proxy settings.

#### `_remote/info` API

The `cluster_name` field is included in the `_remote/info` API response when configured:

```json
{
  "cluster_alias": {
    "connected": true,
    "mode": "sniff",
    "seeds": ["10.19.8.59:25668"],
    "num_nodes_connected": 3,
    "max_connections_per_cluster": 30,
    "cluster_name": "expected-cluster-name",
    "initial_connect_timeout": "30s",
    "skip_unavailable": false
  }
}
```

#### Serialization Compatibility

The `expectedClusterName` field is serialized using `writeOptionalString`/`readOptionalString` with a version gate at `Version.V_3_5_0`, ensuring backward compatibility with older nodes in mixed-version clusters.

### Configuration Example

```json
PUT _cluster/settings
{
  "persistent": {
    "cluster.remote": {
      "my-remote-cluster": {
        "seeds": ["remote-host-1:9300", "remote-host-2:9300"],
        "cluster_name": "production-analytics"
      }
    }
  }
}
```

## Limitations

- Only supported in sniff mode; proxy mode is not affected
- Uses cluster name (not cluster UUID) for validation — cluster UUID validation may be considered in the future
- The setting is optional; existing deployments without it continue to work as before

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| https://github.com/opensearch-project/OpenSearch/pull/20532 | Support expected remote cluster name in CCS sniff mode | — |

### Documentation
- https://docs.opensearch.org/3.4/search-plugins/cross-cluster-search/
