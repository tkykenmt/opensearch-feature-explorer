# SQL/PPL Bug Fixes

## Summary

OpenSearch v3.1.0 includes 17 bug fixes for the SQL/PPL plugin, addressing issues in query execution, function behavior, filter pushdown, and Calcite engine compatibility. Key fixes resolve crashes with long IN-lists, incorrect function results for `ATAN`, `CONV`, and `UNIX_TIMESTAMP`, and field resolution issues in JOIN operations.

## Details

### What's New in v3.1.0

This release focuses on stability and correctness improvements across both the legacy v2 engine and the new Calcite-based engine.

### Technical Changes

#### Query Execution Fixes

| Issue | Fix | PR |
|-------|-----|-----|
| Long IN-lists cause StackOverflowError | Rewrite `or` tree as balanced tree for logarithmic recursion | [#3660](https://github.com/opensearch-project/sql/pull/3660) |
| NPE in Calcite aggregate queries | Add trimmed project before aggregate | [#3621](https://github.com/opensearch-project/sql/pull/3621) |
| Limit with offset exceeds maxResultWindow | Prevent pushdown when startFrom reaches maxResultWindow | [#3713](https://github.com/opensearch-project/sql/pull/3713) |
| query.size_limit affects intermediate results | Make size_limit only affect final results | [#3623](https://github.com/opensearch-project/sql/pull/3623) |

#### Function Fixes

| Function | Issue | Fix | PR |
|----------|-------|-----|-----|
| `ATAN(x, y)` | Two-parameter form not supported in v3 | Add two-parameter support in Calcite engine | [#3748](https://github.com/opensearch-project/sql/pull/3748) |
| `CONV(x, a, b)` | Incorrect type conversion | Fix type conversion logic | [#3748](https://github.com/opensearch-project/sql/pull/3748) |
| `UNIX_TIMESTAMP` | Incorrect precision with timestamp strings | Reorder signatures to prioritize timestamp coercion | [#3679](https://github.com/opensearch-project/sql/pull/3679) |

#### Field and Type Handling Fixes

| Issue | Fix | PR |
|-------|-----|-----|
| Alias type referring to nested field fails | Support alias type with nested field path | [#3674](https://github.com/opensearch-project/sql/pull/3674) |
| Script filter with struct field throws error | Prevent pushdown for struct type fields | [#3693](https://github.com/opensearch-project/sql/pull/3693) |
| Filter with nested text field fails | Use original field's keyword for text type | [#3645](https://github.com/opensearch-project/sql/pull/3645) |
| Ambiguous column names in JOIN output | Rename duplicated columns with alias/table prefix | [#3760](https://github.com/opensearch-project/sql/pull/3760) |

#### Infrastructure and Maintenance

| Change | PR |
|--------|-----|
| Migrate UDFs to PPLFuncImpTable | [#3576](https://github.com/opensearch-project/sql/pull/3576) |
| Revert stream pattern method, implement SIMPLE_PATTERN | [#3553](https://github.com/opensearch-project/sql/pull/3553) |
| Remove duplicated timestamp row in data type mapping | [#2617](https://github.com/opensearch-project/sql/pull/2617) |
| Update PPL Limitation Docs | [#3656](https://github.com/opensearch-project/sql/pull/3656) |
| Create org/opensearch/direct-query/ directory | [#3649](https://github.com/opensearch-project/sql/pull/3649) |
| Add TPC-H PPL query suite | [#3622](https://github.com/opensearch-project/sql/pull/3622) |
| Modified workflow: Grammar Files & Async Query Core | [#3715](https://github.com/opensearch-project/sql/pull/3715) |

### Usage Example

```sql
-- Long IN-list now works without StackOverflowError
SELECT * FROM my_index WHERE id IN (1, 2, 3, ... /* hundreds of values */)

-- ATAN with two parameters now supported
SELECT ATAN(1, 2) FROM my_index

-- UNIX_TIMESTAMP returns correct precision
SELECT UNIX_TIMESTAMP('2025-01-10 12:30:45.123') FROM my_index

-- JOIN with ambiguous columns now properly qualified
source=table1 | join left=t1 right=t2 on t1.id=t2.id table2 | fields t1.id, t2.id
```

## Limitations

- Script filter pushdown is disabled for struct type fields in v2 engine (Calcite engine doesn't support script pushdown)
- Alias fields pointing to text type require using the original field's keyword for filter operations

## References

### Documentation
- [SQL and PPL Documentation](https://docs.opensearch.org/3.1/search-plugins/sql/index/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#3693](https://github.com/opensearch-project/sql/pull/3693) | Fix error when pushing down script filter with struct field |
| [#3674](https://github.com/opensearch-project/sql/pull/3674) | Fix alias type referring to nested field |
| [#3660](https://github.com/opensearch-project/sql/pull/3660) | Fix: Long IN-lists causes crash |
| [#3621](https://github.com/opensearch-project/sql/pull/3621) | Add a trimmed project before aggregate to avoid NPE in Calcite |
| [#3760](https://github.com/opensearch-project/sql/pull/3760) | Fix field not found issue in join output when column names are ambiguous |
| [#3748](https://github.com/opensearch-project/sql/pull/3748) | Fix: correct ATAN(x, y) and CONV(x, a, b) functions bug |
| [#3679](https://github.com/opensearch-project/sql/pull/3679) | Return double with correct precision for UNIX_TIMESTAMP |
| [#3713](https://github.com/opensearch-project/sql/pull/3713) | Prevent push down limit with offset reach maxResultWindow |
| [#3645](https://github.com/opensearch-project/sql/pull/3645) | Fix pushing down filter with nested field of the text type |
| [#3623](https://github.com/opensearch-project/sql/pull/3623) | Make query.size_limit only affect the final results |
| [#3553](https://github.com/opensearch-project/sql/pull/3553) | Revert stream pattern method in V2 and implement SIMPLE_PATTERN |
| [#2617](https://github.com/opensearch-project/sql/pull/2617) | Remove the duplicated timestamp row in data type mapping table |
| [#3576](https://github.com/opensearch-project/sql/pull/3576) | Migrate existing UDFs to PPLFuncImpTable |
| [#3715](https://github.com/opensearch-project/sql/pull/3715) | Modified workflow: Grammar Files & Async Query Core |
| [#3656](https://github.com/opensearch-project/sql/pull/3656) | Update PPL Limitation Docs |
| [#3649](https://github.com/opensearch-project/sql/pull/3649) | Create a new directory org/opensearch/direct-query/ |
| [#3622](https://github.com/opensearch-project/sql/pull/3622) | Add a TPC-H PPL query suite |

### Issues (Design / RFC)
- [Issue #1469](https://github.com/opensearch-project/sql/issues/1469): Long IN-lists causes crash
- [Issue #3312](https://github.com/opensearch-project/sql/issues/3312): Script filter with struct field error
- [Issue #3646](https://github.com/opensearch-project/sql/issues/3646): Alias type referring to nested field
- [Issue #3566](https://github.com/opensearch-project/sql/issues/3566): NPE in Calcite aggregate
- [Issue #3617](https://github.com/opensearch-project/sql/issues/3617): Field not found in join output
- [Issue #3672](https://github.com/opensearch-project/sql/issues/3672): ATAN and CONV function bugs
- [Issue #3611](https://github.com/opensearch-project/sql/issues/3611): UNIX_TIMESTAMP precision
- [Issue #3102](https://github.com/opensearch-project/sql/issues/3102): Limit with offset exceeds maxResultWindow

## Related Feature Report

- [Full feature documentation](../../../features/sql/sql-ppl-bug-fixes.md)
