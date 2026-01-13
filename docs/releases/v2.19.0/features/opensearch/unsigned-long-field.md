---
tags:
  - opensearch
---
# Unsigned Long Field

## Summary

OpenSearch v2.19.0 adds two improvements to the `unsigned_long` field type: support for retrieving doc values using the `docvalue_fields` parameter, and a fix for multi-value sorting that previously produced incorrect results when using sort modes (min, max, avg, sum, median) on fields with multiple values.

## Details

### What's New in v2.19.0

#### Doc Values Retrieval Support

Previously, attempting to use the `docvalue_fields` parameter to retrieve values from an `unsigned_long` field would throw an `UnsupportedOperationException`. This release implements the `LeafFieldData#getLeafValueFetcher` method for unsigned long fields, enabling doc values retrieval.

```json
GET my_index/_search
{
  "docvalue_fields": ["my_unsigned_long_field"],
  "query": {
    "match_all": {}
  }
}
```

#### Multi-Value Sort Fix

When sorting on multi-value `unsigned_long` fields using sort modes (min, max, avg, sum, median), the results were incorrect because Lucene treats the stored values as signed numbers. This caused values greater than `Long.MAX_VALUE` (9223372036854775807) to be incorrectly compared as negative numbers.

The fix introduces:
- `SortedNumericUnsignedLongValues`: A new abstract class for handling unsigned long doc values with proper unsigned comparison
- `LongToSortedNumericUnsignedLongValues`: Wrapper class that converts standard `SortedNumericDocValues` to unsigned long values
- Extended `MultiValueMode` enum with unsigned long support for all sort modes (SUM, AVG, MEDIAN, MIN, MAX)

### Technical Changes

| Component | Change |
|-----------|--------|
| `SortedNumericIndexFieldData` | Added `getLeafValueFetcher` implementation for unsigned long |
| `SortedNumericUnsignedLongValues` | New class for unsigned long doc values iteration |
| `LongToSortedNumericUnsignedLongValues` | Wrapper for converting signed to unsigned values |
| `UnsignedLongValuesComparatorSource` | Updated to use new unsigned long values classes |
| `MultiValueMode` | Added `pick()` methods for `SortedNumericUnsignedLongValues` |

### Usage Example

Multi-value sorting now works correctly:

```json
PUT my_index
{
  "mappings": {
    "properties": {
      "values": {
        "type": "unsigned_long"
      }
    }
  }
}

POST my_index/_bulk
{"index": {"_id": 1}}
{"values": [13835058055282163712, 3]}
{"index": {"_id": 2}}
{"values": [13835058055282163713, 2]}
{"index": {"_id": 3}}
{"values": [13835058055282163714, 1]}

GET my_index/_search
{
  "sort": [
    {
      "values": {
        "order": "desc",
        "mode": "max"
      }
    }
  ]
}
```

## Limitations

- The fix is specific to sorting operations; other operations already handled unsigned comparison correctly
- Performance impact is minimal as the wrapper classes add negligible overhead

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16543](https://github.com/opensearch-project/OpenSearch/pull/16543) | Support retrieving doc values of unsigned long field | - |
| [#16732](https://github.com/opensearch-project/OpenSearch/pull/16732) | Fix multi-value sort for unsigned long | [#16698](https://github.com/opensearch-project/OpenSearch/issues/16698) |

### Issues
- [#16698](https://github.com/opensearch-project/OpenSearch/issues/16698): Sort on multi-value unsigned long field is incorrect
