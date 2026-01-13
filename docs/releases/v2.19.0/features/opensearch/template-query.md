---
tags:
  - opensearch
---
# Template Query

## Summary

OpenSearch v2.19.0 introduces the Template Query, a new specialized query type that enables dynamic placeholder substitution in search queries. This feature allows queries to contain variables that are resolved at runtime by search request processors, enabling powerful use cases like converting text to vector embeddings during search.

## Details

### What's New in v2.19.0

The Template Query is a new query type that wraps query content with placeholder variables using the `"${variable_name}"` syntax. These placeholders remain unresolved until processed by search request processors, decoupling query construction from validation.

### Architecture

```mermaid
flowchart TB
    subgraph "Search Request Flow"
        A[Search Request with Template Query] --> B[Search Request Processors]
        B --> C[Variable Resolution]
        C --> D[Query Rewrite]
        D --> E[Execute Final Query]
    end
    
    subgraph "Template Query Structure"
        F["template: { knn: { vector: \"${embedding}\" } }"]
    end
    
    subgraph "Context Variables"
        G[PipelineProcessingContext]
        G --> H[Attributes Map]
    end
    
    F --> A
    H --> C
```

### Technical Changes

| Component | Change |
|-----------|--------|
| `TemplateQueryBuilder` | New query builder that holds template content with placeholders |
| `QueryRewriteContext` | Refactored from class to interface |
| `BaseQueryRewriteContext` | New base implementation of QueryRewriteContext |
| `QueryCoordinatorContext` | New context carrying pipeline variables for coordinator-level rewrite |
| `PipelineProcessingContext` | Added `getAttributes()` method to expose context variables |
| `PipelinedRequest` | Added `getPipelineProcessingContext()` method |
| `SearchService` | Modified `getRewriteContext()` to accept PipelinedRequest |

### Variable Substitution

Placeholders use the `"${variable_name}"` syntax (enclosed in quotes). During query rewrite:
1. Template content is serialized to JSON
2. Variables from `PipelineProcessingContext` are converted to JSON strings
3. Placeholders are replaced with actual values
4. The resulting JSON is parsed into the appropriate QueryBuilder

### Supported Variable Types

| Type | Example Use Case |
|------|------------------|
| String | Term query values |
| List | Terms query values |
| GeoPoint | Geo-distance queries |
| Numeric | Range query bounds |
| Nested Map | Complex query structures |

### Usage Example

```json
GET /my-index/_search?search_pipeline=my_pipeline
{
  "query": {
    "template": {
      "knn": {
        "text_embedding": {
          "vector": "${text_embedding}",
          "k": 2
        }
      }
    }
  },
  "ext": {
    "ml_inference": {
      "text": "search query"
    }
  }
}
```

## Limitations

- Template queries cannot be executed directly without a search request processor
- Rewriting must occur at the coordinator node level (not shard level)
- If variable resolution fails, the query will throw an `IllegalArgumentException`
- Empty or null templates are not allowed

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16818](https://github.com/opensearch-project/OpenSearch/pull/16818) | Introduce Template query | [#16823](https://github.com/opensearch-project/OpenSearch/issues/16823) |

### Documentation
- [Template Query DSL](https://docs.opensearch.org/2.19/query-dsl/specialized/template/)
- [Template Queries Tutorial](https://docs.opensearch.org/2.19/search-plugins/search-relevance/template-query/)
- [ML Inference Search Request Processor](https://docs.opensearch.org/2.19/search-plugins/search-pipelines/ml-inference-search-request/)
