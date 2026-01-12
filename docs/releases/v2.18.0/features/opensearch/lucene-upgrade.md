---
tags:
  - indexing
  - performance
  - search
---

# Lucene 9.12.0 Upgrade

## Summary

OpenSearch v2.18.0 upgrades the underlying Apache Lucene library from 9.11.1 to 9.12.0. This upgrade brings significant performance improvements, new features, and optimizations to the search engine core, including a new default postings format with improved skip data handling, JDK 23 support for Panama Vectorization, and various query and indexing optimizations.

## Details

### What's New in v2.18.0

The Lucene 9.12.0 upgrade introduces several key improvements:

- **New Lucene912PostingsFormat**: The default postings format now uses only 2 levels of skip data inlined into postings, improving performance for queries that need skipping such as conjunctions
- **JDK 23 Support**: Panama Vectorization Provider now supports JDK 23
- **Dynamic Range Facets**: New faceting feature that automatically picks balanced numeric ranges based on value distribution
- **Search Concurrency Configuration**: TieredMergePolicy and LogMergePolicy now support configurable search concurrency
- **Memory Optimizations**: Reduced memory allocations and improved heap usage for HNSW and scalar quantized vector writers

### Technical Changes

#### Version Update

| Component | Previous | New |
|-----------|----------|-----|
| Apache Lucene | 9.11.1 | 9.12.0 |

#### Key Improvements from Lucene 9.12.0

**Performance Optimizations:**
- Lucene912PostingsFormat with 2-level skip data inlined into postings for faster conjunction queries
- OnHeapHnswGraph no longer allocates a lock for every graph node
- Optimized decoding logic for blocks of postings
- Improved NumericComparator competitive iterator logic
- Max WAND optimizations with ToParentBlockJoinQuery when using ScoreMode.Max

**New API Features:**
- `TermInSetQuery#getBytesRefIterator` for iterating over query terms
- `FlatVectorsFormat` exposed as a first-class format configurable via custom Codec
- `IndexSearcher#searchLeaf` protected method for customizing per-leaf search behavior
- `BitSet#nextSetBit(int, int)` for getting first set bit in range
- `DrillSideways#search` method supporting any CollectorManagers

**Memory and Arena Improvements:**
- Shared Arena grouping for files from the same segment to reduce performance degradation when closing many index files
- Configurable `sharedArenaMaxPermits` system property for controlling mmapped file associations

### Usage Example

No configuration changes are required. The upgrade is transparent to users. The new postings format is automatically used for new segments.

To verify the Lucene version:

```bash
GET /_nodes?filter_path=nodes.*.version,nodes.*.build_hash
```

### Migration Notes

- This is a transparent upgrade with no breaking changes
- Existing indices remain compatible
- New segments will automatically use Lucene912PostingsFormat
- No reindexing required

## Limitations

- The new postings format optimizations primarily benefit conjunction queries
- JDK 23 Panama Vectorization requires running on JDK 23 or later

## References

### Documentation
- [Lucene 9.12.0 Changelog](https://lucene.apache.org/core/9_12_0/changes/Changes.html): Official release notes
- [OpenSearch PR #15333](https://github.com/opensearch-project/OpenSearch/pull/15333): Main implementation PR

### Pull Requests
| PR | Description |
|----|-------------|
| [#15333](https://github.com/opensearch-project/OpenSearch/pull/15333) | Update Apache Lucene to 9.12.0 |

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/opensearch-lucene-upgrade.md)
