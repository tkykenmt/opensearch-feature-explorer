---
tags:
  - opensearch
---
# Flat Object Field Enhancements

## Summary

OpenSearch v2.19.0 brings significant improvements to the `flat_object` field type, including support for searching from DocValues using `termQuery` and `termQueryCaseInsensitive` even when `index=false`, and a major performance optimization that reduces JSON parsing from two passes to a single pass.

## Details

### What's New in v2.19.0

#### 1. DocValues-Based Term Query Support

Previously, `flat_object` and `keyword` fields could not be searched using `termQuery` or `termQueryCaseInsensitive` when `index=false`. This was inconsistent with numeric fields which supported DocValues-based searching. In v2.19.0, this limitation is removed.

**Key Changes:**
- `termQuery` now falls back to DocValues when the field is not indexed but has DocValues enabled
- `termQueryCaseInsensitive` supports case-insensitive searching via DocValues using automaton queries
- Both `flat_object` and `keyword` field types benefit from this enhancement

**Example:**
```json
PUT /test-index
{
  "mappings": {
    "properties": {
      "metadata": {
        "type": "flat_object"
      }
    }
  }
}

// Case-insensitive term query now works even with index=false
GET /test-index/_search
{
  "query": {
    "term": {
      "metadata.labels.name": {
        "value": "ABC",
        "case_insensitive": true
      }
    }
  }
}
```

#### 2. Single-Pass Parsing Performance Optimization

The `flat_object` field parsing has been optimized from a two-pass approach to a single-pass approach, significantly improving indexing performance.

**Benchmark Results (noaa workload with `station` field as `flat_object`):**

| Metric | Baseline | Contender | Improvement |
|--------|----------|-----------|-------------|
| Mean Throughput | 142,195 docs/s | 144,423 docs/s | +1.6% |
| Median Throughput | 143,126 docs/s | 146,146 docs/s | +2.1% |
| 90th percentile latency | 544.9 ms | 505.0 ms | -7.3% |
| 99th percentile latency | 1,225.6 ms | 1,162.6 ms | -5.1% |
| 99.9th percentile latency | 1,867.9 ms | 1,568.1 ms | -16.0% |

**Technical Changes:**
- Removed `JsonToStringXContentParser` class (two-pass parsing)
- Integrated parsing directly into `FlatObjectFieldMapper`
- Simplified internal field handling by removing separate `ValueFieldMapper` and `ValueAndPathFieldMapper` classes
- Improved code maintainability by consolidating parsing logic

### Technical Changes

| Component | Change |
|-----------|--------|
| `FlatObjectFieldMapper` | Refactored to use single-pass parsing, removed nested mapper classes |
| `KeywordFieldMapper` | Added `termQuery` and `termQueryCaseInsensitive` support for DocValues-only fields |
| `JsonToStringXContentParser` | Removed (functionality merged into FlatObjectFieldMapper) |
| `DocValueFetcher` | Updated to handle flat_object DocValue format |

## Limitations

- DocValues retrieval still requires full dot-path notation (root field not supported)
- Aggregations on subfields using dot notation remain unsupported
- Painless scripting for subfield value retrieval is not supported

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16974](https://github.com/opensearch-project/OpenSearch/pull/16974) | Support searching from doc_value using termQueryCaseInsensitive/termQuery in flat_object/keyword field | [#16973](https://github.com/opensearch-project/OpenSearch/issues/16973) |
| [#16297](https://github.com/opensearch-project/OpenSearch/pull/16297) | Improve flat_object field parsing performance by reducing two passes to a single pass | - |
| [#16802](https://github.com/opensearch-project/OpenSearch/pull/16802) | Added ability to retrieve value from DocValues in flat_object field | [#16742](https://github.com/opensearch-project/OpenSearch/issues/16742) |

### Documentation
- [Flat object documentation](https://docs.opensearch.org/latest/field-types/supported-field-types/flat-object/)
