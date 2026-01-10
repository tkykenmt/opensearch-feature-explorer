# ML Commons Configuration

## Summary

This bugfix improves the availability of the `.plugins-ml-config` index by changing its `index.auto_expand_replicas` setting from `0-1` to `0-all`. This ensures the ML configuration index has a replica on every node in the cluster, maximizing availability for this small but critical index.

## Details

### What's New in v2.18.0

The `.plugins-ml-config` index now uses `index.auto_expand_replicas: 0-all` instead of `0-1`, ensuring replicas exist on all nodes in the cluster.

### Technical Changes

#### Index Settings Changes

| Setting | Before | After |
|---------|--------|-------|
| `index.auto_expand_replicas` for `.plugins-ml-config` | `0-1` | `0-all` |

#### New Index Utility Constants

The `IndexUtils` class was refactored to support different replication strategies:

| Constant | Description | Settings |
|----------|-------------|----------|
| `DEFAULT_INDEX_SETTINGS` | Standard index settings | `shards: 1`, `auto_expand_replicas: 0-1` |
| `ALL_NODES_REPLICA_INDEX_SETTINGS` | Maximum availability settings | `shards: 1`, `auto_expand_replicas: 0-all` |
| `UPDATED_DEFAULT_INDEX_SETTINGS` | Dynamic update for standard | `auto_expand_replicas: 0-1` |
| `UPDATED_ALL_NODES_REPLICA_INDEX_SETTINGS` | Dynamic update for all-nodes | `auto_expand_replicas: 0-all` |

#### Schema Version Update

The ML config index schema version was incremented from 3 to 4 to trigger the settings update on existing clusters.

### Affected Components

| Component | Change |
|-----------|--------|
| `MLIndicesHandler` | Uses `ALL_NODES_REPLICA_INDEX_SETTINGS` for config index |
| `ConversationMetaIndex` | Uses `DEFAULT_INDEX_SETTINGS` (unchanged behavior) |
| `InteractionsIndex` | Uses `DEFAULT_INDEX_SETTINGS` (unchanged behavior) |

### Migration Notes

- Existing clusters will automatically update the `.plugins-ml-config` index settings when the schema version check detects the change
- No manual intervention required
- The change increases storage requirements proportionally to cluster size

## Limitations

- Using `0-all` can significantly increase storage requirements and indexing load on large clusters
- This setting is only suitable for small, critical indices like the ML config index

## Related PRs

| PR | Description |
|----|-------------|
| [#3017](https://github.com/opensearch-project/ml-commons/pull/3017) | Support index.auto_expand_replicas 0-all for .plugins-ml-config |

## References

- [Issue #3002](https://github.com/opensearch-project/ml-commons/issues/3002): Feature request for 0-all support
- [ML Commons cluster settings](https://docs.opensearch.org/2.18/ml-commons-plugin/cluster-settings/): Official documentation

## Related Feature Report

- [Full feature documentation](../../../../features/ml-commons/ml-commons-configuration.md)
