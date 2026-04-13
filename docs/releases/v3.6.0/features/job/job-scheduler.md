---
tags:
  - job
---
# Job Scheduler

## Summary

Two bug fixes for the Job Scheduler plugin in v3.6.0: a critical fix to the sweep query sort field that prevented job sweeping when `indices.id_field_data.enabled` was set to `false`, and a build infrastructure fix replacing deprecated Gradle Shadow plugin API usage.

## Details

### What's New in v3.6.0

#### Sweep Query Sort Field Fix

The `JobSweeper` component uses `search_after` pagination to iterate over job metadata documents in each shard. Previously, the sweep query sorted by `_id` using `FieldSortBuilder("_id")`. When the cluster setting `indices.id_field_data.enabled` was set to `false`, this caused the sweep to fail with:

> Fielddata access on the _id field is disallowed, you can re-enable it by updating the dynamic cluster setting: indices.id_field_data.enabled

The fix replaces the sort field from `_id` to `_seq_no` in `JobSweeper.java`:

- Sort field changed from `FieldSortBuilder("_id")` with `unmappedType("keyword")` to `FieldSortBuilder("_seq_no")` with `unmappedType("long")`
- `search_after` parameter changed from `String[]` to `Long[]`
- `sweepShard` method signature changed: `startAfter` parameter type from `String` to `long`, with initial value `-1L` instead of `null`
- Added `try-catch` around the search call to gracefully handle exceptions, logging the error and aborting the shard sweep instead of propagating the exception
- Pagination termination changed from `searchAfter = null` check to `break` when no hits are returned

`_seq_no` has `doc_values` enabled by default (no fielddata needed) and is unique per shard, which the sweeper already scopes to via `_shards` preference.

A related fix was also applied in the Alerting plugin (`opensearch-project/alerting#2039`) which had the same `_id` sort issue in its own `JobSweeper` copy.

#### Shadow Plugin Deprecated API Update

The `spi/build.gradle` was updated to replace the deprecated `project.shadow.component(publication)` call with `publication.artifact(tasks.shadowJar)` in the Maven publication configuration. This prepares the build for future Gradle Shadow plugin updates.

## Limitations

- The `_seq_no` sort order may differ from the previous `_id` sort order, but this has no functional impact since the sweeper processes all documents regardless of order.
- `_seq_no` values can change when documents are updated, but this is acceptable since the sweeper reads all documents in each cycle.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| https://github.com/opensearch-project/job-scheduler/pull/896 | Replace search sorted by `_id` to `_seq_no` for sweep query | https://github.com/opensearch-project/job-scheduler/issues/892 |
| https://github.com/opensearch-project/job-scheduler/pull/884 | Update shadow plugin usage to replace deprecated API | - |
| https://github.com/opensearch-project/alerting/pull/2039 | Related: same `_id` to `_seq_no` fix in Alerting plugin | https://github.com/opensearch-project/alerting/issues/2037 |
