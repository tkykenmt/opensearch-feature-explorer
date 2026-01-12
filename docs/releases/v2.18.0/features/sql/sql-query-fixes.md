---
tags:
  - indexing
  - search
  - sql
---

# SQL Query Fixes

## Summary

This release includes two bug fixes for the SQL plugin: resolving alias issues in legacy SQL queries with filters, and correcting an overly permissive regular expression range in the Grok pattern compiler.

## Details

### What's New in v2.18.0

Two critical bug fixes improve SQL query reliability:

1. **Alias Resolution with Filters**: Legacy SQL queries using index aliases with filters now work correctly
2. **Regex Range Correction**: Fixed overly permissive character range `[A-z]` in Grok pattern matching

### Technical Changes

#### Fix 1: Alias Issues in Legacy SQL with Filters

**Problem**: When executing legacy SQL queries against an index alias with a filter parameter, the query failed with "Index type [alias-name] does not exist" error.

**Root Cause**: The `SelectResultSet.loadFromEsState()` method used the alias name directly for field mapping lookups, but OpenSearch requires the actual index name.

**Solution**: Added alias-to-index resolution using `GetAliasesRequest` before loading field mappings.

```java
// Before: Used alias name directly
String indexName = fetchIndexName(query);

// After: Resolve alias to actual index name
GetAliasesResponse getAliasesResponse =
    client.admin().indices().getAliases(new GetAliasesRequest(indexName)).actionGet();
if (getAliasesResponse != null && !getAliasesResponse.getAliases().isEmpty()) {
    indexName = getAliasesResponse.getAliases().keySet().iterator().next();
}
```

**Affected File**: `legacy/src/main/java/org/opensearch/sql/legacy/executor/format/SelectResultSet.java`

#### Fix 2: Regular Expression Range Correction

**Problem**: The regex pattern `[A-z]` in Grok compiler matched unintended characters: `[ \ ] ^ _ \``

**Root Cause**: In ASCII, characters between 'Z' (90) and 'a' (97) include special characters that were inadvertently matched.

**Solution**: Changed `[A-z]` to `[a-zA-Z_]` for explicit character class definition.

```java
// Before: Overly permissive range
private static final Pattern patternLinePattern = Pattern.compile("^([A-z0-9_]+)\\s+(.*)$");

// After: Explicit character classes
private static final Pattern patternLinePattern = Pattern.compile("^([a-zA-Z0-9_]+)\\s+(.*)$");
```

**Affected Files**:
- `common/src/main/java/org/opensearch/sql/common/grok/GrokCompiler.java`
- `common/src/main/java/org/opensearch/sql/common/grok/GrokUtils.java`

### Usage Example

After the fix, alias queries with filters work correctly:

```bash
# Create an index and alias
PUT /my-index
POST /_aliases
{
  "actions": [
    { "add": { "index": "my-index", "alias": "my-alias" } }
  ]
}

# Query using alias with filter - now works in v2.18.0
POST /_plugins/_sql
{
  "query": "SELECT * FROM my-alias",
  "fetch_size": 10,
  "filter": {
    "term": {
      "field_name": "value"
    }
  }
}
```

## Limitations

- The alias resolution fix applies only to legacy SQL queries (not the new SQL engine)
- When an alias points to multiple indices, the first index in the response is used for field mapping resolution

## References

### Documentation
- [SQL Documentation](https://docs.opensearch.org/2.18/search-plugins/sql/sql/index/): OpenSearch SQL plugin documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#3109](https://github.com/opensearch-project/sql/pull/3109) | Backport: Resolve Alias Issues in Legacy SQL with Filters |
| [#3107](https://github.com/opensearch-project/sql/pull/3107) | Backport: Correct regular expression range |
| [#2960](https://github.com/opensearch-project/sql/pull/2960) | Original: Resolve Alias Issues in Legacy SQL with Filters |
| [#2836](https://github.com/opensearch-project/sql/pull/2836) | Original: Correct regular expression range |

### Issues (Design / RFC)
- [Issue #2912](https://github.com/opensearch-project/sql/issues/2912): Pagination of index aliases is not supported - Re-opened
- [Issue #1398](https://github.com/opensearch-project/sql/issues/1398): Original alias pagination bug report

## Related Feature Report

- [Full feature documentation](../../../features/sql/sql-query-fixes.md)
