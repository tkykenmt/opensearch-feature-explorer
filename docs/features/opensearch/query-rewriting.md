---
tags:
  - performance
  - search
---

# Query Rewriting

## Summary

Query Rewriting is an automatic query optimization feature that transforms user queries into more efficient forms before execution. It applies multiple optimization strategies including boolean flattening, terms merging, must-to-filter conversion, and match_all removal to reduce query complexity by 60-70% for typical filtered queries while preserving exact query semantics.

## Details

### Architecture

```mermaid
graph TB
    subgraph "Query Execution Flow"
        A[Search Request] --> B[QueryBuilder Tree]
        B --> C[QueryRewriterRegistry]
        
        subgraph "Rewriter Chain"
            D[BooleanFlatteningRewriter]
            E[MustToFilterRewriter]
            F[MustNotToShouldRewriter]
            G[TermsMergingRewriter]
            H[MatchAllRemovalRewriter]
        end
        
        C --> D
        D --> E
        E --> F
        F --> G
        G --> H
        
        H --> I[Optimized QueryBuilder]
        I --> J[Lucene Query]
        J --> K[Query Execution]
    end
```

### Data Flow

```mermaid
flowchart TB
    subgraph "SearchService.parseSource()"
        A[source.query()] --> B{Rewriting Enabled?}
        B -->|Yes| C[QueryRewriterRegistry.rewrite]
        B -->|No| D[Original Query]
        C --> E[Sorted Rewriters by Priority]
        E --> F[Apply Each Rewriter]
        F --> G[Optimized Query]
        G --> H[toQuery via QueryShardContext]
        D --> H
    end
```

### Components

| Component | Priority | Description |
|-----------|----------|-------------|
| `QueryRewriter` | - | Interface defining `rewrite(QueryBuilder, QueryShardContext)` method |
| `QueryRewriterRegistry` | - | Singleton managing rewriter registration and execution chain |
| `BooleanFlatteningRewriter` | 100 | Flattens nested boolean queries with single clause types |
| `MustToFilterRewriter` | 150 | Moves scoring-irrelevant queries from must to filter |
| `MustNotToShouldRewriter` | 175 | Converts must_not to should for complement-aware queries |
| `TermsMergingRewriter` | 200 | Merges multiple term queries into terms query |
| `MatchAllRemovalRewriter` | 300 | Removes redundant match_all queries |

### Configuration

| Setting | Description | Default | Dynamic |
|---------|-------------|---------|---------|
| `search.query_rewriting.enabled` | Enable/disable query rewriting globally | `true` | Yes |
| `search.query_rewriting.terms_threshold` | Minimum number of term queries to trigger merging | `16` | Yes |

### Rewriter Details

#### BooleanFlatteningRewriter

Flattens unnecessary nested boolean queries:

```json
// Before
{"bool": {"filter": [{"bool": {"filter": [{"term": {"field": "value"}}]}}]}}

// After
{"bool": {"filter": [{"term": {"field": "value"}}]}}
```

#### MustToFilterRewriter

Moves scoring-irrelevant clauses from must to filter for better caching:

```json
// Before
{"bool": {"must": [{"range": {"date": {"gte": "2024-01-01"}}}, {"match": {"title": "search"}}]}}

// After
{"bool": {"filter": [{"range": {"date": {"gte": "2024-01-01"}}}], "must": [{"match": {"title": "search"}}]}}
```

Applies to:
- Range queries (always)
- GeoBoundingBox queries (always)
- Term/Terms/Match queries on numeric fields (requires QueryShardContext)

#### MustNotToShouldRewriter

Converts must_not range queries to should clauses for single-valued numeric fields:

```json
// Before
{"bool": {"must_not": [{"range": {"age": {"gte": 18, "lte": 65}}}]}}

// After
{"bool": {"must": [{"bool": {"should": [
  {"range": {"age": {"lt": 18}}},
  {"range": {"age": {"gt": 65}}}
], "minimum_should_match": 1}}]}}
```

Requirements:
- Field must be numeric with point values
- All documents must have exactly one value for the field
- Only one complement-aware query per field

#### TermsMergingRewriter

Merges multiple term queries on the same field into a single terms query:

```json
// Before (with 16+ terms)
{"bool": {"filter": [
  {"term": {"status": "active"}},
  {"term": {"status": "pending"}},
  // ... 14+ more terms
]}}

// After
{"bool": {"filter": [{"terms": {"status": ["active", "pending", ...]}}]}}
```

Only merges in filter and should contexts (not must or must_not).

#### MatchAllRemovalRewriter

Removes redundant match_all queries from boolean contexts:

```json
// Before
{"bool": {"filter": [{"match_all": {}}, {"term": {"status": "active"}}]}}

// After
{"bool": {"filter": [{"term": {"status": "active"}}]}}
```

### Usage Example

```bash
# Disable query rewriting
PUT /_cluster/settings
{
  "persistent": {
    "search.query_rewriting.enabled": false
  }
}

# Adjust terms merging threshold
PUT /_cluster/settings
{
  "persistent": {
    "search.query_rewriting.terms_threshold": 8
  }
}
```

### Custom Rewriter Registration

```java
// Register a custom rewriter
QueryRewriterRegistry.INSTANCE.registerRewriter(new QueryRewriter() {
    @Override
    public QueryBuilder rewrite(QueryBuilder query, QueryShardContext context) {
        // Custom rewriting logic
        return query;
    }
    
    @Override
    public int priority() {
        return 500; // Execute after built-in rewriters
    }
    
    @Override
    public String name() {
        return "custom_rewriter";
    }
});
```

## Limitations

- Terms merging only triggers when term count meets threshold (default: 16)
- Must-not-to-should requires single-valued numeric fields with complete coverage
- Rewriters execute in priority order; later rewriters see results of earlier ones
- Custom rewriters must be registered programmatically (no plugin API yet)
- Query names and boosts are preserved but may affect flattening eligibility

## Change History

- **v3.3.0** (2026-01): Initial implementation with five built-in rewriters (boolean flattening, must-to-filter, must-not-to-should, terms merging, match-all removal)

## Related Features
- [OpenSearch Dashboards](../opensearch-dashboards/ai-chat.md)

## References

### Documentation
- [Documentation](https://docs.opensearch.org/3.0/search-plugins/search-relevance/query-rewriting/): Query rewriting overview

### Pull Requests
| Version | PR | Description | Related Issue |
|---------|-----|-------------|---------------|
| v3.3.0 | [#19060](https://github.com/opensearch-project/OpenSearch/pull/19060) | Initial implementation of query rewriting infrastructure |   |

### Issues (Design / RFC)
- [Issue #18906](https://github.com/opensearch-project/OpenSearch/issues/18906): RFC for Query Rewriting, Logical Planning, and Cost-Based Execution
- [Issue #12390](https://github.com/opensearch-project/OpenSearch/issues/12390): RFC for Query Planning and Rewriting
