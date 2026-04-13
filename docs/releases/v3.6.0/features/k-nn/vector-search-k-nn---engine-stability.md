---
tags:
  - k-nn
---
# Vector Search (k-NN) - Engine Stability

## Summary

OpenSearch v3.6.0 includes several engine stability improvements for the k-NN plugin, addressing critical issues in native engine merge operations, Lucene codec compatibility, custom codec delegation, and derived source reader lifecycle management. These fixes improve cluster stability during shard relocations, ensure compatibility with Lucene 10.4.0, enable k-NN usage with custom codecs (e.g., ZSTD), and resolve a race condition in `DerivedSourceReaders` ref-counting.

## Details

### What's New in v3.6.0

#### Abortable Native Engine Merges (PR #2529)

Long-running native engine merge tasks (Faiss HNSW graph builds) previously blocked shard close operations during relocations. When a shard relocation was initiated while a merge was in progress, the `clusterApplierService` thread would block on `IndexWriter.abortMerges()`, eventually causing the master to mark the node as stale and remove it from the cluster.

The fix introduces an abort mechanism using Faiss's `InterruptCallback` infrastructure:

- `OpenSearchMergeInterruptCallback` — a custom Faiss `InterruptCallback` that calls back into the JVM via JNI to check merge abort status
- `MergeAbortChecker` — a Java utility using reflection to access `ConcurrentMergeScheduler.MergeThread`'s private `merge` field and check `OneMerge.isAborted()`
- `IndexBuildAbortedException` — a new exception type propagated from JNI through the build strategy to `NativeIndexWriter`, which converts it to `MergePolicy.MergeAbortedException`
- The callback is registered as a singleton during `FaissService` static initialization via `setMergeInterruptCallback()` JNI call

The abort check is performed periodically during Faiss graph construction (controlled by `get_period_hint`), allowing long-running merges to be interrupted within seconds rather than blocking indefinitely.

#### Lucene 10.4.0 Compatibility (PR #3135)

OpenSearch core upgraded Lucene from 10.3.2 to 10.4.0, which broke k-NN build and runtime. Key changes:

- Created `KNN1040Codec` as the new current codec (based on `Lucene104Codec`), moving `KNN1030Codec` to `backward_codecs`
- Created `Lucene99RWHnswScalarQuantizedVectorsFormat` — a read-write format class because `Lucene99HnswScalarQuantizedVectorsFormat` no longer supports writes after Lucene PR #15223
- Created `Lucene99RWScalarQuantizedVectorsFormat` and copied `Lucene99ScalarQuantizedVectorsWriter` to maintain write support for the legacy format with `confidenceInterval` and `compress` parameters
- Updated `KNNCodecVersion` and `KNNCodecService` to use `KNN1040Codec`
- Temporarily disabled `CustomCodecsIT` integration tests pending custom codec plugin upgrade

#### KNN1030Codec Custom Codec Delegation Fix (PR #3093)

The `KNN1030Codec` did not properly support delegation for non-default codecs on the read path. When using k-NN with custom codecs like `zstd` (from `opensearch-custom-codecs`), the write path worked but the read path failed with `IllegalStateException: missing value for Lucene90StoredFieldsFormat.mode`.

The fix stores the delegating codec name in Lucene segment attributes (`knn_delegate_stored_fields_codec_key`) so it can be properly restored on read:

- `KNN10010DerivedSourceStoredFieldsFormat` now accepts a `name` parameter and stores it via `segmentInfo.putAttribute()` during writes
- On reads, `getStoredFieldsFormat()` checks the segment attribute and resolves the correct codec via `Codec.forName()` when it differs from the default
- The fix is scoped to `storedFieldsFormat()` only since it does not have per-field equivalents

#### DerivedSourceReaders Lifecycle Simplification (PR #3138)

The `DerivedSourceReaders` class had a manual reference-counting mechanism that was prone to race conditions. When `freeReaderContext` tried to close the `OpensearchReaderManager` on a cloned instance of `StoredFieldsReader`, the ref count could reach 0 prematurely and close underlying readers that were still in use.

The fix replaces manual ref-counting with Lucene's ownership model:

- The public constructor creates an owning instance with a real `close()` action
- `clone()` and `getMergeInstance()` produce non-owning instances with a no-op `close()`
- This aligns with `Lucene90CompressingStoredFieldsReader`'s clone implementation
- Only the owning instance drives resource cleanup, eliminating the race condition

### Technical Changes

| Area | Change | Impact |
|------|--------|--------|
| JNI Layer | `OpenSearchMergeInterruptCallback` with `want_interrupt()` | Faiss graph builds can be aborted during merge |
| Codec | `KNN1040Codec` based on `Lucene104Codec` | Lucene 10.4.0 compatibility |
| Codec | `Lucene99RWHnswScalarQuantizedVectorsFormat` | Maintains SQ write support post-Lucene 10.4.0 |
| Codec | Segment attribute `knn_delegate_stored_fields_codec_key` | Custom codec read path delegation |
| Derived Source | `DerivedSourceReaders` ownership model | Eliminates ref-counting race condition |

## Limitations

- The merge abort mechanism relies on reflection to access `ConcurrentMergeScheduler.MergeThread`'s private `merge` field, which may break with future Lucene internal changes
- `CustomCodecsIT` integration tests are temporarily disabled pending custom codec plugin upgrade for Lucene 10.4.0

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#2529](https://github.com/opensearch-project/k-NN/pull/2529) | Support aborting native engine merges to prevent shard relocation and cluster stability issues | [#2530](https://github.com/opensearch-project/k-NN/issues/2530) |
| [#3135](https://github.com/opensearch-project/k-NN/pull/3135) | Fix k-NN build and run compatibility with Lucene 10.4.0 upgrade | [#3134](https://github.com/opensearch-project/k-NN/issues/3134) |
| [#3093](https://github.com/opensearch-project/k-NN/pull/3093) | Fix KNN1030Codec to properly support delegation for non-default codecs on the read path | [#3092](https://github.com/opensearch-project/k-NN/issues/3092) |
| [#3138](https://github.com/opensearch-project/k-NN/pull/3138) | Simplify DerivedSourceReaders lifecycle by removing manual ref-counting | [#20622](https://github.com/opensearch-project/OpenSearch/issues/20622), [#3191](https://github.com/opensearch-project/k-NN/issues/3191) |
| [#3252](https://github.com/opensearch-project/k-NN/pull/3252) | Update changelog for v3.6.0 | |
