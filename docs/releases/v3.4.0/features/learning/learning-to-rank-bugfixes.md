# Learning to Rank Bugfixes

## Summary

This release includes four bug fixes for the Learning to Rank (LTR) plugin addressing version serialization compatibility, integration test stability, and feature logging functionality. The fixes ensure proper operation with OpenSearch 3.4.0 and resolve issues with rescore-only SLTR logging.

## Details

### What's New in v3.4.0

Four bug fixes improve plugin stability and compatibility:

1. **Legacy Version ID Computation** - Updated to use `Version.computeID` instead of deprecated `computeLegacyID` for binary serialization compatibility
2. **ML Index Warning Fix** - Fixed YAML test parsing to properly specify index parameter for refresh operations
3. **Implicit Refresh for Tests** - Replaced explicit index refresh with `wait_for` to avoid system index warnings
4. **Rescore-Only Feature Logging** - Fixed SLTR logging when queries exist only in the rescore phase

### Technical Changes

#### Legacy Version Serialization Fix (PR #264)

OpenSearch removed support for ES-style legacy version IDs in binary streams. The plugin now uses `Version.computeID` for version computation:

```java
// Before
return Version.fromId(Version.computeLegacyID(major, minor, revision, build));

// After
return Version.fromId(Version.computeID(major, minor, revision, build));
```

The version checks for feature normalizers serialization were also simplified by removing legacy version conditionals.

#### Integration Test Stability (PR #269, #271)

Tests were triggering warnings about accessing internal indexes like `.plugins-ml-config` when refreshing all indexes. Two fixes were applied:

1. **PR #269**: Fixed YAML test parsing where `indices.refresh: { test }` was incorrectly parsed as `null` argument instead of `index: test` parameter
2. **PR #271**: Replaced explicit refresh with implicit `wait_for` on document indexing to avoid touching system indexes

```yaml
# Before
- do:
    indices.refresh: { test }

# After
- do:
    index:
      index: test
      id: 1
      body: { ... }
      refresh: wait_for
```

#### Rescore-Only Feature Logging Fix (PR #266)

Feature logging failed when SLTR queries existed only in the rescore phase with no named queries in the main query. The `_ltrlog` field was missing from search results.

**Root Cause**: Rescore logging was inside a `if (namedQueries.size() > 0)` block, skipping it when no named queries existed.

**Solution**: Process rescore logging independently when no named query log specs are requested:

```java
if (namedQueries.size() > 0) {
    // Process both named query and rescore logging
} else if (!hasNamedQueryLogSpecs) {
    // Rescore-only: process rescore logging
}
// else: inner hits context - skip logging
```

The fix also handles an edge case where inner hits processing creates a separate fetch context with empty `namedQueries` but available `rescoreContexts`.

### Usage Example

Rescore-only logging now works correctly:

```json
GET test_index/_search
{
  "query": { "match": { "title": "OpenSearch" } },
  "rescore": {
    "query": {
      "rescore_query": {
        "sltr": { "featureset": "my_features", "params": { "query": "OpenSearch" } }
      }
    }
  },
  "ext": {
    "ltr_log": {
      "log_specs": { "name": "rescore_log", "rescore_index": 0 }
    }
  }
}
```

**Before fix**: No `_ltrlog` field in response
**After fix**: `_ltrlog` present with feature values

## Limitations

- The `wait_for` refresh approach may not work in serverless configurations, but this only affects tests, not production usage

## Related PRs

| PR | Description |
|----|-------------|
| [#264](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/264) | Use OpenSearch Version.computeID for legacy version IDs |
| [#269](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/269) | Fix ML index warning in YAML test parsing |
| [#271](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/271) | Use implicit wait_for instead of explicit refresh |
| [#266](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/266) | Fix rescore-only feature SLTR logging |

## References

- [Issue #265](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/265): Integration test failures for v3.4.0
- [OpenSearch PR #19793](https://github.com/opensearch-project/OpenSearch/pull/19793): Legacy version ID removal in OpenSearch core
- [Learning to Rank Documentation](https://docs.opensearch.org/3.0/search-plugins/ltr/index/)

## Related Feature Report

- [Full feature documentation](../../../../features/learning/learning-to-rank.md)
