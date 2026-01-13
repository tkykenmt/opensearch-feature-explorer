---
tags:
  - domain/core
  - component/server
  - ml
  - search
---
# Common Utils Bugfixes

## Summary

This release fixes a long-standing bug where several `ctx` (context) variables documented for Alerting monitor actions were not actually available at runtime. The fix adds missing template argument fields to various alerting model classes, ensuring that users can access all documented context variables in their monitor action templates.

## Details

### What's New in v2.17.0

The PR adds missing `ctx` variables that were documented but not implemented in the Alerting plugin. This allows users to access additional context information when configuring monitor actions.

### Technical Changes

#### New Context Variables Added

The following context variables are now available in monitor action templates:

| Model | New Fields |
|-------|------------|
| `Monitor` | `monitor_type`, `enabled_time`, `last_update_time`, `schedule`, `inputs` |
| `Action` | `id`, `destination_id`, `throttle_enabled` |
| `QueryLevelTrigger` | `condition.script.source`, `condition.script.lang` |
| `DocumentLevelTrigger` | `condition.script.source`, `condition.script.lang` |
| `BucketLevelTrigger` | `condition.script.source`, `condition.script.lang` |
| `Schedule` (Cron) | `cron.expression`, `cron.timezone` |
| `Schedule` (Interval) | `period.interval`, `period.unit` |
| `SearchInput` | `search.indices`, `search.query` |

#### Modified Components

| Component | Description |
|-----------|-------------|
| `Monitor.kt` | Extended `asTemplateArg()` to include monitor type, enabled time, last update time, schedule, and inputs |
| `Action.kt` | Extended `asTemplateArg()` to include id, destination_id, and throttle_enabled |
| `QueryLevelTrigger.kt` | Added condition field with script source and language |
| `DocumentLevelTrigger.kt` | Added condition field with script source and language |
| `BucketLevelTrigger.kt` | Added condition field with script source and language |
| `Schedule.kt` | Added `asTemplateArg()` method to both `CronSchedule` and `IntervalSchedule` |
| `SearchInput.kt` | Added `asTemplateArg()` method with indices and query |
| `Input.kt` | Added abstract `asTemplateArg()` method to interface |

### Usage Example

With this fix, users can now access additional context variables in their monitor action message templates:

```mustache
Monitor "{{ctx.monitor.name}}" (type: {{ctx.monitor.monitor_type}}) triggered!

Trigger: {{ctx.trigger.name}}
Condition: {{ctx.trigger.condition.script.source}}

Action: {{ctx.action.name}} (ID: {{ctx.action.id}})
Destination: {{ctx.action.destination_id}}

Schedule: {{#ctx.monitor.schedule.period}}Every {{interval}} {{unit}}{{/ctx.monitor.schedule.period}}
Last updated: {{ctx.monitor.last_update_time}}
```

## Limitations

- This fix is in the common-utils library; the Alerting plugin must use the updated version to benefit from these changes
- The original issue (alerting#200) remains open as there may be additional context variables to add

## References

### Documentation
- [OpenSearch Alerting Documentation](https://opensearch.org/docs/latest/monitoring-plugins/alerting/monitors/#available-variables): Available variables documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#710](https://github.com/opensearch-project/common-utils/pull/710) | Add missing ctx variables |
| [#318](https://github.com/opensearch-project/common-utils/pull/318) | Original PR (superseded by #710) |

### Issues (Design / RFC)
- [Issue #200](https://github.com/opensearch-project/alerting/issues/200): Missing ctx variables for Actions

## Related Feature Report

- [Full feature documentation](../../../../features/common-utils/common-utils-alerting-context-variables.md)
