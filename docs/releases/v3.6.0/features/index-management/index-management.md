---
tags:
  - index-management
---
# Index Management

## Summary

Bug fixes and infrastructure improvements for the Index Management plugin in v3.6.0. This release fixes a flaky rollup test caused by race conditions with background coroutines, fixes a typo in the `validFileNameExcludingAsterisk` validation method that caused a build failure, adds Remote Store integration test infrastructure for ISM, and updates the Gradle shadow plugin to replace a deprecated API.

## Details

### What's New in v3.6.0

#### Flaky Rollup Test Fix (PR #1530)

Fixed a race condition in rollup integration tests where background coroutines continued running after test cleanup. The root cause was:

1. Tests create enabled rollups → JobScheduler schedules them
2. `RollupRunner.runJob()` launches coroutines via `launch {}`
3. Test `@After` wipes indices
4. Coroutines still running in background write metadata after indices are wiped
5. Index auto-creates with wrong dynamic mappings (`long` vs `date`)
6. Next test fails with mapping conflict on `rollup_metadata.continuous.next_window_end_time`

The fix introduces `stopAllRollupJobs()` and `waitForRollupJobsToStop()` methods in `RollupRestTestCase` that explicitly stop all rollup jobs and wait for them to be disabled before index cleanup proceeds.

#### Fix Typo in `validFileNameExcludingAsterisk` (PR #1608)

Fixed a typo in `ISMTemplateService.kt` where `Strings.validFileNameExcludingAstrix` was called instead of the correctly-spelled `Strings.validFileNameExcludingAsterisk`. This was caused by an upstream OpenSearch API rename and resulted in a build failure for the index-management 3.6.0 distribution (AUTOCUT Issue #1590).

#### Remote Store Integration Test Infrastructure (PR #1589)

Added a `remoteStoreIntegTest` Gradle task with a dedicated two-node test cluster configured for Remote Store:

- Node 0: `[cluster_manager, data, warm]` roles
- Node 1: `[search]` role
- Remote Store enabled with `fs` type repository for segment, translog, and state
- Segment Replication enabled

Includes `SearchOnlyActionIT` as the first test on this infrastructure, validating the `search_only` ISM action which requires Remote Store + Segment Replication + search replicas. Also updates `IndexManagementRestTestCase` to ignore segment replication background tasks (`segrep_publish_checkpoint`, `indices:admin/publishCheckpoint`) during test teardown.

#### Update Shadow Plugin Usage (PR #1587)

Replaced deprecated `project.shadow.component(it)` API call with `from components.shadow` in `spi/build.gradle` to prepare for an update to the Gradle shadow plugin dependency.

## Limitations

- The `remoteStoreIntegTest` task is not yet included in CI workflows; it must be run ad hoc with `./gradlew remoteStoreIntegTest`

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1530](https://github.com/opensearch-project/index-management/pull/1530) | Fix flaky rollup test by stopping jobs before index cleanup | [#90](https://github.com/opensearch-project/index-management/issues/90) |
| [#1608](https://github.com/opensearch-project/index-management/pull/1608) | Fix typo in `validFileNameExcludingAsterisk` validation method | [#1590](https://github.com/opensearch-project/index-management/issues/1590) |
| [#1589](https://github.com/opensearch-project/index-management/pull/1589) | Add Remote Store integration test infrastructure with SearchOnlyActionIT | [#1564](https://github.com/opensearch-project/index-management/issues/1564) |
| [#1587](https://github.com/opensearch-project/index-management/pull/1587) | Update shadow plugin usage to replace deprecated Gradle API | |
