# Cross-Cluster Replication Bugfixes

## Summary

This release fixes a usability issue in the Cross-Cluster Replication (CCR) plugin where the pause replication API required an empty request body `{}` even when no custom pause reason was needed. The fix makes the request body optional, improving API ergonomics.

## Details

### What's New in v3.4.0

The `POST /_plugins/_replication/{index}/_pause` API no longer requires a request body. Previously, calling this endpoint without a body resulted in a `parse_exception` error:

```json
{
  "error": {
    "root_cause": [
      {
        "type": "parse_exception",
        "reason": "request body or source parameter is required"
      }
    ],
    "type": "parse_exception",
    "reason": "request body or source parameter is required"
  },
  "status": 400
}
```

### Technical Changes

#### Modified Component

| Component | Description |
|-----------|-------------|
| `PauseIndexReplicationHandler` | REST handler for pause replication API |

#### Implementation Details

The `PauseIndexReplicationHandler.prepareRequest()` method was modified to:

1. Check if the request has content (`request.hasContent()`) or a source parameter (`request.hasParam("source")`)
2. If content/source exists, parse it as before using `contentOrSourceParamParser()`
3. If no content/source, create a `PauseIndexReplicationRequest` with the default reason: `"User initiated"` (from `ReplicationMetadataManager.CUSTOMER_INITIATED_ACTION`)

### Usage Example

#### Before (v3.3.0 and earlier)
```bash
# Required empty body - would fail without it
POST /_plugins/_replication/follower-index/_pause
{}
```

#### After (v3.4.0)
```bash
# Body is now optional
POST /_plugins/_replication/follower-index/_pause

# Custom reason still supported
POST /_plugins/_replication/follower-index/_pause
{
  "reason": "Maintenance window"
}
```

### Migration Notes

No migration required. Existing scripts that include an empty body `{}` will continue to work. Scripts can optionally be updated to remove the empty body for cleaner API calls.

## Limitations

- The default pause reason is always `"User initiated"` when no body is provided
- This change only affects the pause API; other CCR APIs retain their existing body requirements

## References

### Documentation
- [Cross-cluster replication API documentation](https://docs.opensearch.org/3.0/tuning-your-cluster/replication-plugin/api/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#1603](https://github.com/opensearch-project/cross-cluster-replication/pull/1603) | Fix the requirement of empty request body in pause replication |

### Issues (Design / RFC)
- [Issue #1468](https://github.com/opensearch-project/cross-cluster-replication/issues/1468): Bug report for required empty request body

## Related Feature Report

- [Full feature documentation](../../../features/cross-cluster-replication/cross-cluster-replication.md)
