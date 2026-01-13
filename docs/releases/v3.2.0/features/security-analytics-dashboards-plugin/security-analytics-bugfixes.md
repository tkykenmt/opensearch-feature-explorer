---
tags:
  - domain/security
  - component/dashboards
  - dashboards
  - indexing
  - security
---
# Security Analytics Bugfixes

## Summary

This release includes two bugfixes for the Security Analytics Dashboards plugin that improve the stability and reliability of the correlations page and threat intelligence IOC type retrieval.

## Details

### What's New in v3.2.0

Two critical bugfixes address issues in the Security Analytics Dashboards plugin:

1. **Correlations Page Fix**: Removed the correlated findings bar chart that was causing the correlations page to break due to Vega visualization issues.

2. **IOC Types API Update**: Changed the method for fetching threat intelligence IOC types from a direct `_search` call to using the `searchThreatIntelSource` API, improving reliability and removing dependency on internal index access.

### Technical Changes

#### Correlations Page Fix (PR #1313)

The correlated findings bar chart component using Vega visualization was causing the correlations page to fail. The fix removes this visualization component entirely:

- Removed `renderCorrelatedFindingsChart` method from `CorrelationsTableView.tsx`
- Removed unused imports (`EuiPanel`, `EuiFlexGroup`, `EuiTitle`, `EuiSpacer`, `EuiEmptyPrompt`, `EuiSmallButton`, `EuiText`, `ChartContainer`, `renderVisualization`)
- The correlations table functionality remains intact

#### IOC Types API Update (PR #1312)

Changed how IOC (Indicator of Compromise) types are fetched for threat intelligence log source configuration:

| Before | After |
|--------|-------|
| Direct `_search` call to `.opensearch-sap-ioc*` index | `searchThreatIntelSource` API call |
| Required index-level access | Uses service API |
| Single source of IOC types | Aggregates IOC types from all threat intel sources |

The new implementation:
1. Calls `threatIntelService.searchThreatIntelSource()`
2. Iterates through all threat intel sources
3. Collects unique IOC types using a `Set`
4. Returns deduplicated array of IOC types

### Usage Example

The IOC types are now fetched through the threat intel service:

```typescript
const loadIocTypes = async () => {
  const res = await threatIntelService.searchThreatIntelSource();
  if (res.ok) {
    const uniqueIocTypes = new Set<string>();
    res.response.forEach((threatIntelSource) => {
      if (threatIntelSource.ioc_types && Array.isArray(threatIntelSource.ioc_types)) {
        threatIntelSource.ioc_types.forEach((iocType) => uniqueIocTypes.add(iocType));
      }
    });
    setIocTypes(Array.from(uniqueIocTypes));
  }
};
```

## Limitations

- The correlated findings bar chart visualization has been removed; users will need to rely on the correlation graph and table views for visualizing correlated findings.

## References

### Documentation
- [Security Analytics Documentation](https://docs.opensearch.org/3.0/security-analytics/)
- [Threat Intelligence Documentation](https://docs.opensearch.org/3.0/security-analytics/threat-intelligence/index/)
- [Working with the Correlation Graph](https://docs.opensearch.org/3.0/security-analytics/usage/correlation-graph/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#1313](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1313) | Remove correlated findings bar chart that uses vega |
| [#1312](https://github.com/opensearch-project/security-analytics-dashboards-plugin/pull/1312) | Update API call to get IOC types |

## Related Feature Report

- [Full feature documentation](../../../../features/security-analytics-dashboards-plugin/security-analytics-dashboards-plugin-security-analytics.md)
