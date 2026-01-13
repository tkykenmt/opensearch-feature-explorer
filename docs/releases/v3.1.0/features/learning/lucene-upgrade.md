---
tags:
  - domain/search
  - component/server
  - ml
  - search
---
# Lucene Upgrade

## Summary

The opensearch-learning-to-rank-base plugin was updated to be compatible with Lucene 10.2.1 in OpenSearch 3.1.0. This bugfix addresses the breaking change where `DisiPriorityQueue` became an abstract class, preventing direct instantiation.

## Details

### What's New in v3.1.0

The Lucene 10.2.1 upgrade changed `DisiPriorityQueue` from a concrete class to an abstract class, requiring the use of a factory method for instantiation.

### Technical Changes

#### API Migration

| Lucene Class | Before (10.1.0) | After (10.2.1) |
|--------------|-----------------|----------------|
| `DisiPriorityQueue` | `new DisiPriorityQueue(size)` | `DisiPriorityQueue.ofMaxSize(size)` |

#### Modified Components

| Component | File | Changes |
|-----------|------|---------|
| `RankerQuery` | `RankerQuery.java` | Updated DisiPriorityQueue initialization |

#### Code Changes

```java
// RankerQuery.java - Before
DisiPriorityQueue disiPriorityQueue = new DisiPriorityQueue(weights.size());

// RankerQuery.java - After
DisiPriorityQueue disiPriorityQueue = DisiPriorityQueue.ofMaxSize(weights.size());
```

### Migration Notes

This is an internal plugin update. No user action is required. The Learning to Rank functionality remains unchanged from a user perspective.

## Limitations

- This update only addresses Lucene API compatibility; no new features are added

## References

### Documentation
- [Apache Lucene 10.2.1 Changes](https://lucene.apache.org/core/10_2_1/changes/Changes.html)

### Pull Requests
| PR | Description |
|----|-------------|
| [#186](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/186) | Lucene 10.2 upgrade changes |

### Issues (Design / RFC)
- [Issue #184](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/184): Unable to build/run due to DisiPriorityQueue being abstract

## Related Feature Report

- [Full feature documentation](../../../../features/learning/learning-to-rank.md)
