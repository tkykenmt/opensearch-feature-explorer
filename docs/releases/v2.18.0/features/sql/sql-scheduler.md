# SQL Scheduler

## Summary

This bugfix removes the SQL scheduler index (`.async-query-scheduler`) from the `SystemIndexDescriptor` registration in the SQL plugin. The scheduler index was incorrectly registered as a system index, which caused issues because the Job Scheduler plugin already manages this index. This change corrects the system index configuration to prevent conflicts.

## Details

### What's New in v2.18.0

The SQL plugin previously registered the `.async-query-scheduler` index as a system index in the `getSystemIndexDescriptors()` method. This was incorrect because:

1. The Job Scheduler plugin already manages the scheduler index lifecycle
2. Duplicate system index registration can cause conflicts during index operations
3. The scheduler index should be managed by the Job Scheduler plugin, not the SQL plugin

### Technical Changes

#### Code Changes

The fix removes the scheduler index registration from `SQLPlugin.java`:

```java
// Before (v2.17.0)
@Override
public Collection<SystemIndexDescriptor> getSystemIndexDescriptors(Settings settings) {
    List<SystemIndexDescriptor> systemIndexDescriptors = new ArrayList<>();
    systemIndexDescriptors.add(
        new SystemIndexDescriptor(
            OpenSearchDataSourceMetadataStorage.DATASOURCE_INDEX_NAME, "SQL DataSources index"));
    systemIndexDescriptors.add(
        new SystemIndexDescriptor(
            SPARK_REQUEST_BUFFER_INDEX_NAME + "*", "SQL Spark Request Buffer index pattern"));
    systemIndexDescriptors.add(
        new SystemIndexDescriptor(
            OpenSearchAsyncQueryScheduler.SCHEDULER_INDEX_NAME, "SQL Scheduler job index"));
    return systemIndexDescriptors;
}

// After (v2.18.0)
@Override
public Collection<SystemIndexDescriptor> getSystemIndexDescriptors(Settings settings) {
    List<SystemIndexDescriptor> systemIndexDescriptors = new ArrayList<>();
    systemIndexDescriptors.add(
        new SystemIndexDescriptor(
            OpenSearchDataSourceMetadataStorage.DATASOURCE_INDEX_NAME, "SQL DataSources index"));
    systemIndexDescriptors.add(
        new SystemIndexDescriptor(
            SPARK_REQUEST_BUFFER_INDEX_NAME + "*", "SQL Spark Request Buffer index pattern"));
    return systemIndexDescriptors;
}
```

#### System Index Registration (After Fix)

| Index | Description | Registered By |
|-------|-------------|---------------|
| `.ql-datasources` | SQL DataSources index | SQL Plugin |
| `.spark-request-buffer*` | SQL Spark Request Buffer index pattern | SQL Plugin |
| `.async-query-scheduler` | Scheduler job index | Job Scheduler Plugin |

### Migration Notes

No migration is required. The fix is transparent to users and does not affect existing scheduler jobs or index data.

## Limitations

None specific to this bugfix.

## Related PRs

| PR | Description |
|----|-------------|
| [#3092](https://github.com/opensearch-project/sql/pull/3092) | Remove scheduler index from SystemIndexDescriptor (main) |
| [#3097](https://github.com/opensearch-project/sql/pull/3097) | Backport to 2.x branch |

## References

- [PR #3092](https://github.com/opensearch-project/sql/pull/3092): Original implementation
- [Documentation](https://docs.opensearch.org/2.18/dashboards/management/scheduled-query-acceleration/): Scheduled Query Acceleration

## Related Feature Report

- [Full feature documentation](../../../../features/sql/flint-query-scheduler.md)
