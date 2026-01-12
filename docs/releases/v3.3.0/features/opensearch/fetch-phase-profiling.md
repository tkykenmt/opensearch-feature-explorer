# Fetch Phase Profiling

## Summary

OpenSearch v3.3.0 expands fetch phase profiling to support inner hits and top hits aggregation phases. Previously (v3.2.0), fetch phase profiling only supported the standard fetch phase. This enhancement provides complete visibility into all fetch operations, enabling developers to identify performance bottlenecks in complex queries involving nested documents and aggregations.

## Details

### What's New in v3.3.0

This release extends the fetch phase profiler to capture timing information for:

1. **Inner Hits Fetch**: Profiling for fetch operations triggered by `inner_hits` in nested or parent-child queries
2. **Top Hits Aggregation Fetch**: Profiling for fetch operations within `top_hits` aggregations

Each fetch type appears as a separate entry in the profile response with a descriptive label indicating its source.

### Technical Changes

#### Profile Response Structure

The fetch profile array now contains multiple entries when inner hits or top hits aggregations are used:

```json
{
  "profile": {
    "shards": [{
      "fetch": [
        {
          "type": "fetch",
          "description": "fetch",
          "time_in_nanos": 500000,
          "breakdown": { ... },
          "children": [...]
        },
        {
          "type": "fetch_inner_hits[nested_field]",
          "description": "fetch_inner_hits[nested_field]",
          "time_in_nanos": 150000,
          "breakdown": { ... },
          "children": [...]
        },
        {
          "type": "fetch_top_hits_aggregation[top_hits_agg1]",
          "description": "fetch_top_hits_aggregation[top_hits_agg1]",
          "time_in_nanos": 200000,
          "breakdown": { ... },
          "children": [...]
        }
      ]
    }]
  }
}
```

#### New Profile Types

| Type | Description |
|------|-------------|
| `fetch_inner_hits[<name>]` | Fetch profile for inner hits with the specified name |
| `fetch_top_hits_aggregation[<name>]` | Fetch profile for top hits aggregation with the specified name |

#### Implementation Changes

| Component | Change |
|-----------|--------|
| `FetchPhase.java` | Removed restriction that limited profiling to standard fetch phase only |
| `InnerHitsPhase.java` | Updated to pass descriptive profile name `fetch_inner_hits[<name>]` |
| `TopHitsAggregator.java` | Updated to pass descriptive profile name `fetch_top_hits_aggregation[<name>]` |
| `FlatFetchProfileTree.java` | Added consolidation logic for concurrent slices and reference counting |

#### Consolidation Behavior

When multiple fetch operations of the same type occur (common with top hits aggregations across many buckets), they are consolidated under a single breakdown entry. This prevents verbose and crowded profiles while still providing accurate timing information.

### Usage Example

Query with inner hits:

```json
GET /my_index/_search
{
  "profile": true,
  "query": {
    "nested": {
      "path": "nested_field",
      "query": { "match_all": {} },
      "inner_hits": { "name": "my_inner_hits" }
    }
  }
}
```

Query with top hits aggregation:

```json
GET /my_index/_search
{
  "profile": true,
  "size": 0,
  "aggs": {
    "by_category": {
      "terms": { "field": "category" },
      "aggs": {
        "top_products": {
          "top_hits": { "size": 3 }
        }
      }
    }
  }
}
```

### Migration Notes

No migration required. The enhanced profiling is automatically available when using `"profile": true` in search requests.

## Limitations

- Profiling adds overhead to search operations
- Each inner hit definition and top hits aggregation creates a separate fetch profile entry
- Concurrent segment search slice statistics are included for all fetch types

## References

### Documentation
- [Profile API Documentation](https://docs.opensearch.org/3.0/api-reference/search-apis/profile/): Official API reference
- [Inner Hits Documentation](https://docs.opensearch.org/3.0/search-plugins/searching-data/inner-hits/): Inner hits usage
- [Top Hits Aggregation](https://docs.opensearch.org/3.0/aggregations/metric/top-hits/): Top hits aggregation usage

### Pull Requests
| PR | Description |
|----|-------------|
| [#18936](https://github.com/opensearch-project/OpenSearch/pull/18936) | Expand fetch phase profiling to support inner hits and top hits aggregation phases |

### Issues (Design / RFC)
- [Issue #18862](https://github.com/opensearch-project/OpenSearch/issues/18862): Feature request for inner hits and top hits profiling
- [Issue #18864](https://github.com/opensearch-project/OpenSearch/issues/18864): META issue for fetch phase profiling

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/profiler.md)
