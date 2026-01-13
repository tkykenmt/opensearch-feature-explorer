---
tags:
  - domain/observability
  - component/server
  - dashboards
  - ml
  - observability
---
# Alerting Bugfixes

## Summary

OpenSearch 3.0.0 includes several bug fixes for the Alerting plugin, addressing issues with bucket selector aggregation, namespace conflicts, build compatibility with Java Agent migration, and release notes corrections. These fixes improve the stability and reliability of the alerting functionality.

## Details

### What's New in v3.0.0

This release focuses on maintenance and compatibility fixes rather than new features:

1. **Bucket Selector Aggregation Fix**: Corrected the pipeline aggregation registration for bucket selector, fixing issues with bucket-level monitors
2. **Namespace Conflict Resolution**: Updated namespace for the alerting plugin to avoid conflicts
3. **Java Agent Migration**: Fixed build issues related to phasing off SecurityManager usage in favor of Java Agent
4. **Dashboard Field Selection Fix**: Ensured `.keyword` subfields are selectable in bucket monitor group-by dropdown
5. **Release Notes Correction**: Fixed the filename for 3.0-beta release notes

### Technical Changes

#### Bucket Selector Aggregation Fix

The bucket selector aggregation writeable name was incorrectly registered, causing issues with bucket-level monitors. PR #1780 fixed the pipeline aggregation registration and moved the unit test suite to common-utils.

This fix depends on changes in [common-utils PR #773](https://github.com/opensearch-project/common-utils/pull/773).

#### Java Agent Migration

Two PRs addressed the transition from SecurityManager to Java Agent:

- **PR #1823**: Initial fix for build compatibility with Java Agent
- **PR #1824**: Adopted the java-agent Gradle plugin for proper support

This change aligns with the broader OpenSearch ecosystem migration away from the deprecated SecurityManager API.

#### Dashboard Subfield Selection

PR #1234 (alerting-dashboards-plugin) fixed an issue where `.keyword` subfields were not selectable in the group-by dropdown when creating bucket monitors. OpenSearch auto-creates `.keyword` subfields for text fields, and these are now properly available for selection.

Example mapping that now works correctly:
```json
{
  "audit_category": {
    "type": "text",
    "fields": {
      "keyword": {
        "type": "keyword",
        "ignore_above": 256
      }
    }
  }
}
```

## Limitations

- The bucket selector aggregation fix requires corresponding changes in common-utils (PR #773)
- Backporting the bucket selector fix to versions prior to v2.4 requires separate PRs due to code location changes

## References

### Documentation
- [Alerting Documentation](https://docs.opensearch.org/3.0/observing-your-data/alerting/index/): Official alerting documentation
- [Monitors Documentation](https://docs.opensearch.org/3.0/observing-your-data/alerting/monitors/): Monitor types and configuration
- [common-utils PR #773](https://github.com/opensearch-project/common-utils/pull/773): Related bucket selector fix in common-utils
- [job-scheduler PR #762](https://github.com/opensearch-project/job-scheduler/pull/762): Related Java Agent migration

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#1780](https://github.com/opensearch-project/alerting/pull/1780) | alerting | Fix bucket selector aggregation writeable name |
| [#1823](https://github.com/opensearch-project/alerting/pull/1823) | alerting | Fix build due to phasing off SecurityManager |
| [#1824](https://github.com/opensearch-project/alerting/pull/1824) | alerting | Use java-agent Gradle plugin |
| [#1831](https://github.com/opensearch-project/alerting/pull/1831) | alerting | Correct release notes filename |
| [#1234](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1234) | alerting-dashboards-plugin | Fix .keyword subfield selection in bucket monitor |

## Related Feature Report

- Full feature documentation
