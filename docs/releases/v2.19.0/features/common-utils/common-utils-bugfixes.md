---
tags:
  - common-utils
---
# Common Utils Bug Fixes

## Summary

Bug fixes and maintenance updates for the Common Utils library in v2.19.0, including fixes for bucket selector aggregation writeable name, monitor model enhancements for fanout control, and release notes.

## Details

### What's New in v2.19.0

#### Bucket Selector Aggregation Fix

Fixed the `getWriteableName()` method in `BucketSelectorIndices` class to return the correct aggregation name instead of the instance name. This fix ensures proper serialization and deserialization of bucket selector aggregations used by the Alerting plugin.

**Key Changes:**
- Changed `getWriteableName()` to return `BucketSelectorExtAggregationBuilder.NAME.preferredName` instead of `name`
- Added `StreamInput` constructor for proper deserialization
- Added comprehensive unit tests for bucket selector aggregation

#### Monitor Model Fanout Control

Added an optional `fanoutEnabled` field to `DocLevelMonitorInput` to control fanout behavior in document-level monitors. This addresses duplicate alert generation when aggregate sigma rules are matched.

**Key Changes:**
- Added `fanoutEnabled` field (optional, defaults to `true`)
- When set to `false`, disables fanout approach for chained findings doc level monitors
- Prevents duplicate alerts in detectors configured with aggregation sigma rules

### Technical Changes

| Component | Change |
|-----------|--------|
| `BucketSelectorIndices` | Fixed writeable name, added StreamInput constructor |
| `DocLevelMonitorInput` | Added `fan_out_enabled` field for fanout control |

## Limitations

- The `fanoutEnabled` field is optional and defaults to `true` for backward compatibility
- Bucket selector fix requires coordinated updates with the Alerting plugin

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#773](https://github.com/opensearch-project/common-utils/pull/773) | Fix bucket selector aggregation writeable name | - |
| [#758](https://github.com/opensearch-project/common-utils/pull/758) | Monitor model changed to add optional fanoutEnabled field | - |
| [#780](https://github.com/opensearch-project/common-utils/pull/780) | Added 2.19.0.0 release notes | [#751](https://github.com/opensearch-project/common-utils/issues/751) |
