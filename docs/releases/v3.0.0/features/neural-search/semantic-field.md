# Semantic Field

## Summary

OpenSearch 3.0 introduces the semantic field type in the neural-search plugin. This new field mapper simplifies semantic search by automatically handling text-to-vector transformations at index time, eliminating the need for separate ingest pipelines.

## Details

### What's New in v3.0.0

#### Semantic Field Mapper

The semantic field type allows users to define fields that automatically generate embeddings using ML models:

- Supports multiple raw field types: `text`, `keyword`, `match_only_text`, `wildcard`, `token_count`, `binary`
- Configurable ML models for indexing and search
- Automatic delegation to underlying field type for storage and queries

### Configuration Parameters

| Parameter | Description | Required | Default |
|-----------|-------------|----------|--------|
| `model_id` | ML model ID for generating embeddings at index time | Yes | - |
| `search_model_id` | ML model ID for query text inference (uses `model_id` if not set) | No | `model_id` |
| `raw_field_type` | Underlying field type for raw data storage | No | `text` |
| `semantic_info_field_name` | Custom field name for semantic information | No | Auto-generated |

### Supported Raw Field Types

| Type | Description |
|------|-------------|
| `text` | Full-text searchable content (default) |
| `keyword` | Exact match strings |
| `match_only_text` | Space-optimized text without scoring |
| `wildcard` | Wildcard pattern matching |
| `token_count` | Token count storage |
| `binary` | Binary data storage |

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

### Technical Implementation

The semantic field mapper uses a delegate pattern:

1. **SemanticFieldMapper**: Main mapper handling semantic parameters
2. **Delegate Field Mapper**: Handles raw data parsing and queries based on `raw_field_type`
3. **SemanticFieldType**: Extends `FilterFieldType` to wrap delegate field type

### Feature Flag

The semantic field is currently gated behind a feature flag:

```java
FeatureFlagUtil.SEMANTIC_FIELD_ENABLED = false  // Default: disabled
```

## Limitations

- Feature is disabled by default (requires feature flag)
- Documentation not yet available in public docs
- API specification companion PR pending

## Related PRs

| PR | Description |
|----|-------------|
| [#1225](https://github.com/opensearch-project/neural-search/pull/1225) | Add semantic field mapper |

## References

- [Issue #803](https://github.com/opensearch-project/neural-search/issues/803): Neural Search field type proposal
- [Issue #1226](https://github.com/opensearch-project/neural-search/issues/1226): Related semantic field implementation

## Related Feature Report

- [Full feature documentation](../../../../features/neural-search/semantic-field.md)
