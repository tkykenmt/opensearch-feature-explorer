---
tags:
  - domain/ml
  - component/server
  - ml
---
# ML Commons Sparse Encoding

## Summary

OpenSearch v3.2.0 adds TOKEN_ID format support for sparse encoding and sparse tokenize models. This enhancement allows users to choose between human-readable word tokens (default) or numeric token IDs as output format, reducing storage requirements and improving compatibility with certain vector operations.

## Details

### What's New in v3.2.0

This release introduces a new `sparse_embedding_format` parameter for sparse encoding (`SPARSE_ENCODING`) and sparse tokenize (`SPARSE_TOKENIZE`) models. Users can now select between two output formats at inference time:

- **WORD** (default): Human-readable token strings (e.g., `{"hello": 6.94, "world": 3.42}`)
- **TOKEN_ID**: Numeric token IDs from the tokenizer vocabulary (e.g., `{"7592": 6.94, "2088": 3.42}`)

### Technical Changes

#### New Components

| Component | Description |
|-----------|-------------|
| `SparseEmbeddingFormat` | New enum defining `WORD` and `TOKEN_ID` output formats |
| `AsymmetricTextEmbeddingParameters` | Extended to support sparse encoding algorithms with new `sparse_embedding_format` field |

#### Modified Components

| Component | Changes |
|-----------|---------|
| `SparseEncodingTranslator` | Processes `sparse_embedding_format` from input and converts output accordingly |
| `SparseTokenizerModel` | Reads format parameter and outputs token IDs or words based on selection |
| `TextEmbeddingModel` | Passes `sparse_embedding_format` to predictor input |
| `HFModelTokenizer` | Supports TOKEN_ID format via TypeAttribute for Lucene analysis |
| `MachineLearningPlugin` | Registers XContent entries for SPARSE_ENCODING and SPARSE_TOKENIZE parameters |

#### API Changes

The predict API now accepts `sparse_embedding_format` in the parameters object:

```json
POST _plugins/_ml/models/<model_id>/_predict
{
  "text_docs": ["hello world"],
  "parameters": {
    "sparse_embedding_format": "TOKEN_ID"
  }
}
```

#### Version Compatibility

- The `sparse_embedding_format` field is only serialized for OpenSearch v3.2.0 and later
- Older versions default to `WORD` format for backward compatibility
- Stream input/output handles version-aware serialization

### Usage Example

#### WORD Format (Default)
```json
POST _plugins/_ml/models/<sparse_model_id>/_predict
{
  "text_docs": ["hello world"],
  "parameters": {
    "sparse_embedding_format": "WORD"
  }
}

// Response
{
  "inference_results": [{
    "output": [{
      "dataAsMap": {
        "response": [{
          "hello": 6.9377565,
          "world": 3.4208686
        }]
      }
    }]
  }]
}
```

#### TOKEN_ID Format
```json
POST _plugins/_ml/models/<sparse_model_id>/_predict
{
  "text_docs": ["hello world"],
  "parameters": {
    "sparse_embedding_format": "TOKEN_ID"
  }
}

// Response
{
  "inference_results": [{
    "output": [{
      "dataAsMap": {
        "response": [{
          "7592": 6.9377565,
          "2088": 3.4208686
        }]
      }
    }]
  }]
}
```

### Migration Notes

- No migration required; existing models continue to work with default `WORD` format
- To use TOKEN_ID format, simply add the `sparse_embedding_format` parameter to predict requests
- Both sparse encoding and sparse tokenize models support this parameter

## Limitations

- TOKEN_ID format requires the model to have a tokenizer with vocabulary mapping
- Remote models may not support this parameter (depends on connector implementation)
- The format selection is per-request; there is no model-level default configuration

## References

### Documentation
- [Register Model API](https://docs.opensearch.org/3.0/ml-commons-plugin/api/model-apis/register-model/): Official documentation for model registration
- [Neural Sparse Search](https://docs.opensearch.org/3.0/vector-search/ai-search/neural-sparse-search/): Neural sparse search documentation

### Blog Posts
- [Improving document retrieval with sparse semantic encoders](https://opensearch.org/blog/improving-document-retrieval-with-sparse-semantic-encoders/): Blog post on sparse encoding

### Pull Requests
| PR | Description |
|----|-------------|
| [#3963](https://github.com/opensearch-project/ml-commons/pull/3963) | Sparse encoding/tokenize support TOKEN_ID format embedding |

### Issues (Design / RFC)
- [Issue #3865](https://github.com/opensearch-project/ml-commons/issues/3865): RFC - Support additional output formats for sparse models

## Related Feature Report

- [Full feature documentation](../../../../features/ml-commons/ml-commons-sparse-encoding.md)
