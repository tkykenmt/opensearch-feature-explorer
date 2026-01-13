---
tags:
  - neural-search
---
# Neural Search General Enhancements

## Summary

OpenSearch v2.19.0 includes several enhancements and bug fixes for the Neural Search plugin, improving text embedding processor flexibility, ML inference reliability, NeuralQueryBuilder API usability, and hybrid query validation.

## Details

### What's New in v2.19.0

#### Empty String Support in Text Embedding Processor

The text embedding processor now supports empty string values for fields in the field map. Previously, documents with empty or whitespace-only values in mapped fields would fail ingestion with an error. Now, fields with empty strings are treated as `null` and skipped during embedding generation, allowing partial document ingestion.

**Before v2.19.0:**
```json
{
  "error": {
    "type": "illegal_argument_exception",
    "reason": "map type field [description] has empty string value, cannot process it"
  }
}
```

**After v2.19.0:**
Documents with empty fields are ingested successfully, with embeddings generated only for non-empty fields.

#### ML Inference Connection Retry Optimization

The ML inference connection retry logic has been optimized with exponential backoff and jitter:
- Base delay: 500ms
- Maximum retries: 3
- Jitter: 10-50ms random delay

This improves reliability when connecting to ML models during transient network issues or node disconnections.

#### NeuralQueryBuilder Builder Pattern Support

Added Lombok `@Builder` annotation support to `NeuralQueryBuilder`, enabling fluent builder-style construction of neural queries programmatically.

#### Hybrid Query Validation for Disjunction Queries

Added validation in `HybridQueryPhaseSearcher` to prevent hybrid queries from being nested inside `dis_max` (disjunction) queries. Hybrid queries must be top-level queries and cannot be wrapped in other query types.

**Error Response:**
```json
{
  "error": {
    "type": "illegal_argument_exception",
    "reason": "hybrid query must be a top level query and cannot be wrapped into other queries"
  }
}
```

### Bug Fixes

#### Nested Object List Ingestion Fix

Fixed a bug where ingestion failed for documents containing lists of nested objects. The text embedding processor now correctly handles documents with nested object arrays in the field map.

**Related Issue:** [#1024](https://github.com/opensearch-project/neural-search/issues/1024)

#### Dot Notation Field Name Fix

Fixed a bug where document embedding failed when field names contained dots. The processor now correctly unflattens/unboxes fields with dot notation to match the field map configuration.

**Example:** A field like `{"a.b": "c"}` is now correctly matched against a field map entry `{"a": {"b": "b_embedding"}}`.

**Related Issue:** [#1042](https://github.com/opensearch-project/neural-search/issues/1042)

#### NeuralQueryBuilder Equality and HashCode Fix

Corrected `doEquals()` and `doHashCode()` methods in `NeuralQueryBuilder` to consider all parameters, ensuring proper behavior when used with caching mechanisms. Also fixed handling of `queryImage` parameter to be consistent with `queryText`.

**Related Issue:** [#1010](https://github.com/opensearch-project/neural-search/issues/1010)

## Limitations

- Hybrid queries cannot be nested inside other query types (e.g., `dis_max`, `bool`)
- Empty string handling only applies to text embedding processor; other processors may behave differently

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1041](https://github.com/opensearch-project/neural-search/pull/1041) | Support empty string for fields in text embedding processor | [#774](https://github.com/opensearch-project/neural-search/issues/774) |
| [#1054](https://github.com/opensearch-project/neural-search/pull/1054) | Optimize ML inference connection retry logic | [#431](https://github.com/opensearch-project/neural-search/issues/431) |
| [#1047](https://github.com/opensearch-project/neural-search/pull/1047) | Support for builder constructor in Neural Query Builder | [#1025](https://github.com/opensearch-project/neural-search/issues/1025) |
| [#1127](https://github.com/opensearch-project/neural-search/pull/1127) | Validate Disjunction query to avoid nested hybrid queries | [#1125](https://github.com/opensearch-project/neural-search/issues/1125) |
| [#1040](https://github.com/opensearch-project/neural-search/pull/1040) | Fix bug where ingested document has list of nested objects | [#1024](https://github.com/opensearch-project/neural-search/issues/1024) |
| [#1045](https://github.com/opensearch-project/neural-search/pull/1045) | Update NeuralQueryBuilder doEquals() and doHashCode() | [#1010](https://github.com/opensearch-project/neural-search/issues/1010) |
| [#1062](https://github.com/opensearch-project/neural-search/pull/1062) | Fix bug where embedding fails for fields with dot in name | [#1042](https://github.com/opensearch-project/neural-search/issues/1042) |

### Documentation

- [Text Embedding Processor](https://docs.opensearch.org/2.19/ingest-pipelines/processors/text-embedding/)
- [Neural Query](https://docs.opensearch.org/2.19/query-dsl/specialized/neural/)
