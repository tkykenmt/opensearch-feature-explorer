---
tags:
  - opensearch
---
# List Shards API

## Summary

Fixed a bug in the `_list/shards` API that caused `index_closed_exception` errors when clusters contained closed indices. The API now properly handles closed indices by filtering them out before fetching index statistics, while still including closed shards in the response without stats.

## Details

### What's New in v2.19.0

The `_list/shards` API (introduced in v2.18.0) failed with `index_closed_exception` when any closed indices existed in the cluster. This occurred because the pagination strategy passed concrete index names directly to `TransportIndicesStatsAction`, which uses `IndicesOptions.strictExpandOpenAndForbidClosed()` by default.

### Technical Changes

The fix modifies `TransportCatShardsAction` to filter out closed indices before calling `TransportIndicesStatsAction`:

```java
private String[] filterClosedIndices(ClusterState clusterState, List<String> strategyIndices) {
    return strategyIndices.stream().filter(index -> {
        IndexMetadata metadata = clusterState.metadata().indices().get(index);
        return metadata != null && metadata.getState().equals(IndexMetadata.State.CLOSE) == false;
    }).toArray(String[]::new);
}
```

### Behavior After Fix

| Query | Behavior |
|-------|----------|
| `/_list/shards` (default) | Returns all shards including closed indices; stats only for open indices |
| `/_list/shards/closed-index` | Returns closed shards without stats (no error) |
| `/_list/shards/closed-index*` | Returns empty (wildcards don't expand to closed indices) |
| `/_list/shards/open-index` | Returns shards with full stats |

This behavior now matches `_cat/shards` API behavior for consistency.

## Limitations

- Closed indices appear in shard listings but without statistics (docs count, store size, etc.)
- Wildcard patterns do not expand to match closed or hidden indices (consistent with `_cat/shards`)

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16606](https://github.com/opensearch-project/OpenSearch/pull/16606) | Fixing _list/shards API for closed indices | [#16626](https://github.com/opensearch-project/OpenSearch/issues/16626) |

### Issues
- [#16626](https://github.com/opensearch-project/OpenSearch/issues/16626): [BUG] _list/shards API failing with index_closed_exception
