---
tags:
  - indexing
  - ml
  - neural-search
  - search
---

# Neural Search Bug Fixes

## Summary

OpenSearch v3.1.0 includes seven bug fixes for the Neural Search plugin, addressing issues across hybrid queries, neural queries with semantic fields, radial search in multi-node clusters, Stats API validation, and internal stability improvements. These fixes improve reliability and correctness for neural search operations.

## Details

### What's New in v3.1.0

This release addresses multiple bug categories in the Neural Search plugin:

1. **Hybrid Query Validation** - Prevents invalid nested hybrid queries
2. **Neural Query with Semantic Fields** - Fixes validation, model inference, and analyzer handling
3. **Radial Search Serialization** - Fixes multi-node cluster compatibility
4. **Stats API Improvements** - Better error handling and BWC compatibility
5. **Stack Overflow Prevention** - Uses iterative approach for semantic field collection
6. **Score Handling** - Fixes null score values for single shard sorting

### Technical Changes

#### Hybrid Query Nesting Validation

Previously, hybrid queries could be nested within other hybrid queries, leading to undefined behavior. The fix adds validation during query parsing to reject nested hybrid queries with a clear error message.

```json
// This invalid query now returns an error
{
  "query": {
    "hybrid": {
      "queries": [
        {
          "hybrid": {  // ERROR: hybrid query cannot be nested
            "queries": [...]
          }
        }
      ]
    }
  }
}
```

Error response:
```
hybrid query cannot be nested in another hybrid query
```

#### Neural Query with Semantic Field Fixes

Five issues were addressed in neural query handling with semantic fields:

| Issue | Description | Fix |
|-------|-------------|-----|
| Missing validation | Validation bypassed when semantic field info available | Ensure validation runs regardless of rewrite path |
| Incorrect model inference | Search analyzer in semantic field triggered model inference | Check semantic field settings for analyzer |
| Token source precedence | Confusing priority between query and field settings | Clear precedence: query settings override field settings |
| Incorrect analyzer | Null analyzer used when only defined in semantic field | Use semantic field analyzer when query doesn't specify one |
| Incorrect tests | Tests verified against wrong analyzer | Fixed tests to verify against correct analyzer |

#### Radial Search Multi-Node Fix

Neural radial search queries with `min_score` or `max_distance` failed in multi-node clusters with the error:
```
[knn] requires exactly one of k, distance or score to be set
```

The fix delegates serialization/deserialization to the k-NN plugin, avoiding version checking conflicts between neural-search and k-NN plugins.

#### Stats API Improvements

Two fixes improve the Stats API:

1. **Invalid stat name handling**: Returns 400 Bad Request with helpful suggestions instead of silently logging
```json
GET /_plugins/_neural/stats/text_embedding
{
  "error": {
    "type": "illegal_argument_exception",
    "reason": "request contains unrecognized stat: [text_embedding] -> did you mean [text_embedding_executions]?"
  },
  "status": 400
}
```

2. **BWC compatibility**: Filters stats based on minimum cluster version during rolling upgrades to prevent enum ordinal reading errors

#### Stack Overflow Prevention

Changed semantic field collection from recursive to iterative approach using a stack data structure, preventing stack overflow errors with deeply nested field structures.

#### Single Shard Score Fix

Fixed score values showing as `null` for single shard indices when sorting by non-score fields. The fix aligns behavior with standard OpenSearch, returning `null` for `_score` when sort field is not score.

## Limitations

- Multi-node integration tests for radial search require manual verification (automated multi-node test CI in progress)
- Stats API BWC fix is a workaround; full fix requires OpenSearch core changes for enum reading

## References

### Documentation
- [Neural Search Documentation](https://docs.opensearch.org/3.0/vector-search/ai-search/neural-sparse-search/)
- [Neural Query DSL](https://docs.opensearch.org/3.0/query-dsl/specialized/neural/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#1277](https://github.com/opensearch-project/neural-search/pull/1277) | Fix score value as null for single shard when sorting |
| [#1291](https://github.com/opensearch-project/neural-search/pull/1291) | Return bad request for invalid stat parameters in stats API |
| [#1305](https://github.com/opensearch-project/neural-search/pull/1305) | Add validation for invalid nested hybrid query |
| [#1357](https://github.com/opensearch-project/neural-search/pull/1357) | Use stack to collect semantic fields to avoid stack overflow |
| [#1373](https://github.com/opensearch-project/neural-search/pull/1373) | Filter requested stats based on minimum cluster version |
| [#1393](https://github.com/opensearch-project/neural-search/pull/1393) | Fix neural radial search serialization in multi-node clusters |
| [#1396](https://github.com/opensearch-project/neural-search/pull/1396) | Fix bugs for neural query with semantic field using sparse model |

### Issues (Design / RFC)
- [Issue #1108](https://github.com/opensearch-project/neural-search/issues/1108): Nested hybrid query bug report
- [Issue #1274](https://github.com/opensearch-project/neural-search/issues/1274): Hybrid search with sort corrupts scores
- [Issue #1368](https://github.com/opensearch-project/neural-search/issues/1368): Stats BWC test failure
- [Issue #1392](https://github.com/opensearch-project/neural-search/issues/1392): Neural query with min_score/max_distance fails on 3.0

## Related Feature Report

- [Full feature documentation](../../../features/neural-search/neural-search-bug-fixes.md)
