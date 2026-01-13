---
tags:
  - opensearch
---
# Star Tree Index

## Summary

OpenSearch v2.19.0 significantly expands star-tree index capabilities with support for additional field types (keyword, IP, object fields), date histogram aggregations with metric sub-aggregations, and an extensible query/field type framework. These enhancements enable star-tree to handle more diverse data models and complex aggregation patterns.

## Details

### What's New in v2.19.0

#### Keyword Field Support
Star-tree index now supports keyword fields as dimensions. Users can include keyword fields in `ordered_dimensions` for grouping and filtering. Metrics remain numeric-only.

```json
{
  "mappings": {
    "composite": {
      "my_star_tree": {
        "type": "star_tree",
        "config": {
          "ordered_dimensions": [
            { "name": "status" },
            { "name": "method" }
          ],
          "metrics": [
            { "name": "latency", "stats": ["avg", "max"] }
          ]
        }
      }
    },
    "properties": {
      "status": { "type": "integer" },
      "method": { "type": "keyword" },
      "latency": { "type": "float" }
    }
  }
}
```

#### IP Field Support
IP address fields can now be used as dimensions in star-tree indexes, enabling efficient aggregations over network traffic data.

```json
{
  "ordered_dimensions": [
    { "name": "client_ip" },
    { "name": "status" }
  ]
}
```

#### Object Field Support
Object fields with nested properties are now supported. Reference nested fields using dot notation (e.g., `nested.status`, `geoip.country_name`). Array values within object fields are still blocked.

```json
{
  "mappings": {
    "composite": {
      "startree1": {
        "type": "star_tree",
        "config": {
          "ordered_dimensions": [
            { "name": "nested.status" },
            { "name": "geoip.country_name" }
          ],
          "metrics": [
            { "name": "nested.status" }
          ]
        }
      }
    },
    "properties": {
      "nested": {
        "properties": {
          "status": { "type": "integer" }
        }
      },
      "geoip": {
        "properties": {
          "country_name": { "type": "keyword" }
        }
      }
    }
  }
}
```

#### Date Histogram with Metric Aggregations
Star-tree can now resolve date histogram aggregations with nested metric sub-aggregations. The implementation uses `StarTreeBucketCollector` to handle bucket collection without traditional Lucene document traversal.

```json
{
  "size": 0,
  "aggs": {
    "by_month": {
      "date_histogram": {
        "field": "@timestamp",
        "calendar_interval": "month"
      },
      "aggs": {
        "sum_status": {
          "sum": { "field": "status" }
        }
      }
    }
  }
}
```

#### Extensible Query and Field Type Framework
A new extensible design enables adding support for different query types and field types:

- `DimensionFilterMapper`: Maps star-tree supported fields and queries
- `StarTreeFilterProvider`: Converts user queries (QueryBuilder) to star-tree traversal filters
- Supports term, terms, and range queries on numeric and keyword fields

### Technical Changes

| Component | Change |
|-----------|--------|
| `StarTreeBucketCollector` | New interface for collecting star-tree entries into aggregation buckets |
| `DimensionFilterMapper` | Maps field types to appropriate dimension filters |
| `StarTreeFilterProvider` | Converts QueryBuilder to star-tree traversal filters |
| Keyword iterator | End-to-end support for keyword fields including flush, merge, and file format |
| IP field support | Dimension support for IP address fields |
| Object field support | Dot notation access to nested object properties |

## Limitations

- Keyword fields supported only as dimensions, not metrics
- Object fields do not support array values
- Date histogram support limited to specific query shapes

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16233](https://github.com/opensearch-project/OpenSearch/pull/16233) | Support for keyword fields in star-tree index | [#16232](https://github.com/opensearch-project/OpenSearch/issues/16232) |
| [#16641](https://github.com/opensearch-project/OpenSearch/pull/16641) | Changes to support IP field in star tree indexing | [#16642](https://github.com/opensearch-project/OpenSearch/issues/16642) |
| [#16728](https://github.com/opensearch-project/OpenSearch/pull/16728) | Support object fields in star-tree index | [#16730](https://github.com/opensearch-project/OpenSearch/issues/16730) |
| [#16674](https://github.com/opensearch-project/OpenSearch/pull/16674) | Resolving Date histogram with metric aggregation using star-tree | [#16552](https://github.com/opensearch-project/OpenSearch/issues/16552) |
| [#17137](https://github.com/opensearch-project/OpenSearch/pull/17137) | Extensible design to support different query and field type | [#16537](https://github.com/opensearch-project/OpenSearch/issues/16537), [#16538](https://github.com/opensearch-project/OpenSearch/issues/16538), [#16539](https://github.com/opensearch-project/OpenSearch/issues/16539) |

### Documentation
- [Star-tree index documentation](https://docs.opensearch.org/2.19/search-plugins/star-tree-index/)
