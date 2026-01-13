---
tags:
  - opensearch
---
# Sliced Search Optimization

## Summary

OpenSearch v2.19.0 introduces an optimization for sliced scroll searches that significantly reduces the number of open scroll contexts. Previously, sliced searches fanned out to every shard and applied a `MatchNoDocsQuery` filter on non-matching shards. Now, the coordinator filters shards before routing, reducing open scroll contexts from `numShards × numSlices` to `max(numShards, numSlices)`.

## Details

### What's New in v2.19.0

The optimization moves shard filtering from the data node level to the coordinator level. When a sliced search is executed, the coordinator now determines which shards belong to each slice before fanning out requests, avoiding unnecessary scroll context creation on shards that won't return results.

### Technical Changes

#### Coordinator-Level Shard Filtering

The `OperationRouting.searchShards()` method now accepts a `SliceBuilder` parameter. When a slice is specified, shards are filtered based on the slice ID and maximum slice count:

```java
public boolean shardMatches(int shardOrdinal, int numShards) {
    if (max >= numShards) {
        // Slices are distributed over shards
        return id % numShards == shardOrdinal;
    }
    // Shards are distributed over slices
    return shardOrdinal % max == id;
}
```

#### Search Shards API Enhancement

The `_search_shards` API now accepts a request body with slice parameters, allowing users to preview which shards will be targeted for a given slice configuration:

```json
GET test_index/_search_shards
{
  "slice": {
    "id": 0,
    "max": 3
  }
}
```

#### Scroll Context Reduction

| Scenario | Before v2.19.0 | After v2.19.0 |
|----------|----------------|---------------|
| 36 shards, 10 slices | 360 contexts | 36 contexts |
| 10 shards, 36 slices | 360 contexts | 36 contexts |
| 51 shards, 10 slices | 510 contexts | 51 contexts |

### Architecture

```mermaid
flowchart TB
    subgraph "Before v2.19.0"
        A1[Coordinator] --> B1[All Shards]
        B1 --> C1[MatchNoDocsQuery on non-matching]
    end
    
    subgraph "After v2.19.0"
        A2[Coordinator] --> F[Filter by Slice]
        F --> B2[Matching Shards Only]
    end
```

### Use Cases

This optimization benefits:

- `delete_by_query` with slices
- `update_by_query` with slices
- Sliced scroll searches for large data exports
- Multi-tenant clusters with concurrent bulk operations

## Limitations

- The optimization applies only to shard-based slicing (default behavior)
- Custom routing parameters are respected and may affect slice-to-shard mapping
- The `_search_shards` API body parameter requires OpenSearch 2.19.0+

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16771](https://github.com/opensearch-project/OpenSearch/pull/16771) | Filter shards for sliced search at coordinator | [#16289](https://github.com/opensearch-project/OpenSearch/issues/16289) |

### Documentation

- [Scroll API](https://docs.opensearch.org/2.19/api-reference/scroll/)
- [Paginate Results](https://docs.opensearch.org/2.19/search-plugins/searching-data/paginate/)
