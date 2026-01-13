---
tags:
  - domain/search
  - component/server
  - indexing
  - k-nn
  - search
---
# k-NN Documentation

## Summary

This release includes a JavaDoc cleanup fix for the k-NN plugin that removes redundant documentation comments from the `RescoreContext` class. The fix addresses a documentation issue that affected JavaDoc generation on Linux machines.

## Details

### What's New in v2.18.0

The `userProvided` field in `RescoreContext.java` had excessive inline documentation that was redundant with the existing brief comment. This PR removes 24 lines of verbose documentation while preserving the essential explanation.

### Technical Changes

#### Code Cleanup

The `RescoreContext` class is used for k-NN query rescoring operations. The `userProvided` flag tracks whether the oversample factor was explicitly set by the user or uses a default value.

**Before (verbose):**
```java
/**
 * Flag to track whether the oversample factor is user-provided or default. The Reason to introduce
 * this is to set default when Shard Level rescoring is false,
 * else we end up overriding user provided value in NativeEngineKnnVectorQuery
 *
 * This flag is crucial to differentiate between user-defined oversample factors...
 * [24 additional lines of documentation]
 */
@Builder.Default
private boolean userProvided = true;
```

**After (concise):**
```java
/**
 * Flag to track whether the oversample factor is user-provided or default. The Reason to introduce
 * this is to set default when Shard Level rescoring is false,
 * else we end up overriding user provided value in NativeEngineKnnVectorQuery
 */
@Builder.Default
private boolean userProvided = true;
```

### Impact

- Cleaner JavaDoc generation on Linux machines
- Reduced code verbosity without losing essential information
- No functional changes to the k-NN plugin behavior

## Limitations

None. This is a documentation-only change with no impact on functionality.

## References

### Documentation
- [PR #2190](https://github.com/opensearch-project/k-NN/pull/2190): Java Docs Fix for 2.x in Linux Machine

### Pull Requests
| PR | Description |
|----|-------------|
| [#2190](https://github.com/opensearch-project/k-NN/pull/2190) | Java Docs Fix For 2.x |

## Related Feature Report

- [k-NN Query Rescore](../../../features/k-nn/k-nn-query-rescore.md)
