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
| V3 Calcite | Apache Calcite-based with advanced optimization | [Calcite Query Engine](calcite-query-engine.md) |
| V2 | Modern query engine | [SQL/PPL Engine](sql-ppl-engine.md) |
| V1 Legacy | Original engine (pagination, cursor) | [SQL/PPL Engine](sql-ppl-engine.md) |

## PPL Commands & Functions

### Commands
| Document | Description |
|----------|-------------|
| [PPL Commands (Calcite)](ppl-commands-calcite.md) | chart, streamstats, multisearch, replace, appendpipe |
| [Patterns Command](ppl-patterns-command.md) | Log pattern extraction |
| [Timechart Command](ppl-timechart-command.md) | Time-series aggregation |
| [Rename Command](ppl-rename-command.md) | Field renaming with wildcards |
| [Rex and Regex Commands](ppl-rex-and-regex-commands.md) | Regex-based text processing |
| [Spath Command](ppl-spath-command.md) | JSON field extraction |

### Functions
| Document | Description |
|----------|-------------|
| [Aggregate Functions](ppl-aggregate-functions.md) | count, avg, sum, take, etc. |
| [Eval Functions](ppl-eval-functions.md) | Data transformation functions |

### Optimization
| Document | Description |
|----------|-------------|
| [Query Optimization](ppl-query-optimization.md) | Pushdown, sort, aggregation optimizations |
| [Query Enhancements](ppl-query-enhancements.md) | Full-text search, time modifiers, JOIN |

## SQL Features

| Document | Description |
|----------|-------------|
| [Pagination](sql-pagination.md) | Cursor-based pagination with PIT |
| [PIT Refactor](sql-pit-refactor.md) | Point in Time for consistent results |
| [Error Handling](sql-error-handling.md) | Error messages and status codes |

## External Data Sources

| Document | Description |
|----------|-------------|
| [Security Lake](security-lake-data-source.md) | Query Amazon Security Lake |
| [Flint Index Operations](flint-index-operations.md) | Flint index management |
| [Flint Query Scheduler](flint-query-scheduler.md) | Automatic index refresh |

## Maintenance

| Document | Description |
|----------|-------------|
| [CI/Tests](sql-ci-tests.md) | Testing infrastructure |
| [Plugin Maintenance](sql-plugin-maintenance.md) | Dependencies and security fixes |
| [Documentation](ppl-documentation.md) | PPL documentation updates |
