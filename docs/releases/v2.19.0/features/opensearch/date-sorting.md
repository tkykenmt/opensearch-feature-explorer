---
tags:
  - opensearch
---
# Date Sorting Overflow Prevention

## Summary

OpenSearch v2.19.0 adds overflow prevention when handling extreme date values during sorting operations. This fix prevents `arithmetic_exception: long overflow` errors that occurred intermittently when sorting on date fields containing extreme values or when documents had missing date values.

## Details

### What's New in v2.19.0

A new `clampToMillisRange()` method was added to `DateUtils` that clamps `Instant` values to the valid epoch millisecond range (`Long.MIN_VALUE` to `Long.MAX_VALUE`). This method is now called during date field conversion to prevent overflow when converting extreme date values to epoch milliseconds.

### Technical Changes

The fix modifies the `DateFieldMapper.Resolution.MILLISECONDS` enum to clamp date values before conversion:

| Component | Change |
|-----------|--------|
| `DateUtils.java` | Added `clampToMillisRange()` method that clamps `Instant` to valid epoch millisecond range |
| `DateFieldMapper.java` | Modified `MILLISECONDS.convert()` to call `clampToValidRange()` before `toEpochMilli()` |
| `DateFieldMapper.java` | Updated `MILLISECONDS.clampToValidRange()` to use `DateUtils.clampToMillisRange()` |

### Root Cause

The overflow occurred when:
1. Sorting on date fields with extreme values (e.g., dates far in the past or future)
2. Documents with missing date values where `missing: "_last"` or `missing: "_first"` was specified
3. The internal conversion from `Instant` to epoch milliseconds exceeded `Long.MAX_VALUE` or went below `Long.MIN_VALUE`

### Clamping Behavior

| Condition | Result |
|-----------|--------|
| Date before `Long.MIN_VALUE` epoch millis | Clamped to `Instant.ofEpochMilli(Long.MIN_VALUE)` |
| Date after `Long.MAX_VALUE` epoch millis | Clamped to `Instant.ofEpochMilli(Long.MAX_VALUE)` |
| Date within valid range | Returned as-is |

## Limitations

- Extreme date values outside the valid epoch millisecond range will be clamped, which may affect sort order precision for such edge cases
- This fix applies only to millisecond resolution date fields; nanosecond resolution fields have separate handling

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16812](https://github.com/opensearch-project/OpenSearch/pull/16812) | Overflow prevention when handling date values | [#16709](https://github.com/opensearch-project/OpenSearch/issues/16709), [#5713](https://github.com/opensearch-project/OpenSearch/issues/5713) |

### Related Issues

- [#16709](https://github.com/opensearch-project/OpenSearch/issues/16709) - arithmetic_exception: long overflow while running sort query on date field
- [#5713](https://github.com/opensearch-project/OpenSearch/issues/5713) - Random arithmetic_exception - "long overflow" errors
