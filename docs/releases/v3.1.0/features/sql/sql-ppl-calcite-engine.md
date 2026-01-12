---
tags:
  - indexing
  - observability
  - performance
  - search
  - sql
---

# SQL/PPL Calcite Engine

## Summary

OpenSearch v3.1.0 significantly expands the Calcite-based PPL engine with support for 15+ new commands and functions. This release adds window functions (`eventstats`), data transformation commands (`flatten`, `expand`, `appendcol`), text processing (`grok`), aggregation commands (`top`, `rare`, `fillnull`), and performance optimizations including LIMIT pushdown and row count estimation. These enhancements make PPL a more complete analytical query language for log analysis and observability workflows.

## Details

### What's New in v3.1.0

This release focuses on expanding PPL command coverage in the Calcite engine, adding essential commands that were previously only available in the legacy V1 engine or not supported at all.

### Technical Changes

#### New PPL Commands

| Command | Description | PR |
|---------|-------------|-----|
| `eventstats` | Window functions (avg, count, sum, min, max, var_samp, var_pop, stddev_samp, stddev_pop) | [#3585](https://github.com/opensearch-project/sql/pull/3585) |
| `flatten` | Flatten nested struct/object fields into separate fields | [#3747](https://github.com/opensearch-project/sql/pull/3747) |
| `expand` | Expand array fields into multiple rows | [#3745](https://github.com/opensearch-project/sql/pull/3745) |
| `trendline` | Calculate trend lines over time-series data | [#3741](https://github.com/opensearch-project/sql/pull/3741) |
| `appendcol` | Append columns from subquery results | [#3729](https://github.com/opensearch-project/sql/pull/3729) |
| `grok` | Parse text using Grok patterns | [#3678](https://github.com/opensearch-project/sql/pull/3678) |
| `top` / `rare` | Find most/least common values with count display options | [#3647](https://github.com/opensearch-project/sql/pull/3647) |
| `fillnull` | Replace null values with specified defaults | [#3634](https://github.com/opensearch-project/sql/pull/3634) |
| `describe` | Show index metadata and field information | [#3624](https://github.com/opensearch-project/sql/pull/3624) |
| `patterns` | Pattern detection using BRAIN method | [#3570](https://github.com/opensearch-project/sql/pull/3570) |

#### New Functions

| Function | Description | PR |
|----------|-------------|-----|
| `coalesce` | Return first non-null value from arguments | [#3628](https://github.com/opensearch-project/sql/pull/3628) |
| `isempty` | Check if string is empty | [#3627](https://github.com/opensearch-project/sql/pull/3627) |
| `isblank` | Check if string is blank (empty or whitespace) | [#3627](https://github.com/opensearch-project/sql/pull/3627) |
| `ispresent` | Check if field has a value | [#3627](https://github.com/opensearch-project/sql/pull/3627) |
| `geoip` | GeoIP lookup for IP addresses | [#3604](https://github.com/opensearch-project/sql/pull/3604) |
| `cidrmatch` | Check if IP matches CIDR range | [#3603](https://github.com/opensearch-project/sql/pull/3603) |

#### Performance Optimizations

| Optimization | Description | PR |
|--------------|-------------|-----|
| LIMIT pushdown | Push LIMIT clause to OpenSearch for reduced data transfer | [#3615](https://github.com/opensearch-project/sql/pull/3615) |
| Row count estimation | Improved query planning with CalciteIndexScan row estimation | [#3605](https://github.com/opensearch-project/sql/pull/3605) |
| ResourceMonitor | Memory monitoring in CalciteEnumerableIndexScan | [#3738](https://github.com/opensearch-project/sql/pull/3738) |

#### Other Improvements

| Improvement | Description | PR |
|-------------|-------------|-----|
| Decimal literal support | Support decimal literals in PPL queries | [#3673](https://github.com/opensearch-project/sql/pull/3673) |
| Parameter validation | Validate PPL function parameters on Calcite | [#3626](https://github.com/opensearch-project/sql/pull/3626) |
| PredicateAnalyzer tests | Unit tests for predicate and aggregate analyzers | [#3612](https://github.com/opensearch-project/sql/pull/3612) |

### Usage Examples

#### eventstats - Window Functions

The `eventstats` command calculates statistics across partitions without reducing rows:

```ppl
source=logs | eventstats avg(response_time), count() by service
```

This is equivalent to SQL window functions:
```sql
SELECT avg(response_time) OVER (PARTITION BY service), 
       count(*) OVER (PARTITION BY service) 
FROM logs
```

Supported window functions: `max`, `min`, `sum`, `count`, `avg`, `var_samp`, `var_pop`, `stddev_samp`, `stddev_pop`

#### flatten - Nested Object Expansion

Flatten extracts nested struct fields into top-level fields:

```ppl
source=users | flatten address
```

Input:
```json
{"name": "Jack", "address": {"state": "Oregon", "city": "Portland"}}
```

Output:
```json
{"name": "Jack", "address": {...}, "state": "Oregon", "city": "Portland"}
```

#### top/rare with Count Display

The `top` and `rare` commands now support count display options (aligned with PPL-Spark):

```ppl
source=logs | top 10 status showcount=true countfield=occurrences
source=logs | rare error_code by service
```

#### grok - Text Pattern Extraction

Parse unstructured text using Grok patterns:

```ppl
source=apache_logs | grok message '%{COMMONAPACHELOG}'
```

### Migration Notes

- Commands previously marked as unsupported in Calcite (`trendline`, `top`, `rare`, `fillnull`) are now available
- The `eventstats` command provides window function capabilities without requiring SQL syntax
- LIMIT pushdown improves performance for queries with result limits

## Limitations

- `eventstats` currently supports basic aggregate functions; advanced window functions (ROW_NUMBER, RANK, etc.) planned for future releases
- `flatten` works only with struct/object fields, not arrays
- `grok` patterns must be valid Grok syntax

## References

### Documentation
- [PPL Commands Documentation](https://docs.opensearch.org/3.0/search-plugins/sql/ppl/functions/): Official PPL command reference
- [SQL Settings](https://docs.opensearch.org/3.0/search-plugins/sql/settings/): Calcite engine configuration

### Blog Posts
- [Enhanced Log Analysis Blog](https://opensearch.org/blog/enhanced-log-analysis-with-opensearch-ppl-introducing-lookup-join-and-subsearch/): PPL 3.0 feature announcement

### Pull Requests
| PR | Description |
|----|-------------|
| [#3738](https://github.com/opensearch-project/sql/pull/3738) | Support ResourceMonitor with Calcite |
| [#3747](https://github.com/opensearch-project/sql/pull/3747) | Support `flatten` command with Calcite |
| [#3745](https://github.com/opensearch-project/sql/pull/3745) | Support `expand` command with Calcite |
| [#3741](https://github.com/opensearch-project/sql/pull/3741) | Support trendline command in Calcite |
| [#3729](https://github.com/opensearch-project/sql/pull/3729) | Support `appendcol` command with Calcite |
| [#3678](https://github.com/opensearch-project/sql/pull/3678) | Support Grok command in Calcite engine |
| [#3673](https://github.com/opensearch-project/sql/pull/3673) | Support decimal literal with Calcite |
| [#3647](https://github.com/opensearch-project/sql/pull/3647) | Support `top`, `rare` commands with Calcite |
| [#3634](https://github.com/opensearch-project/sql/pull/3634) | Support `fillnull` command with Calcite |
| [#3628](https://github.com/opensearch-project/sql/pull/3628) | Support function `coalesce` with Calcite |
| [#3627](https://github.com/opensearch-project/sql/pull/3627) | Support functions `isempty`, `isblank`, `ispresent` |
| [#3626](https://github.com/opensearch-project/sql/pull/3626) | Implement Parameter Validation for PPL functions |
| [#3624](https://github.com/opensearch-project/sql/pull/3624) | Support `describe` command with Calcite |
| [#3615](https://github.com/opensearch-project/sql/pull/3615) | Support Limit pushdown |
| [#3612](https://github.com/opensearch-project/sql/pull/3612) | Add UT for PredicateAnalyzer and AggregateAnalyzer |
| [#3605](https://github.com/opensearch-project/sql/pull/3605) | Add row count estimation for CalciteIndexScan |
| [#3604](https://github.com/opensearch-project/sql/pull/3604) | Implement `geoip` udf with Calcite |
| [#3603](https://github.com/opensearch-project/sql/pull/3603) | Implement `cidrmatch` udf with Calcite |
| [#3585](https://github.com/opensearch-project/sql/pull/3585) | Support `eventstats` command with Calcite |
| [#3570](https://github.com/opensearch-project/sql/pull/3570) | Calcite patterns command brain pattern method |

### Issues (Design / RFC)
- [Issue #3454](https://github.com/opensearch-project/sql/issues/3454): ResourceMonitor feature request
- [Issue #3563](https://github.com/opensearch-project/sql/issues/3563): eventstats feature request
- [Issue #3464](https://github.com/opensearch-project/sql/issues/3464): top/rare commands feature request

## Related Feature Report

- [Full feature documentation](../../../../features/sql/calcite-query-engine.md)
