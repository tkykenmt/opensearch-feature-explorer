# Calcite Query Engine

## Summary

The Calcite Query Engine is an Apache Calcite-based query processing framework for OpenSearch's SQL/PPL plugin. It provides advanced query optimization, cross-index data correlation capabilities (joins, lookups, subsearches), and an extensible UDF framework. The engine transforms PPL from a simple query language into a powerful analytical tool for log analysis and observability workflows.

## Details

### Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        Client[Client Request]
        REST[REST Handler]
    end
    
    subgraph "Query Parsing"
        ANTLR[ANTLR4 Grammar]
        AST[Abstract Syntax Tree]
    end
    
    subgraph "Engine Selection"
        Router{Query Router}
        V1[V1 Legacy Engine]
        V2[V2 Engine]
        V3[V3 Calcite Engine]
    end
    
    subgraph "Calcite Processing"
        RelBuilder[RelBuilder]
        RelNode[RelNode Tree]
        TypeSystem[OpenSearch Type System]
        Optimizer[Query Optimizer]
        Rules[Transformation Rules]
        OSRel[OpenSearchEnumerableRel]
    end
    
    subgraph "Function Framework"
        FuncTable[PPLFuncImpTable]
        BuiltinOps[PPLBuiltinOperators]
        UDF[User Defined Functions]
    end
    
    subgraph "Execution"
        ThreadPool[Calcite Thread Pool]
        Linq4j[Linq4j Code Gen]
        Pushdown[Filter/Agg Pushdown]
        QueryBuilder[OpenSearch QueryBuilder]
    end
    
    subgraph "OpenSearch"
        OS[(OpenSearch Cluster)]
    end
    
    Client --> REST
    REST --> ANTLR
    ANTLR --> AST
    AST --> Router
    Router -->|SQL| V1
    Router -->|SQL| V2
    Router -->|PPL + Calcite| V3
    V3 --> RelBuilder
    RelBuilder --> RelNode
    RelNode --> TypeSystem
    TypeSystem --> Optimizer
    Optimizer --> Rules
    Rules --> OSRel
    OSRel --> FuncTable
    FuncTable --> BuiltinOps
    BuiltinOps --> UDF
    OSRel --> ThreadPool
    ThreadPool --> Linq4j
    ThreadPool --> Pushdown
    Pushdown --> QueryBuilder
    Linq4j --> OS
    QueryBuilder --> OS
    V1 --> OS
    V2 --> OS
```

### Data Flow

```mermaid
flowchart TB
    subgraph "Query Lifecycle"
        Query[PPL Query Text]
        Parse[ANTLR4 Parsing]
        AST[Build AST]
        Convert[Convert to RelNode]
        Bind[Catalog Binding]
        Optimize[Apply Optimization Rules]
        Plan[Generate Physical Plan]
        Execute[Execute in Thread Pool]
        Format[Format Response]
        Response[Return Results]
    end
    
    Query --> Parse
    Parse --> AST
    AST --> Convert
    Convert --> Bind
    Bind --> Optimize
    Optimize --> Plan
    Plan --> Execute
    Execute --> Format
    Format --> Response
    
    subgraph "Optimization"
        FilterPush[Filter Pushdown]
        AggPush[Aggregation Pushdown]
        ProjectPush[Projection Pushdown]
    end
    
    Optimize --> FilterPush
    Optimize --> AggPush
    Optimize --> ProjectPush
```

### Components

| Component | Description |
|-----------|-------------|
| `CalcitePPLParser` | Converts PPL AST to Calcite RelNode tree using RelBuilder |
| `OpenSearchTypeSystem` | Custom Calcite type system for OpenSearch data types |
| `OpenSearchTypeFactory` | Factory for creating OpenSearch-specific type instances |
| `PPLFuncImpTable` | Registry for logical-level function implementations |
| `PPLBuiltinOperators` | Physical-level UDF implementations mapped to Calcite |
| `CalciteEnumerableIndexScan` | OpenSearch index scan operator with pushdown support |
| `OpenSearchEnumerableRel` | Base class for OpenSearch-specific Calcite operators |
| `CalciteQueryPlanner` | Orchestrates query planning and optimization |
| `PushDownContext` | Tracks pushdown state for filters and aggregations |

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `plugins.calcite.enabled` | Enable Calcite engine for PPL queries | `true` (v3.3.0+, was `false`) |
| `plugins.calcite.fallback.allowed` | Allow fallback to v2 engine on failure | `false` (v3.2.0+) |
| `plugins.sql.enabled` | Enable SQL support | `true` |
| `plugins.ppl.enabled` | Enable PPL support | `true` |
| `plugins.query.memory_limit` | Query memory limit | `85%` |
| `plugins.query.size_limit` | Maximum query result size | `200` |

### PPL Commands

| Command | Description | Syntax | Since |
|---------|-------------|--------|-------|
| `join` | Correlate data from multiple indexes | `source=a \| join [LEFT\|RIGHT\|INNER\|OUTER\|CROSS\|SEMI\|ANTI] ON condition b` | v3.0.0 |
| `lookup` | Enrich data with reference table | `source=a \| lookup b match_field [AS alias], [output_field, ...]` | v3.0.0 |
| `subsearch` | Dynamic filtering with subqueries | `where [NOT] exists/in [subquery]` | v3.0.0 |
| `dedup` | Remove duplicate records | `source=a \| dedup field1, field2` | v3.0.0 |
| `parse` | Extract fields using regex | `source=a \| parse field 'pattern'` | v3.0.0 |
| `eventstats` | Window functions over partitions | `source=a \| eventstats avg(field) by group` | v3.1.0 |
| `flatten` | Flatten nested struct fields | `source=a \| flatten nested_field` | v3.1.0 |
| `expand` | Expand array fields into rows | `source=a \| expand array_field` | v3.1.0 |
| `trendline` | Calculate trend lines | `source=a \| trendline sma(2, field)` | v3.1.0 |
| `appendcol` | Append columns from subquery | `source=a \| appendcol [subquery]` | v3.1.0 |
| `grok` | Parse text using Grok patterns | `source=a \| grok field '%{PATTERN}'` | v3.1.0 |
| `top` | Find most common values | `source=a \| top N field [by group]` | v3.1.0 |
| `rare` | Find least common values | `source=a \| rare field [by group]` | v3.1.0 |
| `fillnull` | Replace null values | `source=a \| fillnull value=default field` | v3.1.0 |
| `describe` | Show index metadata | `describe index_name` | v3.1.0 |
| `patterns` | Pattern detection (BRAIN method) | `source=a \| patterns field` | v3.1.0 |
| `timechart` | Time-series aggregation with binning | `source=a \| timechart span=1m avg(field) [by group]` | v3.3.0 |

### Supported Functions

| Category | Functions |
|----------|-----------|
| Math | `abs`, `ceil`, `floor`, `round`, `sqrt`, `pow`, `exp`, `ln`, `log`, `log10`, `log2`, `atan`, `atan2`, `sin`, `cos`, `tan` |
| String | `concat`, `length`, `lower`, `upper`, `trim`, `ltrim`, `rtrim`, `substring`, `replace`, `reverse`, `position`, `left`, `right`, `mvjoin`, `regex_match` |
| Condition | `if`, `ifnull`, `nullif`, `coalesce`, `case`, `isnull`, `isempty`, `isblank`, `ispresent` |
| Geo | `geoip`, `cidrmatch` |
| Date/Time | `now`, `curdate`, `curtime`, `date`, `time`, `timestamp`, `date_add`, `date_sub`, `datediff`, `timediff`, `time_to_sec` |
| Type | `typeof`, `cast` |
| Aggregation | `count`, `sum`, `avg`, `min`, `max`, `take` |

### Supported Data Types

| Type | OpenSearch Mapping | Description |
|------|-------------------|-------------|
| `DATE` | `date` | Date without time |
| `TIME` | `date` | Time without date |
| `TIMESTAMP` | `date` | Full date and time |
| `IP` | `ip` | IPv4/IPv6 addresses |
| `GEO_POINT` | `geo_point` | Geographic coordinates |
| `BINARY` | `binary` | Binary data |
| `ALIAS` | `alias` | Field aliases |
| `NESTED` | `nested` | Nested objects |

### Usage Example

```bash
# Enable Calcite engine
PUT _cluster/settings
{
  "transient": {
    "plugins.calcite.enabled": true
  }
}

# Lookup: Enrich authentication logs with user details
POST /_plugins/_ppl
{
  "query": "source=auth_logs | lookup user_info user_id | where status='failed' | fields timestamp, user_id, department, status"
}

# Join: Correlate logs within time window
POST /_plugins/_ppl
{
  "query": "source=auth_logs | join left=l right=r ON l.user_id = r.user_id AND TIME_TO_SEC(TIMEDIFF(r.timestamp, l.timestamp)) <= 60 app_logs | fields timestamp, user_id, action, status"
}

# Subsearch EXISTS: Find suspicious activity
POST /_plugins/_ppl
{
  "query": "source=auth_logs | where status='failed' AND exists [source=app_logs | where user_id=auth_logs.user_id AND action='login']"
}

# Subsearch IN: Filter by department
POST /_plugins/_ppl
{
  "query": "source=logs | where user_id in [source=users | where department='Security' | fields user_id]"
}

# Explain query plan
POST /_plugins/_ppl
{
  "query": "explain source=auth_logs | lookup user_info user_id | where status='failed'"
}

# Response shows logical and physical plans:
# LogicalProject -> LogicalFilter -> LogicalJoin -> CalciteLogicalIndexScan
# EnumerableCalc -> EnumerableMergeJoin -> CalciteEnumerableIndexScan (with pushdown)
```

## Limitations

- Only PPL queries optimized by Calcite (SQL support planned)
- JOIN queries auto-terminate after 60 seconds
- `dedup` with `consecutive=true` not supported
- Pagination/cursor not supported
- Aggregation over expressions has limited support
- Subquery in FROM clause has limited support
- `eventstats` supports basic aggregate functions; advanced window functions (ROW_NUMBER, RANK, etc.) planned for future releases
- `flatten` works only with struct/object fields, not arrays
- `timechart` does not support pivot formatting or multiple aggregation functions

## Change History

- **v3.3.0** (2026-01-11): Calcite enabled by default (`plugins.calcite.enabled=true`); implicit fallback to V2 for unsupported commands; new functions (`mvjoin`, `regex_match`); `timechart` command for time-series aggregation; enhanced cost computing mechanism; project pushdown optimization for non-identity projections
- **v3.2.0** (2026-01-11): Major pushdown expansion - sort, aggregation with scripts, partial filter, span, relevance queries, Sarg values; secure RelJson serialization for filter scripts; performance optimization skipping codegen for simple queries (~30% improvement); v2 fallback disabled by default; new UDFs (compare_ip, IP casting); function argument coercion
- **v3.1.0** (2026-01-10): Expanded command support - eventstats (window functions), flatten, expand, trendline, appendcol, grok, top/rare, fillnull, describe, patterns; new functions (coalesce, isempty, isblank, ispresent, geoip, cidrmatch); performance optimizations (LIMIT pushdown, row count estimation, ResourceMonitor)
- **v3.0.0** (2025-05-06): Initial implementation - Apache Calcite integration, join/lookup/subsearch commands, UDF framework, custom type system, thread pool execution, enhanced explain output

## References

### Documentation
- [SQL Settings Documentation](https://docs.opensearch.org/3.0/search-plugins/sql/settings/): Configuration reference
- [SQL Limitations](https://docs.opensearch.org/3.0/search-plugins/sql/limitation/): Engine limitations
- [PPL Commands](https://docs.opensearch.org/3.0/search-plugins/sql/ppl/functions/): PPL command reference
- [Apache Calcite](https://calcite.apache.org/): Query optimization framework
- [SQL Plugin Repository](https://github.com/opensearch-project/sql): Source code

### Blog Posts
- [Enhanced Log Analysis Blog](https://opensearch.org/blog/enhanced-log-analysis-with-opensearch-ppl-introducing-lookup-join-and-subsearch/): Feature announcement

### Pull Requests
| Version | PR | Description |
|---------|-----|-------------|
| v3.3.0 | [#4372](https://github.com/opensearch-project/sql/pull/4372) | Enable Calcite by default and implicit fallback for unsupported commands |
| v3.3.0 | [#4353](https://github.com/opensearch-project/sql/pull/4353) | Enhance cost computing mechanism and push down context |
| v3.3.0 | [#4279](https://github.com/opensearch-project/sql/pull/4279) | Push down project operator with non-identity projections into scan |
| v3.3.0 | [#4217](https://github.com/opensearch-project/sql/pull/4217) | `mvjoin` support in PPL Calcite |
| v3.3.0 | [#4092](https://github.com/opensearch-project/sql/pull/4092) | Add `regex_match` function for PPL with Calcite engine support |
| v3.3.0 | [#3993](https://github.com/opensearch-project/sql/pull/3993) | Support `timechart` command with Calcite |
| v3.2.0 | [#3620](https://github.com/opensearch-project/sql/pull/3620) | Support Sort pushdown |
| v3.2.0 | [#3916](https://github.com/opensearch-project/sql/pull/3916) | Support aggregation push down with scripts |
| v3.2.0 | [#3850](https://github.com/opensearch-project/sql/pull/3850) | Support partial filter push down |
| v3.2.0 | [#3834](https://github.com/opensearch-project/sql/pull/3834) | Support relevance query functions pushdown |
| v3.2.0 | [#3859](https://github.com/opensearch-project/sql/pull/3859) | Filter script pushdown with RelJson serialization |
| v3.2.0 | [#3853](https://github.com/opensearch-project/sql/pull/3853) | Skip codegen for Scan only plan (~30% improvement) |
| v3.2.0 | [#3952](https://github.com/opensearch-project/sql/pull/3952) | Disable v2 fallback by default |
| v3.2.0 | [#3823](https://github.com/opensearch-project/sql/pull/3823) | Support span push down |
| v3.2.0 | [#3840](https://github.com/opensearch-project/sql/pull/3840) | Support filter push down for Sarg value |
| v3.2.0 | [#3864](https://github.com/opensearch-project/sql/pull/3864) | Support pushdown physical sort for SortMergeJoin |
| v3.2.0 | [#3880](https://github.com/opensearch-project/sql/pull/3880) | Push down QUERY_SIZE_LIMIT |
| v3.2.0 | [#3914](https://github.com/opensearch-project/sql/pull/3914) | Support function argument coercion |
| v3.2.0 | [#3919](https://github.com/opensearch-project/sql/pull/3919) | Support casting to IP with Calcite |
| v3.2.0 | [#3821](https://github.com/opensearch-project/sql/pull/3821) | Add compare_ip operator UDFs |
| v3.1.0 | [#3738](https://github.com/opensearch-project/sql/pull/3738) | Support ResourceMonitor with Calcite |
| v3.1.0 | [#3747](https://github.com/opensearch-project/sql/pull/3747) | Support `flatten` command with Calcite |
| v3.1.0 | [#3745](https://github.com/opensearch-project/sql/pull/3745) | Support `expand` command with Calcite |
| v3.1.0 | [#3741](https://github.com/opensearch-project/sql/pull/3741) | Support trendline command in Calcite |
| v3.1.0 | [#3729](https://github.com/opensearch-project/sql/pull/3729) | Support `appendcol` command with Calcite |
| v3.1.0 | [#3678](https://github.com/opensearch-project/sql/pull/3678) | Support Grok command in Calcite engine |
| v3.1.0 | [#3673](https://github.com/opensearch-project/sql/pull/3673) | Support decimal literal with Calcite |
| v3.1.0 | [#3647](https://github.com/opensearch-project/sql/pull/3647) | Support `top`, `rare` commands with Calcite |
| v3.1.0 | [#3634](https://github.com/opensearch-project/sql/pull/3634) | Support `fillnull` command with Calcite |
| v3.1.0 | [#3628](https://github.com/opensearch-project/sql/pull/3628) | Support function `coalesce` with Calcite |
| v3.1.0 | [#3627](https://github.com/opensearch-project/sql/pull/3627) | Support functions `isempty`, `isblank`, `ispresent` |
| v3.1.0 | [#3626](https://github.com/opensearch-project/sql/pull/3626) | Implement Parameter Validation for PPL functions |
| v3.1.0 | [#3624](https://github.com/opensearch-project/sql/pull/3624) | Support `describe` command with Calcite |
| v3.1.0 | [#3615](https://github.com/opensearch-project/sql/pull/3615) | Support Limit pushdown |
| v3.1.0 | [#3612](https://github.com/opensearch-project/sql/pull/3612) | Add UT for PredicateAnalyzer and AggregateAnalyzer |
| v3.1.0 | [#3605](https://github.com/opensearch-project/sql/pull/3605) | Add row count estimation for CalciteIndexScan |
| v3.1.0 | [#3604](https://github.com/opensearch-project/sql/pull/3604) | Implement `geoip` udf with Calcite |
| v3.1.0 | [#3603](https://github.com/opensearch-project/sql/pull/3603) | Implement `cidrmatch` udf with Calcite |
| v3.1.0 | [#3585](https://github.com/opensearch-project/sql/pull/3585) | Support `eventstats` command with Calcite |
| v3.1.0 | [#3570](https://github.com/opensearch-project/sql/pull/3570) | Calcite patterns command brain pattern method |
| v3.0.0 | [#3249](https://github.com/opensearch-project/sql/pull/3249) | Framework of Calcite Engine |
| v3.0.0 | [#3364](https://github.com/opensearch-project/sql/pull/3364) | PPL join command |
| v3.0.0 | [#3419](https://github.com/opensearch-project/sql/pull/3419) | Lookup command |
| v3.0.0 | [#3371](https://github.com/opensearch-project/sql/pull/3371) | IN subquery |
| v3.0.0 | [#3388](https://github.com/opensearch-project/sql/pull/3388) | EXISTS subquery |
| v3.0.0 | [#3374](https://github.com/opensearch-project/sql/pull/3374) | UDF interface |
| v3.0.0 | [#3468](https://github.com/opensearch-project/sql/pull/3468) | Enable Calcite by default |
| v3.0.0 | [#3521](https://github.com/opensearch-project/sql/pull/3521) | Enhanced explain output |
