# Job Scheduler Bugfixes

## Summary

This release fixes a compatibility issue with v1 index templates in the Job Scheduler plugin. The bug caused system indexes (`LockService` and `JobDetailsService`) to use dynamic mappings instead of the specified mappings when a deprecated v1 index template was present in the cluster.

## Details

### What's New in v2.17.0

Fixed the `CreateIndexRequest.mapping()` calls in `LockService` and `JobDetailsService` to include the required `MediaType` parameter, ensuring proper mapping application even when v1 index templates exist.

### Technical Changes

#### Root Cause

The `CreateIndexRequest.mapping(String)` method requires the mapping JSON to be wrapped in a `_doc` field when v1 index templates are present. However, the Job Scheduler code was using the single-argument version without specifying the content type, which caused the mapping to be silently ignored.

#### The Fix

The fix adds the `MediaType` parameter to `CreateIndexRequest.mapping()` calls:

```java
// Before (broken with v1 templates)
CreateIndexRequest request = new CreateIndexRequest(indexName).mapping(mapping);

// After (works with v1 templates)
CreateIndexRequest request = new CreateIndexRequest(indexName).mapping(
    mapping,
    (MediaType) XContentType.JSON
);
```

#### Affected Components

| Component | File | Description |
|-----------|------|-------------|
| `LockService` | `spi/src/main/java/org/opensearch/jobscheduler/spi/utils/LockService.java` | Distributed lock index creation |
| `JobDetailsService` | `src/main/java/org/opensearch/jobscheduler/utils/JobDetailsService.java` | Job metadata index creation |

### Impact

Without this fix, clusters with v1 index templates (deprecated but still supported) would experience:
- System indexes created with dynamic mappings instead of specified mappings
- Potential `IllegalArgumentException` errors like `mapper [master_key] cannot be changed from type [text] to [keyword]`
- Job scheduling failures due to incorrect field types

### Migration Notes

No migration required. The fix is automatically applied when upgrading to v2.17.0. Existing indexes with incorrect mappings may need to be recreated if experiencing mapping conflicts.

## Limitations

- This fix addresses the Job Scheduler plugin only; similar issues exist in other plugins (see Related Issues)
- V1 index templates remain deprecated and should be migrated to v2 composable templates

## References

### Documentation
- [CreateIndexRequest Javadoc](https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/action/admin/indices/create/CreateIndexRequest.java#L246-L257): Documentation for mapping method
- [Job Scheduler Documentation](https://docs.opensearch.org/2.17/monitoring-your-cluster/job-scheduler/index/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#658](https://github.com/opensearch-project/job-scheduler/pull/658) | Fix system index compatibility with v1 templates |

### Issues (Design / RFC)
- [Issue #14984](https://github.com/opensearch-project/OpenSearch/issues/14984): Original bug report affecting multiple plugins

## Related Feature Report

- [Full feature documentation](../../../../features/job-scheduler/job-scheduler.md)
