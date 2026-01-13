---
tags:
  - domain/core
  - component/server
  - indexing
  - performance
  - search
---
# Segment Concurrent Search Optimization

## Summary

This release optimizes the segment grouping algorithm for concurrent segment search, improving load balancing across search slices. The new algorithm ensures documents are distributed more evenly across groups, reducing the maximum-minimum document difference between slices and improving search latency for parallel segment searches.

## Details

### What's New in v3.2.0

The segment concurrent search feature now uses an optimized grouping algorithm that replaces the previous round-robin distribution approach with a priority queue-based algorithm that balances document counts across slices.

### Technical Changes

#### Algorithm Change

The previous round-robin approach could lead to significant imbalance in document counts across groups. For example, with segments containing [10, 8, 7, 6, 5, 4] documents and a slice size of 4:

**Previous (Round-Robin) Grouping:**
- group0: 10, 5 (15 docs)
- group1: 8, 4 (12 docs)
- group2: 7 (7 docs)
- group3: 6 (6 docs)
- Max-min difference: 9 documents

**New (Optimized) Grouping:**
- group0: 10 (10 docs)
- group1: 8 (8 docs)
- group2: 7, 4 (11 docs)
- group3: 6, 5 (11 docs)
- Max-min difference: 3 documents

#### Implementation Details

The `MaxTargetSliceSupplier` class now uses a `PriorityQueue` to track the document count sum for each group:

```java
PriorityQueue<Group> groupQueue = new PriorityQueue<>();
for (int i = 0; i < targetSliceCount; i++) {
    groupQueue.offer(new Group(i));
}

for (int i = 0; i < sortedLeaves.size(); ++i) {
    Group minGroup = groupQueue.poll();
    groupedLeaves.get(minGroup.index).add(
        IndexSearcher.LeafReaderContextPartition.createForEntireSegment(sortedLeaves.get(i))
    );
    minGroup.sum += sortedLeaves.get(i).reader().maxDoc();
    groupQueue.offer(minGroup);
}
```

The algorithm:
1. Sorts segments by document count in descending order
2. Maintains a priority queue of groups ordered by total document count
3. Assigns each segment to the group with the smallest current document sum
4. Updates the group's sum and reinserts into the priority queue

#### New Components

| Component | Description |
|-----------|-------------|
| `Group` | Inner class tracking group index and document sum, implementing `Comparable` for priority queue ordering |

### Usage Example

Concurrent segment search is enabled at the cluster or index level:

```json
PUT _cluster/settings
{
   "persistent": {
      "search.concurrent_segment_search.mode": "all"
   }
}
```

The optimization is applied automatically when concurrent segment search is enabled. No additional configuration is required.

### Performance Impact

The optimized grouping algorithm provides:
- More balanced workload distribution across search threads
- Reduced tail latency for concurrent segment searches
- Better resource utilization when segments have varying document counts

## Limitations

- The optimization is most effective when segments have significantly different document counts
- For segments with similar document counts, the improvement may be minimal

## References

### Documentation
- [Concurrent Segment Search Documentation](https://docs.opensearch.org/3.0/search-plugins/concurrent-segment-search/): Official documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#18451](https://github.com/opensearch-project/OpenSearch/pull/18451) | Optimize grouping for segment concurrent search by ensuring that documents within each group are as equal as possible |

### Issues (Design / RFC)
- [Issue #7358](https://github.com/opensearch-project/OpenSearch/issues/7358): Original issue discussing slice computation mechanisms

## Related Feature Report

- Full feature documentation
