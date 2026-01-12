---
tags:
  - indexing
  - observability
  - search
---

# Wildcard Field

## Summary

The wildcard field type is a specialized string field designed for efficient wildcard (`*`), prefix, and regular expression queries on arbitrary substrings. Unlike standard `text` fields that tokenize content, wildcard fields use n-gram indexing to enable fast pattern matching without token boundaries, making them ideal for log analysis, code search, and other use cases where substring matching is required.

## Details

### Architecture

```mermaid
graph TB
    subgraph "Indexing"
        Input[Input String] --> Tokenizer[WildcardFieldTokenizer]
        Tokenizer --> NGrams[3-gram Tokens]
        NGrams --> Index[Inverted Index]
    end
    
    subgraph "Querying"
        Query[Wildcard Query] --> Extract[Extract Required N-grams]
        Extract --> Candidate[Candidate Document Filter]
        Candidate --> Verify[Second-Phase Verification]
        Verify --> Results[Final Results]
    end
    
    Index --> Candidate
```

### Data Flow

```mermaid
flowchart TB
    A[Document] --> B[Wildcard Field Mapper]
    B --> C[N-gram Tokenizer]
    C --> D[Index Terms]
    
    E[Search Query] --> F[Pattern Analysis]
    F --> G[N-gram Extraction]
    G --> H[Index Lookup]
    H --> I[Candidate Docs]
    I --> J[Pattern Verification]
    J --> K[Results]
```

### Components

| Component | Description |
|-----------|-------------|
| `WildcardFieldMapper` | Main field mapper that handles indexing and query building |
| `WildcardFieldTokenizer` | Custom tokenizer that generates 3-gram tokens with anchors |
| `WildcardFieldType` | Field type implementation with query methods |
| `WildcardMatchingQuery` | Two-phase query with approximation and verification |

### How It Works

1. **Indexing**: Input strings are split into overlapping 3-character sequences (trigrams) with special anchor characters (null bytes) marking string boundaries
2. **Query Processing**: Search patterns are analyzed to extract required n-grams
3. **Two-Phase Search**: 
   - First phase: Fast index lookup for candidate documents containing required n-grams
   - Second phase: Exact pattern matching against source values to filter false positives

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `doc_values` | Enable doc values for aggregations/sorting | `true` (since v3.4.0, was `false` before) |
| `ignore_above` | Maximum string length to index | `2147483647` |
| `normalizer` | Normalizer for preprocessing (e.g., `lowercase`) | none |
| `null_value` | Value to use for null fields | `null` |

### Usage Example

Create an index with a wildcard field:

```json
PUT logs
{
  "mappings": {
    "properties": {
      "log_line": {
        "type": "wildcard",
        "fields": {
          "lower": {
            "type": "wildcard",
            "normalizer": "lowercase"
          }
        }
      }
    }
  }
}
```

Index documents:

```json
POST logs/_bulk
{"index": {"_id": 1}}
{"log_line": "org.opensearch.transport.NodeDisconnectedException: [node_s0] disconnected"}
{"index": {"_id": 2}}
{"log_line": "[2024-06-08T06:31:37,443][INFO] cluster-manager node failed"}
```

Search with wildcard patterns:

```json
GET logs/_search
{
  "query": {
    "wildcard": {
      "log_line": {
        "value": "*Exception*disconnected*"
      }
    }
  }
}
```

Case-insensitive search using the normalized sub-field:

```json
GET logs/_search
{
  "query": {
    "wildcard": {
      "log_line.lower": {
        "value": "*exception*"
      }
    }
  }
}
```

## Limitations

- **Exact match queries**: `term` and `terms` queries are less efficient on wildcard fields compared to `keyword` fields
- **Short patterns**: Patterns with fewer than 3 consecutive non-wildcard characters may result in broader index scans
- **Storage overhead**: While optimized in v3.0.0, wildcard fields still require more storage than keyword fields due to n-gram indexing
- **Not for full-text search**: Wildcard fields don't support full-text analysis; use `text` fields for natural language content

## Change History

- **v3.4.0** (2025-11-18): Changed `doc_values` default from `false` to `true`, fixing nested query issues
- **v3.3.0** (2025-09-10): Fixed sorting bug when `doc_values` enabled by disabling Lucene's dynamic pruning optimization
- **v3.0.0** (2025-05-06): Changed indexing strategy from 1-3 gram to 3-gram only, reducing index size by ~20% and improving write throughput by 5-30%
- **v2.18.0** (2024-11-05): Fixed escaped wildcard character handling and case-insensitive query behavior
- **v2.15.0** (2024-06-25): Initial introduction of wildcard field type with 1-3 gram indexing

## Related Features
- [OpenSearch Dashboards](../opensearch-dashboards/opensearch-dashboards-ai-chat.md)

## References

### Documentation
- [Wildcard Field Documentation](https://docs.opensearch.org/3.0/field-types/supported-field-types/wildcard/): Official documentation

### Blog Posts
- [OpenSearch 2.15 Blog](https://opensearch.org/blog/diving-into-opensearch-2-15/): Initial feature announcement

### Pull Requests
| Version | PR | Description | Related Issue |
|---------|-----|-------------|---------------|
| v3.4.0 | [#19796](https://github.com/opensearch-project/OpenSearch/pull/19796) | Change doc_values default to true | [#18678](https://github.com/opensearch-project/OpenSearch/issues/18678) |
| v3.3.0 | [#18568](https://github.com/opensearch-project/OpenSearch/pull/18568) | Fix sorting bug by disabling pruning for doc_values |   |
| v3.0.0 | [#17349](https://github.com/opensearch-project/OpenSearch/pull/17349) | Optimize to 3-gram only indexing | [#17099](https://github.com/opensearch-project/OpenSearch/issues/17099) |
| v2.18.0 | [#15737](https://github.com/opensearch-project/OpenSearch/pull/15737) | Fix wildcard query containing escaped character | [#15555](https://github.com/opensearch-project/OpenSearch/issues/15555) |
| v2.18.0 | [#15882](https://github.com/opensearch-project/OpenSearch/pull/15882) | Fix case-insensitive query on wildcard field | [#15855](https://github.com/opensearch-project/OpenSearch/issues/15855) |
| v2.15.0 | Initial | Wildcard field type introduction |   |

### Issues (Design / RFC)
- [Issue #18678](https://github.com/opensearch-project/OpenSearch/issues/18678): Bug report for nested query on wildcard field returning no results
- [Issue #18461](https://github.com/opensearch-project/OpenSearch/issues/18461): Bug report for wildcard sort error with doc_values
- [Issue #17099](https://github.com/opensearch-project/OpenSearch/issues/17099): 3-gram optimization feature request with benchmarks
- [Issue #15555](https://github.com/opensearch-project/OpenSearch/issues/15555): Bug report for escaped wildcard character handling
- [Issue #15855](https://github.com/opensearch-project/OpenSearch/issues/15855): Bug report for case-insensitive query issue
