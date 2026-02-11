---
tags:
  - job-scheduler
---
# Job Scheduler

## Summary

Job Scheduler v3.5.0 includes CI/CD maintenance improvements focused on test reliability and workflow compatibility. The changes address flaky integration tests in the sample-extension-plugin and update GitHub Actions dependencies to Node.js 24.

## Details

### What's New in v3.5.0

#### Integration Test Retry Mechanism
Added retry logic (up to 3 attempts) for integration tests in the sample-extension-plugin to reduce CI flakiness. This addresses intermittent failures in multi-node integration tests without modifying the underlying test logic.

#### Changelog Workflow Fix
Renamed `CHANGELOG` to `CHANGELOG.md` to ensure the `changelog_verifier` workflow functions correctly. This aligns with the standard markdown file extension expected by the verification tooling.

#### GitHub Actions Updates
Updated GitHub Actions dependencies to support Node.js 24:
- `actions/upload-artifact`: v5 → v6
- `actions/download-artifact`: v6 → v7

These updates require Actions Runner version 2.327.1 or later for self-hosted runners.

### Technical Changes

| Change | Description |
|--------|-------------|
| Test retry | Added `maxRetries: 3` configuration for sample-extension-plugin integTest |
| File rename | `CHANGELOG` → `CHANGELOG.md` for workflow compatibility |
| Dependency bump | GitHub Actions artifact actions updated to Node.js 24 runtime |

## Limitations

- The test retry mechanism is a workaround; root causes of flaky tests in multi-node integration tests remain unaddressed
- Self-hosted runners must be updated to version 2.327.1+ before upgrading to the new GitHub Actions versions

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#872](https://github.com/opensearch-project/job-scheduler/pull/872) | Add integTest retry for sample-extension-plugin | [Flaky test example](https://github.com/opensearch-project/job-scheduler/actions/runs/20444634620/job/58745294299) |
| [#843](https://github.com/opensearch-project/job-scheduler/pull/843) | Rename CHANGELOG to CHANGELOG.md to ensure changelog_verifier workflow works | |
| [#868](https://github.com/opensearch-project/job-scheduler/pull/868) | Dependabot: bump actions/download-artifact from 6 to 7 | |
| [#867](https://github.com/opensearch-project/job-scheduler/pull/867) | Dependabot: bump actions/upload-artifact from 5 to 6 | |
