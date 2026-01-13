---
tags:
  - skills
---
# Skills CI Fixes

## Summary

This release fixes GitHub Actions CI build failures on Linux and a missing return statement bug in RAGTool that could cause unexpected behavior when content generation is disabled.

## Details

### GitHub Actions CI Fix

The Linux CI builds were failing due to GLIBC version incompatibilities with Node.js 20:

```
/__e/node20/bin/node: /lib64/libm.so.6: version `GLIBC_2.27' not found
/__e/node20/bin/node: /lib64/libstdc++.so.6: version `GLIBCXX_3.4.20' not found
/__e/node20/bin/node: /lib64/libc.so.6: version `GLIBC_2.28' not found
```

The fix updates the CI workflow to use the shared `get-ci-image-tag.yml` workflow from `opensearch-build` repository instead of manually fetching the CI image tag. This ensures consistent CI image usage across OpenSearch projects.

**Key Changes:**
- Replaced manual CI image tag fetching with reusable workflow from `opensearch-project/opensearch-build`
- Updated GitHub Actions versions: `actions/checkout@v3` → `v4`, `actions/setup-java@v3` → `v4`
- Updated `codecov/codecov-action@v1` → `v4`
- Added proper container start commands using workflow outputs

### RAGTool Missing Return Fix

Fixed a bug in `RAGTool.java` where a missing `return` statement after calling `listener.onResponse(r)` when `enableContentGeneration` is `false` could cause the method to continue execution unexpectedly.

```java
// Before (buggy)
if (!this.enableContentGeneration) {
    listener.onResponse(r);
    // Missing return - execution continues
}

// After (fixed)
if (!this.enableContentGeneration) {
    listener.onResponse(r);
    return;  // Properly exits the method
}
```

### Test Improvements

Enhanced test infrastructure with better error handling and logging:
- Added try-catch in `parseResponseToMap()` to handle JSON parsing failures gracefully
- Added logging for agent execution responses to aid debugging

## Limitations

None.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#477](https://github.com/opensearch-project/skills/pull/477) | Fix github ci linux build and RAG tool missing return | [#445](https://github.com/opensearch-project/skills/issues/445) |

### Related Issues
| Issue | Description |
|-------|-------------|
| [#445](https://github.com/opensearch-project/skills/issues/445) | Flaky test in RAGToolIT |
