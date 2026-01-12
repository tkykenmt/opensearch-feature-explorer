---
tags:
  - neural-search
  - search
---

# Query & Aggregation Fixes

## Summary

OpenSearch v3.0.0 includes several important bug fixes for query and aggregation functionality. These fixes address issues with terms aggregation missing buckets, explain action failures on query rewrite, FunctionScoreQueryBuilder inner query processing, wildcard field queries, flat_object exists queries, match_only_text highlighting, and PIT creation exceptions.

## Details

### What's New in v3.0.0

This release resolves multiple query and aggregation bugs that affected search reliability and correctness.

### Technical Changes

#### Terms Aggregation Missing Bucket Fix

Fixed a regression where terms aggregation with a `missing` value parameter failed to create a bucket for documents without the specified field.

**Before fix:**
```json
{
  "aggregations": {
    "nick": {
      "buckets": [
        { "key": "daenerys", "doc_count": 1 },
        { "key": "stormborn", "doc_count": 1 }
      ]
    }
  }
}
```

**After fix:**
```json
{
  "aggregations": {
    "nick": {
      "buckets": [
        { "key": "no_nickname", "doc_count": 6 },
        { "key": "daenerys", "doc_count": 1 },
        { "key": "stormborn", "doc_count": 1 }
      ]
    }
  }
}
```

#### Explain Action Query Rewrite Fix

Fixed an exception when calling explain API in "by_doc_id" mode with queries that use async rewrite (like NeuralQueryBuilder or TermsQueryBuilder). The fix moves query rewrite to the coordinator in `TransportExplainAction`.

**Error before fix:**
```json
{
  "error": {
    "type": "query_shard_exception",
    "reason": "failed to create query: async actions are left after rewrite"
  }
}
```

#### FunctionScoreQueryBuilder Inner Query Visit Fix

Implemented the `visit` method in `FunctionScoreQueryBuilder` to allow subqueries to be processed properly. This enables features like `default_model_id` in neural query enricher pipelines to work correctly with function_score queries.

#### Wildcard Field Query Fixes

Fixed multiple issues with wildcard field type queries:
- Case insensitive regexp queries now return expected results
- Escaped characters in queries are handled correctly
- Null pointer exception on plain text regex queries resolved
- Term queries with special characters (like `*`) now perform exact match

#### Flat Object Exists Query Fix

Fixed `string_index_out_of_bounds_exception` when running exists queries on nested flat_object fields. The issue occurred when querying the parent object field containing a flat_object subfield.

**Example that now works:**
```json
{
  "query": {
    "exists": {
      "field": "foo"
    }
  }
}
```

#### Match Only Text Highlighting

Added highlighting support for wildcard search on `match_only_text` field type. Previously, highlighting was unavailable after changing field types from `text` to `match_only_text`.

#### PIT Creation Exception Fix

Fixed `IllegalArgumentException: No enum constant org.opensearch.action.search.SearchPhaseName.CREATE_PIT` thrown when creating a Point in Time (PIT). The fix adds a try-catch block in `SearchRequestStats` to gracefully handle search phases not tracked by the stats system.

### Usage Example

**Terms aggregation with missing value:**
```json
POST /index/_search
{
  "size": 0,
  "aggs": {
    "field_values": {
      "terms": {
        "field": "nickname",
        "missing": "no_value",
        "size": 10
      }
    }
  }
}
```

**Wildcard field with case insensitive regexp:**
```json
POST /index/_search
{
  "query": {
    "regexp": {
      "wildcard_field": {
        "value": "TtAa",
        "case_insensitive": true
      }
    }
  }
}
```

## Limitations

- The wildcard field type still has known performance characteristics compared to keyword fields for exact match queries
- Match_only_text highlighting uses plain highlighter since positions are not stored

## References

### Documentation
- [Terms Aggregation Documentation](https://docs.opensearch.org/3.0/aggregations/bucket/terms/)
- [Wildcard Field Type Documentation](https://docs.opensearch.org/3.0/field-types/supported-field-types/wildcard/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#17418](https://github.com/opensearch-project/OpenSearch/pull/17418) | Fix missing bucket in terms aggregation with missing value |
| [#17286](https://github.com/opensearch-project/OpenSearch/pull/17286) | Fix explain action on query rewrite |
| [#16776](https://github.com/opensearch-project/OpenSearch/pull/16776) | Fix visit of inner query for FunctionScoreQueryBuilder |
| [#16827](https://github.com/opensearch-project/OpenSearch/pull/16827) | Fix case insensitive and escaped query on wildcard |
| [#16803](https://github.com/opensearch-project/OpenSearch/pull/16803) | Fix exists queries on nested flat_object fields throws exception |
| [#17101](https://github.com/opensearch-project/OpenSearch/pull/17101) | Add highlighting for match_only_text field |
| [#16781](https://github.com/opensearch-project/OpenSearch/pull/16781) | Fix illegal argument exception when creating a PIT |

### Issues (Design / RFC)
- [Issue #17391](https://github.com/opensearch-project/OpenSearch/issues/17391): Missing bucket in terms aggregation
- [Issue #16795](https://github.com/opensearch-project/OpenSearch/issues/16795): Exists queries on nested flat_object fields
- [Issue #16754](https://github.com/opensearch-project/OpenSearch/issues/16754): Term query on wildcard field
- [Issue #16750](https://github.com/opensearch-project/OpenSearch/issues/16750): PIT creation exception
- [Issue #15403](https://github.com/opensearch-project/OpenSearch/issues/15403): FunctionScoreQueryBuilder default_model_id

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/query-and-aggregation-fixes.md)
