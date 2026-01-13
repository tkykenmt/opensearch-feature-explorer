---
tags:
  - domain/core
  - component/server
  - indexing
  - k-nn
  - performance
  - search
---
# Lucene Upgrade

## Summary

OpenSearch 3.1.0 upgrades Apache Lucene from 10.1.0 to 10.2.1, bringing bug fixes, performance optimizations, and new features for vector search. This upgrade includes API changes that required updates across multiple OpenSearch repositories.

## Details

### What's New in v3.1.0

The Lucene 10.2.1 upgrade introduces:

- **Bug fixes**: Fixes for DISIDocIdStream, TermOrdValComparator, and lead cost computations
- **New features**: SeededKnnVectorQuery, binary quantized vector codecs, TopDocs#rrf for Reciprocal Rank Fusion
- **API changes**: DocIdSetIterator#intoBitSet, Bits#applyMask, DocIdSetIterator#docIDRunEnd
- **Performance**: Dense conjunction speedups, postings encoded as bit sets

### Technical Changes

#### API Changes

| API | Change Type | Description |
|-----|-------------|-------------|
| `DisiPriorityQueue` | Constructor change | Use `DisiPriorityQueue.ofMaxSize(int)` instead of constructor |
| `TopScoreDocCollectorManager` | Deprecated constructor | Use new constructor without deprecated parameters |
| `DocIdSetIterator#intoBitSet` | New method | Convert iterator to bit set |
| `Bits#applyMask` | New method | Apply mask to bits |
| `DocIdSetIterator#docIDRunEnd` | New method | Get end of document ID run |

#### New Vector Search Features

| Feature | Description |
|---------|-------------|
| `SeededKnnVectorQuery` | KNN query with seeding for improved recall |
| Binary quantized vector codecs | Efficient storage for quantized vectors |
| `TopDocs#rrf` | Reciprocal Rank Fusion for combining search results |

### Migration Notes

Code using Lucene APIs directly may need updates:

```java
// Before (Lucene 10.1.0)
DisiPriorityQueue queue = new DisiPriorityQueue(size);

// After (Lucene 10.2.1)
DisiPriorityQueue queue = DisiPriorityQueue.ofMaxSize(size);
```

## Limitations

- Plugins using Lucene APIs directly must be updated for compatibility
- Index format remains compatible; no reindexing required

## References

### Documentation
- [Apache Lucene 10.2.1 Release Notes](https://lucene.apache.org/core/10_2_1/changes/Changes.html)
- [Apache Lucene 10.2.0 Release Notes](https://lucene.apache.org/core/10_2_0/changes/Changes.html)

### Pull Requests
| Repository | PR | Description | Related Issue |
|------------|-----|-------------|---------------|
| OpenSearch | [#17961](https://github.com/opensearch-project/OpenSearch/pull/17961) | Core Lucene upgrade to 10.2.1 |   |
| OpenSearch | [#18395](https://github.com/opensearch-project/OpenSearch/pull/18395) | Replace deprecated TopScoreDocCollectorManager construction | [#18394](https://github.com/opensearch-project/OpenSearch/issues/18394) |
| neural-search | [#1336](https://github.com/opensearch-project/neural-search/pull/1336) | Update Lucene dependencies |   |
| opensearch-learning-to-rank-base | [#186](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/186) | Lucene 10.2 upgrade changes |   |

### Issues (Design / RFC)
- [Issue #184](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/184): Learning to Rank compatibility issue

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/opensearch-lucene-upgrade.md)
