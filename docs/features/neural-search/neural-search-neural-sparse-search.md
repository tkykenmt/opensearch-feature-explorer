---
tags:
  - neural-search
---
# Neural Sparse Search

## Summary

Neural sparse search is a semantic search technique that uses sparse vector representations to find relevant documents. Unlike dense vector search which uses fixed-dimension embeddings, sparse vectors have variable dimensions where each dimension corresponds to a vocabulary token with an associated weight. This approach combines the interpretability of keyword search with the semantic understanding of neural models.

## Details

### Architecture

```mermaid
graph TB
    subgraph "Indexing"
        A[Document] --> B[Sparse Encoding Model]
        B --> C[Sparse Vector]
        C --> D[rank_features Field]
    end
    
    subgraph "Query Processing"
        E[Query Text] --> F{Encoding Method}
        F -->|model_id| G[ML Commons Model]
        F -->|analyzer| H[Lucene Analyzer]
        F -->|query_tokens| I[Direct Tokens]
        G --> J[Query Tokens]
        H --> J
        I --> J
    end
    
    subgraph "Search"
        J --> K[BooleanQuery]
        K --> L[FeatureField Queries]
        L --> M[Ranked Results]
    end
```

### Data Flow

```mermaid
flowchart TB
    A[Query Text] --> B{Encoding Method}
    B -->|ML Model| C[ML Commons Inference]
    B -->|Analyzer| D[Lucene TokenStream]
    B -->|Raw Tokens| E[Direct Token Map]
    C --> F[Token-Weight Map]
    D --> F
    E --> F
    F --> G[Build BooleanQuery]
    G --> H[FeatureField.newLinearQuery per token]
    H --> I[Execute Search]
    I --> J[Return Results]
```

### Components

| Component | Description |
|-----------|-------------|
| `NeuralSparseQueryBuilder` | Query builder that constructs neural sparse queries from text, model, analyzer, or raw tokens |
| `NeuralSparseQueryTwoPhaseInfo` | Encapsulates two-phase execution state for query optimization |
| `sparse_encoding` processor | Ingest processor that generates sparse vectors from text during indexing |
| `neural_sparse_two_phase` processor | Search pipeline processor for two-phase query optimization |

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `query_text` | The text to encode into sparse vectors | Required (unless `query_tokens` provided) |
| `model_id` | ID of the sparse encoding model in ML Commons | Optional |
| `analyzer` | Name of the Lucene analyzer for tokenization | `bert-uncased` |
| `query_tokens` | Pre-computed token-weight map | Optional |
| `max_token_score` | (Deprecated) Maximum token score threshold | N/A |

### Query Modes

Neural sparse query supports three encoding methods:

1. **Model-based**: Uses ML Commons sparse encoding model
   ```json
   {
     "neural_sparse": {
       "field": {
         "query_text": "search query",
         "model_id": "<model-id>"
       }
     }
   }
   ```

2. **Analyzer-based** (v3.0.0+): Uses Lucene analyzer for tokenization
   ```json
   {
     "neural_sparse": {
       "field": {
         "query_text": "search query",
         "analyzer": "bert-uncased"
       }
     }
   }
   ```

3. **Raw tokens**: Directly provides token-weight map
   ```json
   {
     "neural_sparse": {
       "field": {
         "query_tokens": {
           "token1": 1.5,
           "token2": 2.3
         }
       }
     }
   }
   ```

### Sparse Vector Pruning

Sparse vectors often exhibit a long-tail distribution where tokens with lower semantic importance occupy significant storage space. Pruning removes these low-weight tokens to reduce index size while preserving search relevance.

#### Pruning Strategies

| Prune Type | Description | Valid Ratio Range |
|------------|-------------|-------------------|
| `top_k` | Keeps only the top K tokens with highest weights | Positive integer |
| `max_ratio` | Keeps tokens whose weight is within ratio of max weight | [0, 1) |
| `alpha_mass` | Keeps tokens whose cumulative sum is within ratio of total | [0, 1) |
| `abs_value` | Keeps tokens with weight above absolute threshold | Non-negative float |

#### Pruning at Ingestion

Configure pruning in the `sparse_encoding` processor:

```json
PUT /_ingest/pipeline/sparse-pipeline
{
  "processors": [
    {
      "sparse_encoding": {
        "model_id": "<model-id>",
        "field_map": {
          "text": "text_sparse"
        },
        "prune_type": "max_ratio",
        "prune_ratio": 0.1
      }
    }
  ]
}
```

### Two-Phase Query Optimization

The neural sparse query supports two-phase execution for improved performance:

```mermaid
flowchart TB
    A[Query Tokens] --> B[Split by Prune Strategy]
    B --> C[High-Weight Tokens]
    B --> D[Low-Weight Tokens]
    C --> E[Phase 1: Initial Search]
    E --> F[Top-K Results]
    F --> G[Phase 2: Rescore]
    D --> G
    G --> H[Final Results]
```

Two-phase status values:
- `NOT_ENABLED`: Standard single-phase execution
- `PHASE_ONE`: First phase with high-weight tokens only
- `PHASE_TWO`: Rescoring phase with low-weight tokens

#### Two-Phase Processor Configuration

Configure pruning strategy in the two-phase processor:

```json
PUT /_search/pipeline/two-phase-pipeline
{
  "request_processors": [
    {
      "neural_sparse_two_phase_processor": {
        "enabled": true,
        "two_phase_parameter": {
          "prune_type": "max_ratio",
          "prune_ratio": 0.4,
          "expansion_rate": 5.0,
          "max_window_size": 10000
        }
      }
    }
  ]
}
```

### Usage Example

```json
PUT /my-sparse-index
{
  "settings": {
    "default_pipeline": "sparse-ingest-pipeline"
  },
  "mappings": {
    "properties": {
      "text_sparse": {
        "type": "rank_features"
      },
      "text": {
        "type": "text"
      }
    }
  }
}

GET /my-sparse-index/_search
{
  "query": {
    "neural_sparse": {
      "text_sparse": {
        "query_text": "semantic search query",
        "analyzer": "bert-uncased"
      }
    }
  }
}
```

## Limitations

- Sparse encoding models must be deployed in ML Commons before use (for model-based queries)
- Analyzer must be configured in index settings (for analyzer-based queries)
- Token weights in analyzer mode must be encoded as 4-byte floats in payload attribute
- Two-phase optimization requires search pipeline configuration
- Cannot specify both `model_id` and `analyzer` in the same query (v3.1.0+)
- Pruning configuration:
  - `prune_ratio` is required when `prune_type` is specified (except for `none`)
  - Cannot specify `prune_ratio` without `prune_type`
  - `top_k` ratio must be a positive integer
  - `max_ratio` and `alpha_mass` ratio must be in range [0, 1)
  - `abs_value` ratio must be non-negative

## Change History

- **v3.1.0**: Added validation to prevent specifying both model_id and analyzer simultaneously
- **v3.0.0** (2025-03-11): Added analyzer-based neural sparse query support, enabling tokenization without ML Commons models
- **v2.19.0** (2025-01-14): Added pruning support for sparse vectors with four strategies (`top_k`, `max_ratio`, `alpha_mass`, `abs_value`) in both ingestion and two-phase search
- **v2.16.0** (2024-08-06): Added BWC tests for neural sparse query two-phase search processor
- **v2.11.0**: Initial implementation of neural sparse query with model-based and raw token support


## References

### Documentation
- [Neural Sparse Query Documentation](https://docs.opensearch.org/3.0/query-dsl/specialized/neural-sparse/)
- [Neural Sparse Search Guide](https://docs.opensearch.org/3.0/vector-search/ai-search/neural-sparse-search/)
- [Neural Search API](https://docs.opensearch.org/3.0/vector-search/api/neural/)
- [Sparse Encoding Processor](https://docs.opensearch.org/2.19/ingest-pipelines/processors/sparse-encoding/)

### Pull Requests
| Version | PR | Description | Related Issue |
|---------|-----|-------------|---------------|
| v3.1.0 | [#1359](https://github.com/opensearch-project/neural-search/pull/1359) | Validate model_id and analyzer mutual exclusivity |   |
| v3.0.0 | [#1088](https://github.com/opensearch-project/neural-search/pull/1088) | Implement analyzer-based neural sparse query |   |
| v2.19.0 | [#988](https://github.com/opensearch-project/neural-search/pull/988) | Implement pruning for neural sparse ingestion and two-phase search | [#946](https://github.com/opensearch-project/neural-search/issues/946) |
| v2.16.0 | [#777](https://github.com/opensearch-project/neural-search/pull/777) | Add backward test cases for neural sparse two phase processor | [#646](https://github.com/opensearch-project/neural-search/issues/646) |
| v2.11.0 | - | Initial neural sparse query implementation |   |

### Issues (Design / RFC)
- [Issue #1052](https://github.com/opensearch-project/neural-search/issues/1052): RFC for analyzer-based neural sparse query
- [Issue #946](https://github.com/opensearch-project/neural-search/issues/946): RFC for implementing pruning for neural sparse search
