---
tags:
  - dashboards
  - indexing
  - observability
---

# Observability Release Maintenance

## Summary

This release item covers routine maintenance activities for the Observability plugins in OpenSearch v3.1.0, including version increments and release notes updates for both the backend plugin (observability) and the frontend plugin (dashboards-observability).

## Details

### What's New in v3.1.0

The v3.1.0 release of the Observability plugins includes:

**Backend Plugin (observability)**:
- Version increment to 3.1.0-SNAPSHOT
- Release notes documentation

**Frontend Plugin (dashboards-observability)**:
- Version increment to 3.1.0.0
- Release notes documentation
- Bug fixes for Jaeger trace end time processing
- Bug fixes for NFW Integration Vega visualization warnings
- Enhancements to trace analytics with merged custom source and data prepper modes
- Span Flyout support for new trace format

### Technical Changes

#### Bug Fixes
| Fix | Description | PR |
|-----|-------------|-----|
| Jaeger End Time | Fix jaeger end time processing in trace analytics | [#2460](https://github.com/opensearch-project/dashboards-observability/pull/2460) |
| Vega Vis Warning | NFW Integration Vega Vis warning message fix | [#2452](https://github.com/opensearch-project/dashboards-observability/pull/2452) |

#### Enhancements
| Enhancement | Description | PR |
|-------------|-------------|-----|
| Trace Analytics Mode | Merge custom source and data prepper mode in trace analytics | [#2457](https://github.com/opensearch-project/dashboards-observability/pull/2457) |
| Span Flyout | Support new format in Span Flyout | [#2450](https://github.com/opensearch-project/dashboards-observability/pull/2450) |

#### Infrastructure
| Change | Description | PR |
|--------|-------------|-----|
| Version Bump | Workflows - Version bump to 3.1.0 | [#2451](https://github.com/opensearch-project/dashboards-observability/pull/2451) |

## Limitations

- This is a maintenance release with no new major features
- Bug fixes are specific to trace analytics functionality

## References

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#1922](https://github.com/opensearch-project/observability/pull/1922) | observability | Increment version to 3.1.0-SNAPSHOT |
| [#1929](https://github.com/opensearch-project/observability/pull/1929) | observability | Adding release notes for 3.1.0 |
| [#2443](https://github.com/opensearch-project/dashboards-observability/pull/2443) | dashboards-observability | Increment version to 3.1.0.0 |
| [#2464](https://github.com/opensearch-project/dashboards-observability/pull/2464) | dashboards-observability | Adding release notes for 3.1.0 |

### Issues (Design / RFC)
- [Issue #1924](https://github.com/opensearch-project/observability/issues/1924): Release notes tracking issue (observability)
- [Issue #2444](https://github.com/opensearch-project/dashboards-observability/issues/2444): Release notes tracking issue (dashboards-observability)

## Related Feature Report

- [Observability UI](../../../features/dashboards-observability/observability-ui.md)
- [Trace Analytics](../../../features/dashboards-observability/trace-analytics.md)
