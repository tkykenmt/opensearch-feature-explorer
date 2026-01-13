---
tags:
  - opensearch-dashboards
---
# Numeric Precision Setting

## Summary

OpenSearch Dashboards v2.19.0 introduces a new Advanced Setting called "Extend Numeric Precision" (`data:withLongNumerals`) that allows users to toggle the handling of extremely large numbers (long numerals) on or off. Previously, long numeral support was always enabled; now users can disable it to optimize performance when high precision for large values isn't required.

## Details

### What's New in v2.19.0

A new UI setting has been added to the Advanced Settings page under the Data section:

| Setting | Key | Default | Description |
|---------|-----|---------|-------------|
| Extend Numeric Precision | `data:withLongNumerals` | `true` (On) | Turn on for precise handling of extremely large numbers. Turn off to optimize performance when high precision for large values isn't required. |

### Technical Changes

The implementation modifies how OpenSearch Dashboards handles numeric values that exceed JavaScript's safe integer limits (`Number.MAX_SAFE_INTEGER` and `Number.MIN_SAFE_INTEGER`).

#### Affected Components

| Component | Change |
|-----------|--------|
| Console Plugin | Now reads `data:withLongNumerals` setting and passes `withLongNumeralsSupport` flag to API requests |
| Discover Plugin | Document search and single document view respect the precision setting |
| Data Plugin | Added `UI_SETTINGS.DATA_WITH_LONG_NUMERALS` constant and `isLongNumeralsSupported()` method to IndexPatternsService |

#### Configuration

The setting can be modified in:
1. **OpenSearch Dashboards UI**: Stack Management → Advanced Settings → Data section
2. **opensearch_dashboards.yml**: `data.withLongNumerals: true` or `false`

### Bug Fix

This PR also fixes a typo in the code that inspects values for large numerals in OpenSearch Dashboards and the JavaScript client.

## Limitations

- Disabling this setting may cause precision loss for numeric values outside JavaScript's safe integer range (±9,007,199,254,740,991)
- The setting affects all queries and document views across the Dashboards application

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#8837](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8837) | Add setting to turn extending numeric precision on or off | - |
