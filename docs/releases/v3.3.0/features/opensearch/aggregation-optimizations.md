---
tags:
  - indexing
  - performance
  - search
---

# Aggregation Optimizations

## Summary

OpenSearch v3.3.0 introduces performance optimizations for three aggregation types: rare terms, string terms, and date histogram aggregations. These improvements reduce latency and memory usage by using smarter algorithms for bucket selection and eliminating unnecessary object allocations.

## Details

### What's New in v3.3.0

This release includes three distinct aggregation optimizations:

1. **Rare Terms Aggregation Precomputation**: Uses Lucene term frequency data to avoid iterating through individual documents
2. **String Terms Aggregation Optimization**: Implements quickselect algorithm for large bucket counts
3. **Date Histogram Optimization**: Reuses rounding utility objects to prevent unnecessary memory allocations

### Technical Changes

#### Rare Terms Aggregation Precomputation

The `StringRareTermsAggregator` now supports precomputation using `Weight.count()` and Lucene's term frequency data. When conditions are met (match-all query, no deletions, no sub-aggregations), the aggregator can compute bucket counts directly from the index without iterating through documents.

Key implementation details:
- Added `tryPrecomputeAggregationForLeaf()` method to `StringRareTermsAggregator`
- Uses `Weight.setWeight()` to access query weight for count optimization
- Iterates over `TermsEnum` to get document frequencies directly
- Handles missing values through `ValuesSourceConfig`

#### String Terms Aggregation Optimization

The `GlobalOrdinalsStringTermsAggregator` now uses adaptive bucket selection strategies:

| Strategy | Condition | Description |
|----------|-----------|-------------|
| `priority_queue` | buckets ≤ 5× size | Traditional PriorityQueue for top-N selection |
| `quick_select` | buckets > 5× size | Lucene's ArrayUtil.select() for faster selection |
| `select_all` | buckets ≤ size | Returns all buckets without selection |

The threshold factor (default: 5) is configurable via `SearchContext.bucketSelectionStrategyFactor()`.

#### Date Histogram Optimization

Refactored `Rounding.java` to reuse rounding utility objects:

| Class | Change |
|-------|--------|
| `FixedToMidnightRounding` | Reuses single `JavaTimeToMidnightRounding` instance |
| `ToMidnightRounding` | Reuses single `JavaTimeToMidnightRounding` instance |
| `FixedRounding` | Reuses single `JavaTimeRounding` instance |
| `VariableRounding` | Reuses single `JavaTimeRounding` instance |

Additional improvements:
- Converted if-else chains to Java 17 switch expressions
- Replaced `ChronoUnit` methods with direct `LocalDateTime` methods (e.g., `plusDays()`)
- Converted `ArrayRounding` to a record class

### Usage Example

```json
// Rare terms aggregation (benefits from precomputation)
GET /logs/_search
{
  "size": 0,
  "aggs": {
    "rare_errors": {
      "rare_terms": {
        "field": "error_code",
        "max_doc_count": 5
      }
    }
  }
}

// String terms aggregation (benefits from quickselect)
GET /logs/_search
{
  "size": 0,
  "aggs": {
    "top_users": {
      "terms": {
        "field": "user_id",
        "size": 1000
      }
    }
  }
}

// Date histogram (benefits from object reuse)
GET /logs/_search
{
  "size": 0,
  "aggs": {
    "by_day": {
      "date_histogram": {
        "field": "@timestamp",
        "calendar_interval": "day"
      },
      "aggs": {
        "total_size": {
          "sum": { "field": "size" }
        }
      }
    }
  }
}
```

### Performance Impact

**Date Histogram Optimization Benchmarks:**

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| 50th percentile latency | 26.5 ms | 12.2 ms | ~2.2x faster |
| 90th percentile latency | 31.2 ms | 16.2 ms | ~1.9x faster |
| 50th percentile service time | 24.4 ms | 9.6 ms | ~2.5x faster |

## Limitations

- Rare terms precomputation only works when:
  - Top-level query matches all documents in the segment
  - No deleted documents exist in the segment
  - No sub-aggregations are present
  - No `_doc_count` field is present
- String terms quickselect optimization does not apply to significant terms aggregations
- Date histogram optimization benefits are most visible with sub-aggregations that prevent precomputation

## References

### Documentation
- [Rare Terms Documentation](https://docs.opensearch.org/3.0/aggregations/bucket/rare-terms/)
- [Terms Aggregation Documentation](https://docs.opensearch.org/3.0/aggregations/bucket/terms/)
- [Date Histogram Documentation](https://docs.opensearch.org/3.0/aggregations/bucket/date-histogram/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#18978](https://github.com/opensearch-project/OpenSearch/pull/18978) | Rare terms aggregation precomputation |
| [#18732](https://github.com/opensearch-project/OpenSearch/pull/18732) | String terms aggregation optimization for large bucket counts |
| [#19088](https://github.com/opensearch-project/OpenSearch/pull/19088) | Date histogram optimization with rounding utility refactoring |

### Issues (Design / RFC)
- [Issue #13122](https://github.com/opensearch-project/OpenSearch/issues/13122): Rare Terms Aggregation Performance Optimization
- [Issue #18704](https://github.com/opensearch-project/OpenSearch/issues/18704): Optimize String terms agg
- [Issue #10954](https://github.com/opensearch-project/OpenSearch/issues/10954): Use Collector.setWeight to improve aggregation performance

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/aggregation-optimizations.md)
