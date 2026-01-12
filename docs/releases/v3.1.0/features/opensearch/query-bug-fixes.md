---
tags:
  - search
---

# Query Bug Fixes

## Summary

OpenSearch v3.1.0 includes several bug fixes that improve query handling, error responses, and field type support. These fixes address issues with object field exists queries, HTTP status codes for parsing errors, null field validation in query builders, IP field terms queries on doc-values-only fields, and aggregator reuse.

## Details

### What's New in v3.1.0

This release addresses five query-related issues:

1. **Object field exists query fix** - Resolves incorrect results when querying object fields with derived subfields or user-defined fields starting with underscore
2. **Bad Request status for InputCoercionException** - Returns HTTP 400 instead of 500 for invalid numeric input values
3. **Null check in QueryStringQueryBuilder** - Validates field names to prevent IllegalStateException
4. **IP field terms_query enhancement** - Supports more than 1024 IP/masks in doc-values-only fields
5. **MatrixStatsAggregator reuse fix** - Fixes aggregator reuse when mode parameter changes

### Technical Changes

#### Object Field Exists Query Fix

Previously, exists queries on object fields would skip subfields starting with `_` to avoid exceptions from internal fields. This caused issues when:
- User-defined subfield names started with `_`
- Object fields contained derived type subfields

The fix changes `DerivedFieldType.existsQuery()` to throw `UnsupportedOperationException` instead of `IllegalArgumentException`, and `ExistsQueryBuilder` now catches and ignores subfields that don't support exists queries.

```java
// DerivedFieldType.java - Changed exception type
@Override
public Query existsQuery(QueryShardContext context) {
    throw new UnsupportedOperationException(
        "Field [" + name() + "] of type [" + typeName() + "] does not support exist queries"
    );
}
```

#### InputCoercionException Handling

Jackson's `InputCoercionException` is thrown for valid but incompatible input values (e.g., integer overflow). The fix adds this exception type to `ExceptionsHelper.status()` to return HTTP 400 Bad Request.

```java
// ExceptionsHelper.java
} else if (t instanceof InputCoercionException) {
    return RestStatus.BAD_REQUEST;
}
```

#### QueryStringQueryBuilder Null Check

Added validation to prevent null field names in the `fields` array, which previously caused an `IllegalStateException` with HTTP 500.

```java
// QueryStringQueryBuilder.java
if (parser.currentToken() == XContentParser.Token.VALUE_NULL) {
    throw new ParsingException(
        parser.getTokenLocation(),
        "[query_string] field name in [" + currentFieldName + "] cannot be null"
    );
}
```

#### IP Field Terms Query Enhancement

For doc-values-only IP fields, the previous implementation was limited by `maxClauses` (1024) when using IP masks. The fix uses Lucene's `DocValuesMultiRangeQuery.SortedSetStabbingBuilder` to handle unlimited IP/masks.

```java
// IpFieldMapper.java - New doc-values query builder
DocValuesMultiRangeQuery.SortedSetStabbingBuilder builder = 
    new DocValuesMultiRangeQuery.SortedSetStabbingBuilder(name());
masks.forEach(q -> builder.add(
    new BytesRef(q.getLowerPoint()), 
    new BytesRef(q.getUpperPoint())
));
ipsBytes.forEach(builder::add);
return builder.build();
```

### Usage Example

```json
// Object field exists query now works correctly
POST test/_search
{
  "query": {
    "exists": {
      "field": "log"
    }
  }
}

// IP terms query with >1024 masks on doc-values-only field
POST test/_search
{
  "query": {
    "terms": {
      "ip_field.dv": ["192.168.0.0/16", "10.0.0.0/8", ...]
    }
  }
}

// Query string with null field now returns 400
POST test/_search
{
  "query": {
    "query_string": {
      "query": "test",
      "fields": ["field1", null]  // Returns 400 Bad Request
    }
  }
}
```

### Migration Notes

- Applications relying on HTTP 500 status for `InputCoercionException` should update error handling to expect HTTP 400
- Queries using IP masks on doc-values-only fields are no longer limited to 1024 terms

## Limitations

- Derived fields still do not support exists queries directly; they are silently skipped when querying parent object fields

## References

### Documentation
- [Query string documentation](https://docs.opensearch.org/3.0/query-dsl/full-text/query-string/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#17843](https://github.com/opensearch-project/OpenSearch/pull/17843) | Fix object field exists query |
| [#18161](https://github.com/opensearch-project/OpenSearch/pull/18161) | Use Bad Request status for InputCoercionException |
| [#18194](https://github.com/opensearch-project/OpenSearch/pull/18194) | Null check field names in QueryStringQueryBuilder |
| [#18357](https://github.com/opensearch-project/OpenSearch/pull/18357) | DocValues-only IP field supports terms_query with more than 1025 IP masks |
| [#18242](https://github.com/opensearch-project/OpenSearch/pull/18242) | Fix MatrixStatsAggregator reuse when mode parameter changes |

### Issues (Design / RFC)
- [Issue #17808](https://github.com/opensearch-project/OpenSearch/issues/17808): Object Field exists query returns wrong result
- [Issue #18131](https://github.com/opensearch-project/OpenSearch/issues/18131): XContent parsing exceptions return 500 status
- [Issue #17394](https://github.com/opensearch-project/OpenSearch/issues/17394): Unlimit IP/masks terms query for doc_values only fields

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/query-bug-fixes.md)
