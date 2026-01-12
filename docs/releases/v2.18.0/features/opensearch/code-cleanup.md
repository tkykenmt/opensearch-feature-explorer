---
tags:
  - performance
  - search
---

# Code Cleanup

## Summary

OpenSearch v2.18.0 includes several code cleanup improvements that simplify the query approximation framework, fix inefficient Stream API usage patterns, and correct a typo in the RemoteStoreNodeAttribute class. These changes improve code maintainability and performance without changing user-facing behavior.

## Details

### What's New in v2.18.0

This release consolidates three code cleanup improvements:

1. **Query Approximation Framework Simplification**: Removed the redundant `ApproximateIndexOrDocValuesQuery` class by leveraging the existing `ApproximateScoreQuery` wrapper
2. **Stream API Optimization**: Fixed inefficient Stream API call chains ending with `count()` in the percolator module
3. **Typo Fix**: Corrected `super.toString()` to `sb.toString()` in `RemoteStoreNodeAttribute`

### Technical Changes

#### Query Approximation Refactoring

The `ApproximateIndexOrDocValuesQuery` class was removed because `ApproximateScoreQuery` already provides the ability to choose between approximate and original queries. The refactoring:

- Removes `ApproximateIndexOrDocValuesQuery.java` (62 lines)
- Updates `DateFieldMapper` to use `ApproximateScoreQuery` directly with `IndexOrDocValuesQuery` as the original query
- Simplifies the approximation check in `ApproximatePointRangeQuery.canApproximate()`
- Makes `ApproximateScoreQuery` final and its `resolvedQuery` field package-private

```java
// Before: Specialized wrapper
new ApproximateIndexOrDocValuesQuery(
    pointRangeQuery,
    approximateQuery,
    dvQuery
)

// After: Generic wrapper with IndexOrDocValuesQuery
new ApproximateScoreQuery(
    new IndexOrDocValuesQuery(pointRangeQuery, dvQuery),
    approximateQuery
)
```

#### Stream API Optimization

Fixed inefficient Stream API patterns in `QueryAnalyzer.minTermLength()`:

```java
// Before: Two separate stream operations
if (extractions.stream().filter(q -> q.term != null).count() == 0
    && extractions.stream().filter(q -> q.range != null).count() > 0) {
    return Integer.MIN_VALUE;
}

// After: Single loop with boolean flags
boolean hasTerm = false;
boolean hasRange = false;
for (QueryExtraction qt : extractions) {
    if (qt.term != null) {
        hasTerm = true;
        min = Math.min(min, qt.bytes().length);
    }
    if (qt.range != null) {
        hasRange = true;
    }
}
if (!hasTerm && hasRange) {
    return Integer.MIN_VALUE;
}
```

#### RemoteStoreNodeAttribute Typo Fix

```java
// Before: Returns Object.toString() instead of built string
public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append('{').append(this.repositoriesMetadata).append('}');
    return super.toString();  // Bug: ignores sb
}

// After: Returns the constructed string
public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append('{').append(this.repositoriesMetadata).append('}');
    return sb.toString();  // Fixed
}
```

### Files Changed

| PR | Files Modified | Lines Changed |
|----|----------------|---------------|
| #16273 | 14 files | +117/-175 |
| #15386 | 2 files | +14/-7 |
| #15362 | 2 files | +2/-1 |

## Limitations

- These are internal code improvements with no user-facing API changes
- The query approximation refactoring requires the `approximate_point_range_query` feature flag to be enabled

## References

### Documentation
- [PR #16273](https://github.com/opensearch-project/OpenSearch/pull/16273): Query approximation framework cleanup
- [PR #15386](https://github.com/opensearch-project/OpenSearch/pull/15386): Stream API optimization
- [PR #15362](https://github.com/opensearch-project/OpenSearch/pull/15362): RemoteStoreNodeAttribute typo fix

### Pull Requests
| PR | Description |
|----|-------------|
| [#16273](https://github.com/opensearch-project/OpenSearch/pull/16273) | Remove ApproximateIndexOrDocValuesQuery |
| [#15386](https://github.com/opensearch-project/OpenSearch/pull/15386) | Fix inefficient Stream API call chains ending with count() |
| [#15362](https://github.com/opensearch-project/OpenSearch/pull/15362) | Fix typo super->sb in method toString() of RemoteStoreNodeAttribute |

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/opensearch-code-cleanup.md)
