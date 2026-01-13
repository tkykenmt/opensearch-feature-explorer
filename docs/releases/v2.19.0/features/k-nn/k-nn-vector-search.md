---
tags:
  - k-nn
---
# k-NN Vector Search

## Summary

OpenSearch v2.19.0 brings significant enhancements to the k-NN plugin including cosine similarity support for FAISS engine, AVX-512 SPR optimizations for Intel Sapphire Rapids processors, binary vector support for Lucene engine, derived source for vector fields, multi-value innerHit support for nested k-NN fields, concurrent graph creation for Lucene, and NMSLIB engine deprecation. The release also includes numerous bug fixes and performance improvements.

## Details

### What's New in v2.19.0

#### Cosine Similarity for FAISS Engine
FAISS engine now natively supports cosine similarity by normalizing vectors before ingestion and using inner product for search. This eliminates the need for manual vector normalization while maintaining competitive search and force merge performance.

```json
PUT /my-index
{
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "knn_vector",
        "dimension": 128,
        "method": {
          "name": "hnsw",
          "space_type": "cosinesimil",
          "engine": "faiss"
        }
      }
    }
  }
}
```

#### AVX-512 SPR Build Mode
New `FAISS_OPT_LEVEL=avx512_spr` build mode enables advanced AVX-512 instructions available on Intel Sapphire Rapids and newer processors, including `avx512_fp16`, `avx512_bf16`, and `avx512_vpopcntdq`. This accelerates Hamming distance evaluation for binary vectors.

#### Binary Vector Support for Lucene Engine
Lucene engine now supports binary vectors, providing an alternative to FAISS for binary vector workloads without native library dependencies.

```json
PUT /binary-index
{
  "mappings": {
    "properties": {
      "binary_vector": {
        "type": "knn_vector",
        "dimension": 64,
        "data_type": "binary",
        "method": {
          "name": "hnsw",
          "engine": "lucene"
        }
      }
    }
  }
}
```

#### Derived Source for Vector Fields (Experimental)
Vectors can now be excluded from `_source` field on disk and reconstructed on read, reducing storage overhead. This feature uses a custom StoredFieldsFormat that removes vectors during write and injects them back during read.

```json
PUT /my-index
{
  "settings": {
    "index.knn.derived_source.enabled": true
  }
}
```

#### Multi-Value innerHit for Nested k-NN Fields
Support for returning all nested fields with their scores inside innerHit for nested k-NN fields, applicable to both Lucene and FAISS engines.

#### Concurrent Graph Creation for Lucene
Lucene engine now supports concurrent graph creation using the `index_thread_qty` setting, improving indexing performance on multi-core systems.

#### NMSLIB Engine Deprecation
The NMSLIB engine is now deprecated. Users should migrate to FAISS or Lucene engines for new indices.

### Technical Changes

| Change | Description | PR |
|--------|-------------|-----|
| Cosine similarity for FAISS | Normalize vectors before ingestion, use inner product for search | [#2376](https://github.com/opensearch-project/k-NN/pull/2376) |
| AVX-512 SPR support | New build mode for Intel Sapphire Rapids processors | [#2404](https://github.com/opensearch-project/k-NN/pull/2404) |
| Binary vectors for Lucene | Binary vector support in Lucene engine | [#2292](https://github.com/opensearch-project/k-NN/pull/2292) |
| Derived source | Remove vectors from _source, reconstruct on read | [#2449](https://github.com/opensearch-project/k-NN/pull/2449) |
| Multi-value innerHit | Return all nested fields with scores | [#2283](https://github.com/opensearch-project/k-NN/pull/2283) |
| expand_nested_docs for NMSLIB | Support expand_nested_docs parameter | [#2331](https://github.com/opensearch-project/k-NN/pull/2331) |
| Concurrent Lucene graph creation | Enable concurrent graph creation with index_thread_qty | [#2480](https://github.com/opensearch-project/k-NN/pull/2480) |
| NMSLIB deprecation | Deprecate NMSLIB engine | [#2427](https://github.com/opensearch-project/k-NN/pull/2427) |

### Enhancements

| Enhancement | Description | PR |
|-------------|-------------|-----|
| expand_nested query parameter | New knn query parameter for nested documents | [#1013](https://github.com/opensearch-project/k-NN/pull/1013) |
| Writing layer for native engines | Introduced writing layer relying on FieldWriter | [#2241](https://github.com/opensearch-project/k-NN/pull/2241) |
| Method parameter override | Allow method parameter override for training-based indices | [#2290](https://github.com/opensearch-project/k-NN/pull/2290) |
| Lucene query optimization | Prevent unnecessary rewrites in Lucene query execution | [#2305](https://github.com/opensearch-project/k-NN/pull/2305) |
| Detailed training error messages | More detailed error messages for KNN model training | [#2378](https://github.com/opensearch-project/k-NN/pull/2378) |
| ANN search optimization | Direct ANN search when filters match all documents | [#2320](https://github.com/opensearch-project/k-NN/pull/2320) |
| Cosine similarity formula | Use single formula for cosine similarity calculation | [#2357](https://github.com/opensearch-project/k-NN/pull/2357) |
| M-series MacOS build | Build works for M-series MacOS without manual changes | [#2397](https://github.com/opensearch-project/k-NN/pull/2397) |
| Memory optimization | Remove DocsWithFieldSet reference from NativeEngineFieldVectorsWriter | [#2408](https://github.com/opensearch-project/k-NN/pull/2408) |
| Quantization graph build | Remove skip building graph check for quantization use case | [#2430](https://github.com/opensearch-project/k-NN/pull/2430) |
| Script scoring optimization | Remove redundant type conversions for binary vectors | [#2351](https://github.com/opensearch-project/k-NN/pull/2351) |
| Default graph build behavior | Update default to 0 to always build graph | [#2452](https://github.com/opensearch-project/k-NN/pull/2452) |

### Bug Fixes

| Bug Fix | Description | PR |
|---------|-------------|-----|
| C++17 upgrade | Updated C++ version in JNI from c++11 to c++17 | [#2259](https://github.com/opensearch-project/k-NN/pull/2259) |
| Dependency upgrade | Upgrade bytebuddy and objenesis to match OpenSearch | [#2279](https://github.com/opensearch-project/k-NN/pull/2279) |
| Byte vector filter bug | Fix Faiss byte vector efficient filter bug | [#2448](https://github.com/opensearch-project/k-NN/pull/2448) |
| Mapping validation | Fix bug where mapping accepts both dimension and model-id | [#2410](https://github.com/opensearch-project/k-NN/pull/2410) |
| Field name validation | Add version check for full field name validation | [#2477](https://github.com/opensearch-project/k-NN/pull/2477) |
| Engine version update | Update engine for version 2.19 or above | [#2501](https://github.com/opensearch-project/k-NN/pull/2501) |
| Missing vector field | Fix bug when segment has no vector field for native engines | [#2282](https://github.com/opensearch-project/k-NN/pull/2282) |
| Fields parameter search | Fix search failure with fields parameter | [#2314](https://github.com/opensearch-project/k-NN/pull/2314) |
| NPE on segment merge | Fix NPE while merging segments after vector field deletion | [#2365](https://github.com/opensearch-project/k-NN/pull/2365) |
| Non-knn index validation | Allow validation for non-knn index only after 2.17.0 | [#2315](https://github.com/opensearch-project/k-NN/pull/2315) |
| index.knn setting update | Prevent updating index.knn setting after index creation | [#2348](https://github.com/opensearch-project/k-NN/pull/2348) |
| Query vector memory | Release query vector memory after execution | [#2346](https://github.com/opensearch-project/k-NN/pull/2346) |
| Shard-level rescoring | Fix shard level rescoring disabled setting flag | [#2352](https://github.com/opensearch-project/k-NN/pull/2352) |
| Filter rewrite logic | Fix filter rewrite logic causing incorrect results | [#2359](https://github.com/opensearch-project/k-NN/pull/2359) |
| space_type retrieval | Retrieve space_type from index setting when both sources available | [#2374](https://github.com/opensearch-project/k-NN/pull/2374) |
| on_disk rescore setting | Fix rescore=false for on_disk knn indices | [#2399](https://github.com/opensearch-project/k-NN/pull/2399) |
| index.knn modification | Prevent index.knn setting modification after creation | [#2445](https://github.com/opensearch-project/k-NN/pull/2445) |
| Cluster version settings | Select index settings based on cluster version | [#2236](https://github.com/opensearch-project/k-NN/pull/2236) |
| Quantization cache maintenance | Added periodic cache maintenance for QuantizationStateCache | [#2308](https://github.com/opensearch-project/k-NN/pull/2308) |
| ExactSearcher NPE | Added null checks for fieldInfo in ExactSearcher | [#2278](https://github.com/opensearch-project/k-NN/pull/2278) |
| Lucene BWC tests | Added Lucene backward compatibility tests | [#2313](https://github.com/opensearch-project/k-NN/pull/2313) |
| jsonpath upgrade | Upgrade jsonpath from 2.8.0 to 2.9.0 | [#2325](https://github.com/opensearch-project/k-NN/pull/2325) |
| Faiss Hamming acceleration | Bump Faiss commit to accelerate Hamming distance | [#2381](https://github.com/opensearch-project/k-NN/pull/2381) |
| Spotless mirror repo | Add spotless mirror repo for fixing builds | [#2453](https://github.com/opensearch-project/k-NN/pull/2453) |

## Limitations

- Derived source feature is experimental
- NMSLIB engine is deprecated; migrate to FAISS or Lucene
- AVX-512 SPR optimizations require Intel Sapphire Rapids or newer processors

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#2376](https://github.com/opensearch-project/k-NN/pull/2376) | Add cosine similarity support for faiss engine | [#2242](https://github.com/opensearch-project/k-NN/issues/2242) |
| [#2404](https://github.com/opensearch-project/k-NN/pull/2404) | Add FAISS_OPT_LEVEL=avx512_spr build mode | - |
| [#2283](https://github.com/opensearch-project/k-NN/pull/2283) | Add multi-value innerHit support for nested k-NN fields | [#2249](https://github.com/opensearch-project/k-NN/issues/2249) |
| [#2292](https://github.com/opensearch-project/k-NN/pull/2292) | Add binary index support for Lucene engine | [#1857](https://github.com/opensearch-project/k-NN/issues/1857) |
| [#2449](https://github.com/opensearch-project/k-NN/pull/2449) | Introduce derived vector source via stored fields | [#2377](https://github.com/opensearch-project/k-NN/issues/2377) |
| [#2331](https://github.com/opensearch-project/k-NN/pull/2331) | Add expand_nested_docs parameter support to NMSLIB engine | - |
| [#2480](https://github.com/opensearch-project/k-NN/pull/2480) | Enable concurrent graph creation for Lucene engine | [#1581](https://github.com/opensearch-project/k-NN/issues/1581) |
| [#2427](https://github.com/opensearch-project/k-NN/pull/2427) | Deprecate nmslib engine | - |

### Documentation
- [k-NN Plugin Documentation](https://docs.opensearch.org/2.19/vector-search/)
- [k-NN API Reference](https://docs.opensearch.org/2.19/vector-search/api/knn/)
