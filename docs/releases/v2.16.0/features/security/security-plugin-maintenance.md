---
tags:
  - security
---
# Security Plugin Maintenance

## Summary

OpenSearch v2.16.0 includes several maintenance updates to the Security plugin, including dependency cleanup, code quality improvements, Gradle updates, test framework modernization, and new permissions for Security Analytics threat intelligence.

## Details

### What's New in v2.16.0

#### Dependency Cleanup
- Removed unused Apache CXF dependency that was previously used for JWT implementation in the SAML flow
- Since v2.12, the JWT implementation changed from Apache CXF to Nimbus ([#3421](https://github.com/opensearch-project/security/pull/3421))
- This cleanup reduces the plugin's dependency footprint and potential security surface

#### Code Quality Improvements
- Removed unnecessary return statements throughout the codebase for cleaner code
- Replaced JUnit `assertEquals()` with Hamcrest `assertThat()` matchers for more expressive test assertions
- Resolves long-standing issues [#1832](https://github.com/opensearch-project/security/issues/1832) and [#3680](https://github.com/opensearch-project/security/issues/3680)

#### Build System Updates
- Updated Gradle from 8.7 to 8.8, then to 8.9
- Keeps the build system current with latest Gradle features and security patches

#### ML Roles Refactoring
- Refactored and updated existing ML (Machine Learning) roles
- Improves role definitions for ML-related operations

#### Security Analytics Integration
- Added new API action names for Security Analytics threat intelligence project
- Supports the threat intelligence feature in Security Analytics ([security-analytics#1117](https://github.com/opensearch-project/security-analytics/issues/1117))

### Technical Changes

| Change | Description | Impact |
|--------|-------------|--------|
| Apache CXF removal | Removed unused JWT library | Reduced dependencies |
| Return statement cleanup | Code style improvement | No functional change |
| Hamcrest matchers | Test framework modernization | Better test assertions |
| Gradle 8.8 → 8.9 | Build system update | Build improvements |
| ML roles update | Role definition changes | ML permission handling |
| Threat intel actions | New API permissions | Security Analytics support |

## Limitations

- These are maintenance changes with no user-facing feature changes
- ML role changes may affect existing ML-related permission configurations

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#4580](https://github.com/opensearch-project/security/pull/4580) | Remove unused dependency Apache CXF | - |
| [#4558](https://github.com/opensearch-project/security/pull/4558) | Remove unnecessary return statements | - |
| [#4544](https://github.com/opensearch-project/security/pull/4544) | Replace JUnit assertEquals() with Hamcrest assertThat() | [#1832](https://github.com/opensearch-project/security/issues/1832), [#3680](https://github.com/opensearch-project/security/issues/3680) |
| [#4553](https://github.com/opensearch-project/security/pull/4553) | Update Gradle to 8.9 | - |
| [#4459](https://github.com/opensearch-project/security/pull/4459) | Update to Gradle 8.8 | - |
| [#4151](https://github.com/opensearch-project/security/pull/4151) | Refactor and update existing ML roles | - |
| [#4498](https://github.com/opensearch-project/security/pull/4498) | Add security analytics threat intel action | [security-analytics#1117](https://github.com/opensearch-project/security-analytics/issues/1117) |
