---
tags:
  - indexing
  - ml
  - neural-search
  - search
---

# Semantic Field

## Summary

OpenSearch 3.0 introduces the `semantic` field type in the neural-search plugin. This field mapper simplifies semantic search by automatically handling text-to-vector transformations at index time, eliminating the need for separate ingest pipelines.

## Details

### What's New in v3.0.0

The semantic field type allows users to define fields that automatically generate embeddings using ML models:

- Supports multiple raw field types: `text`, `keyword`, `match_only_text`, `wildcard`, `token_count`, `binary`
- Configurable ML models for indexing and search via `model_id` and `search_model_id`
- Automatic delegation to underlying field type for storage and queries
- Uses delegate pattern to wrap existing field mappers

### Technical Changes

#### New Components

| Component | Description |
|-----------|-------------|
| `SemanticFieldMapper` | Main field mapper handling semantic field configuration and delegation |
| `SemanticFieldType` | Field type extending `FilterFieldType` for delegate wrapping |
| `SemanticParameters` | DTO holding `model_id`, `search_model_id`, `raw_field_type`, `semantic_info_field_name` |
| `SemanticFieldConstants` | Constants for semantic field parameter names |
| `MappingConstants` | Constants for index mapping |
| `FeatureFlagUtil` | Controls semantic field feature availability |

#### New Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `model_id` | ML model ID for generating embeddings at index time | Required |
| `search_model_id` | ML model ID for query text inference | Uses `model_id` |
| `raw_field_type` | Underlying field type for raw data storage | `text` |
| `semantic_info_field_name` | Custom field name for semantic information | Auto-generated |

### Usage Example

```json
PUT /my-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "semantic",
        "model_id": "my-embedding-model",
        "raw_field_type": "text"
      }
    }
  }
}
```

### Migration Notes

The semantic field is gated behind a feature flag (`semantic_field_enabled`) and is disabled by default in v3.0.0. To enable:

1. Set the feature flag to enable semantic field support
2. Define semantic fields in index mappings with required `model_id`
3. Documents indexed will automatically generate embeddings

## Limitations

- Feature is disabled by default (requires feature flag)
- Cannot change `raw_field_type` after index creation
- Cannot change `semantic_info_field_name` after index creation
- Does not support dynamic mapping

## References

### Documentation
- [Semantic Search Documentation](https://docs.opensearch.org/3.0/vector-search/ai-search/semantic-search/)

### Blog Posts
- [Blog: The new semantic field](https://opensearch.org/blog/the-new-semantic-field-simplifying-semantic-search-in-opensearch/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#1225](https://github.com/opensearch-project/neural-search/pull/1225) | Add semantic field mapper |

### Issues (Design / RFC)
- [Issue #803](https://github.com/opensearch-project/neural-search/issues/803): Neural Search field type proposal
- [Issue #1226](https://github.com/opensearch-project/neural-search/issues/1226): Clean up unnecessary feature flag

## Related Feature Report

- [Full feature documentation](../../../../features/neural-search/semantic-field.md)
