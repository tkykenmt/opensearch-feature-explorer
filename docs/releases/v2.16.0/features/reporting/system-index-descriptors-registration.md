---
tags:
  - reporting
---
# System Index Descriptors Registration

## Summary

In v2.16.0, the reporting and sql plugins now formally register their system indices through the `SystemIndexPlugin.getSystemIndexDescriptors` extension point in OpenSearch core. This change is part of a broader initiative to strengthen system index protection across the plugin ecosystem.

## Details

### What's New in v2.16.0

Previously, plugins managed their system indices informally without registering them through the core extension point. This change introduces formal registration of system indices, enabling better security controls and protection mechanisms.

### Technical Changes

#### Reporting Plugin

The `ReportsSchedulerPlugin` class now implements `SystemIndexPlugin` and registers two system indices:

| Index Name | Description |
|------------|-------------|
| `.opendistro-reports-definitions` | Reports Scheduler Plugin Definitions index |
| `.opendistro-reports-instances` | Reports Scheduler Plugin Instances index |

```kotlin
class ReportsSchedulerPlugin : Plugin(), ActionPlugin, SystemIndexPlugin, JobSchedulerExtension {
    override fun getSystemIndexDescriptors(settings: Settings): Collection<SystemIndexDescriptor> {
        return listOf(
            SystemIndexDescriptor(REPORT_DEFINITIONS_INDEX_NAME, "Reports Scheduler Plugin Definitions index"),
            SystemIndexDescriptor(REPORT_INSTANCES_INDEX_NAME, "Reports Scheduler Plugin Instances index")
        )
    }
}
```

#### SQL Plugin

The `SQLPlugin` class now implements `SystemIndexPlugin` and registers:

| Index Pattern | Description |
|---------------|-------------|
| `.ql-datasources` | SQL DataSources index |
| `.spark-request-buffer*` | SQL Spark Request Buffer index pattern |

```java
public class SQLPlugin extends Plugin implements ActionPlugin, ScriptPlugin, SystemIndexPlugin {
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
}
```

### Background

This change is related to a broader security initiative ([security#4439](https://github.com/opensearch-project/security/issues/4439)) to strengthen system index protection. The goal is to:

1. Formally register all plugin system indices through the `SystemIndexPlugin` extension point
2. Enable the security plugin to enforce access controls based on registered system indices
3. Prevent unauthorized access to plugin system indices when the ThreadContext is stashed

## Limitations

- The indices are functionally unchanged; this is purely a formal registration
- Full system index protection requires additional security plugin changes (ongoing work)

## References

### Pull Requests

| PR | Repository | Description |
|----|------------|-------------|
| [#1009](https://github.com/opensearch-project/reporting/pull/1009) | reporting | Register system index descriptors through SystemIndexPlugin |
| [#2817](https://github.com/opensearch-project/sql/pull/2817) | sql | Backport: Register system index descriptors through SystemIndexPlugin |
| [#2772](https://github.com/opensearch-project/sql/pull/2772) | sql | Original: Register system index descriptors through SystemIndexPlugin |

### Related Issues

| Issue | Repository | Description |
|-------|------------|-------------|
| [#4439](https://github.com/opensearch-project/security/issues/4439) | security | RFC: Strengthen System Index Protection in the Plugin Ecosystem |
