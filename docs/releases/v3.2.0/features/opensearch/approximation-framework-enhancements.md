---
tags:
  - domain/core
  - component/server
  - performance
  - search
---
# Approximation Framework Enhancements

## Summary

OpenSearch v3.2.0 brings three significant enhancements to the Approximation Framework: support for `search_after` pagination with numeric queries, approximation support for range queries using `now` in date fields, and automatic disabling of approximation when multiple sort fields are present. These changes improve query performance for paginated results while ensuring correctness for complex sorting scenarios.

## Details

### What's New in v3.2.0

#### 1. `search_after` Support for Numeric Queries

The Approximation Framework now supports `search_after` pagination for numeric queries, enabling efficient deep pagination while maintaining the performance benefits of early termination.

**How it works:**
- For `ASC` sort: The `search_after` value becomes the new lower bound (exclusive)
- For `DESC` sort: The `search_after` value becomes the new upper bound (exclusive)
- The framework adjusts the BKD tree traversal range dynamically based on the `search_after` value

**Performance improvement:**
- `asc_sort_with_after_timestamp`: P90 latency reduced from ~194 ms to ~8 ms
- `desc_sort_with_after_timestamp`: P90 latency reduced from ~188 ms to ~7 ms

#### 2. Range Queries with `now` in Date Fields

Previously, range queries using `now` (e.g., `@timestamp > now-1d`) bypassed the Approximation Framework because they were wrapped in `DateRangeIncludingNowQuery`. This version restructures the query wrapping to ensure approximation is applied.

**Before v3.2.0:**
```
DateRangeIncludingNowQuery
  └── ApproximateScoreQuery
        └── PointRangeQuery
```

**After v3.2.0:**
```
ApproximateScoreQuery
  └── DateRangeIncludingNowQuery
        └── PointRangeQuery
```

#### 3. Multiple Sort Fields Handling

The framework now automatically disables approximation when queries use multiple sort fields. This prevents incorrect results that could occur because secondary sort fields are only applied after document collection, not during the BKD traversal phase.

### Technical Changes

#### New API: `NumericPointEncoder.encodePoint(Object, boolean)`

A new method was added to the `NumericPointEncoder` interface to support `search_after` value encoding:

```java
/**
 * Encodes an Object value to byte array for Approximation Framework search_after optimization.
 * @param value the search_after value as Object
 * @param roundUp whether to round up (for lower bounds) or down (for upper bounds)
 * @return encoded byte array
 */
byte[] encodePoint(Object value, boolean roundUp);
```

This method is implemented for all numeric types:
- `HALF_FLOAT`, `FLOAT`, `DOUBLE`: Uses `nextUp()`/`nextDown()` for exclusive bounds
- `BYTE`, `SHORT`, `INTEGER`, `LONG`, `UNSIGNED_LONG`: Increments/decrements by 1
- `DateFieldType`: Parses date math expressions and adjusts timestamp

#### Modified Components

| Component | Change |
|-----------|--------|
| `ApproximatePointRangeQuery` | Added `search_after` bound computation and multi-sort detection |
| `ApproximateMatchAllQuery` | Added multi-sort detection to prevent approximation |
| `DateFieldMapper` | Restructured `DateRangeIncludingNowQuery` wrapping |
| `NumberFieldMapper` | Added `encodePoint(Object, boolean)` for all numeric types |
| `ScaledFloatFieldMapper` | Added `encodePoint(Object, boolean)` implementation |

### Usage Example

```json
// search_after with approximation (now optimized)
GET logs/_search
{
  "query": {
    "range": {
      "@timestamp": {
        "gte": "now-7d",
        "lt": "now"
      }
    }
  },
  "sort": [{ "@timestamp": "desc" }],
  "size": 100,
  "search_after": ["2026-01-10T00:00:00.000Z"]
}
```

```json
// Range query with now (now uses approximation)
GET logs/_search
{
  "query": {
    "range": {
      "@timestamp": {
        "gte": "now-1h",
        "lt": "now"
      }
    }
  },
  "sort": [{ "@timestamp": "desc" }],
  "size": 50
}
```

```json
// Multiple sorts - approximation automatically disabled
GET logs/_search
{
  "query": { "match_all": {} },
  "sort": [
    { "@timestamp": "desc" },
    { "agent.name": "asc" }
  ],
  "size": 100
}
```

### Migration Notes

These enhancements are transparent and require no configuration changes. Queries that previously bypassed approximation will now automatically benefit from the optimization where applicable.

## Limitations

- `search_after` optimization only works with single sort field on the same field as the range query
- Multiple sort fields will disable approximation to ensure result correctness
- `search_after` with multiple tie-breaker values is not optimized (falls back to standard execution)

## References

### Blog Posts
- [OpenSearch Approximation Framework Blog](https://opensearch.org/blog/opensearch-approximation-framework/): Comprehensive overview

### Pull Requests
| PR | Description |
|----|-------------|
| [#18896](https://github.com/opensearch-project/OpenSearch/pull/18896) | Support `search_after` numeric queries with Approximation Framework |
| [#18511](https://github.com/opensearch-project/OpenSearch/pull/18511) | Added approximation support for range queries with `now` in date field |
| [#18763](https://github.com/opensearch-project/OpenSearch/pull/18763) | Disable approximation framework when dealing with multiple sorts |

### Issues (Design / RFC)
- [Issue #18546](https://github.com/opensearch-project/OpenSearch/issues/18546): Feature request for `search_after` support
- [Issue #18503](https://github.com/opensearch-project/OpenSearch/issues/18503): Bug report for `now` range queries skipping approximation
- [Issue #18619](https://github.com/opensearch-project/OpenSearch/issues/18619): META issue for Approximation Framework

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/opensearch-approximation-framework.md)
