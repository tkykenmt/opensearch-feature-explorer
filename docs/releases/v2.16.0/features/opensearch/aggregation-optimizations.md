---
tags:
  - opensearch
---
# Aggregation Optimizations

## Summary

OpenSearch v2.16.0 extends the fast filter rewrite optimization, previously available only for date histogram aggregations, to range aggregations on numeric fields. This optimization leverages the BKD tree index structure to compute bucket counts directly without iterating through documents, delivering dramatic performance improvements for range aggregations.

## Details

### What's New in v2.16.0

The date histogram rewrite optimization has been extended to range aggregations. This optimization uses the BKD tree (Points) index structure to efficiently count documents within specified ranges without document iteration.

### Technical Changes

#### NumericPointEncoder Interface

A new `NumericPointEncoder` interface was introduced to standardize point encoding across numeric field types:

```java
public interface NumericPointEncoder {
    byte[] encodePoint(Number value);
}
```

This interface is implemented by:
- `NumberFieldType` (all numeric types: HALF_FLOAT, FLOAT, DOUBLE, BYTE, SHORT, INTEGER, LONG, UNSIGNED_LONG)
- `DateFieldType`
- `ScaledFloatFieldType`

#### RangeAggregationType

A new `RangeAggregationType` class was added to `FastFilterRewriteHelper` to handle range aggregation optimization:

```java
public static class RangeAggregationType implements AggregationType {
    private final ValuesSourceConfig config;
    private final Range[] ranges;
    
    @Override
    public boolean isRewriteable(Object parent, int subAggLength) {
        // Requires: no parent, no sub-aggs, no script, no missing value
        // Field must be searchable and implement NumericPointEncoder
        // Ranges must be non-overlapping
    }
    
    @Override
    public Ranges buildRanges(SearchContext context, MappedFieldType fieldType) {
        // Encodes range boundaries as byte arrays for BKD tree traversal
    }
}
```

#### Optimization Conditions

The range aggregation optimization applies when:
1. No parent aggregation
2. No sub-aggregations
3. No script or missing value configuration
4. Field type implements `NumericPointEncoder`
5. Ranges are non-overlapping (sorted by `from`, then `to`)
6. No deleted documents in the segment
7. No `_doc_count` field present

#### Performance Benchmarks

From the PR benchmarks on the big5 workload:

| Metric | Baseline | Optimized | Improvement |
|--------|----------|-----------|-------------|
| 50th percentile latency (range-agg-1) | 1,233,760 ms | 4.74 ms | ~260,000x |
| 90th percentile latency (range-agg-1) | 1,428,680 ms | 5.14 ms | ~278,000x |
| 50th percentile service time (range-agg-1) | 5,420.99 ms | 3.49 ms | ~1,554x |

On the noaa workload:

| Metric | Baseline | Optimized | Improvement |
|--------|----------|-----------|-------------|
| 50th percentile latency | 1,484.37 ms | 10.80 ms | ~137x |
| 50th percentile service time | 1,481.79 ms | 6.98 ms | ~212x |

### Supported Field Types

| Field Type | Supported |
|------------|-----------|
| `byte` | ✓ |
| `short` | ✓ |
| `integer` | ✓ |
| `long` | ✓ |
| `float` | ✓ |
| `double` | ✓ |
| `half_float` | ✓ |
| `unsigned_long` | ✓ |
| `scaled_float` | ✓ |
| `date` | ✓ (via date histogram) |

### Usage Example

```json
GET /metrics/_search
{
  "size": 0,
  "aggs": {
    "value_ranges": {
      "range": {
        "field": "response_time",
        "ranges": [
          { "to": 100 },
          { "from": 100, "to": 500 },
          { "from": 500, "to": 1000 },
          { "from": 1000 }
        ]
      }
    }
  }
}
```

### Debug Information

When profiling is enabled, the optimization provides debug information:

```json
{
  "profile": {
    "shards": [{
      "aggregations": [{
        "debug": {
          "optimized_segments": 1,
          "unoptimized_segments": 0,
          "leaf_visited": 1,
          "inner_visited": 0
        }
      }]
    }]
  }
}
```

## Limitations

- Ranges must be non-overlapping for the optimization to apply
- Does not work with sub-aggregations
- Does not work with scripts or missing value configuration
- Segments with deleted documents fall back to standard collection
- Documents with `_doc_count` field disable the optimization

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#13865](https://github.com/opensearch-project/OpenSearch/pull/13865) | Apply the date histogram rewrite optimization to range aggregation | [#13531](https://github.com/opensearch-project/OpenSearch/issues/13531) |

### Related Issues
- [#13531](https://github.com/opensearch-project/OpenSearch/issues/13531): Apply the fast filter optimization to range aggregation
- [#13317](https://github.com/opensearch-project/OpenSearch/pull/13317): Date histogram optimization algorithm details
- [#12073](https://github.com/opensearch-project/OpenSearch/pull/12073): Date histogram buildRange method details
