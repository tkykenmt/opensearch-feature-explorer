# Learning to Rank Enhancements

## Summary

This release includes test infrastructure improvements for the Learning to Rank (LTR) plugin that eliminate system index access warnings during integration tests. The changes improve test isolation and enable parallel test execution by narrowing the scope of index cleanup operations.

## Details

### What's New in v3.4.0

Two enhancements improve test infrastructure:

1. **System Index Warning Allowances** (PR #256) - Temporary fix to allow warnings about `.plugins-ml-config` index access during tests
2. **Test Isolation Improvements** (PR #259) - Root cause fix that narrows index cleanup scope to LTR-specific indexes only

### Technical Changes

#### System Index Warning Allowances (PR #256)

Integration tests were failing due to unexpected warnings about accessing system indexes like `.plugins-ml-config`. This PR added temporary `allowed_warnings` sections to REST API spec tests:

```yaml
- do:
    allowed_warnings:
      - "this request accesses system indices: [.plugins-ml-config], but in a future major version, direct access to system indices will be prevented by default"
    ltr.create_store: {}
```

This was a stopgap measure while the root cause was investigated.

#### Test Isolation Improvements (PR #259)

The root cause of system index warnings was identified and fixed:

**Problem 1**: `LtrQueryClientYamlTestSuiteIT` was wiping ALL indexes after tests, including system indexes created by other plugins:

```java
// Before: Deleted all non-security indexes
for (Map<String, Object> index : parserList) {
    String indexName = (String) index.get("index");
    if (indexName != null && !".opendistro_security".equals(indexName)) {
        adminClient().performRequest(new Request("DELETE", "/" + indexName));
    }
}
```

**Solution**: Narrow cleanup to only LTR-specific indexes:

```java
// After: Delete only LTR indexes
@After
protected void wipeLtrIndices() throws IOException {
    Request delete = new Request("DELETE", "/.ltrstore*");
    delete.addParameter("ignore_unavailable", "true");
    delete.addParameter("allow_no_indices", "true");
    delete.addParameter("expand_wildcards", "all");
    adminClient().performRequest(delete);
}
```

**Problem 2**: YAML tests created `test_index` without cleanup, forcing the broad index deletion.

**Solution**: Added `teardown` sections to clean up test indexes and made index creation lenient:

```yaml
teardown:
    - do:
          indices.delete:
              index: test_index
              ignore_unavailable: true
              expand_wildcards: all

---
"Test case":
  - do:
      indices.create:
        index: test
        ignore: [400]  # Allow already exists
```

**Problem 3**: Deprecated security settings constants were used.

**Solution**: Updated to use string literals for security settings:

```java
// Before
.put(OPENSEARCH_SECURITY_SSL_HTTP_KEYSTORE_PASSWORD, "changeit")
.put(OPENSEARCH_SECURITY_SSL_HTTP_KEYSTORE_KEYPASSWORD, "changeit")

// After
.put("plugins.security.ssl.http.keystore_password", "changeit")
.put("plugins.security.ssl.http.keystore_keypassword", "changeit")
```

### Benefits

| Improvement | Description |
|-------------|-------------|
| Test Isolation | Tests no longer interfere with other plugins' system indexes |
| Parallel Execution | Enables running LTR tests alongside other integration tests |
| Cleaner Output | Removes `allowed_warnings` noise from test specifications |
| Maintainability | Proper teardown sections make test intent clearer |

### Files Changed

| File | Changes |
|------|---------|
| `LtrQueryClientYamlTestSuiteIT.java` | Narrowed index cleanup, updated security settings |
| `10_manage.yml` | Added teardown, removed allowed_warnings |
| `20_features.yml` | Removed allowed_warnings |
| `30_featuresets.yml` | Removed allowed_warnings |
| `40_models.yml` | Removed allowed_warnings |
| `50_add_features_to_set.yml` | Removed allowed_warnings |
| `60_create_model_from_set.yml` | Removed allowed_warnings |
| `70_validation.yml` | Added teardown, removed allowed_warnings |
| `80_search_w_partial_models.yml` | Added teardown, removed allowed_warnings |

## Limitations

- The `ignore: [400]` parameter for index creation may mask legitimate errors in some edge cases

## References

### Documentation
- [Learning to Rank Documentation](https://docs.opensearch.org/3.0/search-plugins/ltr/index/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#256](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/256) | Allow warnings about directly accessing the .plugins-ml-config index |
| [#259](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/259) | Feature/ltr system origin avoid warnings |

### Issues (Design / RFC)
- [Issue #245](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/245): Integration test failures for v2.19.4
- [Issue #249](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues/249): Integration test failures for v3.3.2

## Related Feature Report

- [Full feature documentation](../../../../features/learning/learning-to-rank.md)
