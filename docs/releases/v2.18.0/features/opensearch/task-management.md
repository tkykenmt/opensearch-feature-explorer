# Task Management

## Summary

This release fixes a critical bug in the `.tasks` index mapping that caused `StrictDynamicMappingException` when storing task results for cancelled tasks. The fix adds missing fields (`cancellation_time_millis` and `resource_stats`) to the task index mapping, ensuring proper task result storage across all OpenSearch operations.

## Details

### What's New in v2.18.0

The `.tasks` index uses strict dynamic mapping, which means all fields must be explicitly defined in the mapping before they can be indexed. Two fields were missing from the mapping:

- `cancellation_time_millis`: Records when a task was cancelled
- `resource_stats`: Contains resource usage statistics for the task

Without these fields, any operation that cancelled a task (such as deleting an auto-follow rule in Cross-Cluster Replication) would fail to update the `.tasks` index.

### Technical Changes

#### Mapping Version Update

The task index mapping version was incremented from 4 to 5 to trigger mapping updates on existing clusters.

#### New Fields Added

| Field | Type | Description |
|-------|------|-------------|
| `cancellation_time_millis` | `long` | Timestamp when the task was cancelled |
| `resource_stats` | `object` (disabled) | Resource usage statistics for the task |

#### Updated Mapping Structure

```json
{
  "_doc": {
    "_meta": {
      "version": 5
    },
    "dynamic": "strict",
    "properties": {
      "task": {
        "properties": {
          "cancellation_time_millis": {
            "type": "long"
          },
          "resource_stats": {
            "type": "object",
            "enabled": false
          }
        }
      }
    }
  }
}
```

### Usage Example

After this fix, task cancellation operations work correctly:

```bash
# Cancel a task - now properly stores result in .tasks index
POST _tasks/<task_id>/_cancel

# View stored task results
GET .tasks/_search
{
  "query": {
    "match_all": {}
  }
}
```

### Migration Notes

- No manual migration required
- The mapping version increment ensures automatic updates
- Existing `.tasks` indexes will be updated when OpenSearch starts

## Limitations

- The `resource_stats` field is stored as a disabled object (not indexed/searchable)
- This fix is specifically for the internal `.tasks` system index

## References

### Documentation
- [Tasks API Documentation](https://docs.opensearch.org/2.18/api-reference/tasks/): Official Tasks API docs

### Pull Requests
| PR | Description |
|----|-------------|
| [#16201](https://github.com/opensearch-project/OpenSearch/pull/16201) | Fix missing fields in task index mapping |

### Issues (Design / RFC)
- [Issue #16060](https://github.com/opensearch-project/OpenSearch/issues/16060): Original bug report

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/task-management.md)
