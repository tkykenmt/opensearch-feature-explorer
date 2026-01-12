---
tags:
  - search
---

# Lucene Integration

## Summary

This release removes the custom `MultiCollectorWrapper` class from OpenSearch and replaces it with the native `MultiCollector.getCollectors()` method from Apache Lucene. This change reduces code duplication and improves maintainability by leveraging Lucene's public API that was made available in Lucene 9.1.

## Details

### What's New in v3.4.0

OpenSearch previously maintained a custom `MultiCollectorWrapper` class to access individual collectors wrapped by Lucene's `MultiCollector`. This was necessary because `MultiCollector.getCollectors()` was package-private in earlier Lucene versions.

With Lucene 9.1+, the `getCollectors()` method became public (via [LUCENE-10244](https://github.com/apache/lucene/pull/455)), allowing OpenSearch to remove its wrapper class and use Lucene's native implementation directly.

### Technical Changes

#### Removed Components

| Component | Description |
|-----------|-------------|
| `MultiCollectorWrapper` | Custom wrapper class that provided access to underlying collectors |

#### Code Changes

The `TopDocsCollectorContext` class was updated to:

1. Replace `MultiCollectorWrapper.wrap()` calls with `MultiCollector.wrap()`
2. Replace `instanceof MultiCollectorWrapper` checks with `instanceof MultiCollector`
3. Use `MultiCollector.getCollectors()` directly instead of the wrapper's method
4. Adopt Java pattern matching for `instanceof` (e.g., `instanceof MultiCollector m`)

```java
// Before (v3.3.x and earlier)
return MultiCollectorWrapper.wrap(manager.newCollector(), maxScoreCollector);
// ...
if (collector instanceof MultiCollectorWrapper) {
    subs.addAll(((MultiCollectorWrapper) collector).getCollectors());
}

// After (v3.4.0)
return MultiCollector.wrap(manager.newCollector(), maxScoreCollector);
// ...
if (collector instanceof MultiCollector m) {
    subs.addAll(List.of(m.getCollectors()));
}
```

### Usage Example

The change is internal and does not affect user-facing APIs. The `CollectorManager` pattern continues to work as before:

```java
// CollectorManager implementation using MultiCollector
class CustomCollectorManager implements CollectorManager<Collector, Result> {
    @Override
    public Collector newCollector() throws IOException {
        return MultiCollector.wrap(new TopDocsCollector(), new MaxScoreCollector());
    }
    
    @Override
    public Result reduce(Collection<Collector> collectors) throws IOException {
        for (Collector collector : collectors) {
            if (collector instanceof MultiCollector m) {
                // Access individual collectors via Lucene's public API
                for (Collector sub : m.getCollectors()) {
                    // Process each sub-collector
                }
            }
        }
        return result;
    }
}
```

### Migration Notes

This is an internal refactoring with no user-facing changes. No migration is required.

## Limitations

None. This is a code cleanup change that improves maintainability.

## References

### Documentation
- [Lucene PR #455](https://github.com/apache/lucene/pull/455): Lucene PR that made `MultiCollector.getCollectors()` public

### Pull Requests
| PR | Description |
|----|-------------|
| [#19595](https://github.com/opensearch-project/OpenSearch/pull/19595) | Remove MultiCollectorWrapper and use MultiCollector in Lucene instead |

### Issues (Design / RFC)
- [LUCENE-10244](https://github.com/apache/lucene/issues/11280): Original Lucene issue requesting public `getCollectors()` method

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/lucene-integration.md)
