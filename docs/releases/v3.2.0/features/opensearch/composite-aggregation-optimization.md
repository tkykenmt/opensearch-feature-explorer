---
tags:
  - domain/core
  - component/server
  - performance
  - search
---
# Composite Aggregation Optimization

## Summary

This release optimizes composite aggregation performance by eliminating unnecessary object allocations in the hot path. The changes reduce GC pressure and improve throughput for composite terms aggregation queries.

## Details

### What's New in v3.2.0

Performance improvements targeting the `collect()` method in composite aggregations, which profiling showed consumed ~50% of query execution time in the `addIfCompetitive()` path.

### Technical Changes

#### Reusable Slot Object (Flyweight Pattern)

The `CompositeValuesCollectorQueue` now uses a reusable `Slot` instance for map lookups instead of creating new objects:

```java
// Before: Created new Slot for every lookup
Integer getCurrentSlot() {
    return map.get(new Slot(CANDIDATE_SLOT));
}

// After: Reuses single Slot instance
private final Slot reusableSlot = new Slot(0);

Integer getCurrentSlot() {
    reusableSlot.set(CANDIDATE_SLOT);
    return map.get(reusableSlot);
}
```

This is thread-safe because each `LeafCollector` is confined to a single thread.

#### Single-Loop Initialization

Replaced 5 separate stream operations with a single for-loop in `CompositeAggregator`:

```java
// Before: 5 stream traversals
this.sourceNames = Arrays.stream(sourceConfigs).map(...).collect(...);
this.reverseMuls = Arrays.stream(sourceConfigs).mapToInt(...).toArray();
this.missingOrders = Arrays.stream(sourceConfigs).map(...).toArray(...);
this.formats = Arrays.stream(sourceConfigs).map(...).collect(...);
// + separate loop for sources

// After: Single loop
for (int i = 0; i < numSources; i++) {
    CompositeValuesSourceConfig sourceConfig = sourceConfigs[i];
    this.sourceNames.add(sourceConfig.name());
    this.reverseMuls[i] = sourceConfig.reverseMul();
    this.missingOrders[i] = sourceConfig.missingOrder();
    this.formats.add(sourceConfig.format());
    this.sources[i] = sourceConfig.createValuesSource(...);
}
```

#### Additional Optimizations

| Change | Description |
|--------|-------------|
| Record class | Converted `Entry` inner class to Java record |
| Removed boxing | Changed `(long) key` to `key` in `bucketOrdProducer` |
| Cleaned signatures | Removed unnecessary `throws IOException` from `doPreCollection()` and `doPostCollection()` |

### Performance Impact

- Reduced object allocation in high-frequency `collect()` path
- Lower GC pressure during composite aggregation execution
- Most beneficial for queries with 2-3 composite fields (typical use case)

### Usage Example

No API changes. Existing composite aggregation queries automatically benefit:

```json
POST /logs-*/_search
{
  "size": 0,
  "aggs": {
    "logs": {
      "composite": {
        "sources": [
          { "timestamp": { "terms": { "field": "@timestamp", "order": "desc" }}},
          { "status": { "terms": { "field": "status", "order": "asc" }}}
        ]
      }
    }
  }
}
```

## Limitations

- Thread safety relies on single-threaded `LeafCollector` execution
- Future intra-segment concurrent search may require additional changes (tracked in [#18879](https://github.com/opensearch-project/OpenSearch/pull/18879))

## References

### Documentation
- [Bucket Aggregations](https://docs.opensearch.org/3.0/aggregations/bucket/index/): OpenSearch documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#18531](https://github.com/opensearch-project/OpenSearch/pull/18531) | Optimize Composite Aggregations by removing unnecessary object allocations |

### Issues (Design / RFC)
- [Issue #18440](https://github.com/opensearch-project/OpenSearch/issues/18440): Composite Terms Aggregation Performance Improvement

## Related Feature Report

- Full feature documentation
