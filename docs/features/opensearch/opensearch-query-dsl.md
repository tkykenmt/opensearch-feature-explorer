---
tags:
  - opensearch
---
# OpenSearch Query DSL

## Summary

OpenSearch Query DSL (Domain Specific Language) provides a full-featured query language for defining searches. It supports full-text queries, term-level queries, compound queries, and specialized queries for various use cases including fuzzy matching, phrase matching, and autocomplete functionality.

## Details

### Query Types

#### Full-Text Queries
| Query | Description |
|-------|-------------|
| `match` | Standard full-text query with fuzzy matching support |
| `match_phrase` | Matches exact phrases in order |
| `match_phrase_prefix` | Matches phrases with prefix matching on the last term |
| `multi_match` | Matches across multiple fields |
| `query_string` | Supports Lucene query syntax |

#### Term-Level Queries
| Query | Description |
|-------|-------------|
| `term` | Exact term matching |
| `terms` | Multiple exact term matching |
| `fuzzy` | Matches terms within edit distance |
| `prefix` | Prefix matching |
| `wildcard` | Wildcard pattern matching |
| `regexp` | Regular expression matching |

### Index Prefixes

The `index_prefixes` mapping parameter enables efficient prefix searches on text fields by creating a hidden sub-field (`{field}._index_prefix`) that indexes edge n-grams.

```json
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "index_prefixes": {
          "min_chars": 2,
          "max_chars": 5
        }
      }
    }
  }
}
```

### Position Increment Gap

When indexing arrays of text values, `position_increment_gap` (default: 100) creates artificial gaps between values to prevent phrase queries from matching across array boundaries.

```json
{
  "mappings": {
    "properties": {
      "tags": {
        "type": "text",
        "position_increment_gap": 100
      }
    }
  }
}
```

### IndexOrDocValuesQuery Optimization

For keyword fields with both `index: true` and `doc_values: true`, OpenSearch can use `IndexOrDocValuesQuery` to choose the most efficient execution path based on the query characteristics.

## Limitations

- Fuzzy queries can be resource-intensive for large edit distances
- `match_phrase_prefix` with `index_prefixes` requires proper `position_increment_gap` handling for multi-value fields
- Expensive queries (fuzzy, prefix, wildcard, regexp) can be disabled via `search.allow_expensive_queries` setting

## Change History

- **v2.16.0** (2024-08-06): Fixed `match_phrase_prefix` query not working on text fields with multiple values and `index_prefixes` enabled; Fixed `FuzzyQuery` on keyword fields to use `IndexOrDocValuesQuery` when both index and doc_values are true

## References

### Documentation
- [Query DSL](https://docs.opensearch.org/latest/query-dsl/)
- [Fuzzy Query](https://docs.opensearch.org/latest/query-dsl/term/fuzzy/)
- [Match Phrase Prefix Query](https://docs.opensearch.org/latest/query-dsl/full-text/match-phrase-prefix/)

### Pull Requests
| Version | PR | Description |
|---------|-----|-------------|
| v2.16.0 | [#10959](https://github.com/opensearch-project/OpenSearch/pull/10959) | Fix match_phrase_prefix_query not working on text field with multiple values and index_prefixes |
| v2.16.0 | [#14378](https://github.com/opensearch-project/OpenSearch/pull/14378) | Fix FuzzyQuery in keyword field will use IndexOrDocValuesQuery when both of index and doc_value are true |
