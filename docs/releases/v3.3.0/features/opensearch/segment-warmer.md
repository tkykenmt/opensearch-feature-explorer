---
tags:
  - indexing
  - observability
  - performance
---

# Segment Warmer Metrics

## Summary

OpenSearch v3.3.0 introduces comprehensive metrics for monitoring merged segment warming operations. These metrics provide visibility into the pre-copy process that transfers merged segments to replica shards before refresh, enabling operators to monitor warming performance, data transfer volumes, and identify potential issues.

## Details

### What's New in v3.3.0

This release adds a new `warmer` section under `merges` statistics, exposing metrics at node, index, and shard levels. The metrics track both cumulative totals and point-in-time state of warming operations.

### Technical Changes

#### New Components

| Component | Description |
|-----------|-------------|
| `MergedSegmentTransferTracker` | Tracks statistics for merged segment replication operations including invocations, failures, bytes transferred, and timing |
| `MergedSegmentWarmerStats` | Stores and serializes warmer statistics for API responses |

#### New Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `total_invocations_count` | Cumulative | Total number of warm operations invoked |
| `total_time_millis` | Cumulative | Total wallclock time spent in warming operations |
| `total_failure_count` | Cumulative | Number of failed warming attempts |
| `total_bytes_sent` | Cumulative | Total data volume uploaded by primary shards |
| `total_bytes_received` | Cumulative | Total data volume downloaded by replica shards |
| `total_send_time_millis` | Cumulative | Time spent uploading segments |
| `total_receive_time_millis` | Cumulative | Time spent downloading segments |
| `ongoing_count` | Point-in-time | Current number of active warming operations |

#### API Changes

The warmer metrics are exposed through existing stats APIs:

**Node Stats API** (`/_nodes/stats/indices/merge`):
```json
{
  "indices": {
    "merges": {
      "warmer": {
        "total_invocations_count": 23,
        "total_time_millis": 4217,
        "total_failure_count": 0,
        "total_bytes_sent": 12107729,
        "total_bytes_received": 0,
        "total_send_time_millis": 1459,
        "total_receive_time_millis": 0,
        "ongoing_count": 0
      }
    }
  }
}
```

**Index Stats API** (`/_stats/merge`):
```json
{
  "_all": {
    "primaries": {
      "merges": {
        "warmer": {
          "total_invocations_count": 19,
          "total_time_millis": 3589,
          "total_failure_count": 0,
          "total_bytes_sent": 9071479,
          "total_bytes_received": 0,
          "total_send_time_millis": 1271,
          "total_receive_time_millis": 0,
          "ongoing_count": 0
        }
      }
    }
  }
}
```

**CAT Shards API** (`/_cat/shards?v&h=index,shard,prirep,merges.warmer.*`):
```
index       shard prirep merges.warmer.total_invocations merges.warmer.total_time ...
test-index  0     p      23                              4.2s
test-index  0     r      0                               0s
```

**CAT Nodes API** (`/_cat/nodes?v&h=id,merges.warmer.*`):
```
id   merges.warmer.total_invocations merges.warmer.total_time ...
n3zT 23                              4.2s
2-by 0                               0s
```

### Usage Example

Monitor segment warmer performance across the cluster:

```bash
# Get warmer stats for all nodes
GET /_nodes/stats/indices/merge?filter_path=**.warmer

# Get warmer stats per shard
GET /_stats/merge?level=shards&filter_path=**.warmer

# Monitor ongoing warming operations
GET /_cat/shards?v&h=index,shard,prirep,merges.warmer.ongoing_count
```

### Interpreting Metrics

- **Primary shards**: Show `total_bytes_sent` and `total_send_time_millis` (uploading merged segments)
- **Replica shards**: Show `total_bytes_received` and `total_receive_time_millis` (downloading merged segments)
- **High `total_failure_count`**: Indicates issues with segment warming; segments fall back to standard replication
- **Non-zero `ongoing_count`**: Active warming operations in progress

## Limitations

- Metrics are only populated when merged segment warmer feature is enabled
- Requires segment replication (`replication.type: SEGMENT`)
- Experimental feature requiring feature flag: `opensearch.experimental.feature.merged_segment_warmer.enabled: true`

## References

### Documentation
- [PR #18683](https://github.com/opensearch-project/OpenSearch/pull/18683): Remote store support for merged segment warming

### Pull Requests
| PR | Description |
|----|-------------|
| [#18929](https://github.com/opensearch-project/OpenSearch/pull/18929) | Add metrics for the merged segment warmer feature |

### Issues (Design / RFC)
- [Issue #17528](https://github.com/opensearch-project/OpenSearch/issues/17528): RFC - Introduce Pre-copy Merged Segment into Segment Replication

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/opensearch-segment-warmer.md)
