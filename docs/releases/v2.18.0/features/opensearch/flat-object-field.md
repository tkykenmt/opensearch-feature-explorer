---
tags:
  - domain/core
  - component/server
  - indexing
---
# Flat Object Field

## Summary

This release fixes a critical bug in the `flat_object` field type that caused an infinite loop when parsing invalid token types. Prior to v2.18.0, providing an array of strings, a plain string, or a number for a `flat_object` field would cause write threads to loop indefinitely, potentially hanging the cluster. The fix adds proper validation and throws a `ParsingException` for unsupported value types.

## Details

### What's New in v2.18.0

The `flat_object` field type now properly validates input and rejects invalid token types with clear error messages instead of entering an infinite loop.

### Technical Changes

#### Bug Root Cause

The infinite loop occurred due to two issues in the parsing logic:

1. `FlatObjectFieldMapper.parseCreateField()` attempted to parse flat object fields that were not objects or null
2. `JsonToStringXContentParser.parseToken()` would encounter an `END_ARRAY` token, ignore it, and not advance the parser

Combined, this created a scenario where passing an array of strings for a `flat_object` would parse the string values, then loop infinitely on the `END_ARRAY` token.

#### Code Changes

| Component | Change |
|-----------|--------|
| `FlatObjectFieldMapper` | Added validation to check for `START_OBJECT` token before parsing |
| `JsonToStringXContentParser` | Simplified `parseToken()` method, removed unused `processNoNestedValue()` method |
| `JsonToStringXContentParser` | Changed exception type from `IOException` to `ParsingException` for invalid tokens |

#### Error Handling

Invalid input now throws a `ParsingException` with a descriptive message:

```
[field_name] unexpected token [TOKEN_TYPE] in flat_object field value
```

Or for unexpected value tokens:

```
Unexpected value token type [TOKEN_TYPE]
```

### Usage Example

```json
// Valid: flat_object expects a JSON object
PUT /test-index/_doc/1
{
  "catalog": {
    "category": "books",
    "price": 29.99
  }
}

// Invalid: These now throw ParsingException instead of infinite loop
// Array of strings
PUT /test-index/_doc/2
{
  "catalog": ["Arrays in Action"]
}

// Plain string
PUT /test-index/_doc/3
{
  "catalog": "Strings in Action"
}

// Number
PUT /test-index/_doc/4
{
  "catalog": 12345
}
```

### Migration Notes

- No migration required
- Existing valid documents are unaffected
- Documents that previously caused infinite loops will now fail with a clear error message
- Applications should ensure `flat_object` fields receive JSON objects, not arrays, strings, or numbers

## Limitations

- `flat_object` fields only accept JSON objects as values
- Arrays, strings, numbers, and other primitive types are not supported as direct values
- This is by design, as `flat_object` is intended to store complex nested JSON structures

## References

### Documentation
- [Flat object documentation](https://docs.opensearch.org/2.18/field-types/supported-field-types/flat-object/): Official docs

### Pull Requests
| PR | Description |
|----|-------------|
| [#15985](https://github.com/opensearch-project/OpenSearch/pull/15985) | Avoid infinite loop in flat_object parsing |

### Issues (Design / RFC)
- [Issue #15982](https://github.com/opensearch-project/OpenSearch/issues/15982): Bug report for unbounded execution

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/opensearch-flat-object-field.md)
