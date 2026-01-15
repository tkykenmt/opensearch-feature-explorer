---
tags:
  - opensearch
---
# Lucene Upgrade

## Summary

OpenSearch v2.16.0 upgrades Apache Lucene from 9.11.0-snapshot to the stable 9.11.0 release. This upgrade brings production-ready stability and includes all features and optimizations from the Lucene 9.11.0 release.

## Details

### What's New in v2.16.0

This release updates the Lucene dependency from a snapshot version (9.11.0-snapshot-4be6531) to the official stable release (9.11.0).

### Lucene 9.11.0 Highlights

| Feature | Description |
|---------|-------------|
| posix_madvise support | MMapDirectory uses IOContext to pass MADV flags to the kernel on Linux/macOS with Java 21+, improving paging logic for large indexes under memory pressure |
| 4-bit HNSW vectors | Support for 4-bit vectors with optional 50% memory reduction through compression |
| Intra-merge parallelism | MergeScheduler can provide an executor for parallel merging via ConcurrentMergeScheduler |
| RWLock for LRUQueryCache | Reduced contention using read-write locks instead of synchronized access |
| MemorySegment Vector scorer | Scoring without copying on-heap, improving search latency by ~2x for byte vectors |
| Primitive collections | Optimized primitive collections for better performance and heap utilization |
| Recursive graph bisection | Now supported on indexes with blocks |
| ICU4J upgrade | Updated to version 74.2 |

### Technical Changes

The PR updates the following Lucene modules:
- lucene-core
- lucene-analysis-common
- lucene-analysis-icu
- lucene-analysis-kuromoji
- lucene-analysis-nori
- lucene-analysis-phonetic
- lucene-analysis-smartcn
- lucene-analysis-stempel
- lucene-analysis-morfologik
- lucene-backward-codecs
- lucene-expressions
- lucene-grouping
- lucene-highlighter

## Limitations

- No breaking changes from the snapshot version
- Index format remains compatible within the 9.x series

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14042](https://github.com/opensearch-project/OpenSearch/pull/14042) | Update to Apache Lucene 9.11.0 | N/A |

### Documentation
- [Lucene 9.11.0 Release Notes](https://lucene.apache.org/core/9_11_0/changes/Changes.html)
- [Lucene 9.11.1 Release Notes](https://cwiki.apache.org/confluence/display/LUCENE/ReleaseNote9_11_1) (patch release)
