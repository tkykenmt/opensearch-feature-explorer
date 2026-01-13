---
tags:
  - domain/search
  - component/server
  - ml
  - neural-search
  - observability
  - search
---
# Neural Search Stats

## Summary

OpenSearch v3.1.0 introduces comprehensive statistics tracking for the Neural Search plugin. The Stats API provides cluster-level and node-level metrics for monitoring semantic and hybrid search features, including ingest processors, search processors, and query execution.

## Details

### What's New in v3.1.0

This release adds extensive statistics coverage across all Neural Search components:

- **Text Chunking Processor Stats**: Track executions and processor counts for delimiter and fixed-length chunking algorithms
- **Text Embedding Processor Stats**: Monitor embedding processor executions with `skip_existing` flag tracking
- **Hybrid Query Stats**: Track hybrid query requests including filter, inner hits, and pagination usage
- **Normalization Processor Stats**: Monitor score-based and rank-based normalization with algorithm-specific metrics
- **Semantic Highlighting Stats**: Track semantic highlighting request counts
- **Additional Processor Stats**: Coverage for sparse encoding, neural query enricher, reranker, and text-image embedding processors
- **API Enhancements**: New query parameters for flexible stats retrieval

### Technical Changes

#### Architecture

```mermaid
graph TB
    subgraph "Stats API"
        API[/_plugins/_neural/stats]
        Params[Query Parameters]
    end
    
    subgraph "Stats Categories"
        Info[Info Stats<br/>Cluster-level]
        AllNodes[All Nodes Stats<br/>Aggregated]
        Nodes[Node Stats<br/>Per-node]
    end
    
    subgraph "Tracked Components"
        Ingest[Ingest Processors]
        Search[Search Processors]
        Query[Query Stats]
        Highlight[Semantic Highlighting]
    end
    
    API --> Info
    API --> AllNodes
    API --> Nodes
    Params --> API
    
    Info --> Ingest
    AllNodes --> Ingest
    AllNodes --> Search
    AllNodes --> Query
    AllNodes --> Highlight
    Nodes --> Ingest
    Nodes --> Search
    Nodes --> Query
    Nodes --> Highlight
```

#### New Statistics

| Category | Statistic | Description |
|----------|-----------|-------------|
| Ingest | `text_chunking_executions` | Total text chunking processor executions |
| Ingest | `text_chunking_delimiter_executions` | Delimiter-based chunking executions |
| Ingest | `text_chunking_fixed_length_executions` | Fixed-length chunking executions |
| Ingest | `text_embedding_executions` | Text embedding processor executions |
| Ingest | `sparse_encoding_executions` | Sparse encoding processor executions |
| Ingest | `text_image_embedding_executions` | Text-image embedding executions |
| Ingest | `skip_existing_executions` | Executions with skip_existing flag |
| Search | `normalization_processor_executions` | Score-based normalization executions |
| Search | `rank_based_normalization_processor_executions` | RRF normalization executions |
| Search | `comb_arithmetic_executions` | Arithmetic combination executions |
| Search | `comb_geometric_executions` | Geometric combination executions |
| Search | `comb_harmonic_executions` | Harmonic combination executions |
| Search | `comb_rrf_executions` | RRF combination executions |
| Search | `norm_l2_executions` | L2 normalization executions |
| Search | `norm_minmax_executions` | Min-max normalization executions |
| Search | `norm_zscore_executions` | Z-score normalization executions |
| Search | `neural_query_enricher_executions` | Neural query enricher executions |
| Search | `neural_sparse_two_phase_executions` | Neural sparse two-phase executions |
| Search | `rerank_ml_executions` | ML reranker executions |
| Search | `rerank_by_field_executions` | By-field reranker executions |
| Query | `hybrid_query_requests` | Total hybrid query requests |
| Query | `hybrid_query_with_filter_requests` | Hybrid queries with filters |
| Query | `hybrid_query_with_inner_hits_requests` | Hybrid queries with inner hits |
| Query | `hybrid_query_with_pagination_requests` | Hybrid queries with pagination |
| Highlight | `semantic_highlighting_request_count` | Semantic highlighting requests |

#### New API Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `include_individual_nodes` | `true` | Include per-node statistics |
| `include_all_nodes` | `true` | Include aggregated cluster statistics |
| `include_info` | `true` | Include cluster-level info statistics |

### Usage Example

Enable statistics collection:
```json
PUT /_cluster/settings
{
  "persistent": {
    "plugins.neural_search.stats_enabled": "true"
  }
}
```

Retrieve stats with selective output:
```bash
GET /_plugins/_neural/stats?include_individual_nodes=false
```

Example response:
```json
{
  "_nodes": { "total": 1, "successful": 1, "failed": 0 },
  "cluster_name": "integTest",
  "info": {
    "cluster_version": "3.1.0",
    "processors": {
      "search": {
        "hybrid": {
          "normalization_processors": 0,
          "rank_based_normalization_processors": 0
        }
      },
      "ingest": {
        "text_chunking_processors": 0,
        "text_embedding_processors_in_pipelines": 0,
        "sparse_encoding_processors": 0
      }
    }
  },
  "all_nodes": {
    "query": {
      "hybrid": {
        "hybrid_query_requests": 0,
        "hybrid_query_with_filter_requests": 0
      }
    },
    "semantic_highlighting": {
      "semantic_highlighting_request_count": 0
    },
    "processors": {
      "search": {
        "hybrid": {
          "normalization_processor_executions": 0,
          "comb_arithmetic_executions": 0
        }
      },
      "ingest": {
        "text_embedding_executions": 0,
        "text_chunking_executions": 0
      }
    }
  }
}
```

## Limitations

- Statistics collection is disabled by default and must be enabled via cluster settings
- When disabled, all values reset and new statistics are not collected
- Statistics are reset on node restart

## References

### Documentation
- [Neural Search Stats API Documentation](https://docs.opensearch.org/3.0/vector-search/api/neural/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#1308](https://github.com/opensearch-project/neural-search/pull/1308) | Add stats for text chunking processor algorithms |
| [#1327](https://github.com/opensearch-project/neural-search/pull/1327) | Add stats tracking for semantic highlighting |
| [#1332](https://github.com/opensearch-project/neural-search/pull/1332) | Add stats for text embedding processor with skip_existing flag |
| [#1326](https://github.com/opensearch-project/neural-search/pull/1326) | Add stats for score/rank based normalization and hybrid query |
| [#1343](https://github.com/opensearch-project/neural-search/pull/1343) | Add stats for neural query enricher, sparse encoding, reranker, text-image embedding |
| [#1360](https://github.com/opensearch-project/neural-search/pull/1360) | Add `include_individual_nodes`, `include_all_nodes`, `include_info` params |
| [#1378](https://github.com/opensearch-project/neural-search/pull/1378) | Combine skip_existing flag stats into single stat |

### Issues (Design / RFC)
- [Issue #1146](https://github.com/opensearch-project/neural-search/issues/1146): Stats for normalization processor
- [Issue #1104](https://github.com/opensearch-project/neural-search/issues/1104): Stats API parameters
- [Issue #1182](https://github.com/opensearch-project/neural-search/issues/1182): Semantic highlighting stats

## Related Feature Report

- Full feature documentation
