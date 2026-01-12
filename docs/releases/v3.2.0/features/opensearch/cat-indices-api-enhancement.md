---
tags:
  - indexing
  - observability
  - performance
---

# Cat Indices API Enhancement

## Summary

OpenSearch v3.2.0 enhances the `_cat/indices` API by adding two new columns that expose the timestamp of the last index request processed for each index. This feature helps operators quickly identify which indices are actively receiving updates, making it easier to monitor indexing activity and troubleshoot cluster performance issues.

## Details

### What's New in v3.2.0

The `_cat/indices` API now includes two new optional columns:

| Column | Alias | Description |
|--------|-------|-------------|
| `last_index_request_timestamp` | `last_index_ts`, `lastIndexRequestTimestamp` | Raw timestamp in milliseconds since epoch |
| `last_index_request_timestamp_string` | `last_index_ts_string`, `lastIndexRequestTimestampString` | Human-readable UTC ISO 8601 format |

This mirrors the existing approach for `creation.date` and `creation.date.string`, providing both machine-friendly and human-friendly representations.

### Technical Changes

#### Architecture Changes

```mermaid
graph TB
    subgraph "Index Request Flow"
        IR[Index/Delete Request] --> IS[IndexShard]
        IS --> IIS[InternalIndexingStats]
        IIS --> MM[MaxMetric]
        MM --> TS[Timestamp Tracking]
    end
    
    subgraph "Cat Indices API"
        CAT[/_cat/indices] --> RIA[RestIndicesAction]
        RIA --> ISR[IndicesStatsRequest]
        ISR --> Stats[IndexingStats]
        Stats --> Response[API Response]
    end
    
    TS --> Stats
```

#### New Components

| Component | Description |
|-----------|-------------|
| `MaxMetric` | New metric class using `LongAccumulator` to track maximum timestamp values efficiently |
| `maxLastIndexRequestTimestamp` field | Added to `IndexingStats.Stats` to store the timestamp |

#### Implementation Details

- The timestamp is updated on successful index and delete operations
- Uses `LongAccumulator` with `Long::max` for thread-safe maximum value tracking
- Timestamp is obtained from `ThreadPool.absoluteTimeInMillis()` for consistency
- Aggregation across shards uses `Math.max()` to surface the most recent timestamp

#### Serialization

The new field is serialized only for OpenSearch v3.2.0 and later:
- Nodes running v3.2.0+ will include `maxLastIndexRequestTimestamp` in the wire protocol
- Older nodes will receive/send `0L` as the default value for backward compatibility

### Usage Example

Query the new columns:

```bash
GET _cat/indices?v&h=index,last_index_request_timestamp,last_index_request_timestamp.string
```

Example response:

```
index                          last_index_request_timestamp last_index_request_timestamp.string
movies                         1710000000000                2024-03-09T16:00:00.000Z
logs-2024.03                   1710001234567                2024-03-09T16:20:34.567Z
```

### Use Cases

1. **Identifying Active Indices**: Quickly determine which indices are receiving updates during high indexing load
2. **Troubleshooting**: When investigating cluster performance issues, identify which shards are actively processing requests
3. **Monitoring**: Track indexing activity patterns across indices over time
4. **Capacity Planning**: Understand which indices are most actively used for write operations

### Migration Notes

- No migration required - this is an additive change
- New columns are disabled by default (use `h=` parameter to include them)
- Mixed-version clusters will show `0` or `null` for nodes running older versions

## Limitations

- The timestamp reflects the last successful index or delete operation only
- Bulk operations update the timestamp once per successful document
- The timestamp is not persisted - it resets when a shard is relocated or the node restarts
- In mixed-version clusters, older nodes will report `0` for this field

## References

### Documentation
- [CAT indices API Documentation](https://docs.opensearch.org/3.0/api-reference/cat/cat-indices/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#18405](https://github.com/opensearch-project/OpenSearch/pull/18405) | Expose Last Index Request Timestamp in Cat Indices API |

### Issues (Design / RFC)
- [Issue #10766](https://github.com/opensearch-project/OpenSearch/issues/10766): Stats API to identify which indices (and shards?) are getting updates

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/opensearch-cat-indices-api.md)
