---
tags:
  - security-dashboards
---
# Security nextUrl Validation

## Summary

Enhanced the `nextUrl` parameter validation in OpenSearch Security Dashboards Plugin to incorporate the `serverBasePath`. This security enhancement ensures that all redirect URLs after authentication must be prefixed with the configured base path, preventing potential open redirect vulnerabilities.

## Details

### What's New in v2.16.0

The `validateNextUrl` function was updated to require that the `nextUrl` parameter starts with the configured `serverBasePath`. This change affects all authentication types:

- Basic authentication
- OpenID Connect (OIDC)
- SAML
- Proxy authentication

### Technical Changes

#### Updated Validation Logic

The validation function signature changed to accept the base path:

```typescript
// Before
export const validateNextUrl = (url: string | undefined): string | void

// After  
export function validateNextUrl(
  url: string | undefined,
  basePath: string | undefined
): string | void
```

#### New Validation Criteria

The updated validation checks:
1. `nextUrl` must start with the configured `basePath` (or `/` if no basePath is set)
2. If the path (minus basePath) is longer than 2 characters, the second character must be alphabetical or underscore
3. Following characters must be alphanumeric, dash, or underscore

```typescript
// server/utils/next_url.ts
const path = url.split(/\?|#/)[0];
const bp = basePath || '';
if (!path.startsWith(bp)) {
  return INVALID_NEXT_URL_PARAMETER_MESSAGE;
}
const pathMinusBase = path.replace(bp, '');
if (
  !pathMinusBase.startsWith('/') ||
  (pathMinusBase.length >= 2 && !/^\/[a-zA-Z_][\/a-zA-Z0-9-_]+$/.test(pathMinusBase))
) {
  return INVALID_NEXT_URL_PARAMETER_MESSAGE;
}
```

#### Files Modified

| File | Change |
|------|--------|
| `server/auth/types/basic/routes.ts` | Added validation with serverBasePath to login page route |
| `server/auth/types/openid/routes.ts` | Updated validation calls to include serverBasePath |
| `server/auth/types/proxy/routes.ts` | Updated validation calls to include serverBasePath |
| `server/auth/types/saml/routes.ts` | Updated validation calls to include serverBasePath |
| `server/utils/next_url.ts` | Enhanced validation logic with basePath support |
| `server/utils/next_url.test.ts` | Added tests for basePath validation |

### Security Improvements

This enhancement provides additional protection against:
- Open redirect attacks via manipulated `nextUrl` parameters
- URL injection attempts that bypass basePath configuration
- JavaScript protocol injection attempts

## Limitations

- The validation is stricter than before, which may affect custom integrations that relied on the previous behavior
- URLs with special characters in the path (beyond alphanumeric, dash, underscore) will be rejected

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#2048](https://github.com/opensearch-project/security-dashboards-plugin/pull/2048) | Update nextUrl validation to incorporate serverBasePath | - |
| [#2050](https://github.com/opensearch-project/security-dashboards-plugin/pull/2050) | Backport to 2.16 branch | - |
