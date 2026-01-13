---
tags:
  - opensearch
---
# Sort Field Merging

## Summary

Fixed incorrect sorting behavior when merging top docs from multiple shards with different numeric field types. The fix ensures correct type widening is used when sort values exceed the maximum safe integer value for double precision.

## Details

### What's New in v2.19.0

This release fixes a bug in the sort field merging logic during the search phase when combining results from multiple shards.

### Problem

When sorting across indices with different numeric field types (e.g., `long` and `integer`), OpenSearch previously used `double` to widen all sort fields. This caused incorrect sorting when values exceeded `2^53 - 1` (the maximum safe integer for double precision), as large `long` values would lose precision when converted to `double`.

### Solution

The `SearchPhaseController.createSort()` method was updated to:

1. Detect the actual numeric type of sort fields using `IndexFieldData.XFieldComparatorSource.reducedType()`
2. Use `Long` type for widening when all sort fields are integer types (long, integer, short, byte)
3. Use `Double` type for widening only when floating-point types (double, float, half_float) are involved
4. Create appropriate `SortedWiderNumericSortField` comparators based on the widened type

### Technical Changes

| Component | Change |
|-----------|--------|
| `SearchPhaseController` | Updated `createSort()` to determine correct widening type based on field types |
| `SortedWiderNumericSortField` | Added type-specific comparators for `Long` and `Double` types |

### Code Changes

The key changes in `SearchPhaseController.java`:

```java
private static SortField.Type getSortType(SortField sortField) {
    if (sortField.getComparatorSource() instanceof IndexFieldData.XFieldComparatorSource) {
        return ((IndexFieldData.XFieldComparatorSource) sortField.getComparatorSource()).reducedType();
    } else {
        return sortField instanceof SortedNumericSortField
            ? ((SortedNumericSortField) sortField).getNumericType()
            : sortField.getType();
    }
}
```

The `SortedWiderNumericSortField` now uses type-specific comparators:

- For `Long` type: `Comparator.comparingLong(Number::longValue)`
- For `Double` type: `Comparator.comparingDouble(Number::doubleValue)`

## Limitations

- `unsigned_long` fields are not supported by widening sort since they cannot be used with other numeric types
- When mixing integer and floating-point types, `Double` widening is still used (potential precision loss for very large integers)

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16881](https://github.com/opensearch-project/OpenSearch/pull/16881) | Use the correct type to widen the sort fields when merging top docs | [#16860](https://github.com/opensearch-project/OpenSearch/issues/16860) |

### Related Issues

- [#16860](https://github.com/opensearch-project/OpenSearch/issues/16860) - Use the correct type to widen the sort fields when merging top field docs
- [#6326](https://github.com/opensearch-project/OpenSearch/issues/6326) - Original issue for sort optimization type widening
