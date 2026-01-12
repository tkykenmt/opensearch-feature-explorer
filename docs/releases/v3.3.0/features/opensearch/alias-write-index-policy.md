---
tags:
  - indexing
---

# Alias Write Index Policy

## Summary

OpenSearch v3.3.0 introduces a new `alias_write_index_policy` parameter for the Restore Snapshot API. This feature allows users to control how the `is_write_index` attribute of aliases is handled during snapshot restore operations, enabling safe bidirectional Cross-Cluster Replication (CCR) scenarios.

## Details

### What's New in v3.3.0

The new `alias_write_index_policy` parameter provides control over alias write index behavior during restore:

- **PRESERVE** (default): Maintains the original `is_write_index` attribute from the snapshot
- **STRIP_WRITE_INDEX**: Forces `is_write_index=false` on all restored aliases

### Technical Changes

#### New Components

| Component | Description |
|-----------|-------------|
| `AliasWriteIndexPolicy` | Enum defining policy options: `PRESERVE` and `STRIP_WRITE_INDEX` |
| `alias_write_index_policy` | New REST parameter for restore snapshot requests |

#### API Changes

The Restore Snapshot API now accepts a new parameter:

```
POST /_snapshot/{repository}/{snapshot}/_restore
{
  "alias_write_index_policy": "strip_write_index"
}
```

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `alias_write_index_policy` | String | Controls write index handling: `preserve` or `strip_write_index` | `preserve` |

### Usage Example

```json
POST /_snapshot/my_repository/my_snapshot/_restore
{
  "indices": "my_index",
  "include_aliases": true,
  "alias_write_index_policy": "strip_write_index"
}
```

This restores `my_index` with all its aliases, but forces `is_write_index=false` on all aliases to prevent write conflicts.

### Use Case: Bidirectional CCR

When setting up bidirectional Cross-Cluster Replication:

1. Leader cluster has index with alias where `is_write_index=true`
2. Snapshot is taken and restored to follower cluster
3. Without this feature, restore fails due to "alias has more than one write index" error
4. With `strip_write_index` policy, follower's restored aliases have `is_write_index=false`
5. Both clusters can now operate without write alias conflicts

### Migration Notes

- Existing restore operations are unaffected (default is `PRESERVE`)
- Use `strip_write_index` when restoring to clusters that already have write aliases
- The policy is applied post-rename during alias restoration

## Limitations

- Only applies to aliases restored from snapshots
- Does not affect existing aliases in the target cluster
- Cannot selectively apply policy to specific aliases (applies to all)

## References

### Documentation
- [Restore Snapshot API](https://docs.opensearch.org/3.0/api-reference/snapshots/restore-snapshot/): Official documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#19368](https://github.com/opensearch-project/OpenSearch/pull/19368) | Enable Safe Bidirectional CCR via Alias policy on Restore |

### Issues (Design / RFC)
- [Issue #16139](https://github.com/opensearch-project/OpenSearch/issues/16139): Unable to restore an index from snapshot that was a write index at the time

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/alias-write-index-policy.md)
