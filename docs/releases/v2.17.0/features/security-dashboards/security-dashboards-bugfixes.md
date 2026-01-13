---
tags:
  - domain/security
  - component/dashboards
  - dashboards
  - security
---
# Security Dashboards Bugfixes

## Summary

This release includes several bugfixes and UX improvements for the Security Dashboards plugin, focusing on the new left navigation feature. Key fixes address tenancy app visibility when disabled, basepath URL validation issues, and page header UX improvements.

## Details

### What's New in v2.17.0

Four bugfixes and enhancements were merged to improve the Security Dashboards plugin experience:

1. **Tenancy App Registration Fix**: The tenancy app is no longer registered when multitenancy is disabled in the configuration
2. **Basepath nextUrl Validation Fix**: Fixed URL validation to properly handle basepath-only nextUrl values
3. **Page Header UX Improvements**: Fixed spacing issues and added contextual breadcrumbs
4. **Navigation Titles and Descriptions**: Updated titles and added descriptions for better UX consistency

### Technical Changes

#### Tenancy App Registration (PR #2057)

When the new left navigation is enabled, security apps are registered individually. Previously, the tenancy app would appear even when `opensearch_security.multitenancy.enabled: false` was set.

```typescript
// Before: Tenancy always registered
core.application.register({
  id: PLUGIN_TENANTS_APP_ID,
  title: 'Tenants',
  ...
});

// After: Conditional registration
if (config.multitenancy.enabled) {
  core.application.register({
    id: PLUGIN_TENANTS_APP_ID,
    title: 'Tenants',
    ...
  });
}
```

#### Basepath nextUrl Validation (PR #2096)

Fixed a bug where basepath-only URLs (e.g., `/osd`) were incorrectly marked as invalid. The validation logic now properly handles cases where `nextUrl` equals the basepath without a trailing slash.

```typescript
// Before: Empty pathMinusBase caused validation failure
if (!pathMinusBase.startsWith('/') || ...)

// After: Handle empty pathMinusBase case
if ((pathMinusBase && !pathMinusBase.startsWith('/')) || ...)
```

#### Page Header UX Fixes (PR #2108)

- Removed extra spacing on the audit log page by moving `EuiSpacer` inside the fallback component
- Added role/user name to breadcrumbs on edit pages for better context

#### Navigation Titles and Descriptions (PR #2084)

Updated navigation items with clearer titles and added descriptions:

| App | Old Title | New Title | Description |
|-----|-----------|-----------|-------------|
| Get Started | Get Started | Get started with access control | - |
| Authentication | Authentication | Authentication and authorization | Set up authentication and authorization sequences |
| Roles | Roles | Roles | Create a set of permissions with specific privileges |
| Internal Users | Internal users | Internal users | Define users to control access to your data |
| Permissions | Permissions | Permissions | Controls access to individual actions and action groups |
| Audit Logs | Audit logs | Audit logs | Configure audit logging for system access activities |

### Files Changed

| PR | Files Modified |
|----|----------------|
| #2057 | `common/index.ts`, `public/plugin.ts`, `public/test/plugin.test.ts` |
| #2096 | `server/utils/next_url.ts`, `server/utils/next_url.test.ts` |
| #2108 | `public/apps/configuration/app-router.tsx`, `audit-logging.tsx`, `internal-user-edit.tsx`, `role-edit.tsx` |
| #2084 | `public/plugin.ts` |

## Limitations

- These fixes are specific to the new left navigation feature flag (`getNavGroupEnabled`)
- The tenancy app visibility fix only affects the new navigation; classic navigation behavior is unchanged

## References

### Documentation
- [Security Dashboards Plugin](https://github.com/opensearch-project/security-dashboards-plugin)

### Pull Requests
| PR | Description |
|----|-------------|
| [#2057](https://github.com/opensearch-project/security-dashboards-plugin/pull/2057) | Do not register tenancy app if disabled in yml |
| [#2096](https://github.com/opensearch-project/security-dashboards-plugin/pull/2096) | Fix basepath nextUrl validation |
| [#2108](https://github.com/opensearch-project/security-dashboards-plugin/pull/2108) | UX fixes for page header |
| [#2084](https://github.com/opensearch-project/security-dashboards-plugin/pull/2084) | Update titles and descriptions |

### Issues (Design / RFC)
- [Issue #2056](https://github.com/opensearch-project/security-dashboards-plugin/issues/2056): Tenant link not hidden when new navigation enabled
- [Issue #2097](https://github.com/opensearch-project/security-dashboards-plugin/issues/2097): invalidNextUrl when nextUrl is basePath

## Related Feature Report

- Full feature documentation
