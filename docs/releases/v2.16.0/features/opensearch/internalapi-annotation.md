---
tags:
  - opensearch
---
# @InternalApi Annotation

## Summary

OpenSearch v2.16.0 enhances the `@InternalApi` annotation to allow marking classes that should not be constructed outside of OpenSearch core, even when they are referenced by public APIs. This change also adds `@InternalApi` to japicmp exclusions, preventing false-positive breaking change reports for internal classes.

## Details

### What's New in v2.16.0

#### Relaxed Constructor Semantics

The `ApiAnnotationProcessor` now allows `@InternalApi` annotation on constructors of `@PublicApi` classes. This enables marking classes as internal when:

- The class is referenced by public APIs (e.g., as a method parameter or return type)
- The class instances should only be created within OpenSearch core
- External consumers should use the class but not instantiate it

Example use case: `IndexShard` has a verbose constructor but instances should not be created outside of core.

```java
@PublicApi(since = "1.0.0")
public class PublicApiConstructorAnnotatedInternalApi {
    @InternalApi
    public PublicApiConstructorAnnotatedInternalApi(NotAnnotated arg) {}
}
```

#### japicmp Exclusions

The `@InternalApi` annotation is now added to japicmp exclusions in the build configuration:

```groovy
tasks.register("japicmp", me.champeau.gradle.japicmp.JapicmpTask) {
    annotationIncludes = ['@org.opensearch.common.annotation.PublicApi', '@org.opensearch.common.annotation.DeprecatedApi']
    annotationExcludes = ['@org.opensearch.common.annotation.InternalApi']
}
```

This prevents the "detect breaking changes" workflow from flagging changes to `@InternalApi` annotated classes as breaking changes.

### Technical Changes

| Component | Change |
|-----------|--------|
| `ApiAnnotationProcessor` | Constructor arguments now have relaxed semantics - can be not annotated or annotated as `@InternalApi` |
| `server/build.gradle` | Added `annotationExcludes` for `@InternalApi` in japicmp task |

### Problem Solved

Previously, classes like `RemoteStorePathStrategy` that were internal but referenced by public APIs had to be marked as `@PublicApi`, causing:

1. False-positive breaking change reports when modifying these classes
2. Incorrect API surface exposure to external consumers

## Limitations

- The `@InternalApi` annotation only affects compile-time checks and build tooling
- Runtime behavior is not enforced - external code can still instantiate these classes
- Developers must rely on documentation and annotation to understand usage restrictions

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14575](https://github.com/opensearch-project/OpenSearch/pull/14575) | Allow @InternalApi annotation on classes not meant to be constructed outside of the OpenSearch core | [#13308](https://github.com/opensearch-project/OpenSearch/issues/13308) |
| [#14597](https://github.com/opensearch-project/OpenSearch/pull/14597) | Add @InternalApi annotation to japicmp exclusions | [#13308](https://github.com/opensearch-project/OpenSearch/issues/13308) |

### Related Issues

- [#13308](https://github.com/opensearch-project/OpenSearch/issues/13308) - Feature Request: Allow annotation of InternalApi on classes not meant to be consumed outside of OpenSearch
- [#13275](https://github.com/opensearch-project/OpenSearch/issues/13275) - Original discussion about RemoteStorePathStrategy annotation issues
