---
tags:
  - k-nn
  - search
---

# k-NN Vector Search

Approximate k-nearest neighbor search for vector similarity in OpenSearch.

## Overview

- [Vector Search (k-NN)](vector-search-k-nn.md) - Core k-NN functionality

## Search Features

| Document | Description |
|----------|-------------|
| [Disk-based Vector Search](disk-based-vector-search.md) | Memory-efficient vector search |
| [Explain API](explain-api.md) | Query explanation for k-NN |
| [Query Rescore](k-nn-query-rescore.md) | Rescore k-NN results |
| [MMR](maximal-marginal-relevance-mmr.md) | Diversity in search results |
| [Late Interaction](late-interaction.md) | ColBERT-style retrieval |

## Engines & Performance

| Document | Description |
|----------|-------------|
| [Engine Enhancements](k-nn-engine-enhancements.md) | Engine improvements |
| [Performance Engine](k-nn-performance-engine.md) | Performance optimizations |
| [Lucene on Faiss](lucene-on-faiss.md) | Faiss backend for Lucene |
| [AVX-512 Support](k-nn-avx512-support.md) | SIMD acceleration |
| [Memory Optimized Warmup](k-nn-memory-optimized-warmup.md) | Efficient index warming |

## Index Building

| Document | Description |
|----------|-------------|
| [Iterative Graph Build](k-nn-iterative-graph-build.md) | Incremental index building |
| [Remote Vector Index Build](remote-vector-index-build.md) | Offload index building |
| [Derived Source Codec](k-nn-derived-source-codec-refactoring.md) | Codec improvements |

## Vector Types & Configuration

| Document | Description |
|----------|-------------|
| [Byte Vector Support](k-nn-byte-vector-support.md) | Quantized vectors |
| [Space Type Configuration](k-nn-space-type-configuration.md) | Distance metrics |
| [Model Metadata](k-nn-model-metadata.md) | Model information storage |
| [Lucene Vector Integration](k-nn-lucene-vector-integration.md) | Native Lucene vectors |

## Sparse Vectors

| Document | Description |
|----------|-------------|
| [SEISMIC Sparse ANN](../neural-search/seismic-sparse-ann.md) | Sparse vector search |

## Maintenance

| Document | Description |
|----------|-------------|
| [Build](k-nn-build.md) | Build infrastructure |
