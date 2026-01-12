---
tags:
  - dashboards
  - performance
---

# CI/CD & Build Fixes

## Summary

OpenSearch Dashboards v3.0.0 includes several CI/CD and build system fixes that improve workflow reliability, address GitHub Actions deprecation warnings, and resolve Windows build issues. These changes ensure stable continuous integration pipelines and cross-platform build compatibility.

## Details

### What's New in v3.0.0

This release addresses four key areas:

1. **GitHub Actions Cache Update**: Updated `actions/cache` from deprecated v1 to v4
2. **Workflow Permissions**: Added proper write permissions for PR comments in performance testing
3. **Windows Build Stability**: Implemented retry logic with long path support for file deletion

### Technical Changes

#### GitHub Actions Updates

The Cypress workflow was updated to use `actions/cache@v4` instead of the deprecated v1:

```yaml
- name: Cache Cypress
  id: cache-cypress
  uses: actions/cache@v4
  with:
    path: ~/.cache/Cypress
    key: cypress-cache-v2-${{ runner.os }}-${{ hashFiles('**/package.json') }}
```

#### Workflow Permissions

The performance testing workflow now includes explicit permissions for PR interactions:

```yaml
permissions:
  contents: read
  issues: write
  pull-requests: write
```

#### Windows Long Path Support

The build system now handles Windows long paths and includes retry logic for file deletion:

```typescript
// src/dev/build/lib/fs.ts
if (process.platform === 'win32') {
  folder = standardize(folder, false, false, true); // extended long path
}

for (let i = 0; i < 3; i++) {
  try {
    await rm(folder, { force: true, recursive: true });
    return;
  } catch (err) {
    if (i === 2) throw err;
    log.debug(`Retry ${i + 1}/3 on ${folder}, waiting for 1000ms`);
    await new Promise((resolveSleep) => setTimeout(resolveSleep, 1000));
  }
}
```

### Files Changed

| File | Change |
|------|--------|
| `.github/workflows/cypress_workflow.yml` | Updated actions/cache v1 → v4 |
| `.github/workflows/performance_testing.yml` | Added PR write permissions |
| `src/dev/build/lib/fs.ts` | Added retry logic and Windows long path support |

## Limitations

- Retry logic adds up to 3 seconds delay per failed deletion attempt
- Windows long path support requires the `@osd/cross-platform` package

## References

### Pull Requests
| PR | Description |
|----|-------------|
| [#9366](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9366) | Update actions/cache from v1 to v4 |
| [#9534](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9534) | Add PR write permission for performance testing |
| [#9581](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9581) | Fix permissions for bundler performance testing CI |
| [#9561](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9561) | Retry on file/folder deletion with Windows longpath support |

### Issues (Design / RFC)
- [Issue #9397](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/9397): Windows build failure discussion
- [Issue #3747](https://github.com/opensearch-project/opensearch-build/issues/3747): opensearch-build Windows issue

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch-dashboards/ci-cd-build-fixes.md)
