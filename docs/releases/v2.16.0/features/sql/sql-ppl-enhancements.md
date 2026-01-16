---
tags:
  - sql
---
# SQL/PPL Enhancements

## Summary

OpenSearch v2.16.0 introduces several SQL/PPL enhancements including flexible span positioning in PPL stats command, a new setting to toggle data source management, grammar updates for improved compatibility, and support for custom date formats in Lucene queries.

## Details

### What's New in v2.16.0

#### Flexible Span Positioning in Stats Command

The PPL `stats` command now allows the `span` clause to be specified after field names in the `BY` clause, providing more flexible query syntax. Previously, span had to be the first grouping key.

```
# Now supported - span after fields
source=logs | stats COUNT() as cnt by response, span(timestamp, 1d)

# Previously required syntax
source=logs | stats COUNT() as cnt by span(timestamp, 1d), response
```

This enhancement improves compatibility with LLM-generated queries and provides a more intuitive syntax for users.

#### Data Source Management Toggle Setting

A new cluster setting allows administrators to disable data source management code paths:

| Setting | Description | Default |
|---------|-------------|---------|
| `plugins.query.datasources.enabled` | Toggle data source management APIs and internal code paths | `true` |

When disabled:
- Explicit data source management APIs are blocked
- Internal code paths that implicitly create data sources are disabled

#### Custom Date Format Support

SQL Lucene queries now support OpenSearch date formats and custom date formats for date fields. Previously, only a limited set of formats were supported, always formatted to ISO local string or epoch.

Key changes:
- `ExprType` refactored to use `OpenSearchDateType` object
- Extracts `OpenSearchDateNamedFormatters` and `OpenSearchDateCustomFormatters` from field mappings
- Format information passed to `ExprValue` for proper date string parsing

#### Grammar Updates

Grammar changes synchronized with the main branch to ensure consistency across versions.

### Bug Fixes

| Fix | Description | PR |
|-----|-------------|-----|
| Pretty response formatting | Raw response now properly formatted when `pretty` query parameter is enabled | [#2829](https://github.com/opensearch-project/sql/pull/2829) |
| SparkExecutionEngineConfigClusterSetting | Fixed deserialization issue | [#2838](https://github.com/opensearch-project/sql/pull/2838) |
| SparkSubmitParameterModifier | Fixed parameter modifier issue | [#2837](https://github.com/opensearch-project/sql/pull/2837) |
| YAML errors | Fixed YAML errors causing CI checks not to run | [#2823](https://github.com/opensearch-project/sql/pull/2823) |
| Node.js version | Temporary use of older Node.js version before Almalinux8 migration | [#2816](https://github.com/opensearch-project/sql/pull/2816) |

## Limitations

- The span clause still functions as the first grouping key internally, regardless of position in the query syntax
- Custom date format support requires proper field mapping configuration

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#2720](https://github.com/opensearch-project/sql/pull/2720) | Span in PPL statsByClause could be specified after fields | [#2719](https://github.com/opensearch-project/sql/issues/2719) |
| [#2723](https://github.com/opensearch-project/sql/pull/2723) | Added Setting to Toggle Data Source Management Code Paths | [OpenSearch#13274](https://github.com/opensearch-project/OpenSearch/issues/13274) |
| [#2762](https://github.com/opensearch-project/sql/pull/2762) | Add support for custom date formats and OpenSearch date formats | [#2700](https://github.com/opensearch-project/sql/issues/2700) |
| [#2850](https://github.com/opensearch-project/sql/pull/2850) | Grammar updates synchronized with main branch | - |
| [#2829](https://github.com/opensearch-project/sql/pull/2829) | Well format raw response when pretty parameter enabled | - |
| [#2838](https://github.com/opensearch-project/sql/pull/2838) | Fix SparkExecutionEngineConfigClusterSetting deserialize issue | - |
| [#2837](https://github.com/opensearch-project/sql/pull/2837) | Fix SparkSubmitParameterModifier issue | - |
