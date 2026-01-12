---
tags:
  - sql
---

# SQL/PPL Plugin

OpenSearch SQL/PPL plugin provides SQL and Piped Processing Language (PPL) query interfaces.

## Overview

- [SQL/PPL Engine](sql-ppl-engine.md) - Plugin overview and engine selection

## Query Engines

| Engine | Description | Document |
|--------|-------------|----------|
| V3 Calcite | Apache Calcite-based with advanced optimization | [Calcite Query Engine](sql-calcite-query-engine.md) |
| V2 | Modern query engine | [SQL/PPL Engine](sql-ppl-engine.md) |
| V1 Legacy | Original engine (pagination, cursor) | [SQL/PPL Engine](sql-ppl-engine.md) |

## PPL Commands & Functions

### Commands
| Document | Description |
|----------|-------------|
| [PPL Commands (Calcite)](sql-ppl-commands-calcite.md) | chart, streamstats, multisearch, replace, appendpipe |
| [Patterns Command](sql-ppl-patterns-command.md) | Log pattern extraction |
| [Timechart Command](sql-ppl-timechart-command.md) | Time-series aggregation |
| [Rename Command](sql-ppl-rename-command.md) | Field renaming with wildcards |
| [Rex and Regex Commands](sql-ppl-rex-and-regex-commands.md) | Regex-based text processing |
| [Spath Command](sql-ppl-spath-command.md) | JSON field extraction |

### Functions
| Document | Description |
|----------|-------------|
| [Aggregate Functions](sql-ppl-aggregate-functions.md) | count, avg, sum, take, etc. |
| [Eval Functions](sql-ppl-eval-functions.md) | Data transformation functions |

### Optimization
| Document | Description |
|----------|-------------|
| [Query Optimization](ppl-opensearch-query-optimization.md) | Pushdown, sort, aggregation optimizations |
| [Query Enhancements](ppl-opensearch-dashboards-query-enhancements.md) | Full-text search, time modifiers, JOIN |

## SQL Features

| Document | Description |
|----------|-------------|
| [Pagination](sql-pagination.md) | Cursor-based pagination with PIT |
| [PIT Refactor](sql-pit-refactor.md) | Point in Time for consistent results |
| [Error Handling](sql-error-handling.md) | Error messages and status codes |

## External Data Sources

| Document | Description |
|----------|-------------|
| [Security Lake](sql-security-lake-data-source.md) | Query Amazon Security Lake |
| [Flint Index Operations](sql-flint-index-operations.md) | Flint index management |
| [Flint Query Scheduler](sql-flint-query-scheduler.md) | Automatic index refresh |

## Maintenance

| Document | Description |
|----------|-------------|
| [CI/Tests](sql-dashboards-observability-search-relevance-ci-tests.md) | Testing infrastructure |
| [Plugin Maintenance](sql-plugin-maintenance.md) | Dependencies and security fixes |
| [Documentation](sql-ppl-documentation.md) | PPL documentation updates |
