---
tags:
  - opensearch
---
# Request Cache

## Summary

OpenSearch v2.19.0 introduces a new dynamic cluster setting `indices.requests.cache.maximum_cacheable_size` that allows caching search requests with `size > 0` in the request cache. Previously, only aggregation-only queries (`size=0`) were cacheable by default. This enhancement is particularly beneficial when used with tiered caching, which provides significantly larger cache capacity.

## Details

### What's New in v2.19.0

The request cache now supports caching queries that return documents (not just aggregations). A new cluster setting controls the maximum `size` parameter value for queries to be eligible for caching.

### Configuration

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `indices.requests.cache.maximum_cacheable_size` | Integer | `0` | Maximum `size` parameter for cacheable queries. Set to `0` to only cache `size=0` queries (default behavior). Set to a positive value (e.g., `200`) to cache queries with `size` up to that value. |

The setting is:
- **Dynamic**: Can be changed at runtime without cluster restart
- **Cluster-level**: Applies to all indices in the cluster

### Usage Example

```bash
# Enable caching for queries with size up to 200
PUT /_cluster/settings
{
  "persistent": {
    "indices.requests.cache.maximum_cacheable_size": 200
  }
}

# This query will now be cached (if other cacheability criteria are met)
GET /my_index/_search
{
  "size": 100,
  "query": {
    "match": {
      "title": "opensearch"
    }
  }
}

# Disable size > 0 caching (restore default behavior)
PUT /_cluster/settings
{
  "persistent": {
    "indices.requests.cache.maximum_cacheable_size": 0
  }
}
```

### Technical Changes

The implementation adds:
- New setting `INDICES_REQUEST_CACHE_MAXIMUM_CACHEABLE_SIZE_SETTING` in `IndicesRequestCache`
- Modified cacheability check in `IndicesService.canCache()` to compare query size against the threshold
- Dynamic setting update consumer to apply changes at runtime

### Use Cases

This feature is most beneficial for:
- **Tiered caching users**: With larger cache capacity from disk-based tiered caching, caching document-returning queries becomes practical
- **Read-heavy workloads**: Repeated queries returning the same documents can benefit from caching
- **Dashboard queries**: Common dashboard queries with moderate result sizes can be cached

### Recommendations

- A reasonable starting value is around `200` based on benchmarking
- Queries with very large sizes (e.g., 10,000) may not benefit as much due to fetch phase overhead
- Monitor cache hit rates and evictions after enabling to tune the threshold

## Limitations

- Queries with `size` exceeding the threshold are still not cached
- Other cacheability rules still apply (no `now`, no scroll queries, etc.)
- Very large result sets may consume significant cache space

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16484](https://github.com/opensearch-project/OpenSearch/pull/16484) | Adds cluster setting to allow caching requests with size>0 in request cache | [#16485](https://github.com/opensearch-project/OpenSearch/issues/16485) |
| [#16570](https://github.com/opensearch-project/OpenSearch/pull/16570) | Change setting to be an int threshold instead of boolean | [#16485](https://github.com/opensearch-project/OpenSearch/issues/16485) |

### Documentation
- [Index request cache](https://docs.opensearch.org/2.19/search-plugins/caching/request-cache/)
- [Tiered cache](https://docs.opensearch.org/2.19/search-plugins/caching/tiered-cache/)
