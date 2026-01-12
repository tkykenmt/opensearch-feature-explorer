---
tags:
  - performance
---

# ApproximatePointRangeQuery Pack Method Optimization

## Summary

This release improves the ApproximatePointRangeQuery implementation by adopting Lucene's native `pack` method for `half_float` and `unsigned_long` field types. Previously, these types used custom encoding methods, but with Lucene 10.3.0 making the `pack` methods public for `BigIntegerPoint` and `HalfFloatPoint`, OpenSearch can now use the standardized Lucene API for all numeric types.

This change simplifies the codebase and ensures consistency with other numeric types (int, long, float, double) that already use the `pack` method.

## Details

### What's New in v3.4.0

The change updates `NumberFieldMapper.java` to use Lucene's `pack` method instead of custom encoding for `half_float` and `unsigned_long` types when constructing `ApproximatePointRangeQuery`.

### Technical Changes

#### Before (v3.2.0)
```java
// half_float - used custom encodePoint method
new ApproximatePointRangeQuery(
    field,
    NumberType.HALF_FLOAT.encodePoint(l),
    NumberType.HALF_FLOAT.encodePoint(u),
    ...
)

// unsigned_long - used custom encodePoint method
new ApproximatePointRangeQuery(
    field,
    NumberType.UNSIGNED_LONG.encodePoint(l),
    NumberType.UNSIGNED_LONG.encodePoint(u),
    ...
)
```

#### After (v3.4.0)
```java
// half_float - uses Lucene's HalfFloatPoint.pack
new ApproximatePointRangeQuery(
    field,
    HalfFloatPoint.pack(l).bytes,
    HalfFloatPoint.pack(u).bytes,
    ...
)

// unsigned_long - uses Lucene's BigIntegerPoint.pack
new ApproximatePointRangeQuery(
    field,
    BigIntegerPoint.pack(l).bytes,
    BigIntegerPoint.pack(u).bytes,
    ...
)
```

#### Code Changes Summary

| Numeric Type | Before | After |
|--------------|--------|-------|
| `half_float` | `NumberType.HALF_FLOAT.encodePoint()` | `HalfFloatPoint.pack().bytes` |
| `unsigned_long` | `NumberType.UNSIGNED_LONG.encodePoint()` | `BigIntegerPoint.pack().bytes` |
| `float` | `FloatPoint.pack(new float[]{})` | `FloatPoint.pack()` (simplified) |
| `double` | `DoublePoint.pack(new double[]{})` | `DoublePoint.pack()` (simplified) |
| `int` | `IntPoint.pack(new int[]{})` | `IntPoint.pack()` (simplified) |
| `long` | `LongPoint.pack(new long[]{})` | `LongPoint.pack()` (simplified) |

### Dependency

This change depends on Lucene 10.3.0, which includes [apache/lucene#14784](https://github.com/apache/lucene/pull/14784) that made the `pack` methods public for `BigIntegerPoint` and `HalfFloatPoint` in the sandbox module.

### Usage Example

No user-facing changes. Range queries on `half_float` and `unsigned_long` fields continue to work as before:

```json
// half_float range query
GET metrics/_search
{
  "query": {
    "range": {
      "score": {
        "gte": 0.5,
        "lte": 1.0
      }
    }
  },
  "sort": [{ "score": "desc" }],
  "size": 100
}
```

```json
// unsigned_long range query
GET counters/_search
{
  "query": {
    "range": {
      "counter": {
        "gte": 1000000000000,
        "lte": 9999999999999
      }
    }
  },
  "sort": [{ "counter": "asc" }],
  "size": 50
}
```

## Limitations

- Requires Lucene 10.3.0 or later
- No functional changes to query behavior or performance

## References

### Documentation
- [PR #18530](https://github.com/opensearch-project/OpenSearch/pull/18530): Extend Approximation Framework to other numeric types (v3.2.0)
- [Lucene 10.3.0 Changes](https://lucene.apache.org/core/10_3_0/changes/Changes.html#v10.3.0.new_features): Lucene release notes

### Pull Requests
| PR | Description |
|----|-------------|
| [#19553](https://github.com/opensearch-project/OpenSearch/pull/19553) | Use Lucene `pack` method for `half_float` and `unsigned_long` |
| [apache/lucene#14784](https://github.com/apache/lucene/pull/14784) | Make `pack` methods public for `BigIntegerPoint` and `HalfFloatPoint` |

### Issues (Design / RFC)
- [Issue #14406](https://github.com/opensearch-project/OpenSearch/issues/14406): Feature request to expand ApproximatePointRangeQuery to other numeric types
- [Issue #18334](https://github.com/opensearch-project/OpenSearch/issues/18334): Feature request to improve numeric range query performance

## Related Feature Report

- [Approximation Framework](../../../features/opensearch/approximation-framework.md)
