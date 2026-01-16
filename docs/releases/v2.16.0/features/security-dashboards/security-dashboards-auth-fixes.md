---
tags:
  - security-dashboards
---
# Security Dashboards Auth Fixes

## Summary

OpenSearch v2.16.0 includes two bug fixes for the Security Dashboards Plugin addressing authentication and URL handling issues: fixing the capabilities API to support carrying authentication information, and resolving a URL duplication issue when navigating to the security plugin.

## Details

### What's New in v2.16.0

#### Capabilities API Authentication Support

The capabilities API (`/api/core/capabilities`) was previously excluded from authentication handling, which prevented plugins from accessing user authentication information when using `core.capabilities.registerSwitcher`. This fix introduces optional authentication for the capabilities endpoint.

**Technical Changes:**
- Moved `/api/core/capabilities` from `ROUTES_TO_IGNORE` to new `ROUTES_AUTH_OPTIONAL` list
- Added `authOptional()` method to check if a route allows optional authentication
- When authentication is optional and credentials are provided, the auth info is now included in the request state

```typescript
// Before: Capabilities API was completely ignored
protected static readonly ROUTES_TO_IGNORE: string[] = [
  '/api/core/capabilities', // FIXME: need to figure out how to bypass this API call
  '/app/login',
];

// After: Capabilities API allows optional authentication
protected static readonly ROUTES_TO_IGNORE: string[] = ['/app/login'];
protected static readonly ROUTES_AUTH_OPTIONAL: string[] = ['/api/core/capabilities'];
```

**Files Changed:**
- `server/auth/types/authentication_type.ts`: Added `ROUTES_AUTH_OPTIONAL` and `authOptional()` method
- `server/auth/types/authentication_type.test.ts`: Added test coverage for capabilities API auth info

#### URL Duplication Fix

Fixed a bug where navigating to the Security Dashboards Plugin would cause the URL fragment to appear twice (e.g., `/app/security-dashboards-plugin#/app/security-dashboards-plugin/getstarted` instead of `/app/security-dashboards-plugin#/getstarted`).

**Root Cause:**
The `HashRouter` component was incorrectly configured with `basename={props.params.appBasePath}`, which caused the base path to be duplicated in the URL hash.

**Fix:**
Removed the `basename` prop from the `HashRouter` component.

```typescript
// Before
<Router basename={props.params.appBasePath}>

// After
<Router>
```

**Files Changed:**
- `public/apps/configuration/app-router.tsx`: Removed basename prop from HashRouter

## Limitations

- The capabilities API authentication is optional - unauthenticated requests will still succeed but without auth info in the state
- These fixes are specific to the Security Dashboards Plugin and do not affect the core Security Plugin

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#2014](https://github.com/opensearch-project/security-dashboards-plugin/pull/2014) | Fix the bug of capabilities request not supporting carrying authinfo | - |
| [#2004](https://github.com/opensearch-project/security-dashboards-plugin/pull/2004) | Fix URL duplication issue | [#1967](https://github.com/opensearch-project/security-dashboards-plugin/issues/1967) |

### Issues
- [#1967](https://github.com/opensearch-project/security-dashboards-plugin/issues/1967): Duplicate URL fragment when clicking on security plugin
