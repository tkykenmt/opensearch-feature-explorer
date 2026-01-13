---
tags:
  - opensearch
---
# Inner Hits Optimization

## Summary

OpenSearch 2.19.0 introduces performance optimizations for inner hits queries used with nested documents. The optimization reduces redundant TermQuery executions by leveraging BitSet caching and direct ObjectMapper lookup for nested inner hit contexts.

## Details

### What's New in v2.19.0

Inner hits queries on nested documents previously suffered from inefficient query execution patterns. The optimization addresses two key areas:

1. **Fast ObjectMapper Lookup**: When the search context is a `NestedInnerHitSubContext`, the system now directly retrieves the `ObjectMapper` instead of iterating through all object mappers and executing TermQuery filters for each.

2. **BitSet Caching for Child Filters**: Child filters (simple TermQueries) are now cached using `bitsetFilterCache`, eliminating redundant query executions during nested identity resolution.

### Technical Changes

| Component | Change |
|-----------|--------|
| `DocumentMapper.findNestedObjectMapper()` | Added fast path for `NestedInnerHitSubContext` to directly return the child ObjectMapper |
| `DocumentMapper.containSubDocIdWithObjectMapper()` | New method using BitSet from `bitsetFilterCache` instead of Weight/Scorer |
| `FetchPhase.getInternalNestedIdentity()` | Replaced Weight/Scorer iteration with BitSet lookup via `bitsetFilterCache` |
| `NestedQueryBuilder.NestedInnerHitSubContext` | Made public and added `getChildObjectMapper()` accessor |

### Performance Impact

The optimization significantly reduces query latency for searches with `inner_hits` on nested documents, particularly when:
- Documents contain many nested objects
- Multiple inner hits are returned per parent document
- The `_source` field is large

In production environments with 80+ nested sub-documents per parent, fetch phase times improved from 3+ seconds to under 1 second.

## Limitations

- The optimization is specific to nested document inner hits; parent-child join inner hits are not affected
- Performance gains are most noticeable with high nested document counts

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16937](https://github.com/opensearch-project/OpenSearch/pull/16937) | Optimize innerhits query performance | [#16878](https://github.com/opensearch-project/OpenSearch/issues/16878) |

### Documentation
- [Inner Hits](https://docs.opensearch.org/2.19/search-plugins/searching-data/inner-hits/)
- [Nested Query](https://docs.opensearch.org/2.19/query-dsl/joining/nested/)
