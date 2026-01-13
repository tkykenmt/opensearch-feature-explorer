---
tags:
  - opensearch
---
# Match Only Text Field

## Summary

OpenSearch 2.19.0 includes two improvements to the `match_only_text` field type: consistent use of `constant_score` queries for better performance and support for wildcard highlighting.

## Details

### What's New in v2.19.0

#### Constant Score Query Optimization

The `match_only_text` field type now always uses `constant_score` queries for term queries. Previously, some query paths could still attempt to compute scores, which prevented early termination optimizations. This change ensures consistent behavior and improved query performance.

**Technical Changes:**
- `termQuery()` and `termQueryCaseInsensitive()` methods in `MatchOnlyTextFieldMapper` now wrap results in `ConstantScoreQuery`
- Eliminates unnecessary score computation attempts when term frequency statistics are not available
- Enables early termination for queries that don't require scoring

#### Wildcard Highlighting Support

Highlighting now works correctly for wildcard searches on `match_only_text` fields. Previously, wildcard patterns in field names would skip `match_only_text` fields during highlighting.

**Technical Changes:**
- `HighlightPhase.java` updated to include `match_only_text` in the list of highlightable field types
- Wildcard field patterns (e.g., `*` or `text*`) now correctly match `match_only_text` fields

### Usage Example

```json
PUT /my-index
{
  "mappings": {
    "properties": {
      "message": {
        "type": "match_only_text"
      }
    }
  }
}

POST /my-index/_search
{
  "query": {
    "match": {
      "message": "error"
    }
  },
  "highlight": {
    "fields": {
      "*": {}
    }
  }
}
```

## Limitations

- `match_only_text` fields do not support interval or span queries
- Phrase query performance may be slower than standard `text` fields due to source field verification
- Scoring is always constant (1.0) - relevance ranking is not available

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16964](https://github.com/opensearch-project/OpenSearch/pull/16964) | Always use constant_score query for match_only_text | Big5 benchmark latency improvement |
| [#17101](https://github.com/opensearch-project/OpenSearch/pull/17101) | Add highlighting for wildcard search on match_only_text field | Community request |

### Documentation
- [String field types](https://docs.opensearch.org/2.19/field-types/supported-field-types/string/)
- [Optimize storage and performance with the MatchOnlyText field](https://opensearch.org/blog/optimize-storage-and-performance-using-matchonlytext-field/)
