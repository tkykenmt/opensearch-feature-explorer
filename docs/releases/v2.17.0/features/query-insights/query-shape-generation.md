---
tags:
  - domain/observability
  - component/server
  - observability
  - performance
  - search
---
# Query Shape Generation

## Summary

OpenSearch v2.17.0 introduces query shape generation and query grouping by similarity to the Query Insights plugin. This enhancement allows users to group similar queries together based on their structural shape, reducing noise from duplicate queries in Top N results and providing better visibility into query patterns. The feature computes a normalized query shape that captures the query structure (query types, aggregations, sorts) while removing specific field values, enabling effective deduplication of similar queries.

## Details

### What's New in v2.17.0

- **Query Shape Generator**: New `QueryShapeGenerator` class that builds a normalized string representation of search queries including query builders, aggregations, and sort builders
- **Query Grouping Framework**: `MinMaxHeapQueryGrouper` implements efficient grouping using min/max heap data structures to track Top N query groups
- **Similarity-based Grouping**: Queries can be grouped by structural similarity using MurmurHash3 hash codes of their query shapes
- **Aggregate Measurements**: New `Measurement` class supports aggregation types (NONE, SUM, AVERAGE) for grouped query metrics
- **Configurable Group Limits**: Settings to control maximum number of tracked groups

### Technical Changes

#### Architecture Changes

```mermaid
graph TB
    subgraph "Query Insights Plugin"
        A[Search Request] --> B[QueryInsightsListener]
        B --> C[QueryShapeGenerator]
        C --> D[Generate Query Shape]
        D --> E[Compute Hash Code]
        
        E --> F{Grouping Enabled?}
        F -->|Yes| G[QueryGroupingService]
        F -->|No| H[TopQueriesService]
        
        G --> I[MinMaxHeapQueryGrouper]
        I --> J[Min Heap - Top N]
        I --> K[Max Heap - Overflow]
        
        J --> L[Aggregate Measurements]
        K --> L
        
        H --> M[Individual Records]
        
        L --> N[/_insights/top_queries]
        M --> N
    end
```

#### New Components

| Component | Description |
|-----------|-------------|
| `QueryShapeGenerator` | Generates normalized query shape strings from SearchSourceBuilder |
| `QueryShapeVisitor` | Visitor pattern implementation for traversing query builder trees |
| `MinMaxHeapQueryGrouper` | Groups queries using min/max heap algorithm for efficient Top N tracking |
| `QueryGrouper` | Interface for query grouping implementations |
| `Measurement` | Encapsulates metric values with aggregation type support |
| `GroupingType` | Enum defining grouping options: `NONE`, `SIMILARITY` |
| `AggregationType` | Enum defining aggregation options: `NONE`, `SUM`, `AVERAGE` |

#### New Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `search.insights.top_queries.group_by` | Grouping type: `none` or `similarity` | `none` |
| `search.insights.top_queries.max_groups_excluding_topn` | Maximum groups to track beyond Top N | `100` |

#### API Changes

The Top N queries response now includes aggregate measurements when grouping is enabled:

```json
{
  "top_queries": [
    {
      "timestamp": 1725495127359,
      "query_hashcode": "b4c4f69290df756021ca6276be5cbb75",
      "source": { "query": { "match_all": {} } },
      "measurements": {
        "latency": {
          "number": 160,
          "count": 10,
          "aggregationType": "AVERAGE"
        }
      }
    }
  ]
}
```

### Usage Example

**Enable query grouping by similarity:**

```bash
PUT _cluster/settings
{
  "persistent": {
    "search.insights.top_queries.latency.enabled": true,
    "search.insights.top_queries.group_by": "similarity"
  }
}
```

**Configure maximum tracked groups:**

```bash
PUT _cluster/settings
{
  "persistent": {
    "search.insights.top_queries.max_groups_excluding_topn": 100
  }
}
```

**Query shape example:**

For a query like:
```json
{
  "query": {
    "bool": {
      "must": [{ "term": { "field1": "value" } }],
      "filter": [{ "range": { "date": { "gte": "2024-01-01" } } }]
    }
  },
  "sort": [{ "timestamp": "desc" }]
}
```

The generated query shape is:
```
bool []
  must:
    term [field1]
  filter:
    range [date]
sort:
  desc [timestamp]
```

### Migration Notes

- Existing Top N queries configurations continue to work without changes
- To enable grouping, set `search.insights.top_queries.group_by` to `similarity`
- When grouping is enabled, the response format changes to include aggregate measurements
- The `query_hashcode` field is added to identify query groups

## Limitations

- Grouping applies to all metric types (latency, CPU, memory) simultaneously
- Maximum groups limit (default 100) may cause some query groups to be discarded in high-cardinality environments
- Query shape generation adds minimal overhead but should be monitored in high-throughput scenarios

## References

### Documentation
- [Grouping Top N Queries Documentation](https://docs.opensearch.org/2.17/observing-your-data/query-insights/grouping-top-n-queries/)

### Blog Posts
- [Query Insights Blog](https://opensearch.org/blog/query-insights/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#44](https://github.com/opensearch-project/query-insights/pull/44) | Add ability to generate query shape for aggregation and sort |
| [#66](https://github.com/opensearch-project/query-insights/pull/66) | Query grouping framework for Top N queries and group by query similarity |
| [#73](https://github.com/opensearch-project/query-insights/pull/73) | Minor enhancements to query categorization on tags and unit types |

### Issues (Design / RFC)
- [Issue #13357](https://github.com/opensearch-project/OpenSearch/issues/13357): RFC - Grouping similar Top N Queries by Latency and Resource Usage

## Related Feature Report

- Full feature documentation
