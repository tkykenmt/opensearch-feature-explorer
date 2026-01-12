# Field Mapping Fixes

## Summary

OpenSearch v3.2.0 includes two important bug fixes for field mapping behavior:

1. **Field-level `ignore_malformed` override**: Field-level `ignore_malformed` settings now correctly override index-level settings, fixing a regression introduced in OpenSearch 2.4.
2. **`scaled_float` encodePoint fix**: Fixed a bug in the `encodePoint` method for `scaled_float` fields that was introduced in PR #18896.

These fixes ensure proper handling of malformed data during indexing and correct point encoding for scaled float range queries.

## Details

### What's New in v3.2.0

#### Fix 1: Field-level `ignore_malformed` Override

Prior to this fix, when both index-level and field-level `ignore_malformed` settings were configured, the index-level setting would always take precedence. This was incorrect behavior - field-level settings should override index-level settings.

**Affected Field Types:**

| Type | Controlling Class |
|------|-------------------|
| `ip` | `IpFieldMapper` |
| `ip_range` | `RangeFieldMapper` |
| `geo_point` | `AbstractGeometryFieldMapper` |
| `geo_shape` | `AbstractGeometryFieldMapper` |
| `xy_point` | `AbstractGeometryFieldMapper` |
| `xy_shape` | `AbstractGeometryFieldMapper` |
| numerics | `NumberFieldMapper`, `ScaledFloatFieldMapper` |
| `derived` | `DerivedFieldMapper` |
| `date` | `DateFieldMapper` |

**Technical Changes:**

The fix introduces an `ignoreMalformed()` method in the `FieldMapper` base class that allows field mappers to expose their field-level setting. The `parse()` method now checks this field-level setting before falling back to the index-level `IGNORE_MALFORMED_SETTING`.

```java
private boolean shouldIgnoreMalformed(IndexSettings is) {
    if (ignoreMalformed() != null) {
        return ignoreMalformed().value();
    }
    if (is == null) {
        return false;
    }
    return IGNORE_MALFORMED_SETTING.get(is.getSettings());
}
```

#### Fix 2: `scaled_float` encodePoint Method

A bug was introduced in PR #18896 where the `encodePoint(Object value, boolean roundUp)` method in `ScaledFloatFieldMapper` was not correctly encoding the scaled value. The fix follows the same pattern used in the `termQuery` method.

**Before (buggy):**
```java
public byte[] encodePoint(Object value, boolean roundUp) {
    double doubleValue = parse(value);
    long scaledValue = Math.round(scale(doubleValue));
    // ... rounding logic
    return encodePoint(scaledValue);  // Wrong: called wrong overload
}
```

**After (fixed):**
```java
public byte[] encodePoint(Object value, boolean roundUp) {
    long scaledValue = Math.round(scale(value));
    // ... rounding logic
    byte[] point = new byte[Long.BYTES];
    LongPoint.encodeDimension(scaledValue, point, 0);
    return point;
}
```

### Usage Example

**Index with field-level override:**
```json
PUT /my-index
{
  "settings": {
    "index.mapping.ignore_malformed": true
  },
  "mappings": {
    "properties": {
      "number_one": {
        "type": "byte"
      },
      "number_two": {
        "type": "integer",
        "ignore_malformed": false
      }
    }
  }
}
```

**Expected behavior (v3.2.0+):**
- `number_one`: Malformed values are ignored (inherits index-level setting)
- `number_two`: Malformed values cause indexing failure (field-level override)

```json
// This will FAIL in v3.2.0+ (correct behavior)
PUT /my-index/_doc/1
{
  "number_two": "not_a_number"
}
```

## Limitations

- The fix only applies to field types that support `ignore_malformed` (listed above)
- Versions prior to 3.2.0 (back to 2.4) have the incorrect behavior where index-level settings always take precedence

## References

### Documentation
- [Numeric field types documentation](https://docs.opensearch.org/3.0/field-types/supported-field-types/numeric/): Official docs for scaled_float
- [Mapping parameters](https://docs.opensearch.org/3.0/field-types/mapping-parameters/index/): Documentation on ignore_malformed

### Pull Requests
| PR | Description |
|----|-------------|
| [#18706](https://github.com/opensearch-project/OpenSearch/pull/18706) | Field-level ignore_malformed should override index-level setting |
| [#18952](https://github.com/opensearch-project/OpenSearch/pull/18952) | Bug fix for `scaled_float` in `encodePoint` method |

### Issues (Design / RFC)
- [Issue #16599](https://github.com/opensearch-project/OpenSearch/issues/16599): Original bug report for ignore_malformed override

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/field-mapping.md)
