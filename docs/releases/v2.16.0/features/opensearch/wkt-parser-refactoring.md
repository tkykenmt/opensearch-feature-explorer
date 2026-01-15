---
tags:
  - opensearch
---
# WKT Parser Refactoring

## Summary

OpenSearch v2.16.0 refactors several recursive parsing methods to use iterative approaches, preventing stack overflow errors and improving stability when processing deeply nested structures.

## Details

### What's New in v2.16.0

Three parsing components were refactored from recursive to iterative implementations:

| Component | File | Change |
|-----------|------|--------|
| WKT Parser | `WellKnownText.java` | GeometryCollection parsing now uses iterative approach with depth limit |
| FilterPath Parser | `FilterPath.java` | Path segment parsing uses regex-based splitting instead of recursion |
| Grok Pattern Validator | `Grok.java` | Pattern bank validation uses stack-based iteration |

### Technical Changes

#### WKT GeometryCollection Parser

The `parseGeometryCollection` method was refactored to use a `Deque` for managing nested geometry collections:

- Uses `ArrayDeque` instead of recursive calls
- Introduces `MAX_DEPTH_OF_GEO_COLLECTION = 1000` limit
- Throws `IllegalArgumentException` when depth exceeds limit

#### FilterPath Parser

The `FilterPath.parse` method was simplified:

- Uses regex `(?<!\\)\\.` to split filter paths by unescaped dots
- Builds `FilterPath` chain iteratively from end to start
- Handles empty strings and null values gracefully

#### Grok Pattern Validator

The `validatePatternBank` method was refactored:

- Uses `Frame` class to track pattern name, path, and start index
- Implements `MAX_PATTERN_DEPTH_SIZE = 500` limit
- Detects circular references using `pathMap` for visited patterns

## Limitations

- GeometryCollection depth limited to 1000 levels
- Grok pattern reference depth limited to 500 levels
- These limits are hardcoded and not configurable

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14086](https://github.com/opensearch-project/OpenSearch/pull/14086) | Switch to iterative version of WKT format parser | - |
| [#14200](https://github.com/opensearch-project/OpenSearch/pull/14200) | Refactoring FilterPath.parse by using an iterative approach | [#12067](https://github.com/opensearch-project/OpenSearch/issues/12067) |
| [#14206](https://github.com/opensearch-project/OpenSearch/pull/14206) | Refactoring Grok.validatePatternBank by using an iterative approach | - |
