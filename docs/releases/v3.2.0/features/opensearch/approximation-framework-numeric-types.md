---
tags:
  - indexing
  - performance
  - search
---

# Approximation Framework: Numeric Types Extension

## Summary

OpenSearch v3.2.0 extends the Approximation Framework to support all numeric field types beyond the previously supported `long` type. This enhancement enables early termination optimization for range queries on `int`, `float`, `double`, `half_float`, and `unsigned_long` fields, significantly improving query performance for numeric range queries across all data types.

## Details

### What's New in v3.2.0

Prior to this release, the Approximation Framework only applied to `long` fields (including date fields). This update extends the optimization to all numeric types:

| Numeric Type | Support Status | Notes |
|--------------|----------------|-------|
| `long` | Existing | Already supported |
| `integer` | **New** | Also covers `byte` and `short` |
| `float` | **New** | Single-precision floating point |
| `double` | **New** | Double-precision floating point |
| `half_float` | **New** | 16-bit floating point |
| `unsigned_long` | **New** | Index sort not supported |

### Technical Changes

#### New Format Decoders in ApproximatePointRangeQuery

New format decoders were added to support byte array decoding for each numeric type:

```java
public static final Function<byte[], String> INT_FORMAT = 
    bytes -> Integer.toString(IntPoint.decodeDimension(bytes, 0));
    
public static final Function<byte[], String> HALF_FLOAT_FORMAT = 
    bytes -> Float.toString(HalfFloatPoint.decodeDimension(bytes, 0));
    
public static final Function<byte[], String> FLOAT_FORMAT = 
    bytes -> Float.toString(FloatPoint.decodeDimension(bytes, 0));
    
public static final Function<byte[], String> DOUBLE_FORMAT = 
    bytes -> Double.toString(DoublePoint.decodeDimension(bytes, 0));
    
public static final Function<byte[], String> UNSIGNED_LONG_FORMAT = 
    bytes -> BigIntegerPoint.decodeDimension(bytes, 0).toString();
```

#### NumberFieldMapper Changes

Each numeric type's `rangeQuery()` method was updated to wrap queries with `ApproximateScoreQuery`:

```java
// Example for INTEGER type
return new ApproximateScoreQuery(
    query,
    new ApproximatePointRangeQuery(
        field,
        IntPoint.pack(new int[] { l }).bytes,
        IntPoint.pack(new int[] { u }).bytes,
        APPROX_QUERY_NUMERIC_DIMS,
        ApproximatePointRangeQuery.INT_FORMAT
    )
);
```

#### Index Sort Support

The implementation also adds `IndexSortSortedNumericDocValuesRangeQuery` support for numeric types that support index sorting:

| Type | Index Sort Support |
|------|-------------------|
| `integer` | ✓ |
| `long` | ✓ |
| `float` | ✓ |
| `double` | ✓ |
| `half_float` | ✓ |
| `unsigned_long` | ✗ (not supported by OpenSearch) |

### Performance Improvements

Based on benchmark results from the `http_logs` and `nyc_taxis` datasets:

| Query Type | Dataset | Before | After | Improvement |
|------------|---------|--------|-------|-------------|
| `range_with_asc_sort` | http_logs | ~300 ms | ~30 ms | ~90% |
| `range_size` | http_logs | ~48 ms | ~8 ms | ~83% |
| `range_with_desc_sort` | http_logs | ~312 ms | ~31 ms | ~90% |
| `desc_sort_passenger_count` | nyc_taxis | ~17 ms | ~12 ms | ~29% |

### Usage Example

```json
// Integer field range query - now optimized
GET metrics/_search
{
  "query": {
    "range": {
      "status_code": {
        "gte": 400,
        "lt": 500
      }
    }
  },
  "sort": [{ "status_code": "asc" }],
  "size": 100
}
```

```json
// Float field range query - now optimized
GET sensors/_search
{
  "query": {
    "range": {
      "temperature": {
        "gte": 20.0,
        "lte": 30.0
      }
    }
  },
  "sort": [{ "temperature": "desc" }],
  "size": 50
}
```

```json
// Double field range query - now optimized
GET transactions/_search
{
  "query": {
    "range": {
      "amount": {
        "gte": 100.00,
        "lte": 1000.00
      }
    }
  },
  "sort": [{ "amount": "asc" }],
  "size": 100
}
```

### Migration Notes

This enhancement is transparent and requires no configuration changes. Existing range queries on numeric fields will automatically benefit from the optimization when eligibility criteria are met.

## Limitations

- `unsigned_long` fields do not support index sorting, so `IndexSortSortedNumericDocValuesRangeQuery` optimization is not available for this type
- Same eligibility criteria as the base Approximation Framework apply:
  - No aggregations in the query
  - `track_total_hits` not set to `true`
  - Sort field matches the range query field (if sorting)

## References

### Documentation
- [Lucene PR #14784](https://github.com/apache/lucene/pull/14784): Related Lucene enhancement for `pack` support in sandbox types

### Blog Posts
- [OpenSearch Approximation Framework Blog](https://opensearch.org/blog/opensearch-approximation-framework/): Comprehensive overview

### Pull Requests
| PR | Description |
|----|-------------|
| [#18530](https://github.com/opensearch-project/OpenSearch/pull/18530) | Extend Approximation Framework to other numeric types |

### Issues (Design / RFC)
- [Issue #14406](https://github.com/opensearch-project/OpenSearch/issues/14406): Feature request to expand ApproximatePointRangeQuery to other numeric types
- [Issue #18334](https://github.com/opensearch-project/OpenSearch/issues/18334): Related tracking issue

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/approximation-framework.md)
