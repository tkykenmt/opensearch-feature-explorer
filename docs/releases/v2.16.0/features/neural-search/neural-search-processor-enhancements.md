---
tags:
  - neural-search
---
# Neural Search Processor Enhancements

## Summary

OpenSearch v2.16.0 introduces enhancements to neural search ingest processors, including batch processing support via `AbstractBatchingProcessor` inheritance and improved nested field syntax for field mappings in text embedding and sparse encoding processors.

## Details

### What's New in v2.16.0

#### Batch Processing Support (PR #820)

The `text_embedding` and `sparse_encoding` processors now inherit from `AbstractBatchingProcessor`, enabling processor-level batch size configuration. This moves the batching logic from the Bulk API to individual processors for better control.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `batch_size` | Number of documents to batch per ML model request | 1 |

Example pipeline with batch size:

```json
PUT /_ingest/pipeline/nlp-pipeline
{
  "processors": [
    {
      "text_embedding": {
        "model_id": "model_id",
        "batch_size": 5,
        "field_map": {
          "passage_text": "passage_embedding"
        }
      }
    }
  ]
}
```

#### Nested Field Syntax for Source Fields (PR #811)

Users can now use dot notation to reference nested source fields in the `field_map` configuration, simplifying processor definitions for complex document structures.

Before v2.16.0 (hierarchical only):
```json
"field_map": {
  "a": {
    "b": {
      "c": "embedding_field"
    }
  }
}
```

New syntax in v2.16.0:
```json
"field_map": {
  "a.b.c": "embedding_field"
}
```

Mixed syntax is also supported:
```json
"field_map": {
  "a.b": {
    "c": "embedding_field"
  }
}
```

#### Nested Field Syntax for Destination Fields (PR #841)

Extends the dot notation support to destination fields, allowing embeddings to be stored in nested structures.

Example:
```json
"field_map": {
  "a.b": "c.vector_field"
}
```

This creates the following document structure:
```json
{
  "a": {
    "b": "source_text",
    "c": {
      "vector_field": [0.1, 0.2, ...]
    }
  }
}
```

### Technical Changes

- `InferenceProcessor` now extends `AbstractBatchingProcessor` from OpenSearch core
- New `batch_size` parameter added to processor configuration
- Field path parsing updated to handle dot-separated paths for both source and destination fields
- Backward compatible: default `batch_size` of 1 maintains existing behavior

## Limitations

- Batch size should be tuned based on ML model capacity and memory constraints
- Very large batch sizes may cause timeouts with external ML services
- Nested field syntax applies to `text_embedding` and `sparse_encoding` processors

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#820](https://github.com/opensearch-project/neural-search/pull/820) | Use AbstractBatchingProcessor for InferenceProcessor | [OpenSearch#14283](https://github.com/opensearch-project/OpenSearch/issues/14283) |
| [#811](https://github.com/opensearch-project/neural-search/pull/811) | Enable '.' for nested field in text embedding processor | [#110](https://github.com/opensearch-project/neural-search/issues/110) |
| [#841](https://github.com/opensearch-project/neural-search/pull/841) | Enhance syntax for nested mapping in destination fields | [#110](https://github.com/opensearch-project/neural-search/issues/110) |

### Documentation
- [Text Embedding Processor](https://docs.opensearch.org/2.16/ingest-pipelines/processors/text-embedding/)
- [Sparse Encoding Processor](https://docs.opensearch.org/2.16/ingest-pipelines/processors/sparse-encoding/)
