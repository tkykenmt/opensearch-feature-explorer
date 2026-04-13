---
tags:
  - opensearch
---
# Search Performance Fixes

## Summary

OpenSearch v3.6.0 includes three search performance bug fixes: delegating `getMin`/`getMax` in `ExitableTerms` to avoid a slow path during field sort, lazily initializing the stored field reader in `SourceLookup` to eliminate unnecessary `madvise` system calls, and correcting the heap usage cancellation message in `HeapUsageTracker` to display the meaningful heap percent threshold.

## Key Changes

### ExitableTerms getMin/getMax Delegation

`ExitableTerms` (the cancellation-aware wrapper around Lucene `Terms`) did not override `getMin()` and `getMax()`, causing `FieldSortBuilder` to fall through to the default `Terms` implementation. The default implementation iterates through all terms to find min/max — a slow path clearly visible in flame graphs during field sort operations.

The fix adds two delegate methods to `ExitableTerms`:

```java
@Override
public BytesRef getMin() throws IOException {
    return in.getMin();
}

@Override
public BytesRef getMax() throws IOException {
    return in.getMax();
}
```

This delegates directly to the underlying `Terms` implementation, which typically reads min/max from segment metadata in O(1) time.

Changed file: `server/src/main/java/org/opensearch/search/internal/ExitableDirectoryReader.java`

### Lazy Stored Field Reader in SourceLookup

`SourceLookup.setSegmentAndDocument()` eagerly called `getMergeInstance()` on every segment transition, which triggered `madvise(SEQUENTIAL)` system calls that acquire a write lock. Scripts that never read `_source` paid this cost unnecessarily.

The fix defers `getMergeInstance()` from `setSegmentAndDocument()` to `loadSourceIfNeeded()`, so the stored field reader is only initialized when `_source` is actually accessed:

```java
// Before: eager — triggers madvise on every segment transition
if (this.reader != context.reader()) {
    fieldReader = lf.getSequentialStoredFieldsReader()::document;
}

// After: lazy — only triggers when _source is actually read
if (this.reader != context.reader()) {
    this.reader = context.reader();
    this.fieldReader = null;  // deferred to loadSourceIfNeeded()
}
```

Changed file: `server/src/main/java/org/opensearch/search/lookup/SourceLookup.java`

### HeapUsageTracker Cancellation Message Fix

The `HeapUsageTracker` in Search Backpressure displayed the moving-average-based `allowedUsage` value in cancellation messages. When historical tasks were lightweight, this value could be extremely small (hundreds of KB), producing nonsensical log messages like `heap usage exceeded [3.4gb >= 800.5kb]`.

The fix changes the message to display the heap percent threshold instead:

- Before: `heap usage exceeded [3.4gb >= 800.5kb]`
- After: `heap usage exceeded [3.4gb >= 150mb]`

Changed file: `server/src/main/java/org/opensearch/search/backpressure/trackers/HeapUsageTracker.java`

## Related Issues

- `https://github.com/opensearch-project/OpenSearch/issues/20933` — SourceLookup madvise performance issue
- `https://github.com/opensearch-project/OpenSearch/issues/17947` — Misleading heap usage cancellation message

## References

- `https://github.com/opensearch-project/OpenSearch/pull/20775` — Delegate getMin/getMax methods for ExitableTerms
- `https://github.com/opensearch-project/OpenSearch/pull/20827` — Lazy init stored field reader in SourceLookup
- `https://github.com/opensearch-project/OpenSearch/pull/20779` — Show heap percent threshold in cancellation message
