---
tags:
  - domain/security
  - component/server
  - security
---
# Security Plugin Bugfixes

## Summary

OpenSearch v2.17.0 includes 11 bugfixes and improvements for the Security plugin, addressing issues with demo certificates, authentication tokens, audit configuration, certificate hot-reload, terms aggregation permissions, and code quality improvements.

## Details

### What's New in v2.17.0

This release focuses on stability and reliability improvements across multiple Security plugin components.

### Technical Changes

#### Bug Fixes

| Issue | Fix | Impact |
|-------|-----|--------|
| Demo certificate validation | Fixed mismatching demo certificate hashes that prevented `plugins.security.allow_unsafe_democertificates` from working | Clusters can now boot with demo certificates when setting is enabled |
| Auth token endpoint | Fixed `generateAuthToken()` method in UserService to properly vend auth tokens for `internalusers` API | Auth token generation now works correctly |
| Audit config null handling | Added null check for audit configuration | Prevents NullPointerException when audit config is not set |
| Certificate SAN ordering | DNS names in SANs are now sorted before comparison during hot reload | Certificate hot reload works correctly with equivalent certificates having different SAN ordering |
| TermsAggregationEvaluator permissions | Fixed READ_ACTIONS to use actual action names instead of patterns | `indices:data/read/field_caps` privilege now works correctly |
| Certificates API timeout | Fixed `timeout` parameter not working as expected | Timeout parameter now functions correctly |

#### Refactoring and Code Quality

| Change | Description |
|--------|-------------|
| Security provider instantiation | Refactored BouncyCastleProvider initialization to support potential FIPS-compatible providers |
| Log4j utility removal | Removed usages of `org.apache.logging.log4j.util.Strings` for better compatibility |
| PluginSubject build fix | Interim fix for PluginSubject related changes to maintain build compatibility |

#### Infrastructure Fixes

| Change | Description |
|--------|-------------|
| Coverage report workflow | Fixed coverage-report workflow |
| Backport handling | Backported PRs with `backport-failed` labels that weren't acted upon |
| PR template update | Updated backport section of PR template |

### Configuration Changes

| Setting | Description | Status |
|---------|-------------|--------|
| `plugins.security.allow_unsafe_democertificates` | Allows cluster to start with demo certificates | Fixed in v2.17.0 |

### Usage Example

```yaml
# opensearch.yml - Demo certificate setting now works correctly
plugins.security.allow_unsafe_democertificates: true
```

## Limitations

- Demo certificates should only be used for development/testing environments
- The `allow_unsafe_democertificates` setting is not recommended for production use

## References

### Pull Requests
| PR | Description |
|----|-------------|
| [#4603](https://github.com/opensearch-project/security/pull/4603) | Fix demo certificate hash validation |
| [#4631](https://github.com/opensearch-project/security/pull/4631) | Fix authtoken endpoint |
| [#4664](https://github.com/opensearch-project/security/pull/4664) | Handle null audit config |
| [#4640](https://github.com/opensearch-project/security/pull/4640) | Sort DNS names in SANs |
| [#4607](https://github.com/opensearch-project/security/pull/4607) | Fix TermsAggregationEvaluator READ_ACTIONS |
| [#4611](https://github.com/opensearch-project/security/pull/4611) | Refactor security provider instantiation |
| [#4653](https://github.com/opensearch-project/security/pull/4653) | Remove Log4j Strings utility usage |
| [#4694](https://github.com/opensearch-project/security/pull/4694) | PluginSubject build fix |
| [#4684](https://github.com/opensearch-project/security/pull/4684) | Fix coverage-report workflow |
| [#4610](https://github.com/opensearch-project/security/pull/4610) | Backport failed PRs |
| [#4625](https://github.com/opensearch-project/security/pull/4625) | Update PR template backport section |

### Issues (Design / RFC)
- [Issue #4599](https://github.com/opensearch-project/security/issues/4599): Demo certificate setting bug
- [Issue #4627](https://github.com/opensearch-project/security/issues/4627): Auth token endpoint issue
- [Issue #4480](https://github.com/opensearch-project/security/issues/4480): Certificate SAN ordering issue
- [Issue #4583](https://github.com/opensearch-project/security/issues/4583): Security provider refactoring
- [Issue #3870](https://github.com/opensearch-project/security/issues/3870): Terms aggregation permissions

## Related Feature Report

- Security Plugin
