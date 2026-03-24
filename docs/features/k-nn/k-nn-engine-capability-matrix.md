---
tags:
  - k-nn
---
# k-NN Engine Capability Matrix

## Engine × Method × Mode

| Engine | Method | Mode | Since | Notes |
|--------|--------|------|-------|-------|
| **NMSLIB** (deprecated) | HNSW | in-memory | 1.0 | Loads entire graph + vectors into native memory |
| **Faiss** | HNSW | in-memory | 1.2 | Default behavior |
| **Faiss** | HNSW | on-disk | 2.17 | `"mode": "on_disk"` — vectors on disk, only graph in memory. Automatically applies SQ fp16 + rescoring |
| **Faiss** | HNSW | memory-optimized | 3.0 | `index.knn.memory_optimized_search: true` — graph read via OS page cache (Lucene Directory abstraction) |
| **Faiss** | IVF | in-memory | 1.2 | Requires training |
| **Lucene** | HNSW | in-memory (JVM managed) | 2.2 | Memory managed by Lucene itself. Does not use native memory cache |

## Engine × Supported Vector Data Types (`data_type`)

The `data_type` parameter specifies the type of vector elements ingested by the user. This is independent of quantization (encoder).

| `data_type` | Size per dim | Faiss | Lucene | NMSLIB |
|-------------|-------------|-------|--------|--------|
| `float` (FP32) | 4 bytes | 1.2 (HNSW, IVF) | 2.2 (HNSW) | 1.0 (HNSW) |
| `byte` (int8) | 1 byte | 2.9 (HNSW, IVF) | 2.9 (HNSW) | — |
| `binary` | 1 bit | 2.16 (HNSW, IVF) | 2.17 (HNSW) | — |

- `float`: Default. Standard embedding model output
- `byte`: Value range [-128, 127]. Compatible with Cohere Embed v3 `int8` output, etc.
- `binary`: Bit vectors. `dimension` must be a multiple of 8. Uses Hamming / Hamming bit distance

## Engine × Built-in Quantization (Encoder)

Quantization compresses `float` data at storage time. This is a separate layer from `data_type`.

| Engine | Encoder | Compressed size | Since | Method | Notes |
|--------|---------|----------------|-------|--------|-------|
| **Faiss** | `flat` (none) | 4 bytes/dim | 1.2 | HNSW, IVF | Default. No compression |
| **Faiss** | `sq` (fp16) | 2 bytes/dim | 2.13 | HNSW, IVF | `encoder: {name: "sq", parameters: {type: "fp16"}}` |
| **Faiss** | `pq` (product quantization) | Variable | 2.0 (IVF), 2.10 (HNSW) | IVF, HNSW | Training required (IVF). HNSW requires `code_size=8` |
| **Faiss** | `bq` (binary quantization) | 1 bit/dim | 3.2 | HNSW | Quantizes FP32 input to 1-bit + rescoring. Supports ADC |
| **Lucene** | `sq` (int8 scalar quantization) | 1 byte/dim | 2.16 | HNSW | Lucene built-in. Different implementation from Faiss SQ |
| **NMSLIB** | — | — | — | — | No quantization support |

### data_type and encoder combinations

| | `data_type: float` | `data_type: byte` | `data_type: binary` |
|---|---|---|---|
| No encoder (flat) | ✅ 4 bytes/dim | ✅ 1 byte/dim | ✅ 1 bit/dim |
| encoder: sq fp16 | ✅ 2 bytes/dim | — (unnecessary) | — |
| encoder: pq | ✅ Variable | — | — |
| encoder: bq | ✅ 1 bit/dim + rescoring | — | — |
| Lucene encoder: sq | ✅ 1 byte/dim | — (unnecessary) | — |

When using `byte` or `binary` as `data_type`, additional encoder-based quantization is unnecessary since the data is already compact. Encoders are designed to compress `float` data at the storage/memory level.

## Engine × Supported Space Types

| Space Type | Faiss HNSW | Faiss IVF | Lucene HNSW | NMSLIB HNSW |
|-----------|-----------|----------|------------|------------|
| `l2` | 1.2 | 1.2 | 2.2 | 1.0 |
| `innerproduct` | 1.2 | 1.2 | 2.13 | 1.0 |
| `cosinesimil` | 2.19 | 2.19 | 2.2 | 1.0 |
| `l1` | — | — | — | 1.0 |
| `linf` | — | — | — | 1.0 |
| `hamming` | 2.16 | 2.16 | — | — |

Note: When using `cosinesimil` with the Faiss engine, vectors are automatically normalized to unit length during indexing because Faiss uses inner product on normalized vectors internally.

## Version Timeline Summary

| Version | Key k-NN additions |
|---------|-------------------|
| 1.0 | NMSLIB HNSW |
| 1.2 | Faiss engine (HNSW + IVF) |
| 2.0 | Faiss IVF + PQ |
| 2.2 | Lucene engine |
| 2.9 | Byte vector support (Faiss, Lucene) |
| 2.10 | Faiss HNSW + PQ |
| 2.12 | Lucene HNSW ef_construction/m default change (512→100/16), nested field improvements |
| 2.13 | Faiss SQ fp16, Lucene innerproduct, SIMD (AVX2/Neon) |
| 2.14 | Clear Cache API, radial search |
| 2.16 | Binary vectors (Faiss), Lucene scalar quantization, Hamming distance |
| 2.17 | Disk-based vector search (`mode: on_disk`), iterative graph build |
| 2.18 | Pluggable storage (Lucene Directory abstraction), AVX-512 |
| 2.19 | Faiss cosinesimil, derived source, NMSLIB deprecated |
| 3.0 | Memory-optimized search, node-level circuit breaker |
| 3.2 | Binary quantization (BQ) + ADC, dynamic `index_thread_qty` |
| 3.4 | Memory-optimized warmup improvements |
| 3.5 | Efficient filter disable option, AVX-512 SPR, Bulk SIMD V2 |

## Disk-Based vs Memory-Optimized vs In-Memory

| | In-Memory (default) | On-Disk (2.17+) | Memory-Optimized (3.0+) |
|---|---|---|---|
| Graph | Native memory | Native memory | OS page cache |
| Vectors | Native memory | Disk (mmap) | OS page cache |
| Memory consumption | Highest | Medium (graph only) | Lowest (OS managed) |
| Latency | Lowest | Medium (disk I/O) | Low–Medium (page cache dependent) |
| Auto quantization | None | SQ fp16 auto-applied + rescoring | None |
| Engine | Faiss, NMSLIB | Faiss only | Faiss only |
| Circuit breaker | Applies | Graph portion only | Not applicable (OS managed) |
