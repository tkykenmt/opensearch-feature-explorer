---
tags:
  - security-dashboards
---
# Security Dashboards Bug Fixes

## Summary

OpenSearch v2.19.0 includes two bug fixes for the Security Dashboards Plugin addressing issues with OpenID Connect login redirects and multi-tenancy default tenant selection.

## Details

### What's New in v2.19.0

#### OpenID Login Redirect URL Preservation

Fixed an issue where query parameters and URL fragments were lost during OpenID Connect authentication redirects.

**Problem**: When users accessed a shared dashboard link while not logged in, after successful OpenID authentication they were redirected to the default dashboards page instead of the original URL they requested.

**Solution**: The `generateNextUrl` method in `openid_auth.ts` now preserves the query string from the original request:

```typescript
private generateNextUrl(request: OpenSearchDashboardsRequest): string {
  let path = getRedirectUrl({
    request,
    basePath: this.coreSetup.http.basePath.serverBasePath,
    nextUrl: request.url.pathname || '/app/opensearch-dashboards',
  });
  if (request.url.search) {
    path += request.url.search;
  }
  return escape(path);
}
```

This also preserves the `security_tenant` parameter when multi-tenancy is enabled, ensuring users are redirected to the correct tenant after login.

#### Tenant Default Selection Fix

Fixed an issue where the default tenant was incorrectly determined based on the order of `opensearch_security.multitenancy.tenants.preferred` instead of the configured default tenant.

**Problem**: If `opensearch_security.multitenancy.tenants.preferred: ["Global", "Private"]` and the default tenant was set to `Private`, users would be logged into `Global` tenant instead.

**Solution**: Added case-insensitive matching for the `Private` tenant in `tenant_resolver.ts`:

```typescript
export const PRIVATE_TENANTS: string[] = [PRIVATE_TENANT_SYMBOL, 'private', 'Private'];
```

This ensures the tenant resolver correctly identifies the requested tenant regardless of case, allowing the default tenant setting to take precedence over the preferred tenants order.

### Technical Changes

| File | Change |
|------|--------|
| `server/auth/types/openid/openid_auth.ts` | Preserve query string in nextUrl during redirect |
| `server/auth/types/openid/routes.ts` | Change `redirectHash` schema from boolean to string |
| `server/multitenancy/tenant_resolver.ts` | Add `'Private'` to PRIVATE_TENANTS array |

## Limitations

- The OpenID redirect fix only applies to OpenID Connect authentication; SAML already had this functionality
- Tenant resolution fix is case-sensitive for custom tenant names (only affects built-in Private/Global tenants)

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#2140](https://github.com/opensearch-project/security-dashboards-plugin/pull/2140) | Preserve Query in nextUrl during openid login redirect | [#1823](https://github.com/opensearch-project/security-dashboards-plugin/issues/1823), [#2119](https://github.com/opensearch-project/security-dashboards-plugin/issues/2119) |
| [#2163](https://github.com/opensearch-project/security-dashboards-plugin/pull/2163) | Fix tenant defaulting incorrectly | [#2019](https://github.com/opensearch-project/security-dashboards-plugin/issues/2019) |

### Issues
| Issue | Description |
|-------|-------------|
| [#1823](https://github.com/opensearch-project/security-dashboards-plugin/issues/1823) | Auth redirect resets query in v2.12+ |
| [#2019](https://github.com/opensearch-project/security-dashboards-plugin/issues/2019) | Tenant defaulting incorrectly based on preferred tenants order |
| [#2119](https://github.com/opensearch-project/security-dashboards-plugin/issues/2119) | Related OpenID redirect issue |
