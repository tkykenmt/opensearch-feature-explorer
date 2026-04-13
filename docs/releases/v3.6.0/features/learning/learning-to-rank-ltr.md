---
tags:
  - learning
---
# Learning to Rank (LTR)

## Summary

Bug fixes for the Learning to Rank plugin in v3.6.0: a critical fix for `JsonGenerationException` when LTR feature logging is used with search pipelines, and a Windows CI build fix for Spotless P2 mirror dependency.

## Details

### What's New in v3.6.0

#### Fix LoggingSearchExtBuilder.toXContent Missing Field Name

`LoggingSearchExtBuilder.toXContent()` called `builder.startObject()` without providing the `"ltr_log"` field name. The `SearchExtBuilder` contract requires each ext builder to write its own field name when serializing, because `SearchSourceBuilder.innerToXContent()` iterates ext builders inside the `"ext"` object without writing field names for them.

The bug was latent — `toXContent()` is never called during normal search execution since ext builders are parsed and used in memory without re-serialization. It only surfaces when something triggers `SearchSourceBuilder.toString()`, which happens in `TrackingSearchRequestProcessorWrapper.processRequestAsync()` — used by search pipelines when `verbose_pipeline=true` or when processors like `ml_inference` modify and re-serialize the request.

The fix changes one line:

```diff
- builder.startObject();
+ builder.startObject(NAME);
```

This writes `"ltr_log": {` instead of just `{`, producing valid JSON when serialized inside the `"ext"` object.

**Impact**: Users combining LTR feature logging (`ext.ltr_log`) with any search pipeline that triggers `SearchSourceBuilder` re-serialization (e.g., `ml_inference` request processor, `verbose_pipeline=true`) would get a 500 error with `JsonGenerationException: Can not start an object, expecting field name`.

**Affected file**: `src/main/java/com/o19s/es/ltr/logging/LoggingSearchExtBuilder.java`

#### Fix Windows CI Build Failure

Removes `withP2Mirrors()` from Spotless Eclipse formatter configuration so it resolves from Maven Central instead of P2 mirror sites (`download.eclipse.org`, `mirror.umd.edu`). These mirrors were unreachable from Windows Docker containers in Jenkins CI.

**Affected file**: `build.gradle`

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#290](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/290) | Fix LoggingSearchExtBuilder.toXContent missing field name | [ml-commons#4607](https://github.com/opensearch-project/ml-commons/issues/4607) |
| [#305](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/305) | Fix Windows CI build failure caused by Spotless P2 mirror timeout | Backport of [#303](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/303) |
