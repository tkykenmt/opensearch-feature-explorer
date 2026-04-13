---
tags:
  - ml-commons
---
# ML Commons Model Pooling

## Summary

OpenSearch v3.6.0 adds two new pooling modes for text embedding models in ML Commons: `LAST_TOKEN` and `NONE`. `LAST_TOKEN` pooling enables proper support for decoder-only embedding models (e.g., Qwen3-Embedding, GPT-style) by extracting the last non-padding token's embedding. `NONE` pooling fixes a bug where MEAN pooling was redundantly applied to models that already provide pre-pooled output, causing incorrect embeddings.

## Details

### What's New in v3.6.0

Two new values for the `pooling_mode` parameter in the Register Model API:

| Pooling Mode | Description | Use Case |
|-------------|-------------|----------|
| `lasttoken` | Extracts the embedding of the last non-padding token | Decoder-only models (GPT-style, Qwen3) where the final token captures cumulative context through causal attention |
| `none` | Uses pre-pooled output from the model directly without additional pooling | Models that already provide pooled embeddings (e.g., `sentence_embedding` or `pooler_output`) |

The full set of supported pooling modes is now: `mean`, `mean_sqrt_len`, `max`, `weightedmean`, `cls`, `lasttoken`, `none`.

### Technical Changes

#### LAST_TOKEN Pooling (PR #4711)

Adds `lastTokenPool()` method to both ONNX and TorchScript translators:

1. Sums the attention mask to determine the count of real (non-padding) tokens
2. Extracts the embedding at the last non-padding token position (index = token_count - 1)
3. Handles edge case of empty sequences by defaulting to index 0

Modified classes:
- `ONNXSentenceTransformerTextEmbeddingTranslator` — uses `toLongArray()` for int64 attention mask
- `HuggingfaceTextEmbeddingTranslator` — uses `toFloatArray()` for float32 attention mask

Validated with Qwen3-Embedding-0.6B producing correct 1024-dimensional normalized embeddings matching Python inference output.

#### NONE Pooling (PR #4710)

Adds `NONE("none")` to the `PoolingMode` enum in `BaseModelConfig` and updates both translators:

- `ONNXSentenceTransformerTextEmbeddingTranslator`: When pooling mode is NONE and multiple outputs exist, uses the second output (`sentence_embedding`) instead of the first (`token_embeddings`)
- `HuggingfaceTextEmbeddingTranslator`: Implements fallback logic for pre-pooled output: `sentence_embedding` → `pooler_output` → second output → first output

This fixes a bug where the ONNX translator always used the first output (token_embeddings) and applied MEAN pooling by default, even for models that already provide pre-pooled `sentence_embedding` output.

### Usage Example

Register a decoder-only embedding model with LAST_TOKEN pooling:

```json
POST /_plugins/_ml/models/_upload
{
  "name": "Qwen3-Embedding-0.6B",
  "model_format": "ONNX",
  "model_config": {
    "model_type": "qwen3",
    "embedding_dimension": 1024,
    "framework_type": "sentence_transformers",
    "pooling_mode": "lasttoken",
    "normalize_result": true
  }
}
```

Register a model with pre-pooled output using NONE pooling:

```json
POST /_plugins/_ml/models/_upload
{
  "name": "all-MiniLM-L6-v2",
  "model_format": "ONNX",
  "model_config": {
    "model_type": "bert",
    "embedding_dimension": 384,
    "framework_type": "sentence_transformers",
    "pooling_mode": "none",
    "normalize_result": true
  }
}
```

## Limitations

- `LAST_TOKEN` pooling is only appropriate for decoder-only models; using it with encoder-only models (BERT-style) will produce suboptimal embeddings
- `NONE` pooling requires the model to actually provide pre-pooled output; using it with models that only output token embeddings will produce incorrect results

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| `https://github.com/opensearch-project/ml-commons/pull/4711` | Add LAST_TOKEN pooling implementation for text embedding models | `https://github.com/opensearch-project/ml-commons/issues/4709` |
| `https://github.com/opensearch-project/ml-commons/pull/4710` | Add NONE pooling mode to support pre-pooled model outputs | `https://github.com/opensearch-project/ml-commons/issues/4708` |

### Documentation

- `https://github.com/opensearch-project/documentation-website/issues/12076` — LAST_TOKEN pooling documentation request
- `https://github.com/opensearch-project/documentation-website/issues/12075` — NONE pooling documentation request
