---
tags:
  - neural-search
---
# Neural Search Enhancements

## Summary

This document covers general enhancements and improvements to the Neural Search plugin that improve text embedding processor flexibility, ML inference reliability, query builder usability, and query validation.

## Details

### Text Embedding Processor

The text embedding processor generates vector embeddings from text fields during document ingestion.

#### Empty String Handling

The processor supports empty string values in field maps. Fields with empty or whitespace-only values are treated as `null` and skipped during embedding generation, allowing documents with partial data to be ingested successfully.

**Pipeline Configuration:**
```json
{
  "processors": [
    {
      "text_embedding": {
        "model_id": "<model_id>",
        "field_map": {
          "title": "title_embedding",
          "description": "description_embedding",
          "body": "body_embedding"
        }
      }
    }
  ]
}
```

**Document with Empty Field:**
```json
{
  "title": "Sample Title",
  "description": " ",
  "body": "Sample body text"
}
```

Result: Embeddings generated for `title` and `body` only; `description` is skipped.

#### Nested Object Support

The processor correctly handles documents containing:
- Lists of nested objects
- Fields with dot notation in names (e.g., `{"a.b": "value"}`)

The processor unflattens dot-notation fields to match field map configurations.

### ML Inference Retry Logic

ML inference connections use exponential backoff with jitter for improved reliability:

| Parameter | Value |
|-----------|-------|
| Base delay | 500ms |
| Max retries | 3 |
| Jitter range | 10-50ms |

This handles transient network issues and node disconnections gracefully.

### NeuralQueryBuilder

#### Builder Pattern

The `NeuralQueryBuilder` supports Lombok `@Builder` annotation for fluent construction:

```java
NeuralQueryBuilder query = NeuralQueryBuilder.builder()
    .fieldName("embedding_field")
    .queryText("search query")
    .modelId("model_id")
    .k(10)
    .build();
```

#### Equality and HashCode

The `doEquals()` and `doHashCode()` methods consider all parameters including `queryImage`, ensuring correct behavior with caching mechanisms.

### Hybrid Query Validation

Hybrid queries must be top-level queries and cannot be nested inside other query types such as `dis_max` or `bool` queries.

**Invalid Query (returns error):**
```json
{
  "query": {
    "dis_max": {
      "queries": [
        { "match": { "title": "text" } },
        { "hybrid": { "queries": [...] } }
      ]
    }
  }
}
```

**Error:**
```
hybrid query must be a top level query and cannot be wrapped into other queries
```

## Limitations

- Empty string handling applies only to text embedding processor
- Hybrid queries cannot be nested in compound queries
- ML inference retry is limited to 3 attempts

## Change History

- **v2.19.0** (2025-02): Added empty string support in text embedding processor, optimized ML inference retry logic, added builder pattern to NeuralQueryBuilder, fixed nested object ingestion, fixed dot notation field handling, fixed NeuralQueryBuilder equality/hashCode, added hybrid query validation

## References

### Documentation

- [Text Embedding Processor](https://docs.opensearch.org/latest/ingest-pipelines/processors/text-embedding/)
- [Neural Query](https://docs.opensearch.org/latest/query-dsl/specialized/neural/)

### Pull Requests

| Version | PR | Description |
|---------|-----|-------------|
| v2.19.0 | [#1041](https://github.com/opensearch-project/neural-search/pull/1041) | Support empty string for fields in text embedding processor |
| v2.19.0 | [#1054](https://github.com/opensearch-project/neural-search/pull/1054) | Optimize ML inference connection retry logic |
| v2.19.0 | [#1047](https://github.com/opensearch-project/neural-search/pull/1047) | Support for builder constructor in Neural Query Builder |
| v2.19.0 | [#1127](https://github.com/opensearch-project/neural-search/pull/1127) | Validate Disjunction query to avoid nested hybrid queries |
| v2.19.0 | [#1040](https://github.com/opensearch-project/neural-search/pull/1040) | Fix nested object list ingestion |
| v2.19.0 | [#1045](https://github.com/opensearch-project/neural-search/pull/1045) | Fix NeuralQueryBuilder doEquals() and doHashCode() |
| v2.19.0 | [#1062](https://github.com/opensearch-project/neural-search/pull/1062) | Fix dot notation field name handling |
