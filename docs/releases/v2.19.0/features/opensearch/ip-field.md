---
tags:
  - opensearch
---
# IP Field

## Summary

Fixed an edge case where doc_values-only IP fields (with `index: false`) could not be searched using CIDR notation (IP masks). Previously, queries like `192.168.0.1/24` on doc_values-only IP fields were silently ignored and returned no results.

## Details

### What's New in v2.19.0

This release fixes IP mask (CIDR notation) searching for IP fields configured with only doc_values enabled (`index: false`). The fix ensures that term queries, terms queries, and range queries all work correctly when searching IP fields using CIDR notation on doc_values-only fields.

### Technical Changes

The `IpFieldMapper.java` was refactored to properly handle doc_values-only queries:

| Query Type | Before v2.19.0 | After v2.19.0 |
|------------|----------------|---------------|
| Term query with CIDR | Silently ignored | Uses `SortedSetDocValuesField.newSlowRangeQuery` |
| Terms query | Only worked with indexed fields | Supports doc_values via `newSlowSetQuery` |
| Range query | Partial support | Full support with `IndexOrDocValuesQuery` |

The implementation now:
1. Extracts lower and upper bounds from `PointRangeQuery` for CIDR notation
2. Creates appropriate `SortedSetDocValuesField` queries for doc_values-only fields
3. Uses `IndexOrDocValuesQuery` when both index and doc_values are available

### Example

```json
PUT testindex
{
  "mappings": {
    "properties": {
      "ip_address": {
        "type": "ip",
        "index": false,
        "doc_values": true
      }
    }
  }
}

GET testindex/_search
{
  "query": {
    "term": {
      "ip_address": "192.168.0.1/24"
    }
  }
}
```

## Limitations

- Doc_values-only queries use "slow" query implementations (`newSlowRangeQuery`, `newSlowSetQuery`) which may have performance implications for large datasets compared to indexed fields

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16628](https://github.com/opensearch-project/OpenSearch/pull/16628) | Fix `doc_values` only (`index:false`) IP field searching for masks | [#11508](https://github.com/opensearch-project/OpenSearch/pull/11508) |

### Documentation
- [IP address field type](https://docs.opensearch.org/2.19/field-types/supported-field-types/ip/)
