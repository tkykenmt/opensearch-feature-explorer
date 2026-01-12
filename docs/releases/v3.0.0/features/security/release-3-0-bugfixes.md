---
tags:
  - security
---

# Security Plugin Bugfixes for Release 3.0

## Summary

OpenSearch 3.0.0 includes several important bugfixes for the Security plugin that address upgrade compatibility issues, authentication handling, and configuration management. These fixes ensure smooth upgrades from 2.x versions and improve support for OIDC authentication scenarios.

## Details

### What's New in v3.0.0

This release addresses critical bugs that affected users upgrading from OpenSearch 2.x to 3.0.0 and improves authentication handling for OIDC use cases.

### Technical Changes

#### Key Bugfixes

| PR | Title | Description |
|----|-------|-------------|
| [#5193](https://github.com/opensearch-project/security/pull/5193) | Assume default of v7 models if _meta portion is not present | Fixes upgrade failures from 2.19 to 3.0.0 when security YAML files lack `_meta` section |
| [#5175](https://github.com/opensearch-project/security/pull/5175) | Escape pipe character for injected users | Enables OIDC usernames containing pipe characters |
| [#5157](https://github.com/opensearch-project/security/pull/5157) | Fix version matcher string in demo config installer | Corrects version parsing for new security packages |

#### Upgrade Compatibility Fix (PR #5193)

The most significant bugfix addresses an upgrade blocker from OpenSearch 2.19 to 3.0.0-alpha1. When security YAML configuration files (like `whitelist.yml`) did not include a `_meta` portion with `config_version: 2`, the system incorrectly assumed v6 format models, causing startup failures.

**Error before fix:**
```
[ERROR] java.io.IOException: Config version 1 is not supported; config type: WHITELIST
```

**Solution:** The default assumption was changed from v6 to v7 models, leveraging the auto-conversion logic introduced in OpenSearch 2.18 that automatically converts v6 to v7 format.

#### OIDC Username Pipe Character Support (PR #5175)

Fixed an issue where OIDC providers sending usernames with pipe characters (e.g., `idp-provider|email@test.com|tenant-id|user-id`) would fail authentication with:

```
java.lang.IllegalStateException: Username cannot have '|' in the security plugin.
```

The fix properly escapes pipe characters in usernames, roles, and tenants when setting UserInfo in ThreadContext.

#### Demo Config Version Matcher Fix (PR #5157)

Fixed a bug in `Installer.java` where the version matcher incorrectly parsed package names. With new packages like `opensearch-security-client` and `opensearch-security-common`, the matcher would extract `common-3.0.0.0` instead of `3.0.0.0`.

### Migration Notes

When upgrading from OpenSearch 2.x to 3.0.0:

1. **No action required** for the v7 model default change - the fix handles this automatically
2. **OIDC users** with pipe characters in usernames will now work without configuration changes
3. **Demo installations** will correctly detect the security plugin version

## Limitations

- The pipe character escaping is applied at the ThreadContext level; downstream systems should handle escaped values appropriately
- Users with custom security configurations should verify compatibility after upgrade

## References

### Documentation
- [Documentation: Configuration APIs](https://docs.opensearch.org/3.0/api-reference/security/configuration/index/)
- [Documentation: Upgrade Perform API](https://docs.opensearch.org/3.0/api-reference/security/configuration/upgrade-perform/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#5193](https://github.com/opensearch-project/security/pull/5193) | Default to v7 models for security config |
| [#5175](https://github.com/opensearch-project/security/pull/5175) | Escape pipe character for injected users |
| [#5157](https://github.com/opensearch-project/security/pull/5157) | Fix version matcher in demo config installer |
| [#4753](https://github.com/opensearch-project/security/pull/4753) | Auto-convert security config models from v6 to v7 (2.18) |

### Issues (Design / RFC)
- [Issue #5191](https://github.com/opensearch-project/security/issues/5191): Upgrade OS from 2.19.0 to 3.0.0-alpha1 failure
- [Issue #2756](https://github.com/opensearch-project/security/issues/2756): Username cannot have '|' in the security plugin

## Related Feature Report

- [Full feature documentation](../../../../features/security/security-configuration.md)
