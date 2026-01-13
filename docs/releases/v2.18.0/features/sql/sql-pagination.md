---
tags:
  - domain/search
  - component/server
  - dashboards
  - search
  - sql
---
# SQL Pagination Bug Fixes

## Summary

This release fixes two bugs related to SQL pagination functionality. The first fix allows SQL pagination to work correctly with the `pretty` URL parameter, which is commonly used in OpenSearch Dashboards Dev Tools. The second fix addresses several minor issues with the SQL PIT (Point in Time) refactor, including NullPointerException errors in join queries and incorrect cursor generation.

## Details

### What's New in v2.18.0

Two bug fixes improve the reliability of SQL pagination:

1. **Pretty Parameter Support**: SQL pagination now works correctly when the `pretty` URL parameter is included in requests, fixing a regression that broke pagination in Dev Tools.

2. **PIT Refactor Bug Fixes**: Several issues discovered during E2E testing of the SQL PIT refactor have been resolved.

### Technical Changes

#### Bug Fix 1: Pretty Parameter Support (PR #2759)

The V2 pagination implementation previously restricted URL parameters, causing requests with the `pretty` parameter to fall back to the V1 engine. This resulted in cursor encoding mismatches and NullPointerException errors.

**Root Cause**: The `isSupported()` method in `SQLQueryRequest.java` only allowed the `format` parameter, rejecting requests with `pretty`.

**Fix**: Updated the parameter validation to accept both `format` and `pretty` as supported parameters:

```java
// Before: Only format was supported
var noUnsupportedParams = params.isEmpty() || 
    (params.size() == 1 && params.containsKey(QUERY_PARAMS_FORMAT));

// After: Both format and pretty are supported
Predicate<String> supportedParams = Set.of(QUERY_PARAMS_FORMAT, QUERY_PARAMS_PRETTY)::contains;
boolean hasUnsupportedParams = (!params.isEmpty()) && 
    params.keySet().stream().dropWhile(supportedParams).findAny().isPresent();
```

#### Bug Fix 2: PIT Refactor Issues (PR #3045)

| Issue | Description | Fix |
|-------|-------------|-----|
| Join query NPE | Join queries failing with NullPointerException when internal errors occur | Added proper exception handling with meaningful error message |
| Incorrect cursor | Cursor returned when not needed (e.g., `SELECT a.* FROM index a`) | Fixed `isDefaultCursor()` to check `fetchSize != 0` before generating cursor |
| Invalid size parameter | Using `size` instead of `fetch_size` generated unusable cursor | Fixed cursor generation logic to only create cursor when `fetch_size` is properly specified |

**Key Code Change in `PrettyFormatRestExecutor.java`**:

```java
protected boolean isDefaultCursor(SearchResponse searchResponse, DefaultQueryAction queryAction) {
    if (LocalClusterState.state().getSettingValue(SQL_PAGINATION_API_SEARCH_AFTER)) {
        // Fixed: Check fetchSize is not 0 before generating cursor
        return queryAction.getSqlRequest().fetchSize() != 0
            && Objects.requireNonNull(searchResponse.getHits().getTotalHits()).value
                >= queryAction.getSqlRequest().fetchSize();
    } else {
        return !Strings.isNullOrEmpty(searchResponse.getScrollId());
    }
}
```

### Usage Example

SQL pagination now works correctly in Dev Tools with the `pretty` parameter:

```bash
# Initial query with fetch_size
POST _plugins/_sql?pretty
{
  "query": "SELECT * FROM accounts",
  "fetch_size": 5
}

# Response includes cursor for pagination
{
  "schema": [...],
  "cursor": "n:1f8b08000000000000ff...",
  "total": 100,
  "datarows": [...],
  "size": 5,
  "status": 200
}

# Subsequent request with cursor (pretty parameter now works)
POST _plugins/_sql?pretty
{
  "cursor": "n:1f8b08000000000000ff..."
}
```

## Limitations

- Pagination only supports basic queries (no aggregations, nested queries, etc.)
- The `fetch_size` parameter is only supported for the `jdbc` response format
- A value of 0 for `fetch_size` falls back to non-paginated response

## References

### Documentation
- [SQL and PPL API Documentation](https://docs.opensearch.org/2.18/search-plugins/sql/sql-ppl-api/): Official API documentation
- [Point in Time Documentation](https://docs.opensearch.org/2.18/search-plugins/searching-data/point-in-time/): PIT in SQL

### Pull Requests
| PR | Description |
|----|-------------|
| [#3106](https://github.com/opensearch-project/sql/pull/3106) | Backport: SQL pagination should work with the `pretty` parameter |
| [#3108](https://github.com/opensearch-project/sql/pull/3108) | Backport: Bug Fixes for minor issues with SQL PIT refactor |
| [#2759](https://github.com/opensearch-project/sql/pull/2759) | Original: SQL pagination should work with the `pretty` parameter |
| [#3045](https://github.com/opensearch-project/sql/pull/3045) | Original: Bug Fixes for minor issues with SQL PIT refactor |

### Issues (Design / RFC)
- [Issue #2460](https://github.com/opensearch-project/sql/issues/2460): SQL pagination doesn't work in Dev tools

## Related Feature Report

- Full feature documentation
