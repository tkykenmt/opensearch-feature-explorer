---
tags:
  - indexing
  - search
---

# OpenSearch Learning to Rank

## Summary

This release includes infrastructure and test stability improvements for the Learning to Rank plugin. The changes upgrade the build toolchain to Gradle 8.14 with JDK 24 support and fix flaky test failures caused by floating-point precision issues in similarity score comparisons.

## Details

### What's New in v3.2.0

Two bug fixes improve the plugin's build infrastructure and test reliability:

1. **Build Toolchain Upgrade**: Gradle upgraded from 8.10.2 to 8.14, codecov action updated to v5, and JDK 24 support added to CI matrix
2. **Flaky Test Fix**: ULP (Units in Last Place) tolerance for similarity score comparisons increased from 1 to 30,000 to handle floating-point precision variations

### Technical Changes

#### Build Infrastructure Updates

| Component | Before | After |
|-----------|--------|-------|
| Gradle | 8.10.2 | 8.14 |
| Codecov Action | v4 | v5 |
| JDK CI Matrix | 21, 23 | 21, 24 |

#### Test Stability Fix

The `LtrQueryTests.testOnRewrittenQueries` test was failing intermittently due to floating-point precision differences in similarity score calculations. Different similarity classes (e.g., `IBSimilarity`) produce varying floating-point accuracy.

```java
// Before: Strict comparison (1 ULP tolerance)
private static final int SCORE_NB_ULP_PREC = 1;

// After: Relaxed comparison (30,000 ULP tolerance)
private static final int SCORE_NB_ULP_PREC = 30000;
```

The ULP (Units in Last Place) value of 30,000 means there can be up to 30,000 representable floating-point numbers between compared similarity scores. This accommodates the inherent precision variations without indicating logic errors.

## Limitations

- The relaxed ULP tolerance is specific to test assertions and does not affect production scoring behavior
- JDK 23 support removed from CI matrix in favor of JDK 24

## References

### Documentation
- [Learning to Rank Documentation](https://docs.opensearch.org/3.0/search-plugins/ltr/index/)
- [GitHub Repository](https://github.com/opensearch-project/opensearch-learning-to-rank-base)

### Pull Requests
| PR | Description |
|----|-------------|
| [#202](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/202) | Bump gradle to 8.14, codecov to v5 and support JDK24 |
| [#205](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/205) | Updating ULP for similarity score comparisons to 30000 to avoid flaky tests |

### Issues (Design / RFC)
- [Issue #196](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/196): Distribution Build Failed for opensearch-learning-to-rank-base-3.2.0
- [Issue #152](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/152): Flaky test LtrQueryTests.testOnRewrittenQueries

## Related Feature Report

- [Full feature documentation](../../../../features/learning/learning-to-rank.md)
