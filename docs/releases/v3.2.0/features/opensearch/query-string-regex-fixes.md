---
tags:
  - domain/core
  - component/server
  - search
---
# Query String & Regex Fixes

## Summary

OpenSearch v3.2.0 includes three important bug fixes for query string and regular expression queries. These fixes address issues with field alias support, backward compatibility for the COMPLEMENT operator, and proper error propagation for overly complex regex patterns.

## Details

### What's New in v3.2.0

This release resolves three distinct bugs affecting regex functionality in OpenSearch:

1. **Field Alias Support**: Regex queries within `query_string` now correctly resolve field aliases
2. **COMPLEMENT Flag Restoration**: The `~` (COMPLEMENT) operator for regexp queries works again after a regression in OpenSearch 3.0
3. **TooComplexToDeterminizeException Propagation**: Complex regex patterns now properly return 400 errors instead of silently failing

### Technical Changes

#### Fix 1: Regex Query with Field Alias (PR #18215)

The `QueryStringQueryParser.getRegexpQuerySingle()` method was updated to use `currentFieldType.regexpQuery()` instead of delegating to Lucene's `super.getRegexpQuery()`. This ensures field aliases are properly resolved through OpenSearch's field mapper.

**Before**: Regex queries on alias fields returned no results
**After**: Regex queries correctly resolve aliases to their target fields

```java
// Changed from:
return super.getRegexpQuery(field, termStr);

// To:
termStr = getAnalyzer().normalize(currentFieldType.name(), termStr).utf8ToString();
return currentFieldType.regexpQuery(termStr, RegExp.ALL, 0, getDeterminizeWorkLimit(), getMultiTermRewriteMethod(), context);
```

#### Fix 2: COMPLEMENT Flag Backward Compatibility (PR #18640)

The `RegexpQueryBuilder.doToQuery()` method was fixed to preserve the COMPLEMENT flag when sanitizing syntax flags. The issue was introduced in OpenSearch 3.0 when Lucene changed `RegExp.ALL` from `0xffff` to `0xff`, which inadvertently dropped the COMPLEMENT bit (`0x10000`).

```java
// Changed from:
int sanitisedSyntaxFlag = syntaxFlagsValue & RegExp.ALL;

// To:
int sanitisedSyntaxFlag = syntaxFlagsValue & (RegExp.ALL | RegExp.DEPRECATED_COMPLEMENT);
```

A deprecation warning is now emitted when using the COMPLEMENT operator, as it will be removed in Lucene 11 (OpenSearch 4.0).

#### Fix 3: TooComplexToDeterminizeException Handling (PR #18883)

The `QueryStringQueryParser` was incorrectly swallowing `TooComplexToDeterminizeException` when `lenient` mode was enabled. The fix adds an explicit check to propagate this exception regardless of lenient mode.

```java
// Changed from:
if (lenient) {
    return newLenientFieldQuery(field, e);
}

// To:
if (lenient && !(e instanceof TooComplexToDeterminizeException)) {
    return newLenientFieldQuery(field, e);
}
```

**Before**: Complex regex in `query_string` returned HTTP 200 with empty results
**After**: Complex regex properly returns HTTP 400 with `too_complex_to_determinize_exception`

### Usage Example

#### Field Alias with Regex Query

```json
PUT /test_index
{
  "mappings": {
    "properties": {
      "test": { "type": "text" },
      "test_alias": { "type": "alias", "path": "test" }
    }
  }
}

GET /test_index/_search
{
  "query": {
    "query_string": {
      "query": "test_alias: /h[a-z].*/"
    }
  }
}
```

#### COMPLEMENT Operator

```json
GET /test/_search
{
  "query": {
    "regexp": {
      "text.keyword": {
        "value": "a~bc",
        "flags": "COMPLEMENT"
      }
    }
  }
}
```

### Migration Notes

- **COMPLEMENT Deprecation**: The `~` operator is deprecated and will be removed in OpenSearch 4.0 (Lucene 11). Consider using character class negation `[^...]` or other query types as alternatives.
- **Error Handling**: Applications relying on `query_string` with complex regex patterns may now receive 400 errors where they previously received empty results. Update error handling accordingly.

## Limitations

- The COMPLEMENT operator (`~`) is deprecated and scheduled for removal in OpenSearch 4.0
- Field alias support for regex is only available in OpenSearch 3.2.0 and later

## References

### Documentation
- [Query String Documentation](https://docs.opensearch.org/3.0/query-dsl/full-text/query-string/): Official query_string docs
- [Regular Expression Syntax](https://docs.opensearch.org/3.0/query-dsl/regex-syntax/): Regex syntax reference

### Pull Requests
| PR | Description |
|----|-------------|
| [#18215](https://github.com/opensearch-project/OpenSearch/pull/18215) | Fix regex query from query string query to work with field alias |
| [#18640](https://github.com/opensearch-project/OpenSearch/pull/18640) | Fix backward compatibility regression with COMPLEMENT for Regexp queries |
| [#18883](https://github.com/opensearch-project/OpenSearch/pull/18883) | Propagate TooComplexToDeterminizeException in query_string regex queries |

### Issues (Design / RFC)
- [Issue #18214](https://github.com/opensearch-project/OpenSearch/issues/18214): Regex query doesn't support field alias
- [Issue #18397](https://github.com/opensearch-project/OpenSearch/issues/18397): COMPLEMENT does not work in Regexp queries
- [Issue #18733](https://github.com/opensearch-project/OpenSearch/issues/18733): query_string behavior using regex when shard failures occur

## Related Feature Report

- Full feature documentation
