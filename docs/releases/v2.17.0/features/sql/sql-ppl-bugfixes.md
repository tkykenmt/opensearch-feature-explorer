---
tags:
  - domain/search
  - component/server
  - search
  - security
  - sql
---
# SQL/PPL Bugfixes

## Summary

OpenSearch v2.17.0 includes several bugfixes for the SQL/PPL plugin addressing issues with PPL boolean function case sensitivity, UDF function restrictions, Spark execution engine configuration, query job type handling, and build infrastructure fixes.

## Details

### What's New in v2.17.0

This release focuses on stability and correctness improvements across the SQL/PPL plugin:

1. **PPL Boolean Function Case Insensitivity**: Fixed an issue where boolean functions like `isnotnull()` worked but `ISNOTNULL()` did not
2. **UDF Function Restrictions**: Blocked UDF creation queries in the async query API for security
3. **SqlBaseParser Update**: Fixed parser file validity for network-disconnected build environments
4. **Spark Execution Engine Config Fix**: Resolved deserialization issues with `SparkExecutionEngineConfigClusterSetting`
5. **Job Type Fixes**: Corrected job type handling for Batch and IndexDML queries
6. **Query Handler Fix**: Fixed handler for existing query scenarios
7. **BWC Test Fix**: Resolved integration test issues with `sqlBwcCluster#fullRestartClusterTask`

### Technical Changes

#### PPL Boolean Function Case Sensitivity

The PPL parser was updated to handle boolean functions in a case-insensitive manner, aligning with standard SQL behavior.

**Before (broken)**:
```ppl
source=logs | where ISNOTNULL(field)  // Error
```

**After (fixed)**:
```ppl
source=logs | where ISNOTNULL(field)  // Works
source=logs | where isnotnull(field)  // Also works
```

#### UDF Function Restrictions

UDF (User Defined Function) creation queries are now blocked in the async query API to prevent potential security issues.

#### Spark Execution Engine Configuration

Fixed a deserialization issue in `SparkExecutionEngineConfigClusterSetting` that could cause configuration loading failures.

#### Job Type Handling

Corrected the job type assignment for Batch and IndexDML queries, ensuring proper query execution routing.

## Limitations

- These are bugfixes only; no new features are introduced
- UDF creation is now restricted in async query API

## References

### Documentation
- [SQL and PPL Documentation](https://docs.opensearch.org/2.17/search-plugins/sql/index/): Official documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#2842](https://github.com/opensearch-project/sql/pull/2842) | Boolean function in PPL should be case insensitive (backport of #2758) |
| [#2884](https://github.com/opensearch-project/sql/pull/2884) | Restrict UDF functions (backport of #2790) |
| [#2890](https://github.com/opensearch-project/sql/pull/2890) | Update SqlBaseParser for build fix |
| [#2972](https://github.com/opensearch-project/sql/pull/2972) | Fix SparkExecutionEngineConfigClusterSetting deserialize issue (backport of #2966) |
| [#2982](https://github.com/opensearch-project/sql/pull/2982) | Fix jobType for Batch and IndexDML query (backport of #2955) |
| [#2983](https://github.com/opensearch-project/sql/pull/2983) | Fix handler for existing query (backport of #2968) |
| [#2996](https://github.com/opensearch-project/sql/pull/2996) | Fix :integ-test:sqlBwcCluster#fullRestartClusterTask (backport of #2900) |

### Issues (Design / RFC)
- [Issue #2431](https://github.com/opensearch-project/sql/issues/2431): Boolean function case sensitivity issue
- [Issue #2761](https://github.com/opensearch-project/sql/issues/2761): UDF restriction requirement

## Related Feature Report

- [SQL/PPL Engine](../../../features/sql/sql-ppl-engine.md)
