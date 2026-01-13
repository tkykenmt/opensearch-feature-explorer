---
tags:
  - domain/core
  - component/server
  - indexing
  - search
---
# Search Tie-breaking

## Summary

OpenSearch v3.3.0 introduces the `_shard_doc` sort field, enabling deterministic tie-breaking for search result pagination. This feature allows users to sort by a composite key of shard ID and document ID, ensuring consistent ordering when paginating through results with `search_after` and Point in Time (PIT). This addresses a common issue where documents with identical scores could appear in inconsistent order across pages.

## Details

### What's New in v3.3.0

The `_shard_doc` pseudo-field provides a unique, deterministic sort key for each document by combining the shard ID and global document ID into a single 64-bit value: `(shardId << 32) | globalDocId`. This ensures that every document has a unique sort value, eliminating duplicates and gaps when paginating through search results.

### Technical Changes

#### Architecture Changes

```mermaid
graph TB
    subgraph "Search Request"
        A[Search Query] --> B{Has _shard_doc sort?}
        B -->|Yes| C[Validate PIT present]
        B -->|No| D[Standard Sort]
        C -->|Valid| E[ShardDocSortBuilder]
        C -->|Invalid| F[Validation Error]
    end
    
    subgraph "Sort Execution"
        E --> G[ShardDocFieldComparatorSource]
        G --> H[Compute: shardId << 32 | docBase + doc]
        H --> I[Long comparison for ordering]
    end
    
    subgraph "Pagination"
        I --> J[Return sort values in response]
        J --> K[Use in search_after for next page]
    end
```

#### New Components

| Component | Description |
|-----------|-------------|
| `ShardDocSortBuilder` | Sort builder for the `_shard_doc` pseudo-field, handles JSON parsing and sort field construction |
| `ShardDocFieldComparatorSource` | Lucene `FieldComparatorSource` that computes the composite key `(shardId << 32) \| globalDocId` |

#### Validation Rules

| Rule | Description |
|------|-------------|
| PIT Required | `_shard_doc` can only be used with Point in Time (PIT) |
| No Scroll | `_shard_doc` cannot be used with scroll API |
| No Duplicates | Only one `_shard_doc` sort can be specified per query |

### Usage Example

```json
// Step 1: Create a Point in Time
POST /my-index/_search/point_in_time?keep_alive=5m

// Step 2: Search with _shard_doc sort
GET /_search
{
  "size": 100,
  "pit": {
    "id": "<pit_id>",
    "keep_alive": "5m"
  },
  "sort": [
    { "timestamp": "desc" },
    { "_shard_doc": "asc" }
  ]
}

// Step 3: Paginate using search_after with the last document's sort values
GET /_search
{
  "size": 100,
  "pit": {
    "id": "<pit_id>",
    "keep_alive": "5m"
  },
  "sort": [
    { "timestamp": "desc" },
    { "_shard_doc": "asc" }
  ],
  "search_after": ["2024-01-15T10:30:00Z", 4294967296]
}
```

### Migration Notes

- If you're currently using `search_after` with PIT and experiencing duplicate results, add `_shard_doc` as a tie-breaker sort field
- Replace scroll-based pagination with PIT + `search_after` + `_shard_doc` for more consistent results
- The `_shard_doc` sort value is a `Long` type in the response

## Limitations

- Requires Point in Time (PIT) - cannot be used without PIT
- Cannot be combined with scroll API
- Only one `_shard_doc` sort field allowed per query
- Bucketed sort is not supported for `_shard_doc`

## References

### Documentation
- [Point in Time Documentation](https://docs.opensearch.org/3.0/search-plugins/searching-data/point-in-time/): Official PIT documentation
- [Paginate Results Documentation](https://docs.opensearch.org/3.0/search-plugins/searching-data/paginate/): Pagination methods in OpenSearch

### Pull Requests
| PR | Description |
|----|-------------|
| [#18924](https://github.com/opensearch-project/OpenSearch/pull/18924) | Add support for search tie-breaking by _shard_doc |

### Issues (Design / RFC)
- [Issue #17064](https://github.com/opensearch-project/OpenSearch/issues/17064): Original feature request for _shard_doc equivalent

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/opensearch-search-tie-breaking.md)
