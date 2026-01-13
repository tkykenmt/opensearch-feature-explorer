---
tags:
  - opensearch
---
# Index Settings API

## Summary

Fixed a bug where the `index.number_of_routing_shards` setting was not displayed in the Get Index Settings API response when it was explicitly set during index creation. Previously, users had to query `_cluster/state` to retrieve this value.

## Details

### What's New in v2.19.0

The `index.number_of_routing_shards` setting is now properly returned by the Get Index Settings API (`GET {index}/_settings`) when it was explicitly specified at index creation time.

### Background

The `number_of_routing_shards` setting determines the number of routing shards used when splitting an index. This value is important for planning index split operations, as it defines the valid split factors and maximum number of splits possible.

Prior to this fix:
- The setting was stored in `IndexMetadata` but removed from the settings before persisting
- Users could only retrieve the value via `GET _cluster/state` under `routing_num_shards`
- The Get Index Settings API did not include this setting even when explicitly set

### Technical Changes

1. **IndexMetadata.java**: Added `Property.NotCopyableOnResize` to the `INDEX_NUMBER_OF_ROUTING_SHARDS_SETTING` definition to prevent the setting from being copied during resize operations while allowing it to be persisted in index settings.

2. **MetadataCreateIndexService.java**: Removed the code that explicitly stripped `INDEX_NUMBER_OF_ROUTING_SHARDS_SETTING` from the aggregated settings before building the index metadata.

### Behavior

| Scenario | Before v2.19.0 | After v2.19.0 |
|----------|----------------|---------------|
| Explicitly set `number_of_routing_shards` | Not shown in `_settings` | Shown in `_settings` |
| Default `number_of_routing_shards` | Not shown | Not shown (expected) |

### Usage Example

```bash
# Create index with explicit routing shards
PUT /my-index
{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 1,
    "number_of_routing_shards": 4
  }
}

# Get settings - now shows number_of_routing_shards
GET /my-index/_settings?flat_settings=true

# Response includes:
# "index.number_of_routing_shards": "4"
```

## Limitations

- The setting is only shown when explicitly set at index creation time
- Default/calculated values are not displayed (this is expected behavior)
- This is a static setting and cannot be changed after index creation

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16294](https://github.com/opensearch-project/OpenSearch/pull/16294) | Fix get index settings API doesn't show `number_of_routing_shards` when explicitly set | [#14199](https://github.com/opensearch-project/OpenSearch/issues/14199) |

### Issues
- [#14199](https://github.com/opensearch-project/OpenSearch/issues/14199): Bug report describing the missing setting in API response
