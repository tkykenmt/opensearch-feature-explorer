---
tags:
  - domain/observability
  - component/dashboards
  - dashboards
  - observability
---
# Observability Bugfixes

## Summary

This release includes two bug fixes for the Dashboards Observability plugin that address issues with trace error display and metrics visualization rendering. These fixes improve the reliability of trace analytics error detection and ensure metrics visualizations display correctly in local cluster instances.

## Details

### What's New in v3.2.0

Two bug fixes addressing critical display issues in the Observability plugin:

1. **Traces Error Display Fix**: Improved error detection for traces using nested `status.code` field format
2. **Metrics Visualization Fix**: Fixed metrics visualizations not rendering in local cluster instances

### Technical Changes

#### Traces Error Display (PR #2475)

The fix addresses error display issues when trace data uses nested field format (`status.code`) instead of flat format (`status.code` as string key).

**Changes to `trace_view_helpers.tsx`:**
- Added fallback check for individual span errors when trace group error is not found
- Now checks both `span._source.status?.code === 2` and `span._source['status.code'] === 2`

**Changes to `traces_request_handler.ts`:**
- Updated error detection to handle both nested and flat status code formats
- Condition changed from `hit._source['status.code'] === 2` to `hit._source.status?.code === 2 || hit._source['status.code'] === 2`

**Changes to `traces_custom_indices_table.tsx`:**
- Exported `resolveFieldValue` function for testing
- Added `getNestedValue` helper for resolving nested field paths like `status.code`
- Enhanced field resolution to support nested object traversal

#### Metrics Visualization Fix (PR #2478)

Fixed metrics visualizations not appearing in local cluster instances by ensuring the `dataSourceMDSId` parameter is properly handled.

**Changes to `custom_panels/helpers/utils.tsx`:**
- Changed `dataSourceMDSId` to `dataSourceMDSId ?? ''` to provide empty string fallback when undefined
- Prevents API call failures when Multi-Data Source ID is not set

### Usage Example

The fixes are automatic and require no configuration changes. Error indicators now correctly display in:

1. **Trace Table**: Error column shows warning icon for traces with errors
2. **Gantt Chart**: Span labels include "⚠ Error" suffix for error spans

```typescript
// Error detection now handles both formats:
// Format 1: Nested object
{ status: { code: 2 } }

// Format 2: Flat key (legacy)
{ 'status.code': 2 }
```

## Limitations

- Error detection relies on status code value of `2` (OTel ERROR status)
- Metrics visualization fix only affects local cluster instances without MDS configuration

## References

### Documentation
- [Trace Analytics Documentation](https://docs.opensearch.org/3.2/observing-your-data/trace/ta-dashboards/): Official trace analytics guide
- [Data Prepper OTel Span Template](https://github.com/opensearch-project/data-prepper/blob/main/data-prepper-plugins/opensearch/src/main/resources/index-template/otel-v1-apm-span-index-standard-template.json): New Data Prepper format reference

### Pull Requests
| PR | Description |
|----|-------------|
| [#2475](https://github.com/opensearch-project/dashboards-observability/pull/2475) | [Bug] Traces error display |
| [#2478](https://github.com/opensearch-project/dashboards-observability/pull/2478) | [Bug] Fixed metrics viz not showing up |

## Related Feature Report

- Full feature documentation
