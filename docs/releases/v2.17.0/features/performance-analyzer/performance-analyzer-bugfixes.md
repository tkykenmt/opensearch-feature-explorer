---
tags:
  - domain/observability
  - component/server
  - observability
  - performance
---
# Performance Analyzer Bugfixes

## Summary

This release item updates the Performance Analyzer plugin to use version 1.6.0 of the PA Commons library. This dependency bump brings in several bug fixes and improvements from the commons library, including fixes for statsCollector scheduling and new metrics constants.

## Details

### What's New in v2.17.0

The Performance Analyzer plugin dependency on `performance-analyzer-commons` was updated from version 1.5.0 to 1.6.0.

### Technical Changes

#### Dependency Update

| Dependency | Previous Version | New Version |
|------------|------------------|-------------|
| performance-analyzer-commons | 1.5.0 | 1.6.0 |

#### Changes in PA Commons 1.6.0

The PA Commons 1.6.0 release includes the following improvements merged between versions 1.5.0 and 1.6.0:

| PR | Description |
|----|-------------|
| [#87](https://github.com/opensearch-project/performance-analyzer-commons/pull/87) | Adds CacheConfig related info for telemetry collector |
| [#86](https://github.com/opensearch-project/performance-analyzer-commons/pull/86) | Adds heap metrics constants |
| [#85](https://github.com/opensearch-project/performance-analyzer-commons/pull/85) | Updates cpu_utilization metric name and adds constant |
| [#84](https://github.com/opensearch-project/performance-analyzer-commons/pull/84) | Adds OSMetrics constants to RTFMetrics |
| [#83](https://github.com/opensearch-project/performance-analyzer-commons/pull/83) | Adds index_uuid as a common dimension |
| [#82](https://github.com/opensearch-project/performance-analyzer-commons/pull/82) | Bugfix: Scheduling statsCollector for all collectorModes |

#### Key Bug Fix

The most significant fix in this update is PR #82, which ensures that the `statsCollector` is properly scheduled for all collector modes. Previously, the statsCollector was not being scheduled in certain collector modes, which could lead to incomplete metrics collection.

### Configuration

No configuration changes are required. The dependency update is transparent to users.

### Usage Example

Performance Analyzer continues to work as before. Query metrics using:

```bash
GET localhost:9600/_plugins/_performanceanalyzer/metrics/units
```

## Limitations

- This is a dependency update only; no new user-facing features are introduced
- Requires restart of the Performance Analyzer agent to pick up the new library

## References

### Documentation
- [Performance Analyzer Documentation](https://docs.opensearch.org/2.17/monitoring-your-cluster/pa/index/): Official documentation
- [PA Commons PR #90](https://github.com/opensearch-project/performance-analyzer-commons/pull/90): Bump PA commons to 1.6.0
- [PA Commons PR #82](https://github.com/opensearch-project/performance-analyzer-commons/pull/82): Bugfix for statsCollector scheduling

### Pull Requests
| PR | Description |
|----|-------------|
| [#712](https://github.com/opensearch-project/performance-analyzer/pull/712) | Bump PA to use 1.6.0 PA commons lib |

## Related Feature Report

- Full feature documentation
