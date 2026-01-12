---
tags:
  - performance
---

# Percentiles Aggregation Performance Improvement

## Summary

OpenSearch v3.1.0 significantly improves the performance of the `percentiles` aggregation by switching the underlying t-digest implementation from `AVLTreeDigest` to `MergingDigest`. This change delivers up to 30x latency improvement for certain workloads while maintaining the same accuracy and API compatibility.

## Details

### What's New in v3.1.0

The percentiles aggregation now uses `MergingDigest` instead of `AVLTreeDigest` from the t-digest library. This is a drop-in replacement that provides substantial performance improvements without changing the aggregation API or behavior.

### Technical Changes

#### Implementation Switch

The `TDigestState` class, which wraps the t-digest library for percentile calculations, now extends `MergingDigest` instead of `AVLTreeDigest`:

```java
// Before v3.1.0
public class TDigestState extends AVLTreeDigest { ... }

// v3.1.0 and later
public class TDigestState extends MergingDigest { ... }
```

#### Backward Compatibility

The serialization format has been updated to support both old and new implementations:

- When communicating with nodes running versions before v3.1.0, the old centroid-based serialization is used
- For v3.1.0+ nodes, the native `MergingDigest` byte serialization is used for exact state preservation

```java
public static void write(TDigestState state, StreamOutput out) throws IOException {
    if (out.getVersion().before(Version.V_3_1_0)) {
        // Legacy format for backward compatibility
        out.writeDouble(state.compression);
        out.writeVInt(state.centroidCount());
        for (Centroid centroid : state.centroids()) {
            out.writeDouble(centroid.mean());
            out.writeVLong(centroid.count());
        }
    } else {
        // New efficient format
        int byteSize = state.byteSize();
        out.writeVInt(byteSize);
        ByteBuffer buf = ByteBuffer.allocate(byteSize);
        state.asBytes(buf);
        out.writeBytes(buf.array());
    }
}
```

#### Median Absolute Deviation Impact

The `MergingDigest` implementation does not support weighted `add()` operations. The median absolute deviation calculation was updated to use iterative addition instead:

```java
for (Centroid centroid : valuesSketch.centroids()) {
    final double deviation = Math.abs(approximateMedian - centroid.mean());
    // Iterative add instead of weighted add
    for (int i = 0; i < centroid.count(); i++) {
        approximatedDeviationsSketch.add(deviation);
    }
}
```

### Performance Benchmarks

Benchmarks on the http_logs dataset (247M documents) show significant improvements:

| Field | Baseline Latency (ms) | New Latency (ms) | Improvement |
|-------|----------------------|------------------|-------------|
| @timestamp (high cardinality) | 13,085 | 6,293 | ~2x faster |
| status (low cardinality) | 196,794 | 6,212 | ~31x faster |

The improvement is especially pronounced for low-cardinality fields.

### Usage Example

The API remains unchanged:

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "percentile_taxful_total_price": {
      "percentiles": {
        "field": "taxful_total_price",
        "tdigest": {
          "compression": 100
        }
      }
    }
  }
}
```

### Migration Notes

- No configuration changes required
- The `compression` parameter continues to work the same way
- Rolling upgrades are supported with automatic serialization format negotiation
- Existing queries will automatically benefit from the performance improvement

## Limitations

- The `MergingDigest` implementation does not support weighted additions, which required a workaround in the median absolute deviation calculation
- During rolling upgrades, mixed-version clusters will use the legacy serialization format

## References

### Documentation
- [Percentile Aggregation Documentation](https://docs.opensearch.org/3.0/aggregations/metric/percentile/): Official documentation
- [t-digest Library](https://github.com/tdunning/t-digest): Upstream library with MergingDigest recommendation

### Pull Requests
| PR | Description |
|----|-------------|
| [#18124](https://github.com/opensearch-project/OpenSearch/pull/18124) | Switch percentiles implementation to MergingDigest |

### Issues (Design / RFC)
- [Issue #18122](https://github.com/opensearch-project/OpenSearch/issues/18122): Feature request for implementation switch

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/percentiles-aggregation.md)
