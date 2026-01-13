---
tags:
  - domain/infra
  - component/server
  - dashboards
  - observability
  - sql
---
# CI/Infrastructure Fixes

## Summary

This release item addresses multiple CI/CD infrastructure issues across OpenSearch plugin repositories. The fixes ensure CI workflows continue to function correctly by addressing deprecated GitHub Actions, GLIBC compatibility issues, and missing plugin dependencies.

## Details

### What's New in v2.17.0

Multiple CI workflow fixes were implemented across different plugin repositories to maintain build stability and test reliability.

### Technical Changes

#### GitHub Actions Updates

| Repository | Change | Reason |
|------------|--------|--------|
| dashboards-observability | `actions/upload-artifact` v1 → v4 | v1/v2 deprecated by GitHub |
| common-utils | Added `ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION` | GLIBC compatibility in Linux containers |

#### CI Workflow Improvements

| Repository | Change | Impact |
|------------|--------|--------|
| dashboards-observability | Added Job Scheduler plugin dependency | SQL plugin dependency chain |
| dashboards-observability | Removed datasources tests | Test suite cleanup |
| dashboards-observability | Updated link checker exclusions | Exclude localhost links |

### Changes by Repository

#### common-utils

Fixed CI build failures in Linux environments caused by Node.js version incompatibility with older GLIBC versions in Docker containers.

```yaml
env:
  ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION: true
```

**Issue**: Build failures with error:
```
/__e/node20/bin/node: /lib64/libm.so.6: version `GLIBC_2.27' not found
/__e/node20/bin/node: /lib64/libc.so.6: version `GLIBC_2.28' not found
```

#### dashboards-observability

1. **Upload Artifact Update**: Updated `actions/upload-artifact` from v1 to v4 across multiple workflow files:
   - `dashboards-observability-test-and-build-workflow.yml`
   - `ftr-e2e-dashboards-observability-test.yml`
   - `integration-tests-workflow.yml`

2. **Job Scheduler Dependency**: Added Job Scheduler plugin installation to CI workflows due to SQL plugin adding it as a dependency.

3. **Link Checker Fix**: Updated link checker to exclude localhost URLs:
   ```yaml
   args: --accept=200,403,429 "./**/*.html" "./**/*.md" "./**/*.txt" --exclude "http://localhost" --exclude "https://localhost"
   ```

4. **Test Suite Cleanup**: Removed `datasources_test` from integration test matrix.

## Limitations

- These are infrastructure-only changes with no user-facing impact
- The `ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION` flag is a temporary workaround

## References

### Blog Posts
- [GitHub Actions upload-artifact deprecation notice](https://github.blog/changelog/2024-02-13-deprecation-notice-v1-and-v2-of-the-artifact-actions/)

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#703](https://github.com/opensearch-project/common-utils/pull/703) | common-utils | Fixed CI build failures due to GLIBC version issues |
| [#2046](https://github.com/opensearch-project/dashboards-observability/pull/2046) | dashboards-observability | Fixed CI workflow checks, added Job Scheduler dependency |
| [#2133](https://github.com/opensearch-project/dashboards-observability/pull/2133) | dashboards-observability | Updated actions/upload-artifact from v1 to v4 |

### Issues (Design / RFC)
- [Issue #1886](https://github.com/opensearch-project/dashboards-observability/issues/1886): Observability CI failures

## Related Feature Report

- Full feature documentation
