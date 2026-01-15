---
tags:
  - opensearch-dashboards
---
# Build & Compilation Fixes

## Summary

This release fixes a bootstrapping error caused by Babel dependency incompatibilities in the 2.x branch. The fix updates `@babel/traverse` and `@babel/plugin-transform-class-static-block` to compatible versions.

## Details

### What's New in v2.16.0

A Babel error was preventing successful bootstrapping of OpenSearch Dashboards on the 2.x branch. The issue was caused by version incompatibilities between Babel packages.

### Technical Changes

The fix updates the following dependencies in `package.json`:

| Dependency | Previous Version | New Version |
|------------|-----------------|-------------|
| `@babel/traverse` (resolution) | ^7.23.2 | ^7.25.0 |
| `@babel/plugin-transform-class-static-block` | ^7.24.4 | ^7.24.7 |

These updates resolve compatibility issues specific to the 2.x branch. The main branch already had compatible versions.

### Files Changed

| File | Changes |
|------|---------|
| `package.json` | Updated Babel dependency versions |
| `yarn.lock` | Updated lockfile with new dependency tree |

## Limitations

- This fix is specific to the 2.x branch
- The main branch does not require these changes

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#7541](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7541) | Fix babel error | - |
