---
tags:
  - observability
  - performance
  - search
  - sql
---

# SQL/PPL Engine

## Summary

The OpenSearch SQL/PPL Engine provides SQL and Piped Processing Language (PPL) query interfaces for OpenSearch. The plugin supports three query engines: V1 (legacy), V2, and V3 (Calcite-based). Starting with v3.0.0, the Calcite engine enables advanced features like joins, lookups, and subsearches.

> **Note**: For detailed information about the V3 Calcite engine, including PPL commands, functions, and optimization features, see [Calcite Query Engine](calcite-query-engine.md).

## Details

### Architecture

```mermaid
graph TB
    subgraph "SQL/PPL Plugin"
        Client[Client Request]
        REST[REST Handler]
        
        subgraph "Query Parsing"
            ANTLR[ANTLR4 Grammar]
            AST[Abstract Syntax Tree]
        end
        
        subgraph "Query Engines"
            V1[V1 Legacy Engine]
            V2[V2 Engine]
            V3[V3 Calcite Engine]
        end
        
        OS[OpenSearch]
    end
    
    Client --> REST
    REST --> ANTLR
    ANTLR --> AST
    AST --> V1
    AST --> V2
    AST --> V3
    V1 --> OS
    V2 --> OS
    V3 --> OS
    
    click V3 "calcite-query-engine.md" "Calcite Engine Details"
```

### Query Engines

| Engine | Description | Use Case |
|--------|-------------|----------|
| V1 (Legacy) | Original SQL engine | Pagination, cursor, JSON output |
| V2 | Modern engine with improved features | General SQL/PPL queries |
| V3 (Calcite) | Apache Calcite-based with advanced optimization | Joins, lookups, subsearches, analytics |

For V3 Calcite engine details, see [Calcite Query Engine](calcite-query-engine.md).

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `plugins.sql.enabled` | Enable/disable SQL support | `true` |
| `plugins.ppl.enabled` | Enable/disable PPL support | `true` |
| `plugins.calcite.enabled` | Enable V3 Calcite engine | `true` (v3.3.0+) |
| `plugins.sql.slowlog` | Slow query log threshold (seconds) | `2` |
| `plugins.sql.cursor.keep_alive` | Cursor keep alive duration | `1m` |
| `plugins.query.memory_limit` | Query memory limit | `85%` |
| `plugins.query.size_limit` | Maximum query result size | `10000` |

### Usage Example

```bash
# SQL Query
POST /_plugins/_sql
{
  "query": "SELECT * FROM my_index WHERE status = 'active' LIMIT 10"
}

# PPL Query
POST /_plugins/_ppl
{
  "query": "source=my_index | where status = 'active' | head 10"
}

# PPL with join (V3 Calcite)
POST /_plugins/_ppl
{
  "query": "source=auth_logs | join ON auth_logs.user_id = users.user_id users | fields timestamp, user_id, name"
}
```

## Limitations

- Pagination/cursor only supported in V1 engine
- JSON formatted output only in V1 engine
- V3 Calcite limitations: see [Calcite Query Engine - Limitations](calcite-query-engine.md#limitations)

## Change History

- **v3.3.0**: Calcite enabled by default; see [Calcite Query Engine](calcite-query-engine.md) for details
- **v3.0.0**: Apache Calcite integration (V3 engine)
- **v2.17.0**: Increased default query size limit (200 → 10000)

## Related Features
- [Calcite Query Engine](calcite-query-engine.md)
- [Query Workbench](../dashboards-query-workbench/query-workbench.md)
- [Observability (Dashboards)](../dashboards-observability/ci-tests.md)

## References

### Documentation
- [SQL and PPL Documentation](https://docs.opensearch.org/3.0/search-plugins/sql/index/)
- [SQL Settings](https://docs.opensearch.org/3.0/search-plugins/sql/settings/)
- [SQL Plugin Repository](https://github.com/opensearch-project/sql)
