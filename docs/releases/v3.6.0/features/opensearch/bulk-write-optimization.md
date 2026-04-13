---
tags:
  - opensearch
---
# Bulk Write Optimization

## Summary

OpenSearch v3.6.0 introduces adaptive shard selection for bulk writes on append-only indices. When enabled, the coordinating node routes all documents in a bulk request to the shard hosted on the best-performing node, based on real-time metrics including service time EWMA (exponentially weighted moving average), queue size, and active client connections. In online log analysis benchmarks, this optimization improved bulk indexing throughput by over 20%.

## Details

### What's New in v3.6.0

Adaptive shard selection for bulk writes uses a two-stage selection algorithm:

1. Collect per-node metrics (service time EWMA, queue size, client connections) from `ResponseCollectorService`
2. Rank nodes using `IndexShardRoutingTable.rankShardsAndUpdateStats()` — the same ranking algorithm used for adaptive replica selection in search
3. Select the best-performing node, then randomly pick one of its primary shards for the target index

This ensures all documents in a single bulk request go to the same shard on the least-loaded node, reducing cross-node network hops and balancing write load.

### Configuration

| Setting | Description | Default | Scope |
|---------|-------------|---------|-------|
| `index.append_only.enabled` | Enable append-only mode (prerequisite) | `false` | Index, Final |
| `index.bulk.adaptive_shard_selection.enabled` | Enable adaptive shard selection for bulk writes | `false` | Index, Dynamic |

Both settings must be enabled for adaptive shard selection to take effect. Enabling `index.bulk.adaptive_shard_selection.enabled` on a non-append-only index raises an `IllegalArgumentException`.

### Usage Example

```json
PUT my-log-index
{
  "settings": {
    "index.append_only.enabled": "true",
    "index.bulk.adaptive_shard_selection.enabled": "true",
    "index.number_of_shards": 3
  }
}
```

Or enable on an existing append-only index:

```json
PUT my-log-index/_settings
{
  "index.bulk.adaptive_shard_selection.enabled": "true"
}
```

### Constraints

- Custom document IDs are not allowed when adaptive shard selection is enabled. Bulk requests with explicit `_id` values return a `validation_exception` (HTTP 400).
- Only `index` operations (without `_id`) are supported; `update`, `delete`, and `create` with `_id` are rejected.
- The feature requires `index.append_only.enabled` to be `true`.

### Technical Changes

- `TransportBulkAction`: Added `bulkAdaptiveSelectShard()` method implementing two-stage node ranking and shard selection. Tracks per-node client connections via `ConcurrentMap`. Collects response metrics (service time EWMA, queue size) from `BulkShardResponse` and feeds them to `ResponseCollectorService`.
- `BulkShardResponse`: Extended with `serviceTimeEWMAInNanos` and `nodeQueueSize` fields, serialized for v3.6.0+ nodes with backward-compatible defaults for older versions.
- `TransportShardBulkAction`: Measures actual service time on the primary shard and reports thread pool queue size via `OpenSearchThreadPoolExecutor.getQueue().size()`.
- `IndexMetadata`: Added `INDEX_BULK_ADAPTIVE_SHARD_SELECTION_ENABLED` setting with validation that prevents enabling on non-append-only indices.
- `IndexShardRoutingTable.rankShardsAndUpdateStats()`: Changed from `private` to `public` to allow reuse by the bulk write path.

## Limitations

- In low-indexing-pressure scenarios, a potential ~5% degradation in indexing performance may occur due to metric collection overhead.
- All documents in a bulk request for a given index are routed to a single shard, which may cause temporary hotspots if the selected shard's node becomes slow between selection and execution.
- Only works with append-only indices; not applicable to indices requiring updates or deletes.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#20065](https://github.com/opensearch-project/OpenSearch/pull/20065) | Add adaptive shard selection for bulk writes on append-only indices | [#18307](https://github.com/opensearch-project/OpenSearch/issues/18307), [#18306](https://github.com/opensearch-project/OpenSearch/issues/18306), [#9219](https://github.com/opensearch-project/OpenSearch/issues/9219) |

### Issues
- [#18307](https://github.com/opensearch-project/OpenSearch/issues/18307): META - Automatic routing for bulk
- [#18306](https://github.com/opensearch-project/OpenSearch/issues/18306): Adaptive shard selection for bulk writes
- [#9219](https://github.com/opensearch-project/OpenSearch/issues/9219): Automatic routing for bulk (original proposal)
