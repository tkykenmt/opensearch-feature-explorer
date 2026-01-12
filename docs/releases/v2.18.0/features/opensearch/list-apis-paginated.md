---
tags:
  - indexing
---

# List APIs (Paginated)

## Summary

OpenSearch 2.18.0 introduces new paginated List APIs (`_list/indices` and `_list/shards`) as alternatives to the existing cat APIs. These APIs address scalability issues in large clusters where cat API responses can become too large, causing client timeouts and cluster stress. Additionally, dynamic cluster settings allow administrators to block non-paginated cat API calls when limits are exceeded.

## Details

### What's New in v2.18.0

- New `/_list/indices` API with pagination support
- New `/_list/shards` API with pagination support
- Dynamic cluster settings to limit cat API responses
- HTTP 429 response when limits are exceeded

### Technical Changes

#### Architecture Changes

```mermaid
graph TB
    subgraph "Client Request"
        REQ[API Request]
    end
    
    subgraph "New List APIs"
        LI[/_list/indices]
        LS[/_list/shards]
    end
    
    subgraph "Legacy Cat APIs"
        CI[/_cat/indices]
        CS[/_cat/shards]
        CSG[/_cat/segments]
    end
    
    subgraph "Request Limit Settings"
        RLS[RequestLimitSettings]
        LIMIT{Limit Check}
    end
    
    REQ --> LI
    REQ --> LS
    REQ --> CI
    REQ --> CS
    REQ --> CSG
    
    CI --> RLS
    CS --> RLS
    CSG --> RLS
    RLS --> LIMIT
    LIMIT -->|Exceeded| E429[HTTP 429]
    LIMIT -->|OK| RESP[Response]
    
    LI --> PAGE[Paginated Response]
    LS --> PAGE
```

#### New Components

| Component | Description |
|-----------|-------------|
| `RestListIndicesAction` | REST handler for `/_list/indices` endpoint |
| `RestListShardsAction` | REST handler for `/_list/shards` endpoint |
| `IndexPaginationStrategy` | Pagination logic using index creation timestamps |
| `ShardPaginationStrategy` | Pagination logic for shards based on index order |
| `RequestLimitSettings` | Dynamic settings for cat API response limits |

#### New Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `cat.indices.response.limit.number_of_indices` | Max indices for `_cat/indices` | -1 (unlimited) |
| `cat.shards.response.limit.number_of_shards` | Max shards for `_cat/shards` | -1 (unlimited) |
| `cat.segments.response.limit.number_of_indices` | Max indices for `_cat/segments` | -1 (unlimited) |

#### API Changes

**New Endpoints:**

| Endpoint | Description |
|----------|-------------|
| `GET /_list/indices` | Paginated list of indices |
| `GET /_list/indices/{indices}` | Paginated list of specific indices |
| `GET /_list/shards` | Paginated list of shards |
| `GET /_list/shards/{indices}` | Paginated list of shards for specific indices |

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `next_token` | String | null | Token for fetching next page |
| `size` | Integer | 2000 (shards), 5000 (indices) | Max items per page |
| `sort` | String | asc | Sort order: `asc` or `desc` |

### Usage Example

**List indices with pagination:**
```bash
# First page
curl "localhost:9200/_list/indices?format=json&size=100"

# Response
{
  "next_token": "eyJsYXN0X3NvcnRfdmFsdWUiOjE2...",
  "indices": [
    {"index": "logs-2024-01", "health": "green", ...},
    {"index": "logs-2024-02", "health": "green", ...}
  ]
}

# Next page using token
curl "localhost:9200/_list/indices?format=json&next_token=eyJsYXN0X3NvcnRfdmFsdWUiOjE2..."
```

**List shards with pagination:**
```bash
curl "localhost:9200/_list/shards?format=json&size=500"

# Response
{
  "next_token": "MCQw",
  "shards": [
    {"index": "test-ind", "shard": "0", "prirep": "p", "state": "STARTED", ...},
    {"index": "test-ind", "shard": "0", "prirep": "r", "state": "STARTED", ...}
  ]
}
```

**Plain text format:**
```bash
curl "localhost:9200/_list/shards"

# Response
test-index 1 p STARTED 0 208b 127.0.0.1 data1
test-index 1 r STARTED 0 208b 127.0.0.1 data5
next_token MCQw
```

**Configure cat API limits:**
```bash
# Set limit to block large cat/indices requests
curl -X PUT "localhost:9200/_cluster/settings" -H 'Content-Type: application/json' -d'
{
  "persistent": {
    "cat.indices.response.limit.number_of_indices": 1000,
    "cat.shards.response.limit.number_of_shards": 10000
  }
}'
```

### Migration Notes

1. For clusters with many indices/shards, switch from `_cat/indices` to `_list/indices` and `_cat/shards` to `_list/shards`
2. Update monitoring scripts to handle paginated responses with `next_token`
3. Consider setting cat API limits to encourage migration to paginated APIs
4. Both JSON and plain text formats are supported for backward compatibility

## Limitations

- Pagination uses index creation timestamps as sort keys; indices created during pagination may appear in unexpected positions depending on sort order
- Shards for a single shard ID cannot span across pages (minimum page size must accommodate max replicas)
- `next_token` is Base64 encoded and should be treated as opaque
- Cat API limits return HTTP 429 when exceeded, requiring client handling

## References

### Documentation
- [List API Documentation](https://docs.opensearch.org/2.18/api-reference/list/): Official docs
- [List indices Documentation](https://docs.opensearch.org/2.18/api-reference/list/list-indices/): List indices API
- [List shards Documentation](https://docs.opensearch.org/2.18/api-reference/list/list-shards/): List shards API

### Pull Requests
| PR | Description |
|----|-------------|
| [#14718](https://github.com/opensearch-project/OpenSearch/pull/14718) | Implementing pagination for `_cat/indices` API |
| [#14641](https://github.com/opensearch-project/OpenSearch/pull/14641) | Implementing pagination for `_cat/shards` |
| [#15986](https://github.com/opensearch-project/OpenSearch/pull/15986) | Add changes to block calls in cat shards, indices and segments based on dynamic limit settings |

### Issues (Design / RFC)
- [Issue #14258](https://github.com/opensearch-project/OpenSearch/issues/14258): Paginate `_cat/indices` API
- [Issue #14257](https://github.com/opensearch-project/OpenSearch/issues/14257): Paginate `_cat/shards` API
- [Issue #15954](https://github.com/opensearch-project/OpenSearch/issues/15954): Blocking non-paginated calls

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/opensearch-list-apis-paginated.md)
