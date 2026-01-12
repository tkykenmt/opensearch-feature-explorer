---
tags:
  - search
---

# Flaky Test Fixes

## Summary

OpenSearch v3.3.0 includes fixes for several flaky tests that were causing intermittent CI failures. These fixes improve test reliability by addressing timing issues, locale-dependent behavior, and query complexity limits in the test framework.

## Details

### What's New in v3.3.0

This release addresses three categories of flaky test failures:

1. **IntervalQueryBuilderTests** - Fixed excessive disjunction expansion causing test failures
2. **SecureReactorNetty4HttpServerTransportTests** - Fixed locale-dependent certificate generation issues

### Technical Changes

#### IntervalQuery Disjunction Fix

The `IntervalQueryBuilderTests.testToQuery` test was failing intermittently when randomly generated interval queries exceeded Lucene's maximum clause count limit during disjunction expansion.

**Root Cause**: When combining multiple `IntervalsSource` objects with `maxGaps=0` and `ORDERED` mode, the number of disjunctions can grow exponentially. Lucene enforces a limit via `IndexSearcher.getMaxClauseCount()`.

**Solution**: Added early detection of disjunction count before attempting to combine sources:

| Component | Change |
|-----------|--------|
| `IntervalBuilder` | Added `canCombineSources()` method to check disjunction count |
| `IntervalsSourceProvider.Combine` | Throws `IllegalArgumentException` when disjunction limit exceeded |
| `AbstractQueryTestCase` | Catches and handles the expected exception in test framework |

#### SecureReactorNetty4HttpServerTransportTests Fix

Multiple tests in `SecureReactorNetty4HttpServerTransportTests` were failing with specific random seeds due to locale-dependent certificate generation.

**Root Cause**: The `JcaX509v1CertificateBuilder` class used locale-dependent date formatting, causing certificate generation to fail with certain locale/timezone combinations.

**Solution**: Replaced `JcaX509v1CertificateBuilder` with `X509v1CertificateBuilder` and explicitly specified `Locale.ROOT` for consistent behavior across all test environments.

| Component | Change |
|-----------|--------|
| `KeyStoreUtils` | Use `X509v1CertificateBuilder` with explicit `Locale.ROOT` |
| Certificate generation | Use `SubjectPublicKeyInfo.getInstance()` for public key encoding |

### Usage Example

The fixes are internal to the test framework and require no user action. Tests now handle edge cases gracefully:

```java
// IntervalBuilder now checks disjunction count before combining
if (maxGaps == 0 && mode == IntervalMode.ORDERED 
    && IntervalBuilder.canCombineSources(ss) == false) {
    throw new IllegalArgumentException("Too many disjunctions to expand");
}
```

### Migration Notes

No migration required. These are internal test framework improvements.

## Limitations

- The disjunction limit check only applies to `maxGaps=0` with `ORDERED` mode
- Other interval query combinations may still hit Lucene limits in edge cases

## References

### Documentation
- [Lucene Disjunctions](https://github.com/apache/lucene/blob/main/lucene/queries/src/java/org/apache/lucene/queries/intervals/Disjunctions.java): Lucene disjunction limit implementation

### Pull Requests
| PR | Description |
|----|-------------|
| [#19332](https://github.com/opensearch-project/OpenSearch/pull/19332) | Fix Flaky IntervalQueryBuilderTests |
| [#19327](https://github.com/opensearch-project/OpenSearch/pull/19327) | Fix flaky test in SecureReactorNetty4HttpServerTransportTests |

### Issues (Design / RFC)
- [Issue #19167](https://github.com/opensearch-project/OpenSearch/issues/19167): IntervalQueryBuilderTests flaky test report
- [Issue #17486](https://github.com/opensearch-project/OpenSearch/issues/17486): SecureReactorNetty4HttpServerTransportTests flaky test report

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/flaky-test-fixes.md)
