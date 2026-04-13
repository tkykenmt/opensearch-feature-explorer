---
tags:
  - opensearch-dashboards
---
# Dashboards CI & Test Infrastructure

## Summary

OpenSearch Dashboards v3.6.0 includes a major overhaul of the CI/CD pipeline, delivering significant reliability and performance improvements. Key changes include a shared source archive to eliminate redundant git checkouts, Cypress group rebalancing for sub-20-minute targets, Jest test group rebalancing, separation of PR and post-merge workflows, and several critical bug fixes for Windows test execution and Lighthouse metrics.

## Details

### What's New in v3.6.0

#### Source Archive & Cache Optimization (PR #11560)

Replaced per-job `git checkout` with a single `prepare-source` job that creates a compressed source archive (~123 MB), uploaded as a GitHub Actions artifact. All downstream jobs download this artifact instead of independently checking out the repository, eliminating exposure to GitHub git server outliers (20s–25min observed).

New jobs introduced:
- `prepare-source`: Single checkout, source archive creation, Linux yarn cache warming
- `prepare-windows-cache`: Windows-specific cache warming; downstream Windows jobs use restore-only
- `prepare-cypress`: Single checkout + bootstrap + plugin build for Cypress workflow
- `build-min-artifact-linux-x64`: Extracted from the 5-platform matrix so BWC tests start immediately

#### Cypress Group Rebalancing (PR #11565)

Reorganized Cypress spec files from 23 groups into 33 smaller groups to meet a sub-20-minute per-job target. The longest group dropped from 43 minutes to 26 minutes. Additional optimizations:
- Disabled video compression (`videoCompression: false`), saving ~2 min/job
- Auto-delete passing spec videos via `after:spec` hook — only failure videos are kept
- Separated post-merge tests from PR tests to eliminate redundant CI runs

#### Jest Test Group Improvements (PR #11546)

- Split integration tests into a dedicated `integration-tests` job (Linux + Windows matrix) with Java 21
- Pre-build plugin bundles once in `build-plugins-artifact` job; functional tests download the artifact
- Added Jest ciGroup5 and rebalanced groups 3/4/5 to keep Windows wall-clock time under 30 min
- Split TSVB functional tests into new ciGroup14
- Fixed `use_node.bat` exit code bug: `ENDLOCAL` was resetting `ERRORLEVEL` to 0, silently swallowing all Node.js test failures on Windows
- Fixed mocha path-separator regex for Windows stack traces
- Added `--forceExit` to `test:jest_integration:ci` to prevent hung workers

#### Platform Plugin Build Optimization (PR #11176)

Reduced platform plugin build time from ~16 minutes to ~4 minutes by building only a single theme (`OSD_OPTIMIZER_THEMES: v8light`) instead of 6–8 distribution themes during CI test runs.

#### CI Workflow Restructuring (PR #11565)

- `build_and_test_workflow.yml`: Removed `push` trigger (PR-only), removed BWC tests and build artifact jobs from PR checks
- New `post_merge_test.yml`: Runs on push to `main` and release branches with focused subset; includes `fail-fast: false` for BWC tests; auto-creates GitHub issue on failure

#### Required Test Path Fix (PR #11324)

Removed `paths-ignore` filters from required CI test workflows. Previously, PRs that only touched docs or non-code files would have required tests skipped, leaving PRs in a stuck state unable to merge.

#### Lighthouse Metrics Fix (PR #11357, #11565)

- Removed bundler CI script
- Updated Lighthouse metrics thresholds
- Fixed warn-vs-fail logic: `warn`-level assertions no longer block PRs
- Added detailed assertion output to CI logs

#### S3 Cypress Test Fix (PR #11326)

Fixed S3 Cypress tests that were not correctly navigating to workspace pages by adjusting `navigateToWorkSpaceSpecificPage` Cypress commands.

#### Code Diff Analyzer Onboarding (PR #11388)

Onboarded the code diff analyzer and reviewer tool for OpenSearch Dashboards, enabling automated code analysis on PRs.

#### Test Snapshot Update (PR #11578)

Updated data connection table test snapshots that were broken by PR #11569 (data connection table styling changes), fixing CI group 5 unit test failures.

#### Documentation Link Fixes (PR #11472)

Fixed broken internal documentation links in `DEVELOPER_GUIDE.md` and `README.md` for developers navigating on GitHub.

### CI Cost Impact

| Area | Before | After |
|------|--------|-------|
| Cypress video processing | ~2 min/job × 32 jobs | 0 (disabled) |
| PR checks: BWC tests | 10 jobs per PR | 0 (post-merge only) |
| PR checks: build artifacts | 5 jobs per PR | 0 (post-merge only) |
| Post-merge duplicate suite | Full suite re-run | Focused subset |
| Git checkout outliers | 30+ independent checkouts | 1 shared archive |
| Plugin builds per Cypress job | ~9 min × 13+ jobs | 1 shared build |

## Limitations

- The `prepare-source` archive excludes `cypress/test_data/` (652 MB), so BWC tests still use `actions/checkout`
- `lint-and-validate` retains `actions/checkout` because it requires real git history for `git status` checks
- macOS jobs still use full `cache` (restore + auto-save) since there is no cache-warming job for macOS

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#11560](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11560) | Add `prepare-source` and `prepare-cypress` jobs for CI reliability |  |
| [#11546](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11546) | Improve "Build and test" CI test groups with integration test split and plugin pre-build |  |
| [#11565](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11565) | Split oversized Cypress CI groups for sub-20-minute target |  |
| [#11176](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11176) | Optimize GitHub CI workflow by reducing platform plugin build time |  |
| [#11324](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11324) | Remove ignore paths for required CI tests to prevent stuck PRs |  |
| [#11326](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11326) | Fix S3 Cypress tests not navigating to workspace page |  |
| [#11357](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11357) | Update Lighthouse metrics and remove bundler CI script |  |
| [#11388](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11388) | Onboard code diff analyzer and reviewer for OSD | [opensearch-build#5912](https://github.com/opensearch-project/opensearch-build/issues/5912) |
| [#11472](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11472) | Fix internal documentation links for developers on GitHub |  |
| [#11578](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11578) | Update data connection table test snapshots |  |
| [#11539](https://github.com/opensearch-project/observability/pull/11539) | CI performance and observability improvements (Windows cache, timeouts, JUnit reporting) |  |
