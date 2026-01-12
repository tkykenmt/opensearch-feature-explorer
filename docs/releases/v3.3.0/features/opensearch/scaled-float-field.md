---
tags:
  - indexing
  - search
---

# Scaled Float Field Precision Fix

## Summary

This release fixes a precision issue in the `scaled_float` field type where `match` queries on certain values (especially large numbers) would fail to return expected results. The fix ensures consistent behavior between indexing and querying by using the same multiplication method for both operations.

## Details

### What's New in v3.3.0

The `scaled_float` field type had an inconsistency between how values were scaled during indexing versus querying:

- **Indexing**: Used direct floating-point multiplication (`doubleValue * scalingFactor`)
- **Querying**: Used `BigDecimal` multiplication for precision

This mismatch caused queries to fail for certain values, particularly large numbers like `92233720368547750` with a scaling factor of `100`.

### Technical Changes

#### Root Cause

The `scale()` method in `ScaledFloatFieldMapper` used `BigDecimal` for query-time scaling:

```java
// Before (problematic)
private double scale(Object input) {
    return new BigDecimal(Double.toString(parse(input)))
        .multiply(BigDecimal.valueOf(scalingFactor))
        .doubleValue();
}
```

This produced different scaled values than the direct multiplication used at index time, causing term mismatches.

#### The Fix

The `scale()` method now uses direct multiplication, matching the indexing behavior:

```java
// After (fixed)
private double scale(Object input) {
    return parse(input) * scalingFactor;
}
```

#### Range Query Changes

The range query logic was also simplified to properly pass through `includeLower` and `includeUpper` parameters instead of manually adjusting bounds:

```java
// Before: Manual bound adjustment
if (includeLower == false) {
    dValue = Math.nextUp(dValue);
}
lo = Math.round(Math.ceil(dValue));

// After: Direct delegation
lo = Math.round(scale(lowerTerm));
Query query = NumberFieldMapper.NumberType.LONG.rangeQuery(
    name(), lo, hi, includeLower, includeUpper, ...);
```

### Usage Example

The fix ensures this scenario now works correctly:

```json
// Create index with scaled_float field
PUT test-index
{
  "mappings": {
    "properties": {
      "price": {
        "type": "scaled_float",
        "scaling_factor": 100
      }
    }
  }
}

// Index a document
PUT test-index/_doc/1
{
  "price": 92233720368547750
}

// Query now returns the document (was broken before)
POST test-index/_search
{
  "query": {
    "match": {
      "price": "92233720368547750"
    }
  }
}
```

### Migration Notes

- No reindexing required - the fix only affects query-time behavior
- Existing indices will work correctly after upgrading
- No configuration changes needed

## Limitations

- Floating-point precision limitations still apply (e.g., `79.99 * 100 = 7998.999...`)
- The fix prioritizes consistency over precision - both indexing and querying now use the same (potentially imprecise) multiplication

## References

### Documentation
- [Numeric field types documentation](https://docs.opensearch.org/3.0/field-types/supported-field-types/numeric/): Official docs for scaled_float

### Pull Requests
| PR | Description |
|----|-------------|
| [#19188](https://github.com/opensearch-project/OpenSearch/pull/19188) | Fix the `scaled_float` precision issue |

### Issues (Design / RFC)
- [Issue #12433](https://github.com/opensearch-project/OpenSearch/issues/12433): Bug report - `match` query on `scaled_float` no longer matches for some values

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/opensearch-scaled-float-field.md)
