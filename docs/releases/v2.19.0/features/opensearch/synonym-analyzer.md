---
tags:
  - opensearch
---
# Synonym Analyzer

## Summary

OpenSearch v2.19.0 introduces a new `synonym_analyzer` configuration setting for the `synonym` and `synonym_graph` token filters. This setting allows users to specify a custom analyzer for reading and parsing synonym files, solving compatibility issues when using certain token filters (like `word_delimiter_graph` or `hunspell`) before synonym expansion.

## Details

### What's New in v2.19.0

The `synonym_analyzer` parameter enables users to specify a separate analyzer for parsing synonym rules, independent of the analyzer chain where the synonym filter is used. This addresses a long-standing limitation where certain token filters could not be used before synonym filters due to token graph parsing restrictions.

### Problem Solved

Previously, when using filters like `word_delimiter_graph` or `hunspell` before `synonym_graph`, users encountered errors such as:

```
Token filter [custom_word_delimiter] cannot be used to parse synonyms
```

This occurred because OpenSearch used the preceding filters in the analyzer chain to parse the synonym file, and some filters (those producing token graphs or modifying token positions) are incompatible with synonym parsing.

### Configuration

The new `synonym_analyzer` parameter can be added to both `synonym` and `synonym_graph` filter configurations:

```json
PUT /my-index
{
  "settings": {
    "analysis": {
      "filter": {
        "custom_synonym_graph_filter": {
          "type": "synonym_graph",
          "synonyms_path": "synonyms.txt",
          "synonym_analyzer": "standard"
        }
      },
      "analyzer": {
        "my_analyzer": {
          "tokenizer": "whitespace",
          "filter": [
            "lowercase",
            "custom_word_delimiter",
            "custom_synonym_graph_filter",
            "flatten_graph"
          ]
        }
      }
    }
  }
}
```

### Technical Changes

The implementation modifies the `AnalysisPlugin` interface to provide access to the `AnalysisModule`, allowing synonym filters to look up analyzers by name from the analysis registry:

- `SynonymTokenFilterFactory` now accepts an `AnalysisRegistry` parameter
- `SynonymGraphTokenFilterFactory` inherits the same capability
- When `synonym_analyzer` is specified, the filter uses that analyzer instead of building one from the preceding filters

## Limitations

- The `synonym_analyzer` must be a valid, registered analyzer name
- If the specified analyzer doesn't exist, the filter falls back to the default behavior
- The analyzer used for synonyms should be compatible with the synonym format being used

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16488](https://github.com/opensearch-project/OpenSearch/pull/16488) | Add new configuration setting `synonym_analyzer` for `synonym` and `synonym_graph` filters | [#16263](https://github.com/opensearch-project/OpenSearch/issues/16263), [#16530](https://github.com/opensearch-project/OpenSearch/issues/16530) |

### Related Issues

- [#16263](https://github.com/opensearch-project/OpenSearch/issues/16263) - Token Filter Order: word_delimiter_graph and synonym_graph
- [#16530](https://github.com/opensearch-project/OpenSearch/issues/16530) - Using synonym filter after hunspell
