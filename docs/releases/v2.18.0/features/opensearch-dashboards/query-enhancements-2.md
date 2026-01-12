# Query Enhancements (2)

## Summary

This release item includes bug fixes for the Query Enhancements feature in OpenSearch Dashboards v2.18.0. The fixes address issues with async query polling, error handling, language compatibility when switching datasets, and saved query persistence.

## Details

### What's New in v2.18.0

This batch of fixes improves the stability and usability of the Query Enhancements feature, particularly for SQL/PPL query execution in Discover.

### Technical Changes

#### Polling Logic Refactoring

The async search polling mechanism was refactored to poll for results only after the current request completes, rather than firing requests at fixed intervals regardless of completion status.

**Before:**
```typescript
// Fired polling request every 5 seconds regardless of previous call status
return timer(0, interval)
  .pipe(
    mergeMap(() => pollQueryResults()),
    // ...
  )
```

**After:**
```typescript
// Wait for current request to complete before polling again
do {
  await delay(interval);
  queryResultsRes = await pollQueryResults();
  queryStatus = queryResultsRes?.status?.toUpperCase();
} while (queryStatus !== 'SUCCESS' && queryStatus !== 'FAILED');
```

#### Error Handling Improvements

| Component | Fix |
|-----------|-----|
| Facet utility | Added success check before processing response in `describeQuery` |
| Error handler | Added `statusCode` fallback and explicit `status` property on errors |
| PPL jobs API | Added proper error handling for async PPL job failures |

#### Language Compatibility

When switching datasets (e.g., from index pattern to S3 connection), the system now automatically updates the query language if the current language is not supported by the new dataset type.

```typescript
// Check if new dataset supports current language
const supportedLanguages = this.datasetService
  .getType(newDataset.type)
  ?.supportedLanguages(newDataset);

if (supportedLanguages && !supportedLanguages.includes(newQuery.language)) {
  // Switch to first supported language and show warning
  newQuery = this.getInitialQuery({
    language: supportedLanguages[0],
    dataset: newQuery.dataset,
  });
}
```

#### Saved Query Dataset Persistence

Fixed saved queries to properly persist the dataset when query enhancements are enabled, ensuring queries can be restored with their original data source context.

### Usage Example

When switching from an index pattern (supporting DQL) to an S3 connection (supporting only SQL/PPL):

1. User is on index pattern with DQL query
2. User selects S3 connection from recent datasets
3. System detects DQL is not supported by S3
4. Language automatically switches to SQL
5. Warning toast notifies user: "Query language changed to SQL"

## Limitations

- The SQL PR #8708 mentioned in the issue body appears to reference a different repository or numbering scheme and could not be verified

## References

### Documentation
- [Dashboards Query Language (DQL)](https://docs.opensearch.org/2.18/dashboards/dql/): Official documentation
- [Query Workbench](https://docs.opensearch.org/2.18/dashboards/query-workbench/): SQL/PPL query interface

### Pull Requests
| PR | Description |
|----|-------------|
| [#8555](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8555) | Refactored polling logic to poll for results once current request completes |
| [#8650](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8650) | Fix random big number when loading in query result |
| [#8724](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8724) | Polling for PPL results; Saved dataset to saved queries |
| [#8743](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8743) | Fix error handling in query enhancement facet |
| [#8749](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8749) | Updates query and language if language is not supported by query data |
| [#8771](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8771) | Fix error handling for ppl jobs API |

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch-dashboards/query-enhancements.md)
