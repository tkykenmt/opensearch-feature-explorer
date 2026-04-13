---
tags:
  - opensearch
---
# ProfileScorer Improvements

## Summary

OpenSearch 3.6.0 introduces the `ProfilingWrapper<T>` public interface and refactors all profiling decorators (`ProfileScorer`, `ProfileCollector`, `ProfilingAggregator`, `ProfilingLeafBucketCollector`) to implement it. This gives plugins a clean, reflection-free way to detect and unwrap profiling wrappers via `instanceof ProfilingWrapper` and `getDelegate()`, solving a long-standing accessibility problem where package-private profiling classes blocked external plugin access even through public methods.

## Details

### What's New in v3.6.0

**Problem**: When search profiling is enabled, OpenSearch wraps scorers, collectors, and aggregators in package-private profiling decorators. Plugin queries (e.g., neural-search's `HybridQuery`) that extend the standard Lucene `Scorer` API with custom methods could not access those methods through the profiling wrapper. The initial `getWrappedScorer()` method added in PR #20549 was insufficient because `ProfileScorer` is a package-private `final class` — Java's access control blocks `Method.invoke()` from external modules on methods of non-public classes, forcing plugins to use `method.setAccessible(true)` with `@SuppressForbidden`.

**Solution**: A two-PR approach:

1. **PR #20549** — Added `getWrappedScorer()` method to `ProfileScorer`, providing direct access to the wrapped scorer. This followed the existing pattern of `ProfileCollector.getDelegate()` and `ProfilingAggregator.unwrapAggregator()`.

2. **PR #20607** — Introduced the `ProfilingWrapper<T>` generic interface (annotated `@PublicApi(since = "3.6.0")`) and refactored all profiling wrappers to implement it. This replaced the class-specific unwrap methods with a unified `getDelegate()` contract that plugins can use via `instanceof` checks without needing to reference package-private classes.

### Technical Changes

**New interface**: `org.opensearch.search.profile.ProfilingWrapper<T>`
```java
@PublicApi(since = "3.6.0")
public interface ProfilingWrapper<T> {
    T getDelegate();
}
```

**Classes updated to implement `ProfilingWrapper`**:

| Class | Type Parameter | Package |
|-------|---------------|---------|
| `ProfileScorer` | `Scorer` | `o.o.search.profile.query` |
| `ProfileCollector` | `Collector` | `o.o.search.profile.query` |
| `ProfilingAggregator` | `Aggregator` | `o.o.search.profile.aggregation` |
| `ProfilingLeafBucketCollector` | `LeafBucketCollector` | `o.o.search.profile.aggregation` |

**Plugin usage pattern**:
```java
if (scorer instanceof ProfilingWrapper) {
    Scorer delegate = ((ProfilingWrapper<Scorer>) scorer).getDelegate();
    // access custom scorer methods on the delegate
}
```

This eliminates the need for reflection, `setAccessible(true)`, or `@SuppressForbidden` annotations in plugin code.

## Limitations

- Calling mutation methods (e.g., `setMinCompetitiveScore()`) directly on the unwrapped delegate bypasses profiling instrumentation for those calls. Functional correctness is preserved, but timing metrics will be incomplete.
- The `getWrappedScorer()` method from PR #20549 was renamed to `getDelegate()` in PR #20607 for consistency with the new interface.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| https://github.com/opensearch-project/OpenSearch/pull/20549 | Add `getWrappedScorer()` method to `ProfileScorer` | https://github.com/opensearch-project/OpenSearch/issues/20548 |
| https://github.com/opensearch-project/OpenSearch/pull/20607 | Introduce `ProfilingWrapper<T>` interface, refactor all profiling decorators | https://github.com/opensearch-project/OpenSearch/issues/20548 |
