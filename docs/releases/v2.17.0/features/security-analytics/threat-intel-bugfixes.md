---
tags:
  - domain/security
  - component/server
  - indexing
  - security
---
# Threat Intel Bugfixes

## Summary

OpenSearch v2.17.0 includes 12 bug fixes for the Threat Intelligence feature in Security Analytics. These fixes address security vulnerabilities, improve stability in multi-node environments, fix integration issues with standard detectors, and enhance error handling for S3 source configurations.

## Details

### What's New in v2.17.0

This release focuses on stability and security improvements for the Threat Intelligence feature, addressing issues discovered after the initial release in v2.15.0.

### Technical Changes

#### Security Improvements

| Fix | Description | PR |
|-----|-------------|-----|
| User validation | Added user validation for threat intel transport layer classes | [#1207](https://github.com/opensearch-project/security-analytics/pull/1207) |
| Thread context stashing | Stashes thread context for all system index interactions | [#1207](https://github.com/opensearch-project/security-analytics/pull/1207) |
| List IOCs API security | Added user permission checks and context stashing for List IOCs API | [#1278](https://github.com/opensearch-project/security-analytics/pull/1278) |

#### Stability Fixes

| Fix | Description | PR |
|-----|-------------|-----|
| Multi-node race condition | Made IOC index creation async to prevent `resource_already_exists_exception` | [#1274](https://github.com/opensearch-project/security-analytics/pull/1274) |
| Event-driven lock release | Refactored source config lock release to be event-driven | [#1254](https://github.com/opensearch-project/security-analytics/pull/1254) |
| Job mapping upgrade | Fixed job index mapping discrepancy when upgrading from v2.12-2.15 to v2.16+ | [#1272](https://github.com/opensearch-project/security-analytics/pull/1272) |

#### Integration Fixes

| Fix | Description | PR |
|-----|-------------|-----|
| Standard detector compatibility | Fixed threat intel to work alongside standard detectors | [#1234](https://github.com/opensearch-project/security-analytics/pull/1234) |
| Search monitor query fix | Fixed search monitor query in update threat intel alert status API | [#1383](https://github.com/opensearch-project/security-analytics/pull/1383) (backported to 2.17) |

#### Data Management Fixes

| Fix | Description | PR |
|-----|-------------|-----|
| IOC mapping structure | Fixed searchString bug and removed nested IOC mapping structure | [#1239](https://github.com/opensearch-project/security-analytics/pull/1239) |
| Empty IOC index cleanup | Cleans up empty IOC indices created by failed source configs | [#1267](https://github.com/opensearch-project/security-analytics/pull/1267) |
| Refresh toggle | Added toggling refresh disable/enable for deactivate/activate operations | [#1240](https://github.com/opensearch-project/security-analytics/pull/1240) |

#### Error Handling Fixes

| Fix | Description | PR |
|-----|-------------|-----|
| S3 validation errors | Fixed S3 validation errors not caught by action listener | [#1257](https://github.com/opensearch-project/security-analytics/pull/1257) |

#### Test Fixes

| Fix | Description | PR |
|-----|-------------|-----|
| Mappings integration tests | Fixed mappings integration tests | [#1213](https://github.com/opensearch-project/security-analytics/pull/1213) |

### Migration Notes

Users upgrading from v2.12-2.15 with threat intel enabled should note:
- The job index mapping (`.opensearch-sap--job`) is automatically updated when creating a new source config
- No manual migration steps are required

## Limitations

- These fixes are backported from main branch; some may have been available in earlier 2.x releases
- Multi-node environments should ensure all nodes are upgraded to v2.17.0 for consistent behavior

## References

### Documentation
- [Threat Intelligence Documentation](https://docs.opensearch.org/2.17/security-analytics/threat-intelligence/index/): Official documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#1207](https://github.com/opensearch-project/security-analytics/pull/1207) | User validation for threat intel transport layer |
| [#1213](https://github.com/opensearch-project/security-analytics/pull/1213) | Fix mappings integration tests |
| [#1234](https://github.com/opensearch-project/security-analytics/pull/1234) | Make threat intel run with standard detectors |
| [#1239](https://github.com/opensearch-project/security-analytics/pull/1239) | Fixed searchString bug, removed nested IOC mapping |
| [#1240](https://github.com/opensearch-project/security-analytics/pull/1240) | Refresh toggle for deactivate/activate operations |
| [#1254](https://github.com/opensearch-project/security-analytics/pull/1254) | Event-driven lock release for source config |
| [#1257](https://github.com/opensearch-project/security-analytics/pull/1257) | Fix S3 validation errors not caught by action listener |
| [#1267](https://github.com/opensearch-project/security-analytics/pull/1267) | Clean up empty IOC indices from failed source configs |
| [#1272](https://github.com/opensearch-project/security-analytics/pull/1272) | Update threat intel job mapping to new version |
| [#1274](https://github.com/opensearch-project/security-analytics/pull/1274) | Fix threat intel multinode tests |
| [#1278](https://github.com/opensearch-project/security-analytics/pull/1278) | Stash context for List IOCs API |

### Issues (Design / RFC)
- [Issue #1224](https://github.com/opensearch-project/security-analytics/issues/1224): Lock release issue
- [Issue #1247](https://github.com/opensearch-project/security-analytics/issues/1247): Job mapping upgrade issue
- [Issue #1255](https://github.com/opensearch-project/security-analytics/issues/1255): Empty IOC index cleanup issue
- [Issue #1256](https://github.com/opensearch-project/security-analytics/issues/1256): S3 validation error issue

## Related Feature Report

- [Full feature documentation](../../../../features/security-analytics/security-analytics-threat-intelligence.md)
