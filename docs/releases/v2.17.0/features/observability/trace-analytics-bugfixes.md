---
tags:
  - domain/observability
  - component/server
  - dashboards
  - observability
  - security
---
# Trace Analytics Bugfixes

## Summary

OpenSearch v2.17.0 includes multiple bug fixes for Trace Analytics in the dashboards-observability plugin. These fixes address issues with Multi-Data Source (MDS) support, URL routing, breadcrumb navigation, and broken links in the Getting Started workflows. The fixes improve stability when using Trace Analytics with multiple data sources and ensure proper navigation within the Application Analytics feature.

## Details

### What's New in v2.17.0

This release focuses on stability improvements for Trace Analytics, particularly around Multi-Data Source (MDS) integration:

1. **MDS ID Handling Fixes**: Multiple PRs address missing or incorrect MDS ID propagation, which caused page crashes when using Trace Analytics with multiple data sources
2. **URL Routing Fixes**: Direct URL navigation to `/traces` path now works correctly instead of defaulting to services page
3. **Navigation Improvements**: Breadcrumbs and ID pathing now work correctly in both old and new navigation modes
4. **Link Fixes**: Broken links in Getting Started workflows and CSV documentation have been corrected
5. **Dependency Updates**: Security vulnerability fix for org.json library (CVE-2023-5072)

### Technical Changes

#### Bug Categories

| Category | Issue | Fix |
|----------|-------|-----|
| MDS Support | Local cluster not rendering correctly | Added proper MDS ID handling for local cluster |
| MDS Support | Missing MDS ID in flyout | Added MDS ID parameter to trace flyout component |
| MDS Support | App Analytics crash | Fixed MDS ID propagation to Traces/Spans tabs |
| URL Routing | Direct URL load fails | Fixed default route path when URL hash is present |
| Navigation | Breadcrumbs incorrect | Fixed breadcrumb generation and ID pathing |
| Documentation | Broken links | Updated Getting Started and CSV workflow links |
| Dependencies | CVE-2023-5072 | Bumped org.json from 20210307 to 20231013 |

#### Components Affected

| Component | Description |
|-----------|-------------|
| TraceAnalytics | Main trace analytics page with MDS support |
| TraceFlyout | Detail flyout for individual traces |
| ApplicationAnalytics | Traces and Spans tabs in app analytics |
| GettingStarted | Getting started workflow links |

### Usage Example

After these fixes, Trace Analytics works correctly with Multi-Data Source:

```
# Direct URL navigation now works
http://host:port/app/observability-traces#/traces

# Previously would redirect to /services, now correctly loads /traces
```

### Migration Notes

No migration required. These are bug fixes that improve existing functionality.

## Limitations

- These fixes are specific to the dashboards-observability plugin
- MDS support requires proper configuration of data sources in OpenSearch Dashboards

## References

### Documentation
- [Trace Analytics Documentation](https://docs.opensearch.org/2.17/observing-your-data/trace/index/): Official documentation
- [CVE-2023-5072](https://nvd.nist.gov/vuln/detail/CVE-2023-5072): org.json vulnerability

### Pull Requests
| PR | Description |
|----|-------------|
| [#2006](https://github.com/opensearch-project/dashboards-observability/pull/2006) | Trace Analytics bug fix for local cluster rendering |
| [#2017](https://github.com/opensearch-project/dashboards-observability/pull/2017) | Fix docker links & index patterns names |
| [#2023](https://github.com/opensearch-project/dashboards-observability/pull/2023) | Traces and Spans tab fix for Application Analytics |
| [#2031](https://github.com/opensearch-project/dashboards-observability/pull/2031) | Getting Started broken link fix for CSV |
| [#2024](https://github.com/opensearch-project/dashboards-observability/pull/2024) | Fix direct URL load for Trace Analytics |
| [#2037](https://github.com/opensearch-project/dashboards-observability/pull/2037) | Trace Analytics bugfix for breadcrumbs and ID pathing |
| [#2100](https://github.com/opensearch-project/dashboards-observability/pull/2100) | Fixed traces bug for missing MDS ID |
| [#2012](https://github.com/opensearch-project/dashboards-observability/pull/2012) | Update Getting Started links to match catalog PR merges |
| [#1966](https://github.com/opensearch-project/dashboards-observability/pull/1966) | Bump org.json:json for CVE-2023-5072 |

### Issues (Design / RFC)
- [Issue #1878](https://github.com/opensearch-project/dashboards-observability/issues/1878): Trace Analytics MDS rendering issue
- [Issue #1931](https://github.com/opensearch-project/dashboards-observability/issues/1931): App Analytics page crash for missing MDS ID

## Related Feature Report

- [Full feature documentation](../../../../features/dashboards-observability/dashboards-observability-trace-analytics.md)
