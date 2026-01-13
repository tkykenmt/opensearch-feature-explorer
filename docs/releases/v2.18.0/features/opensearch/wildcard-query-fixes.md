---
tags:
  - domain/core
  - component/server
  - indexing
  - search
---
# Wildcard Query Fixes

## Summary

OpenSearch v2.18.0 fixes two bugs in wildcard queries on wildcard field types: escaped wildcard characters (`\*`, `\?`) are now handled correctly, and case-insensitive queries return expected results. These fixes ensure wildcard fields behave consistently with keyword fields for pattern matching.

## Details

### What's New in v2.18.0

Two critical bug fixes for the wildcard field type:

1. **Escaped Character Handling** ([#15737](https://github.com/opensearch-project/OpenSearch/pull/15737)): Wildcard queries containing escaped `\*` or `\?` characters now work correctly on wildcard fields, matching the behavior of keyword fields.

2. **Case-Insensitive Query Fix** ([#15882](https://github.com/opensearch-project/OpenSearch/pull/15882)): The `case_insensitive` parameter now properly returns all matching documents regardless of case.

### Technical Changes

#### Bug 1: Escaped Wildcard Characters

**Problem**: When searching for literal `*` or `?` characters using escape sequences (`\*`, `\?`), wildcard fields returned no results while keyword fields worked correctly.

**Root Cause**: The `WildcardFieldMapper.getRequiredNGrams()` method did not properly handle escape sequences when extracting n-grams for the index lookup phase.

**Fix**: Added `performEscape()` method to properly process escape sequences:

```java
private static String performEscape(String str) {
    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < str.length(); i++) {
        if (str.charAt(i) == '\\' && (i + 1) < str.length()) {
            char c = str.charAt(i + 1);
            if (c == '*' || c == '?') {
                i++;
            }
        }
        sb.append(str.charAt(i));
    }
    return sb.toString();
}
```

Also updated `getNonWildcardSequence()` to recognize escaped wildcards as literal characters.

#### Bug 2: Case-Insensitive Queries

**Problem**: Queries with `case_insensitive: true` only returned exact case matches instead of all case variations.

**Root Cause**: The `matchAllTermsQuery()` method used case-sensitive `TermQuery` for the approximation phase, filtering out documents with different case before the verification phase could run.

**Fix**: Updated `matchAllTermsQuery()` to use `AutomatonQueries.caseInsensitiveTermQuery()` when case-insensitive matching is requested:

```java
private static BooleanQuery matchAllTermsQuery(String fieldName, Set<String> terms, boolean caseInsensitive) {
    BooleanQuery.Builder matchAllTermsBuilder = new BooleanQuery.Builder();
    Query query;
    for (String term : terms) {
        if (caseInsensitive) {
            query = AutomatonQueries.caseInsensitiveTermQuery(new Term(fieldName, term));
        } else {
            query = new TermQuery(new Term(fieldName, term));
        }
        matchAllTermsBuilder.add(query, BooleanClause.Occur.FILTER);
    }
    return matchAllTermsBuilder.build();
}
```

### Usage Example

**Escaped wildcard search** (searching for literal `*`):

```json
PUT escape_test
{
  "mappings": {
    "properties": {
      "content": { "type": "wildcard" }
    }
  }
}

POST escape_test/_doc
{ "content": "* test *" }

GET escape_test/_search
{
  "query": {
    "wildcard": {
      "content": {
        "value": "\\**"
      }
    }
  }
}
```

**Case-insensitive search**:

```json
PUT case_test
{
  "mappings": {
    "properties": {
      "name": { "type": "wildcard" }
    }
  }
}

POST case_test/_bulk
{"index": {}}
{"name": "TtAa"}
{"index": {}}
{"name": "ttaa"}
{"index": {}}
{"name": "TTAA"}

GET case_test/_search
{
  "query": {
    "wildcard": {
      "name": {
        "value": "TtAa",
        "case_insensitive": true
      }
    }
  }
}
// Returns all 3 documents
```

## Limitations

- These fixes apply only to the `wildcard` field type, not to wildcard queries on `keyword` or `text` fields (which already worked correctly)

## References

### Documentation
- [Wildcard Field Documentation](https://docs.opensearch.org/2.18/field-types/supported-field-types/wildcard/): Official documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#15737](https://github.com/opensearch-project/OpenSearch/pull/15737) | Fix wildcard query containing escaped character |
| [#15882](https://github.com/opensearch-project/OpenSearch/pull/15882) | Fix case-insensitive query on wildcard field |

### Issues (Design / RFC)
- [Issue #15555](https://github.com/opensearch-project/OpenSearch/issues/15555): Bug report for escaped wildcard character handling
- [Issue #15855](https://github.com/opensearch-project/OpenSearch/issues/15855): Bug report for case-insensitive query issue

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/opensearch-wildcard-field.md)
