---
tags:
  - security
---
# Security Build & Test Improvements

## Summary

OpenSearch Security plugin v2.16.0 includes build infrastructure improvements and test stability fixes. Key changes include custom Cypress build scripts for the Security Dashboards plugin to handle version compatibility, removal of opensearch-build repository dependencies, and fixes for flaky integration tests.

## Details

### What's New in v2.16.0

#### Build Infrastructure Improvements (Security Dashboards Plugin)

Two PRs addressed build issues in the Security Dashboards plugin:

1. **Custom Cypress Build Script** ([#2027](https://github.com/opensearch-project/security-dashboards-plugin/pull/2027)): Added a custom `build.sh` script to support different Cypress versions from OpenSearch Dashboards core. This resolves build failures caused by Cypress version mismatches between the plugin and core.

2. **Removed opensearch-build Dependency** ([#2033](https://github.com/opensearch-project/security-dashboards-plugin/pull/2033)): Cleaned up the custom build script to remove dependencies on the opensearch-build repository libs, making the build process more self-contained.

#### Test Stability Fixes (Security Plugin)

Three PRs improved test reliability:

1. **Flaky Integration Tests Fix** ([#4452](https://github.com/opensearch-project/security/pull/4452)): Fixed `AbstractDefaultConfigurationTests` which used `configurationFolder` as a constant. All inherited tests shared the same config folder, causing unpredictable cleanup behavior and test failures.

2. **FlsAndFieldMaskingTests Fix** ([#4548](https://github.com/opensearch-project/security/pull/4548)): Fixed test failures in `flsWithIncludesRulesIncludesFieldMappersFromPlugins` and `testFlsOnAClosedAndReopenedIndex`. Both tests created identical test users via REST API, but the second test received HTTP 200 instead of 201 because the user already existed. The fix moved user creation to global test setup.

3. **securityadmin.sh Typo Fix** ([#4526](https://github.com/opensearch-project/security/pull/4526)): Corrected a typo in the securityadmin.sh hint message, changing `-cl` to `-cn` (cluster name parameter).

### Technical Changes

| Change | Component | Impact |
|--------|-----------|--------|
| Custom build.sh for Cypress | security-dashboards-plugin | Enables independent Cypress version management |
| Remove opensearch-build deps | security-dashboards-plugin | Simplifies build process |
| Fix configurationFolder sharing | security plugin tests | Eliminates flaky test failures |
| Fix FLS test user creation | security plugin tests | Prevents HTTP status code mismatches |
| Fix securityadmin.sh hint | security plugin | Corrects CLI help message |

## Limitations

- The custom build script is specific to the Security Dashboards plugin and may need updates when Cypress versions change significantly
- Test fixes are internal improvements with no user-facing impact

## References

### Pull Requests
| PR | Repository | Description | Related Issue |
|----|------------|-------------|---------------|
| [#2027](https://github.com/opensearch-project/security-dashboards-plugin/pull/2027) | security-dashboards-plugin | Add custom build script for Cypress version support | [#1786](https://github.com/opensearch-project/security-dashboards-plugin/issues/1786) |
| [#2033](https://github.com/opensearch-project/security-dashboards-plugin/pull/2033) | security-dashboards-plugin | Remove opensearch-build repo dependency | [#2030](https://github.com/opensearch-project/security-dashboards-plugin/issues/2030) |
| [#4452](https://github.com/opensearch-project/security/pull/4452) | security | Fix flaky integration tests |  |
| [#4526](https://github.com/opensearch-project/security/pull/4526) | security | Fix typo in securityadmin.sh hint | [#4376](https://github.com/opensearch-project/security/issues/4376) |
| [#4548](https://github.com/opensearch-project/security/pull/4548) | security | Fix FlsAndFieldMaskingTests failures |  |
