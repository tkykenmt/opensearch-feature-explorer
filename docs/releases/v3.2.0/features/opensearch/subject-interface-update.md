---
tags:
  - search
---

# Subject Interface Update

## Summary

This release item updates the `Subject` interface's `runAs` method to use `CheckedRunnable` instead of `Callable`. This is a code cleanup that improves the API by removing an unused return value and providing more specific exception handling.

## Details

### What's New in v3.2.0

The `Subject.runAs()` method signature has been changed from:

```java
<T> T runAs(Callable<T> callable) throws Exception
```

to:

```java
<E extends Exception> void runAs(CheckedRunnable<E> r) throws E
```

### Technical Changes

#### API Changes

| Before | After |
|--------|-------|
| `Callable<T>` parameter | `CheckedRunnable<E>` parameter |
| Returns `T` | Returns `void` |
| Throws generic `Exception` | Throws specific exception type `E` |

#### Rationale

1. **Unused return value**: The return value from `Callable.call()` was never used in practice
2. **Better exception handling**: `CheckedRunnable<E>` allows callers to specify the exact exception type, avoiding generic `Exception` propagation
3. **Cleaner API**: The `void` return type better reflects the actual usage pattern

#### Updated Components

| Component | Description |
|-----------|-------------|
| `Subject` interface | Core identity interface with updated `runAs` method |
| `NoopPluginSubject` | Noop implementation updated to use `CheckedRunnable` |
| `ShiroPluginSubject` | Shiro implementation updated to use `CheckedRunnable` |
| `CheckedRunnable` | Promoted to `@PublicApi(since = "3.2.0")` |

### Usage Example

Before (v3.1.0 and earlier):
```java
subject.runAs(() -> {
    // perform action
    return null;  // unused return value
});
```

After (v3.2.0):
```java
subject.runAs(() -> {
    // perform action
});
```

### Migration Notes

If you have custom `Subject` implementations or use `Subject.runAs()`:

1. Update `runAs` method signature to accept `CheckedRunnable<E>` instead of `Callable<T>`
2. Change return type from `T` to `void`
3. Remove any `return` statements from lambda expressions passed to `runAs`

## Limitations

- This is a breaking API change for custom `Subject` implementations
- Existing code using the return value (though unlikely) will need modification

## References

### Documentation
- [PR #18570](https://github.com/opensearch-project/OpenSearch/pull/18570): Main implementation
- [PR #14630](https://github.com/opensearch-project/OpenSearch/pull/14630): Related - Add runAs to Subject interface and introduce IdentityAwarePlugin extension point

### Pull Requests
| PR | Description |
|----|-------------|
| [#18570](https://github.com/opensearch-project/OpenSearch/pull/18570) | Update Subject interface to use CheckedRunnable |
| [#14630](https://github.com/opensearch-project/OpenSearch/pull/14630) | Original PR that introduced `runAs` to Subject interface |

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/subject-interface.md)
