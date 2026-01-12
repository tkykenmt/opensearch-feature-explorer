# Concurrent Segment Search

## Summary

This release fixes an assertion error that occurred when using field collapsing with concurrent segment search enabled. The bug caused inconsistent search results and could crash nodes when collapsing search results across multiple segments searched in parallel.

## Details

### What's New in v3.3.0

This release addresses a critical bug where the `shardIndex` was being set twice during field collapsing operations with concurrent segment search enabled, causing an assertion error and inconsistent results.

### Technical Changes

#### Root Cause

When concurrent segment search is enabled, segments are searched in parallel and results are merged. The `CollapseTopFieldDocs.merge()` method had a `setShardIndex` parameter that would set the shard index on score documents during the merge. However, when concurrent segment search was enabled, the shard index was already being set in the query phase (`TopDocsCollectorContext`), causing a double-set that triggered an assertion error:

```
java.lang.AssertionError: shardIndex is already set
    at org.opensearch.action.search.SearchPhaseController.setShardIndex
```

#### Fix Implementation

The fix removes the `setShardIndex` parameter from `CollapseTopFieldDocs.merge()`, aligning it with the Lucene 9.0.0 change that removed this capability from `TopDocs.merge()`. The key changes include:

1. **Removed `setShardIndex` parameter**: The merge method no longer accepts or uses this parameter
2. **Updated tie-breaking logic**: Uses a default comparator that handles both set and unset shard indices
3. **Added consistency validation**: Throws `IllegalArgumentException` if shard indices are inconsistent across documents

#### Modified Components

| Component | Change |
|-----------|--------|
| `CollapseTopFieldDocs.java` | Removed `setShardIndex` parameter, added default tie-breaker comparators |
| `SearchPhaseController.java` | Updated merge call to remove `setShardIndex` argument |
| `TopDocsCollectorContext.java` | Updated merge call to remove `setShardIndex` argument |

#### New Tie-Breaking Logic

```java
private static final Comparator<ScoreDoc> SHARD_INDEX_TIE_BREAKER = 
    Comparator.comparingInt(d -> d.shardIndex);
private static final Comparator<ScoreDoc> DOC_ID_TIE_BREAKER = 
    Comparator.comparingInt(d -> d.doc);
private static final Comparator<ScoreDoc> DEFAULT_TIE_BREAKER = 
    SHARD_INDEX_TIE_BREAKER.thenComparing(DOC_ID_TIE_BREAKER);
```

### Usage Example

Field collapsing with concurrent segment search now works correctly:

```json
PUT test_index/_settings
{
    "index.search.concurrent_segment_search.mode": "all"
}

GET test_index/_search
{
  "collapse": {
    "field": "category"
  },
  "sort": [{ "timestamp": "desc" }]
}
```

### Migration Notes

No migration required. This is a bug fix that makes field collapsing work correctly with concurrent segment search. Users who previously disabled concurrent segment search to work around this issue can now re-enable it.

## Limitations

- The fix ensures consistent behavior between concurrent and non-concurrent search paths
- When documents have the same sort value, tie-breaking uses shard index first, then document ID

## References

### Documentation
- [Concurrent Segment Search Documentation](https://docs.opensearch.org/3.0/search-plugins/concurrent-segment-search/): Official documentation
- [Lucene PR #757](https://github.com/apache/lucene-solr/pull/757): Original Lucene change that removed setShardIndex from TopDocs.merge()

### Pull Requests
| PR | Description |
|----|-------------|
| [#19053](https://github.com/opensearch-project/OpenSearch/pull/19053) | Remove the setShardIndex parameter in CollapseTopFieldDocs.merge() |

### Issues (Design / RFC)
- [Issue #19051](https://github.com/opensearch-project/OpenSearch/issues/19051): Collapsing search results with concurrent segment search enabled triggers assertion error
- [Issue #19111](https://github.com/opensearch-project/OpenSearch/issues/19111): Inconsistent field collapsing search results with concurrent segment search

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/concurrent-segment-search.md)
