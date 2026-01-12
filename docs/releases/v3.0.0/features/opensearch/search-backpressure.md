# Search Backpressure Stats Enhancement

## Summary

This release adds task completion count (`completion_count`) to the Search Backpressure Stats API response. This new metric enables operators to calculate cancellation percentages and supports auto-tuning of heap-based cancellation thresholds.

## Details

### What's New in v3.0.0

The Search Backpressure Stats API (`/_nodes/stats/search_backpressure`) now includes a `completion_count` field for both `search_task` and `search_shard_task` statistics. This field tracks the total number of successfully completed search tasks since the node last restarted.

### Technical Changes

#### New Response Field

The `completion_count` field is added to both `SearchTaskStats` and `SearchShardTaskStats` classes:

| Field | Type | Description |
|-------|------|-------------|
| `completion_count` | long | Total number of successfully completed tasks since node restart |

#### API Response Changes

The stats API response now includes `completion_count` in both task types:

```json
{
  "search_backpressure": {
    "search_task": {
      "resource_tracker_stats": { ... },
      "completion_count": 1000,
      "cancellation_stats": {
        "cancellation_count": 10,
        "cancellation_limit_reached_count": 2
      }
    },
    "search_shard_task": {
      "resource_tracker_stats": { ... },
      "completion_count": 5000,
      "cancellation_stats": {
        "cancellation_count": 50,
        "cancellation_limit_reached_count": 5
      }
    },
    "mode": "monitor_only"
  }
}
```

#### Version Compatibility

The `completion_count` field is only serialized for OpenSearch 3.0.0 and later. When communicating with older nodes:
- Reading from older nodes: `completion_count` defaults to `-1`
- Writing to older nodes: `completion_count` is not included in the response

### Usage Example

Calculate the cancellation percentage for search shard tasks:

```bash
# Get search backpressure stats
curl "localhost:9200/_nodes/stats/search_backpressure?pretty"

# Calculate cancellation percentage
# cancellation_percentage = cancellation_count / (completion_count + cancellation_count) * 100
```

### Migration Notes

No migration required. The new field is automatically available after upgrading to v3.0.0.

## Limitations

- The `completion_count` is reset when the node restarts
- When querying mixed-version clusters, nodes running versions prior to 3.0.0 will return `-1` for `completion_count`

## References

### Documentation
- [Search Backpressure Documentation](https://docs.opensearch.org/3.0/tuning-your-cluster/availability-and-recovery/search-backpressure/): Official docs

### Pull Requests
| PR | Description |
|----|-------------|
| [#10028](https://github.com/opensearch-project/OpenSearch/pull/10028) | Add task completion count in search backpressure stats API |

### Issues (Design / RFC)
- [Issue #8698](https://github.com/opensearch-project/OpenSearch/issues/8698): Original feature request

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/search-backpressure.md)
