---
tags:
  - domain/core
  - component/server
  - search
---
# Field Type Fixes

## Summary

This release fixes `instanceof` checks throughout the OpenSearch codebase to properly handle the new `FilterFieldType` wrapper pattern. With the introduction of `FilterFieldType` in v3.0.0, field types can now be wrapped by delegate types (e.g., `SemanticFieldType`). All `instanceof` checks must now call `unwrap()` before checking the underlying field type to ensure correct behavior.

## Details

### What's New in v3.0.0

The `FilterFieldType` class was introduced to allow developers to wrap existing field types while delegating behavior by default. This enables features like `SemanticFieldType` in neural-search to wrap delegate field types. However, existing code that used `instanceof` checks on `MappedFieldType` would fail to recognize wrapped types.

This fix updates all `instanceof` checks across the codebase to call `fieldType.unwrap()` before performing type checks.

### Technical Changes

#### Pattern Change

Before:
```java
if (fieldType instanceof DateFieldMapper.DateFieldType) {
    // handle date field
}
```

After:
```java
if (fieldType.unwrap() instanceof DateFieldMapper.DateFieldType) {
    // handle date field
}
```

#### Affected Components

| Component | Files Modified | Description |
|-----------|----------------|-------------|
| Expression Script Engine | 1 | GeoPoint and Date field type checks |
| Mapper Extras | 1 | RankFeature query builder |
| Percolator | 1 | Percolator field type check |
| Star Tree | 3 | Composite field type validation |
| Analyze Action | 1 | String field type check |
| Codec | 1 | Completion field type check |
| Derived Field Resolver | 2 | Derived field type resolution |
| Mapping Lookup | 1 | Timestamp field check |
| Query Builders | 8 | Various query type checks |
| Aggregations | 6 | Composite and filter rewrite sources |
| Search | 3 | Match query and query string parser |
| Term Vectors | 1 | String field validation |

#### Key Changes by Area

**Query Builders:**
- `GeoPolygonQueryBuilder`: GeoPoint field validation
- `PrefixQueryBuilder`: Constant field type optimization
- `TermQueryBuilder`: Constant field type optimization
- `TermsQueryBuilder`: Number field and constant field checks
- `WildcardQueryBuilder`: Constant field type optimization
- `DecayFunctionBuilder`: Date, GeoPoint, and Number field handling

**Aggregations:**
- `BinaryValuesSource`: String field type check
- `GlobalOrdinalValuesSource`: String field type check
- `LongValuesSource`: Number and Date field checks
- `UnsignedLongValuesSource`: Number field check
- `CompositeAggregatorBridge`: Date field optimization
- `DateHistogramAggregatorBridge`: Date field optimization

**Mappers:**
- `MapperService`: Composite field type detection
- `MappingLookup`: Timestamp field validation
- `DefaultDerivedFieldResolver`: Derived field type resolution
- `DerivedFieldType`: Prefilter field validation

### Usage Example

For plugin developers working with field types:

```java
public void processField(MappedFieldType fieldType) {
    // Always unwrap before instanceof check
    MappedFieldType unwrapped = fieldType.unwrap();
    
    if (unwrapped instanceof DateFieldMapper.DateFieldType) {
        DateFieldMapper.DateFieldType dateType = (DateFieldMapper.DateFieldType) unwrapped;
        // Process date field
    } else if (unwrapped instanceof GeoPointFieldType) {
        // Process geo point field
    }
}
```

### Migration Notes

Plugin developers who perform `instanceof` checks on `MappedFieldType` should:

1. Call `unwrap()` before any `instanceof` check
2. Add null checks where appropriate (some code paths now include `fieldType != null` guards)
3. Test with wrapped field types like `SemanticFieldType`

## Limitations

- The `unwrap()` method returns `this` for non-wrapped types, so existing code will continue to work
- Casting after `instanceof` check should use the original `fieldType` if the wrapper behavior is needed

## References

### Documentation
- [Mappings and field types](https://docs.opensearch.org/3.0/field-types/): OpenSearch field types documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#17951](https://github.com/opensearch-project/OpenSearch/pull/17951) | Add unwrap function to all fieldType instanceof checks |
| [#17627](https://github.com/opensearch-project/OpenSearch/pull/17627) | Add FilterFieldType (prerequisite) |

### Issues (Design / RFC)
- [Issue #17802](https://github.com/opensearch-project/OpenSearch/issues/17802): Unwrap FieldType before instanceof check
- [Issue #17624](https://github.com/opensearch-project/OpenSearch/issues/17624): FilterFieldType feature request

## Related Feature Report

- Full feature documentation
