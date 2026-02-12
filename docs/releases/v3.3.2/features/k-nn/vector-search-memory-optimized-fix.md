---
tags:
  - k-nn
---
# Vector Search (k-NN) Memory Optimized Search Fix

## Summary

Fixed a NullPointerException that occurred when memory optimized search was applied to indices created before OpenSearch 2.17.

## Details

### What's New in v3.3.2

For indices created before 2.17, the old codec returns `null` as `VectorReader`, causing a NullPointerException when memory optimized search is enabled. The fix adds an index creation version check that returns `false` for `isMemoryOptimizedSearchEnabled` on old indices, allowing the flow to fall back to the default logic which delegates C++ to load vectors into off-heap memory.

For indices created with 2.18+, the codec includes the LuceneOnFaiss implementation and delegates search to the Faiss index as expected.

### Impact
- Indices created before 2.17: Memory optimized search is disabled, falls back to off-heap vector loading
- Indices created with 2.18+: Memory optimized search works normally via LuceneOnFaiss

## References

| PR | Description |
|----|-------------|
| [#2918](https://github.com/opensearch-project/k-NN/pull/2918) | Do not apply memory optimized search for old indices |
| [#2917](https://github.com/opensearch-project/k-NN/issues/2917) | Related issue |
