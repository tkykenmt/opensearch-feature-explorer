---
tags:
  - k-nn
---
# k-NN Vector Streaming & Memory Bug Fixes

## Summary

OpenSearch 2.16.0 includes several critical bug fixes for the k-NN plugin addressing vector streaming arithmetic, segment replication compatibility, memory management, and nested field file matching issues.

## Details

### What's New in v2.16.0

This release addresses four bug fixes that improve k-NN plugin stability and correctness:

#### 1. Vector Streaming Arithmetic Fix
Fixed incorrect arithmetic when calculating the number of vectors to stream from Java to JNI layer. The calculation error could affect vector data transfer during index operations.

#### 2. Segment Replication LeafReader Casting Fix
Fixed `ClassCastException` when searching on replicas with segment replication enabled and deleted documents present. The issue occurred because:
- Segment replication opens IndexReaders via directory path (not IndexWriter)
- Soft deletes handling wraps SegmentReader in `SoftDeletesFilterCodecReader` or `SoftDeletesFilterLeafReader`
- The k-NN plugin incorrectly cast these wrapped readers directly to `SegmentReader`

The fix properly unwraps readers through `FilterLeafReader` and `FilterCodecReader` layers using OpenSearch Core helper functions.

#### 3. Memory Release for Array Types
Fixed improper memory deallocation for array types in native code. Changed `delete` to `delete[]` for `heap_group_ids` array allocation. While no immediate user impact existed (single query execution path), this follows C++ best practices for array memory management.

#### 4. Nested Field File Suffix Matching Fix
Fixed a bug where nested k-NN fields with similar suffixes caused incorrect index file selection, resulting in zero recall. For example, with fields:
- `MultipleMatrix.Vector` → `_3_2011_MultipleMatrix.Vector.hnsw`
- `PersonMultipleMatrix.Vector` → `_3_2011_PersonMultipleMatrix.Vector.hnsw`

The filter `.endsWith(engineSuffix)` incorrectly matched both files when searching `MultipleMatrix.Vector`. The fix uses underscore prefix (`_MultipleMatrix.Vector.hnsw`) to distinguish field boundaries.

### Technical Changes

| Component | Change |
|-----------|--------|
| `KNNWeight.java` | Proper LeafReader unwrapping for segment replication |
| JNI Layer | Corrected vector count arithmetic for streaming |
| Native Memory | Use `delete[]` for array type deallocation |
| File Matching | Underscore-prefixed suffix matching for nested fields |

## Limitations

- Segment replication fix requires proper unwrapping through multiple reader wrapper layers
- The nested field fix changes file matching behavior; existing indices are unaffected

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1804](https://github.com/opensearch-project/k-NN/pull/1804) | Fix vector streaming count arithmetic | - |
| [#1808](https://github.com/opensearch-project/k-NN/pull/1808) | Fix LeafReader casting for segment replication | [#1807](https://github.com/opensearch-project/k-NN/issues/1807) |
| [#1820](https://github.com/opensearch-project/k-NN/pull/1820) | Fix memory release for array types | - |
| [#1802](https://github.com/opensearch-project/k-NN/pull/1802) | Fix nested field suffix matching | [#1803](https://github.com/opensearch-project/k-NN/issues/1803) |

### Issues
- [#1803](https://github.com/opensearch-project/k-NN/issues/1803): Same suffix causes recall drop to zero
- [#1807](https://github.com/opensearch-project/k-NN/issues/1807): k-NN queries fail with segment replication and deleted docs
