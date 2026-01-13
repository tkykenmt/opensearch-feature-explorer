---
tags:
  - domain/infra
  - component/server
  - indexing
  - observability
  - performance
  - search
  - security
---
# Release Notes

## Summary

This release item covers the addition of v2.18.0 release notes across multiple OpenSearch plugin repositories. These PRs document the changes, enhancements, bug fixes, and maintenance updates included in the v2.18.0 release for each plugin.

## Details

### What's New in v2.18.0

Release notes were added to 5 plugin repositories documenting the changes included in OpenSearch v2.18.0:

| Repository | Release Notes File |
|------------|-------------------|
| alerting | `opensearch-alerting.release-notes-2.18.0.0.md` |
| common-utils | `opensearch-common-utils.release-notes-2.18.0.0.md` |
| notifications | `opensearch-notifications.release-notes-2.18.0.0.md` |
| query-insights | `opensearch-query-insights.release-notes-2.18.0.0.md` |
| security | `opensearch-security.release-notes-2.18.0.0.md` |

### Release Notes Content Summary

#### Alerting (v2.18.0.0)
- **Refactoring**: Alerting Comments system indices, remote monitor logging, separate doc-level monitor query indices
- **Bug Fixes**: Query index deletion timing, bucket level monitor optimization, query index shard configuration

#### Common Utils (v2.18.0.0)
- **Maintenance**: Version bump to 2.18.0-SNAPSHOT, Gradle 8.10.2 update
- **Enhancements**: Dynamic deletion support for doc-level monitor query indices

#### Notifications (v2.18.0.0)
- **Maintenance**: Version bump to 2.18.0-SNAPSHOT, CI workflow fixes

#### Query Insights (v2.18.0.0)
- **Enhancements**: Time range parameter for historical top N queries, health_stats API, OpenTelemetry error metrics, query field name/type grouping settings
- **Bug Fixes**: Measurement parsing logic refactor
- **Maintenance**: Security-based integration tests, default settings updates

#### Security (v2.18.0.0)
- **Enhancements**: Improved certificate error messages, datastreams as AuditLog sink, V6→V7 config auto-conversion, circuit breaker override, AD index permissions, PBKDF2 password hashing fix
- **Bug Fixes**: Non-flat YAML settings handling, system index read protection, dual mode flag propagation, SAML login fix, stored fields hashing, closed index mappings
- **Maintenance**: Multiple dependency bumps, maintainer updates, CVE-2024-47554 fix

## References

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#1718](https://github.com/opensearch-project/alerting/pull/1718) | alerting | Added 2.18.0 release notes |
| [#750](https://github.com/opensearch-project/common-utils/pull/750) | common-utils | Added 2.18.0.0 release notes |
| [#980](https://github.com/opensearch-project/notifications/pull/980) | notifications | Added 2.18.0 release notes |
| [#148](https://github.com/opensearch-project/query-insights/pull/148) | query-insights | Add release notes for 2.18 |
| [#1399](https://github.com/opensearch-project/security/pull/1399) | security | Added 2.18.0 release notes |

### Issues (Design / RFC)
- [Issue #1654](https://github.com/opensearch-project/alerting/issues/1654): Alerting release notes tracking
- [Issue #730](https://github.com/opensearch-project/common-utils/issues/730): Common-utils release notes tracking
- [Issue #958](https://github.com/opensearch-project/notifications/issues/958): Notifications release notes tracking

## Related Feature Report

- Full feature documentation
