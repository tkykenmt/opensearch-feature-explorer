# SQL/PPL Bug Fixes

## Summary

OpenSearch v3.3.0 includes 26 bug fixes and improvements for the SQL/PPL plugin, addressing issues in query execution, data type handling, function behavior, and documentation. Key fixes include count overflow handling, decimal precision improvements, nested field aggregation fixes, and enhanced error handling for index patterns.

## Details

### What's New in v3.3.0

This release focuses on stability and correctness improvements across the SQL/PPL plugin, with particular attention to the Calcite query engine and PPL grammar.

### Technical Changes

#### Query Execution Fixes

| Issue | Fix | PR |
|-------|-----|-----|
| count(*) capped at MAX_INTEGER | Changed return type from integer to bigint | [#4416](https://github.com/opensearch-project/sql/pull/4416) |
| Filter pushdown missing analyzed node | Fixed node handling in Search call pushdown | [#4388](https://github.com/opensearch-project/sql/pull/4388) |
| Limit pushdown with offset exceeding maxResultWindow | Prevent pushdown before action building | [#4377](https://github.com/opensearch-project/sql/pull/4377) |
| ClassCastException for nested field aggregates | Handle Map objects in value-storing aggregates | [#4360](https://github.com/opensearch-project/sql/pull/4360) |

#### Data Type and Function Fixes

| Issue | Fix | PR |
|-------|-----|-----|
| MOD function returns float for decimal operands | Return decimal type for decimal inputs | [#4407](https://github.com/opensearch-project/sql/pull/4407) |
| Negative scale in decimal literals | Ensure positive scale in Calcite | [#4401](https://github.com/opensearch-project/sql/pull/4401) |
| parse/grok/patterns returns empty string for NULL | Return NULL instead of empty string | [#4381](https://github.com/opensearch-project/sql/pull/4381) |
| Geopoint handling in complex data types | Fixed map case handling | [#4325](https://github.com/opensearch-project/sql/pull/4325) |

#### Error Handling Improvements

| Issue | Fix | PR |
|-------|-----|-----|
| Missing index pattern returns wrong error | Throw IndexNotFoundException | [#4369](https://github.com/opensearch-project/sql/pull/4369) |
| Alphanumeric search starting with number | Fixed PPL grammar for NUMERICID | [#4334](https://github.com/opensearch-project/sql/pull/4334) |
| Legacy JDBC type mapping inconsistency | Added type mapping at serialization | [#3613](https://github.com/opensearch-project/sql/pull/3613) |
| PPL Anonymizer not masking PPL queries | Updated Anonymizer to mask PPL | [#4352](https://github.com/opensearch-project/sql/pull/4352) |

### Usage Example

```sql
-- count(*) now returns bigint for large datasets
source = accounts | stats count(requestId)
-- Result type: bigint (was: integer capped at 2147483647)

-- MOD function with decimal operands
SELECT MOD(10.5, 3.2) as result
-- Result type: decimal (was: float)

-- Nested field aggregation now works correctly
source=logs-otel-v1* | stats first(`resource.attributes.telemetry.sdk.language`) by severityNumber

-- Alphanumeric search starting with number
source=demo-logs-otel-v1* 5a57f0a17fc6f59fb2ad8ec6b52ea3fa
-- Now correctly translates to Lucene query
```

### CI/CD and Documentation Improvements

| Category | Description | PRs |
|----------|-------------|-----|
| Test Infrastructure | Split test actions into unit, integ, and doctest | [#4193](https://github.com/opensearch-project/sql/pull/4193) |
| Precommit Hooks | Added spotless precommit hook + license check | [#4306](https://github.com/opensearch-project/sql/pull/4306), [#4320](https://github.com/opensearch-project/sql/pull/4320) |
| Doctest | Enable doctest with Calcite, fix branch | [#4379](https://github.com/opensearch-project/sql/pull/4379), [#4292](https://github.com/opensearch-project/sql/pull/4292) |
| CLI | Use 1.0 branch of CLI instead of main | [#4219](https://github.com/opensearch-project/sql/pull/4219) |
| Workflows | Add merge_group trigger to test workflows | [#4216](https://github.com/opensearch-project/sql/pull/4216) |

### Documentation Updates

| Document | Update | PR |
|----------|--------|-----|
| bin.rst | Updated and added to doctest | [#4384](https://github.com/opensearch-project/sql/pull/4384) |
| SPL/PPL cheat sheet | Updated timechart | [#4382](https://github.com/opensearch-project/sql/pull/4382) |
| rex doc | Corrected comparison table | [#4321](https://github.com/opensearch-project/sql/pull/4321) |
| coalesce | Updated documentation | [#4305](https://github.com/opensearch-project/sql/pull/4305) |
| fields/table commands | Updated documentation | [#4177](https://github.com/opensearch-project/sql/pull/4177) |
| UDF/UDAF | Added development guide | [#4094](https://github.com/opensearch-project/sql/pull/4094) |
| PPL cheat sheet | Added Splunk comparison | [#3726](https://github.com/opensearch-project/sql/pull/3726) |

## Limitations

- Geopoint fix currently handles only map case; array and other complex scenarios require follow-up
- Some backports to 2.19-dev branch failed and required manual backporting

## References

### Documentation
- [SQL and PPL Documentation](https://docs.opensearch.org/3.0/search-plugins/sql/index/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#4416](https://github.com/opensearch-project/sql/pull/4416) | Fix count(*) and dc(field) to be capped at MAX_INTEGER |
| [#4407](https://github.com/opensearch-project/sql/pull/4407) | Mod function should return decimal instead of float |
| [#4401](https://github.com/opensearch-project/sql/pull/4401) | Scale of decimal literal should always be positive in Calcite |
| [#4388](https://github.com/opensearch-project/sql/pull/4388) | Fix bug of missed analyzed node when pushdown filter for Search call |
| [#4384](https://github.com/opensearch-project/sql/pull/4384) | Update bin.rst and add bin to doctest |
| [#4382](https://github.com/opensearch-project/sql/pull/4382) | Update timechart in SPL/PPL cheat sheet |
| [#4381](https://github.com/opensearch-project/sql/pull/4381) | Fix parse related functions return behavior in case of NULL input |
| [#4379](https://github.com/opensearch-project/sql/pull/4379) | Enable doctest with Calcite |
| [#4377](https://github.com/opensearch-project/sql/pull/4377) | Prevent limit pushdown before action building |
| [#4369](https://github.com/opensearch-project/sql/pull/4369) | No index found with given index pattern should throw IndexNotFoundException |
| [#4360](https://github.com/opensearch-project/sql/pull/4360) | Fix ClassCastException for value-storing aggregates on nested PPL fields |
| [#4352](https://github.com/opensearch-project/sql/pull/4352) | Change Anonymizer to mask PPL |
| [#4334](https://github.com/opensearch-project/sql/pull/4334) | Fix alphanumeric search which starts with number |
| [#4325](https://github.com/opensearch-project/sql/pull/4325) | Fix geopoint issue in complex data types |
| [#4321](https://github.com/opensearch-project/sql/pull/4321) | Correct the comparison table for rex doc |
| [#4320](https://github.com/opensearch-project/sql/pull/4320) | Spotless precommit: apply instead of check |
| [#4306](https://github.com/opensearch-project/sql/pull/4306) | Add spotless precommit hook + license check |
| [#4305](https://github.com/opensearch-project/sql/pull/4305) | Updating coalesce documentation |
| [#4292](https://github.com/opensearch-project/sql/pull/4292) | Fix doctest branch |
| [#4219](https://github.com/opensearch-project/sql/pull/4219) | Doctest: Use 1.0 branch of CLI instead of main |
| [#4216](https://github.com/opensearch-project/sql/pull/4216) | Add merge_group trigger to test workflows |
| [#4193](https://github.com/opensearch-project/sql/pull/4193) | Split up test actions into unit, integ, and doctest |
| [#4177](https://github.com/opensearch-project/sql/pull/4177) | Updating documentation for fields and table commands |
| [#4094](https://github.com/opensearch-project/sql/pull/4094) | Add documents on how to develop a UDF / UDAF |
| [#3726](https://github.com/opensearch-project/sql/pull/3726) | Add splunk to ppl cheat sheet |
| [#3613](https://github.com/opensearch-project/sql/pull/3613) | Bugfix: SQL type mapping for legacy JDBC output |

### Issues (Design / RFC)
- [Issue #4387](https://github.com/opensearch-project/sql/issues/4387): Filter pushdown missing analyzed node
- [Issue #4380](https://github.com/opensearch-project/sql/issues/4380): parse/grok/patterns NULL handling
- [Issue #4376](https://github.com/opensearch-project/sql/issues/4376): Limit pushdown with offset
- [Issue #4406](https://github.com/opensearch-project/sql/issues/4406): MOD function return type
- [Issue #4391](https://github.com/opensearch-project/sql/issues/4391): Decimal literal negative scale
- [Issue #4342](https://github.com/opensearch-project/sql/issues/4342): IndexNotFoundException for missing index
- [Issue #4359](https://github.com/opensearch-project/sql/issues/4359): ClassCastException for nested field aggregates
- [Issue #4324](https://github.com/opensearch-project/sql/issues/4324): Geopoint in complex data types
- [Issue #1545](https://github.com/opensearch-project/sql/issues/1545): Legacy JDBC type mapping
- [Issue #3159](https://github.com/opensearch-project/sql/issues/3159): Legacy JDBC type mapping

## Related Feature Report

- [Full feature documentation](../../../features/sql/sql-ppl-bug-fixes.md)
