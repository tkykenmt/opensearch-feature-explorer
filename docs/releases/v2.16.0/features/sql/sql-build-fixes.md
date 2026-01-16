---
tags:
  - sql
---
# SQL Build Fixes

## Summary

Fixed GitHub Actions workflow failures in the SQL plugin by addressing checkout action compatibility issues and restoring MacOS build workflows with proper runner configuration.

## Details

### What's New in v2.16.0

Two build infrastructure fixes were implemented:

1. **Checkout Action Fix (PR #2819)**: Added `ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION` environment variable to allow Node16 actions in GitHub Actions workflows, resolving checkout action failures.

2. **MacOS Workflow Restoration (PR #2831)**: Re-enabled MacOS build workflows that were previously removed due to M-series artifact issues. The fix uses `macos-13` runner instead of `macos-latest` to ensure Intel-based artifacts are available.

### Technical Changes

#### Checkout Action Fix

Modified workflow files to allow Node16 actions:

```yaml
# .github/workflows/integ-tests-with-security.yml
# .github/workflows/sql-test-and-build-workflow.yml
env:
  ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION: true
```

#### MacOS Workflow Restoration

Updated OS matrix to include MacOS:

```yaml
# integ-tests-with-security.yml
matrix:
  os: [ windows-latest, macos-13 ]  # Added macos-13

# sql-test-and-build-workflow.yml
matrix:
  entry:
    - { os: windows-latest, java: 21, os_build_args: -x doctest -PbuildPlatform=windows }
    - { os: macos-13, java: 21 }  # Added MacOS entry
```

### Files Changed

| File | Changes |
|------|---------|
| `.github/workflows/integ-tests-with-security.yml` | Added Node16 env var, added macos-13 to OS matrix |
| `.github/workflows/sql-test-and-build-workflow.yml` | Added Node16 env var, added macos-13 build entry |

## Limitations

- MacOS builds use `macos-13` (Intel) instead of `macos-latest` (M-series) due to artifact availability
- Node16 action compatibility workaround may need updates when actions are upgraded

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#2819](https://github.com/opensearch-project/sql/pull/2819) | Fix checkout action failure (backport from #2807) | - |
| [#2831](https://github.com/opensearch-project/sql/pull/2831) | Add MacOS workflows back and fix artifact not found issue | [#2662](https://github.com/opensearch-project/sql/pull/2662) |
