---
tags:
  - multi-plugin
---
# System Index Descriptors Registration

## Summary

In v2.16.0, the alerting, anomaly-detection, and flow-framework plugins now formally register their system indices through the `SystemIndexPlugin.getSystemIndexDescriptors` extension point in OpenSearch core. This is part of a broader initiative to strengthen system index protection across the plugin ecosystem.

## Details

### What's New in v2.16.0

These plugins previously managed their system indices informally. This change introduces formal registration through the core extension point, enabling better security controls and protection mechanisms.

### Technical Changes

#### Alerting Plugin

The `AlertingPlugin` class now implements `SystemIndexPlugin` and registers:

| Index Pattern | Description |
|---------------|-------------|
| `.opendistro-alerting-alerts*` | Alerting Plugin system index pattern |
| `.opendistro-alerting-config` | Alerting Plugin Configuration index |

```kotlin
internal class AlertingPlugin : PainlessExtension, ActionPlugin, ScriptPlugin, 
    ReloadablePlugin, SearchPlugin, SystemIndexPlugin, PercolatorPluginExt() {
    
    override fun getSystemIndexDescriptors(settings: Settings): Collection<SystemIndexDescriptor> {
        return listOf(
            SystemIndexDescriptor(ALL_ALERT_INDEX_PATTERN, "Alerting Plugin system index pattern"),
            SystemIndexDescriptor(SCHEDULED_JOBS_INDEX, "Alerting Plugin Configuration index")
        )
    }
}
```

#### Anomaly Detection Plugin

The `TimeSeriesAnalyticsPlugin` class now implements `SystemIndexPlugin` and registers:

| Index Name | Description |
|------------|-------------|
| `.opendistro-anomaly-detectors` | Time Series Analytics config index |
| `.opendistro-anomaly-results*` | AD result index pattern |
| `.opendistro-anomaly-checkpoints` | AD Checkpoints index |
| `.opendistro-anomaly-detection-state` | AD State index |
| `.opensearch-forecast-checkpoints` | Forecast Checkpoints index |
| `.opensearch-forecast-state` | Forecast state index |
| `.opendistro-anomaly-detector-jobs` | Time Series Analytics job index |

```java
public class TimeSeriesAnalyticsPlugin extends Plugin 
    implements ActionPlugin, ScriptPlugin, SystemIndexPlugin, JobSchedulerExtension {
    
    @Override
    public Collection<SystemIndexDescriptor> getSystemIndexDescriptors(Settings settings) {
        List<SystemIndexDescriptor> systemIndexDescriptors = new ArrayList<>();
        systemIndexDescriptors.add(new SystemIndexDescriptor(CONFIG_INDEX, "Time Series Analytics config index"));
        systemIndexDescriptors.add(new SystemIndexDescriptor(ALL_AD_RESULTS_INDEX_PATTERN, "AD result index pattern"));
        systemIndexDescriptors.add(new SystemIndexDescriptor(CHECKPOINT_INDEX_NAME, "AD Checkpoints index"));
        systemIndexDescriptors.add(new SystemIndexDescriptor(DETECTION_STATE_INDEX, "AD State index"));
        systemIndexDescriptors.add(new SystemIndexDescriptor(FORECAST_CHECKPOINT_INDEX_NAME, "Forecast Checkpoints index"));
        systemIndexDescriptors.add(new SystemIndexDescriptor(FORECAST_STATE_INDEX, "Forecast state index"));
        systemIndexDescriptors.add(new SystemIndexDescriptor(JOB_INDEX, "Time Series Analytics job index"));
        return systemIndexDescriptors;
    }
}
```

#### Flow Framework Plugin

The `FlowFrameworkPlugin` class now implements `SystemIndexPlugin` and registers:

| Index Name | Description |
|------------|-------------|
| `.plugins-flow-framework-config` | Flow Framework Config index |
| `.plugins-flow-framework-templates` | Flow Framework Global Context index |
| `.plugins-flow-framework-state` | Flow Framework Workflow State index |

```java
public class FlowFrameworkPlugin extends Plugin implements ActionPlugin, SystemIndexPlugin {
    
    @Override
    public Collection<SystemIndexDescriptor> getSystemIndexDescriptors(Settings settings) {
        return List.of(
            new SystemIndexDescriptor(CONFIG_INDEX, "Flow Framework Config index"),
            new SystemIndexDescriptor(GLOBAL_CONTEXT_INDEX, "Flow Framework Global Context index"),
            new SystemIndexDescriptor(WORKFLOW_STATE_INDEX, "Flow Framework Workflow State index")
        );
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
| [#1594](https://github.com/opensearch-project/alerting/pull/1594) | alerting | Backport: Register system index descriptors through SystemIndexPlugin |
| [#1251](https://github.com/opensearch-project/anomaly-detection/pull/1251) | anomaly-detection | Register system index descriptors through SystemIndexPlugin |
| [#750](https://github.com/opensearch-project/flow-framework/pull/750) | flow-framework | Register system index descriptors through SystemIndexPlugin |

### Related Issues

| Issue | Repository | Description |
|-------|------------|-------------|
| [#4439](https://github.com/opensearch-project/security/issues/4439) | security | RFC: Strengthen System Index Protection in the Plugin Ecosystem |
