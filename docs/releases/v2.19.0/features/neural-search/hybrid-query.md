---
tags:
  - neural-search
---
# Hybrid Query

## Summary

OpenSearch v2.19.0 brings significant enhancements to hybrid query functionality, including pagination support, Reciprocal Rank Fusion (RRF) score normalization, explainability via the `explain` flag, and critical bug fixes for scoring consistency.

## Details

### What's New in v2.19.0

#### Pagination Support

Hybrid queries now support pagination using the `pagination_depth` parameter, enabling users to navigate through large result sets efficiently.

Key features:
- New `pagination_depth` parameter in hybrid query clause
- Works with standard `from` and `size` parameters
- Handles single shard scenarios where fetch phase runs before normalization
- Scroll operation is disabled for hybrid queries

```json
GET /my-index/_search?search_pipeline=hybrid-pipeline
{
  "from": 20,
  "size": 10,
  "query": {
    "hybrid": {
      "pagination_depth": 100,
      "queries": [
        { "match": { "text": "search terms" } },
        { "neural": { "embedding": { "query_text": "semantic query", "model_id": "xxx", "k": 10 } } }
      ]
    }
  }
}
```

#### Reciprocal Rank Fusion (RRF)

A new `score-ranker-processor` enables RRF-based score combination, providing an alternative to score-based normalization techniques.

RRF calculates scores using the formula: `score = 1 / (rank_constant + rank)`

Key features:
- Rank-based scoring reduces sensitivity to score magnitude differences
- Configurable `rank_constant` parameter (default: 60)
- Smaller score deltas between documents compared to score-based methods

```json
PUT /_search/pipeline/rrf-pipeline
{
  "phase_results_processors": [
    {
      "score-ranker-processor": {
        "combination": {
          "technique": "rrf",
          "parameters": {
            "rank_constant": 60
          }
        }
      }
    }
  ]
}
```

#### Explainability

Hybrid queries now support the `explain` flag to help users understand how final scores are computed.

Key features:
- Shows normalization technique applied (e.g., `min_max normalization of:`)
- Displays combination technique and weights (e.g., `arithmetic_mean, weights [0.3, 0.7] combination of:`)
- Requires `explanation_response_processor` in the search pipeline

```json
PUT /_search/pipeline/explain-pipeline
{
  "phase_results_processors": [
    {
      "normalization-processor": {
        "normalization": { "technique": "min_max" },
        "combination": { "technique": "arithmetic_mean", "parameters": { "weights": [0.3, 0.7] } }
      }
    }
  ],
  "response_processors": [
    { "explanation_response_processor": {} }
  ]
}
```

Example response with `explain=true`:
```json
{
  "_explanation": {
    "value": 1.0,
    "description": "arithmetic_mean, weights [0.3, 0.7] combination of:",
    "details": [
      {
        "value": 1.0,
        "description": "min_max normalization of:",
        "details": [{ "value": 1.0, "description": "field1:[0 TO 500]", "details": [] }]
      },
      {
        "value": 1.0,
        "description": "min_max normalization of:",
        "details": [{ "value": 0.026301946, "description": "within top 12", "details": [] }]
      }
    ]
  }
}
```

### Bug Fixes

#### Inconsistent Scoring Fix (PR #998)

Fixed a critical bug where hybrid queries with complex sub-queries could produce inconsistent scores or `e_o_f_exception` errors.

Root cause: When sub-queries use `DocIdSetIterator` with two-phase approximation (introduced in 2.13), the iterator and two-phase scorer could go out of sync, pointing to different document IDs.

#### Sorted Hybrid Query Mismatch Fix (PR #1043)

Fixed document source and score field mismatch in sorted hybrid queries.

Root cause: The min heap used for sorting maintained only a single leaf element, but hybrid queries require separate elements for each sub-query. This caused incorrect propagation of updates across sub-query results.

## Limitations

- Scroll operation is not supported with hybrid queries
- Explain by document ID (`_explain/{doc_id}`) is not supported; only search-level explain is available
- RRF does not currently support weights when combining processed sub-query scores

## References

### Documentation
- [Paginating Hybrid Query Results](https://docs.opensearch.org/2.19/vector-search/ai-search/hybrid-search/pagination/)
- [Hybrid Search Explain](https://docs.opensearch.org/2.19/vector-search/ai-search/hybrid-search/explain/)
- [Score Ranker Processor](https://docs.opensearch.org/2.19/search-plugins/search-pipelines/score-ranker-processor/)
- [Hybrid Query DSL](https://docs.opensearch.org/2.19/query-dsl/compound/hybrid/)

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1048](https://github.com/opensearch-project/neural-search/pull/1048) | Pagination in Hybrid query | [#280](https://github.com/opensearch-project/neural-search/issues/280) |
| [#874](https://github.com/opensearch-project/neural-search/pull/874) | Reciprocal Rank Fusion (RRF) normalization technique | [#865](https://github.com/opensearch-project/neural-search/issues/865), [#659](https://github.com/opensearch-project/neural-search/issues/659) |
| [#970](https://github.com/opensearch-project/neural-search/pull/970) | Explainability in hybrid query | [#658](https://github.com/opensearch-project/neural-search/issues/658), [#905](https://github.com/opensearch-project/neural-search/issues/905) |
| [#998](https://github.com/opensearch-project/neural-search/pull/998) | Address inconsistent scoring in hybrid query results | [#964](https://github.com/opensearch-project/neural-search/issues/964) |
| [#1043](https://github.com/opensearch-project/neural-search/pull/1043) | Fixed document source and score field mismatch in sorted hybrid queries | [#1044](https://github.com/opensearch-project/neural-search/issues/1044) |
