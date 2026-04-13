---
tags:
  - k-nn
---
# Vector Search (k-NN) - Scoring & Search

## Summary

OpenSearch 3.6.0 introduces a major refactoring of the k-NN scoring and search infrastructure. The core change is a new VectorScorers factory that replaces the legacy ExactKNNIterator-based exact search with Lucene's VectorScorer API, enabling unified scorer creation across all vector storage formats. This release also adds Hamming distance scoring for binary vectors, vector prefetching during ANN search for memory-optimized mode, and fixes several bugs in radial search, filtered search, and rescoring.

## Details

### What's New in v3.6.0

#### VectorScorers Factory and Unified Scoring Architecture

A new `VectorScorers` factory class centralizes VectorScorer instance creation based on the underlying vector storage format (BinaryDocValues, FloatVectorValues, ByteVectorValues). Key components:

- `VectorScorerFactory` with float and byte target overloads
- `ScoreMode` interface with `SCORE` and `RESCORE` strategies to abstract scorer vs rescorer creation
- ADC scorer integration with a TODO to remove once `ByteVectorValues.scorer()` is implemented natively

The `ExactSearcher` was refactored to use `VectorScorers.createScorer` instead of the legacy `ExactKNNIterator` approach. This eliminates multiple iterator subclasses (`VectorIdsExactKNNIterator`, `BinaryVectorIdsExactKNNIterator`, and their nested variants) by delegating vector type dispatch and nested wrapping to the factory.

#### New VectorScorer Implementations

- `NestedBestChildVectorScorer`: Groups child documents by parent and returns the best-scoring child per parent. Adapted from Lucene's `DiversifyingChildrenVectorScorer` to implement `VectorScorer`. Supports both filtered and unfiltered iteration.
- `KnnBinaryDocValuesScorer`: Scores documents backed by `BinaryDocValues` by deserializing stored vectors and comparing against the query vector using `SpaceType`. Supports both `float[]` and `byte[]` query vectors via overloaded factory methods.

#### Hamming Distance Scorer for Binary Vectors

Routes `SpaceType.HAMMING` to a dedicated `createHammingScorer` via `FlatVectorsScorerProvider` for memory-optimized binary vector search. Propagates `fieldInfo` to byte-target `createScorer` APIs for space-type-aware scorer resolution.

#### Vector Prefetch During ANN Search

A new `PrefetchableVectorScorer` wraps `FlatVectorScorer` and calls prefetch before `bulkScore` operations during ANN search in memory-optimized mode. Key details:
- Prefetch is gated behind a feature flag
- Works for Byte, FP32 vectors in the ANN flow
- Passed from `FlatVectorFormat` to `FaissMemoryOptimizedSearcher`

#### Scorer-Aware ByteVectorValues Wrapper for FAISS

`FaissScorableByteVectorValues` wraps raw FAISS byte vectors with scoring capability via `FlatVectorsScorer`. This bridges the gap where FAISS-backed `ByteVectorValues` is a random-access store that cannot produce a `DocIndexIterator` on its own, which `VectorScorer` requires for document traversal.

#### ByteVectorIdsExactKNNIterator Optimization

Moved float-to-byte array conversion from `computeScore()` to the constructor, extracting conversion logic into a private `convertToByteArray()` method. This eliminates repeated array allocation and conversion on every score calculation.

### Bug Fixes

#### FaissIdMap acceptOrds Double Mapping Fix

In `FaissIdMapIndex`, the `getAcceptOrds` method in both `SparseByteVectorValuesImpl` and `SparseFloatVectorValuesImpl` applied the ordinal-to-docID mapping twice. The fix skips the nested index's `getAcceptOrds` and maps directly: `acceptDocs.get((int) idMappingReader.get(internalVectorId))`.

#### Radial Search Fix for IndexHNSWCagra

`IndexHNSWCagra` was not overriding `range_search`, causing it to fall back to `IndexHNSW::range_search` which does not use CAGRA's entry points for graph traversal. The fix adds a Faiss patch that refactors `IndexHNSW::search` to accept optional entry points and overrides `range_search` in `IndexHNSWCagra`.

#### Cosine Space Type Score Conversion Fix

Fixed score translation logic for exact radial search with cosine space type in filtered scenarios.

#### Lucene Rescore TopK Reduction Fix

Fixed a regression where oversampled k results were incorrectly reduced to the actual k value before the rescoring phase. Rescoring now operates on the full oversampled result set. Additionally, rescoring is temporarily disabled when `expandNested` is enabled to prevent incorrect results.

## Limitations

- Prefetch integration with NativeScorer (BulkSIMD) and ADCScorer is not yet complete
- Rescoring is disabled when `expandNested` is enabled (temporary workaround)
- The ADC scorer in VectorScorers has a TODO to be removed once `ByteVectorValues.scorer()` is implemented

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#3183](https://github.com/opensearch-project/k-NN/pull/3183) | Introduce VectorScorers factory for storage-format-aware scorer creation | |
| [#3179](https://github.com/opensearch-project/k-NN/pull/3179) | Add NestedBestChildVectorScorer and KnnBinaryDocValuesScorer | |
| [#3214](https://github.com/opensearch-project/k-NN/pull/3214) | Add Hamming distance scorer for byte vectors | |
| [#3173](https://github.com/opensearch-project/k-NN/pull/3173) | Add prefetch functionality for vectors during ANN search | [#2577](https://github.com/opensearch-project/k-NN/issues/2577) |
| [#3192](https://github.com/opensearch-project/k-NN/pull/3192) | Add scorer-aware ByteVectorValues wrapper for FAISS index | |
| [#3207](https://github.com/opensearch-project/k-NN/pull/3207) | Refactor ExactSearcher to use VectorScorer API | [#3105](https://github.com/opensearch-project/k-NN/issues/3105) |
| [#3171](https://github.com/opensearch-project/k-NN/pull/3171) | Optimize ByteVectorIdsExactKNNIterator array conversion | |
| [#3196](https://github.com/opensearch-project/k-NN/pull/3196) | Fix FaissIdMap double ordinal-to-docID mapping | |
| [#3201](https://github.com/opensearch-project/k-NN/pull/3201) | Fix radial search returning 0 results for IndexHNSWCagra | [#3160](https://github.com/opensearch-project/k-NN/issues/3160) |
| [#3110](https://github.com/opensearch-project/k-NN/pull/3110) | Fix score conversion for filtered radial exact search with cosine | [#3099](https://github.com/opensearch-project/k-NN/issues/3099) |
| [#3124](https://github.com/opensearch-project/k-NN/pull/3124) | Fix Lucene reduce to topK when rescoring is enabled | [#2940](https://github.com/opensearch-project/k-NN/issues/2940) |
