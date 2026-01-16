---
tags:
  - query-insights
---
# Query Plugin Fixes

## Summary

Bug fixes for the Query Insights plugin in v2.16.0, addressing input validation and stream serialization issues. These fixes were synced from OpenSearch core to the standalone plugin repository.

## Details

### What's New in v2.16.0

#### Top N Size Validation Fix

Added lower bound validation for the `top_n_size` setting. Previously, negative values could be set which would cause unexpected behavior.

**Before**: Setting `top_n_size` to -1 was accepted
**After**: Values must be between 1 and `MAX_N_SIZE` (100)

```bash
# This now returns an error
PUT _cluster/settings
{
  "persistent": {
    "search.insights.top_queries.latency.top_n_size": -1
  }
}

# Error response
{
  "error": {
    "type": "illegal_argument_exception",
    "reason": "Top N size setting for [latency] should be between 1 and 100, was (-1)"
  },
  "status": 400
}
```

#### Stream Serialization Fix

Fixed stream serialization issues for complex data structures in `SearchQueryRecord`. The `TASK_RESOURCE_USAGES` attribute containing `TaskResourceInfo` objects was not being properly serialized/deserialized.

**Changes**:
- Added `writeValueTo()` method in `Attribute` class to handle `List<Writeable>` types
- Added `readAttributeValue()` method to properly deserialize `TaskResourceInfo` lists
- Added `readAttributeMap()` method for reading attribute maps with type-aware deserialization
- Updated `SearchQueryRecord.writeTo()` to use the new serialization methods

## Limitations

None specific to these fixes.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [query-insights#13](https://github.com/opensearch-project/query-insights/pull/13) | Sync bug fixes from core to plugin repo | - |
| [OpenSearch#14587](https://github.com/opensearch-project/OpenSearch/pull/14587) | Validate lower bound for top n size | - |
| [OpenSearch#14681](https://github.com/opensearch-project/OpenSearch/pull/14681) | Add task resource tracking service to cluster service | - |
