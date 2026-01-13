---
tags:
  - sql
---
# SQL/PPL

## Summary

OpenSearch v2.19.0 brings enhancements to the SQL/PPL plugin including improved query validation, metadata field support in PPL, async query state management, and various bug fixes for datetime parsing, CSV output, and query execution.

## Details

### What's New in v2.19.0

#### PPL Metadata Fields Support
PPL queries now support OpenSearch reserved metadata fields (`_id`, `_index`, `_sort`, `_score`, `_max_score`). Previously, fields starting with underscore were not allowed in PPL clauses.

```ppl
source=my_index | fields _id, _index, field1
```

#### Grammar Validation for PPL
Added grammar validation for PPL queries with support for validating unsupported types, identifiers, and commands. This provides better error messages when users attempt to use unsupported grammar elements.

#### Flint Extension Query Validation
Added validation method for Flint extension queries wired into the dispatcher, improving query validation for Flint-based operations.

#### Async Query State Management
- Query cancellation now properly calls `updateState` to update cancel status
- LeaseManager is now called for BatchQuery operations

### Bug Fixes

| Issue | Fix |
|-------|-----|
| Datetime parsing with custom format | Fixed regression in parsing datetime strings with custom time format in Span operations |
| CSV/Raw output quote escaping | Fixed quote escaping in CSV and Raw output formats |
| FilterOperator consumption | Fixed FilterOperator to cache next element, preventing repeated consumption on `hasNext()` calls |
| `str_to_date` two-digit year | Fixed `str_to_date` function to correctly handle two-digit years (RFC 822 format) |
| `field_type_tolerance` documentation | Added documentation for the `plugins.query.field_type_tolerance` setting |

### Configuration

| Setting | Description |
|---------|-------------|
| `plugins.query.field_type_tolerance` | Controls field type tolerance behavior in queries |

## Limitations

- Grammar validation for unsupported types/identifiers/commands may reject previously accepted (but unsupported) queries

## References

### Pull Requests

| PR | Description |
|----|-------------|
| [#2789](https://github.com/opensearch-project/sql/pull/2789) | Allow metadata fields in PPL query |
| [#3167](https://github.com/opensearch-project/sql/pull/3167) | Add grammar validation for PPL |
| [#3195](https://github.com/opensearch-project/sql/pull/3195) | Add validation for unsupported type/identifier/commands |
| [#3096](https://github.com/opensearch-project/sql/pull/3096) | Add validation method for Flint extension queries |
| [#3139](https://github.com/opensearch-project/sql/pull/3139) | Call updateState when query is cancelled |
| [#3153](https://github.com/opensearch-project/sql/pull/3153) | Call LeaseManager for BatchQuery |
| [#3079](https://github.com/opensearch-project/sql/pull/3079) | Fix datetime string parsing with custom time format in Span |
| [#3063](https://github.com/opensearch-project/sql/pull/3063) | Fix CSV and Raw output quote escaping |
| [#3123](https://github.com/opensearch-project/sql/pull/3123) | Fix FilterOperator to cache next element |
| [#2841](https://github.com/opensearch-project/sql/pull/2841) | Fix str_to_date with two-digit year |
| [#3118](https://github.com/opensearch-project/sql/pull/3118) | Add field_type_tolerance setting documentation |

### Documentation
- [SQL and PPL Documentation](https://docs.opensearch.org/2.19/search-plugins/sql/index/)
