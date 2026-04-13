---
tags:
  - opensearch
---
# Bitmap64 Query Support

## Summary

OpenSearch v3.6.0 extends bitmap filtering to support 64-bit long fields. Previously, bitmap filtering (introduced in v2.17.0) only worked with 32-bit integer fields using `RoaringBitmap`. This release adds `Roaring64NavigableMap`-based queries, enabling the same `value_type: "bitmap"` terms query syntax on `long` type fields. This allows efficient large-scale filtering on fields with values exceeding the 32-bit integer range, such as large user IDs, timestamps, or other long identifiers.

## Details

### What's New in v3.6.0

The existing bitmap filtering feature used 32-bit `RoaringBitmap` for `integer` fields. This release adds two new query classes to handle 64-bit `long` fields:

- `Bitmap64IndexQuery` — uses BKD tree (point values) intersection with a merge-sort style visitor for indexed fields
- `Bitmap64DocValuesQuery` — uses doc values iteration with `TwoPhaseIterator` for doc-values-only fields

When both index and doc values are available, the queries are wrapped in Lucene's `IndexOrDocValuesQuery` to dynamically choose the optimal execution path at runtime.

### Technical Changes

The implementation overrides `bitmapQuery()` in the `LONG` number type within `NumberFieldMapper.java`. The bitmap bytes are deserialized using `Roaring64NavigableMap.deserializePortable()`, which follows the portable serialization format specified in the RoaringBitmap format specification.

Key implementation details:

| Component | Class | Description |
|-----------|-------|-------------|
| Index query | `Bitmap64IndexQuery` | Traverses BKD tree point values using a `MergePointVisitor` that merge-sorts encoded bitmap values against leaf node values |
| Doc values query | `Bitmap64DocValuesQuery` | Uses `TwoPhaseIterator` with min/max range guards for early termination; handles both singleton and multi-value doc values |
| Deserialization | `NumberFieldMapper.LONG.bitmapQuery()` | Deserializes `Roaring64NavigableMap` from portable format bytes |

Query execution strategy:

| Field Configuration | Query Used |
|---------------------|------------|
| Indexed + doc values (default) | `IndexOrDocValuesQuery(Bitmap64IndexQuery, Bitmap64DocValuesQuery)` |
| Indexed only | `Bitmap64IndexQuery` |
| Doc values only | `Bitmap64DocValuesQuery` |

### Usage

The query syntax is identical to the existing 32-bit bitmap filtering, but now works on `long` fields:

```json
{
  "mappings": {
    "properties": {
      "user_id": { "type": "long" }
    }
  }
}
```

Direct bitmap query:

```json
POST my_index/_search
{
  "query": {
    "terms": {
      "user_id": ["<base64-encoded Roaring64NavigableMap portable bytes>"],
      "value_type": "bitmap"
    }
  }
}
```

Terms lookup from a stored binary field:

```json
POST my_index/_search
{
  "query": {
    "terms": {
      "user_id": {
        "index": "filters",
        "id": "filter1",
        "path": "members",
        "store": true
      },
      "value_type": "bitmap"
    }
  }
}
```

### Design Decision: Roaring64NavigableMap vs Roaring64Bitmap

The implementation uses `Roaring64NavigableMap` rather than `Roaring64Bitmap` (which uses an ART data structure and has better performance). This choice was made because `Roaring64NavigableMap` is the only 64-bit implementation that supports the well-specified portable serialization format from the RoaringBitmap format specification. Consistent, cross-platform serialization is essential for OpenSearch's use case where bitmaps are serialized by clients and deserialized by the server.

## Limitations

- Only `long` field type is supported for 64-bit bitmap queries; `integer`, `short`, and `byte` fields continue to use the existing 32-bit `RoaringBitmap` path
- `Roaring64NavigableMap` has lower performance than `Roaring64Bitmap` due to the use of `TreeMap` internally, but provides guaranteed portable serialization
- The `LongIterator` from `Roaring64NavigableMap` does not support `advanceIfNeeded()` (unlike `PeekableLongIterator` in `Roaring64Bitmap`), so the index query uses a manual advance loop

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| `https://github.com/opensearch-project/OpenSearch/pull/20606` | Add bitmap64 query support | `https://github.com/opensearch-project/OpenSearch/issues/20597` |

### Related
- Feature request: `https://github.com/opensearch-project/OpenSearch/issues/20597`
- Original 32-bit bitmap filtering: `https://github.com/opensearch-project/OpenSearch/pull/14774`
- Bitmap index query performance improvement: `https://github.com/opensearch-project/OpenSearch/pull/16936`
- RoaringBitmap 64-bit format spec: https://github.com/RoaringBitmap/RoaringFormatSpec
- Blog post on bitmap filtering: https://opensearch.org/blog/introduce-bitmap-filtering-feature/
