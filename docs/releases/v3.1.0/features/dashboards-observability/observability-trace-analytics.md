---
tags:
  - indexing
  - observability
  - search
---

# Observability Trace Analytics

## Summary

In v3.1.0, Trace Analytics receives significant enhancements that merge the custom source mode with the default Data Prepper mode, providing a unified experience with improved features. The span flyout now supports the new Data Prepper format with nested field flattening, and all custom source features (cross-cluster search, custom indices, new data grid, dynamic filters) are now available in the default mode.

## Details

### What's New in v3.1.0

1. **Unified Data Prepper Mode**: The experimental "custom source" mode introduced in v2.17 has been merged into the default Data Prepper mode, eliminating the need for separate mode selection.

2. **Span Flyout Format Support**: The span detail flyout now properly handles the new Data Prepper format with nested fields by flattening them for display and filter operations.

3. **Feature Consolidation**: All features previously exclusive to custom source mode are now available in the default Data Prepper mode:
   - Cross-cluster indices support
   - Custom index names
   - New data grid for traces
   - Dynamic attribute filters
   - Service filters on traces page
   - Trace to logs correlation

### Technical Changes

#### Mode Simplification

The `TraceAnalyticsMode` type has been simplified from three modes to two:

```typescript
// Before
type TraceAnalyticsMode = 'jaeger' | 'data_prepper' | 'custom_data_prepper';

// After
type TraceAnalyticsMode = 'jaeger' | 'data_prepper';
```

#### Span Flyout Nested Field Flattening

A new `flattenObject` function handles nested fields in the new Data Prepper format:

```typescript
export const flattenObject = (
  obj: any,
  prefix = '',
  result: Record<string, any> = {}
): Record<string, any> => {
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      const newKey = prefix ? `${prefix}.${key}` : key;
      if (obj[key] !== null && typeof obj[key] === 'object' && !Array.isArray(obj[key])) {
        flattenObject(obj[key], newKey, result);
      } else {
        result[newKey] = obj[key];
      }
    }
  }
  return result;
};
```

This enables proper display of nested attributes like:
- `instrumentationScope.name`
- `resource.attributes.service.name`
- `attributes.http.method`

#### Index Resolution Changes

The `getSpanIndices` and `getServiceIndices` functions now use custom settings for Data Prepper mode:

```typescript
export const getSpanIndices = (mode: TraceAnalyticsMode) => {
  switch (mode) {
    case 'data_prepper':
      return TraceSettings.getCustomSpanIndex();
    case 'jaeger':
    default:
      return JAEGER_INDEX_NAME;
  }
};
```

### Usage Example

```typescript
// Accessing trace analytics with custom indices
// Configure in Advanced Settings:
// observability:traceAnalyticsSpanIndices = "my-custom-span-*"
// observability:traceAnalyticsServiceIndices = "my-custom-service-*"

// Cross-cluster search example:
// observability:traceAnalyticsSpanIndices = "cluster1:otel-v1-apm-span-*,cluster2:otel-v1-apm-span-*"
```

### Migration Notes

- Users of the experimental "custom_data_prepper" mode should switch to "data_prepper" mode
- Custom index configurations remain in Advanced Settings
- No data migration required - existing indices continue to work

## Limitations

- The `dataPrepperIndicesExist` check has been removed; users should configure indices in Advanced Settings if defaults don't exist
- Nested field filtering in span flyout requires the new flattening logic

## References

### Documentation
- [Trace Analytics Documentation](https://docs.opensearch.org/3.0/observing-your-data/trace/ta-dashboards/): Official documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#2457](https://github.com/opensearch-project/dashboards-observability/pull/2457) | Merge custom source and data prepper mode in trace analytics |
| [#2450](https://github.com/opensearch-project/dashboards-observability/pull/2450) | Span Flyout - support new format with nested field flattening |

### Issues (Design / RFC)
- [Issue #2141](https://github.com/opensearch-project/dashboards-observability/issues/2141): RFC: Enhancements to Trace Analytics Plugin

## Related Feature Report

- [Full feature documentation](../../../features/dashboards-observability/dashboards-observability-trace-analytics.md)
