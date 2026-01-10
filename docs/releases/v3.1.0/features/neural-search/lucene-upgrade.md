# Lucene Upgrade

## Summary

The neural-search plugin was updated to be compatible with Lucene 10.2.1 in OpenSearch 3.1.0. This bugfix addresses breaking API changes in Lucene's `DisiPriorityQueue`, `DisjunctionDISIApproximation`, and `DocIdStream` classes that prevented the plugin from building and running.

## Details

### What's New in v3.1.0

The Lucene 10.2.1 upgrade introduced breaking API changes that required updates to the neural-search plugin's hybrid query implementation:

- **DisiPriorityQueue**: Changed from direct instantiation to factory method
- **DisjunctionDISIApproximation**: Constructor signature changed to require Collection and cost parameter
- **DocIdStream**: New abstract method `mayHaveRemaining()` and updated `forEach()` signature

### Technical Changes

#### API Migration

| Lucene Class | Before (10.1.0) | After (10.2.1) |
|--------------|-----------------|----------------|
| `DisiPriorityQueue` | `new DisiPriorityQueue(size)` | `DisiPriorityQueue.ofMaxSize(size)` |
| `DisjunctionDISIApproximation` | `new DisjunctionDISIApproximation(DisiPriorityQueue)` | `new DisjunctionDISIApproximation(Collection, long)` |
| `DocIdStream.forEach()` | `forEach(CheckedIntConsumer)` | `forEach(int upTo, CheckedIntConsumer)` |

#### Modified Components

| Component | File | Changes |
|-----------|------|---------|
| `HybridQueryScorer` | `HybridQueryScorer.java` | Updated DisiPriorityQueue initialization and DisjunctionDISIApproximation construction |
| `HybridQueryDocIdStream` | `HybridQueryDocIdStream.java` | Implemented `mayHaveRemaining()`, `count()`, updated `forEach()` signature |
| `HybridBulkScorer` | `HybridBulkScorer.java` | Added getter for `maxDoc` field |

#### Code Changes

```java
// HybridQueryScorer - Before
DisiPriorityQueue subScorersPQ = new DisiPriorityQueue(numSubqueries);
this.approximation = new HybridSubqueriesDISIApproximation(this.subScorersPQ);

// HybridQueryScorer - After
List<HybridDisiWrapper> hybridDisiWrappers = initializeSubScorersList();
this.subScorersPQ = DisiPriorityQueue.ofMaxSize(numSubqueries);
this.subScorersPQ.addAll(hybridDisiWrappers.toArray(new DisiWrapper[0]), 0, hybridDisiWrappers.size());
this.approximation = new HybridSubqueriesDISIApproximation(hybridDisiWrappers, subScorersPQ);
```

```java
// HybridQueryDocIdStream - New methods
@Override
public boolean mayHaveRemaining() {
    return this.upTo + 1 < hybridBulkScorer.getMaxDoc();
}

@Override
public int count(int upTo) throws IOException {
    int[] count = new int[1];
    forEach(upTo, (doc -> count[0]++));
    return count[0];
}
```

### Migration Notes

This is an internal plugin update. No user action is required. The hybrid query functionality remains unchanged from a user perspective.

## Limitations

- This update only addresses Lucene API compatibility; no new features are added
- The `hybridScores()` method was removed from `HybridQueryScorer` as part of the refactoring

## Related PRs

| PR | Description |
|----|-------------|
| [#1336](https://github.com/opensearch-project/neural-search/pull/1336) | Update Lucene dependencies |

## References

- [Issue #1334](https://github.com/opensearch-project/neural-search/issues/1334): Cannot gradle run the neural search repo
- [Issue #1338](https://github.com/opensearch-project/neural-search/issues/1338): Integration test failures
- [Apache Lucene 10.2.1 Changes](https://lucene.apache.org/core/10_2_1/changes/Changes.html)

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/lucene-upgrade.md)
