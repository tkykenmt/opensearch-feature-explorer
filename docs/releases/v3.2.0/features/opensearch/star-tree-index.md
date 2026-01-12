# Star Tree Index

## Summary

OpenSearch v3.2.0 enhances the star-tree index feature with two key improvements: support for IP field type in star-tree queries and new search statistics for monitoring star-tree query performance. These additions expand the dimension types available for star-tree aggregations and provide visibility into star-tree usage at the node, index, and shard levels.

## Details

### What's New in v3.2.0

#### IP Field Search Support

Star-tree index now supports the `ip` field type as a dimension in star-tree queries. This enables aggregations with queries filtering on IP address fields, which is particularly useful for network analytics, security monitoring, and log analysis use cases.

The implementation adds a new `IpFieldMapper` class that handles:
- Parsing IP addresses from various input types (`InetAddress`, `BytesRef`, `String`)
- Converting IP values to sortable `BytesRef` using Lucene's `InetAddressPoint.encode()`
- Supporting both exact match and range-based filtering on IP dimensions

#### Star-Tree Search Statistics

New metrics are now available to monitor star-tree query performance across nodes, indices, and shards:

| Metric | Description |
|--------|-------------|
| `startree_query_total` | Total number of queries resolved using star-tree |
| `startree_query_time_in_millis` | Total time spent resolving queries using star-tree |
| `startree_query_current` | Number of currently running star-tree queries |

### Technical Changes

#### New Components

| Component | Description |
|-----------|-------------|
| `IpFieldMapper` | Handles IP address dimension filtering in star-tree queries |
| `OrdinalFieldMapper` | Abstract base class for ordinal-based dimension mappers (keyword, IP) |
| `StarTreeSearchStatsIT` | Integration tests for star-tree search statistics |

#### API Changes

Statistics are available through existing stats APIs:

```bash
# Node-level stats
GET /_nodes/stats/indices/search

# Index-level stats
GET /_stats/search

# Shard-level stats
GET /_stats/search?level=shards
```

Example response showing star-tree stats:
```json
{
  "search": {
    "query_total": 7,
    "query_time_in_millis": 74,
    "startree_query_total": 4,
    "startree_query_time_in_millis": 40,
    "startree_query_current": 0
  }
}
```

### Usage Example

```yaml
# Index mapping with IP field as star-tree dimension
PUT logs
{
  "settings": {
    "index.composite_index": true,
    "index.append_only.enabled": true
  },
  "mappings": {
    "composite": {
      "network_aggs": {
        "type": "star_tree",
        "config": {
          "ordered_dimensions": [
            { "name": "client_ip" },
            { "name": "status" }
          ],
          "metrics": [
            { "name": "bytes", "stats": ["sum", "avg"] }
          ]
        }
      }
    },
    "properties": {
      "client_ip": { "type": "ip" },
      "status": { "type": "integer" },
      "bytes": { "type": "long" }
    }
  }
}
```

```json
// Query with IP field filter - automatically uses star-tree
POST /logs/_search
{
  "size": 0,
  "query": {
    "term": { "client_ip": "192.168.1.1" }
  },
  "aggs": {
    "total_bytes": { "sum": { "field": "bytes" } }
  }
}
```

## Limitations

- IP field support is limited to IPv4 and IPv6 addresses
- Star-tree statistics are only available in OpenSearch 3.2.0+
- Existing star-tree limitations still apply (immutable data, no updates/deletes)

## References

### Documentation
- [Documentation PR #10667](https://github.com/opensearch-project/documentation-website/pull/10667): Star-tree stats documentation
- [Documentation PR #10668](https://github.com/opensearch-project/documentation-website/pull/10668): IP field support documentation
- [Star-tree index documentation](https://docs.opensearch.org/3.0/search-plugins/star-tree-index/): Official documentation

### Blog Posts
- [OpenSearch 3.2 announcement](https://opensearch.org/blog/introducing-opensearch-3-2-next-generation-search-and-anayltics-with-enchanced-ai-capabilities/): Release blog post

### Pull Requests
| PR | Description |
|----|-------------|
| [#18707](https://github.com/opensearch-project/OpenSearch/pull/18707) | Add star-tree search related stats for nodes, indices, and shards |
| [#18671](https://github.com/opensearch-project/OpenSearch/pull/18671) | Add search support for IP field type in star-tree queries |

### Issues (Design / RFC)
- [Issue #16547](https://github.com/opensearch-project/OpenSearch/issues/16547): IP field support feature request

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/star-tree-index.md)
