---
tags:
  - opensearch
---
# Circuit Breaker Improvements

## Summary

OpenSearch v2.16.0 adds circuit breaker protection to the histogram aggregation's empty bucket generation process. Previously, histogram aggregations with small intervals and large data ranges could cause OutOfMemoryError and crash the node. Now, the request circuit breaker monitors memory usage during empty bucket creation and trips before memory is exhausted.

## Details

### What's New in v2.16.0

The `InternalHistogram.addEmptyBuckets()` method now calls `reduceContext.consumeBucketsAndMaybeBreak(0)` each time an empty bucket is created. This integrates with the existing request circuit breaker to track memory allocation during the reduce phase.

### Problem Addressed

When a histogram aggregation spans a large value range with a small interval, OpenSearch generates empty buckets to fill gaps between actual data points. For example, with values at 1 and 1,234,567,890 using interval=100, OpenSearch would attempt to create over 12 million empty buckets.

Before this fix:
- The empty bucket generation bypassed circuit breaker checks
- Memory allocation continued until JVM heap was exhausted
- Node crashed with `OutOfMemoryError`

After this fix:
- Each empty bucket allocation is tracked by the circuit breaker
- When memory limit is reached, a `CircuitBreakingException` is thrown
- The request fails gracefully with HTTP 429 status

### Technical Changes

Modified `InternalHistogram.java` to add circuit breaker checks in four locations within `addEmptyBuckets()`:
1. When filling empty buckets for the entire range (no data)
2. When filling empty buckets before the first data point
3. When filling empty buckets between data points
4. When filling empty buckets after the last data point

### Error Response

When the circuit breaker trips, clients receive a structured error response:

```json
{
  "error": {
    "type": "search_phase_execution_exception",
    "caused_by": {
      "type": "circuit_breaking_exception",
      "reason": "[parent] Data too large, data for [allocated_buckets] would be...",
      "durability": "TRANSIENT"
    }
  },
  "status": 429
}
```

### Workarounds (Pre-v2.16.0)

For users on earlier versions:
- Use `"min_doc_count": 1` to skip empty bucket generation
- Increase JVM heap size (temporary mitigation only)
- Use larger interval values

## Limitations

- The circuit breaker check adds minimal overhead per bucket
- Existing `search.max_buckets` limit (default: 65,535) may trip before the circuit breaker for moderately large ranges

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14754](https://github.com/opensearch-project/OpenSearch/pull/14754) | Use circuit breaker in InternalHistogram when adding empty buckets | [#14558](https://github.com/opensearch-project/OpenSearch/issues/14558) |

### Documentation
- [Circuit breaker settings](https://docs.opensearch.org/2.16/install-and-configure/configuring-opensearch/circuit-breaker/)
- [Histogram aggregation](https://docs.opensearch.org/2.16/aggregations/bucket/histogram/)
