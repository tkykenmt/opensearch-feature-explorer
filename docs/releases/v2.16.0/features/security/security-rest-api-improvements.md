---
tags:
  - security
---
# Security REST API Improvements

## Summary

OpenSearch v2.16.0 includes several improvements to the Security REST API, focusing on enhanced validation, test refactoring, and development workflow improvements. Key changes include PATCH API validation to prevent no-op updates, refactored REST API tests for better maintainability, and updated PR templates to ensure API changes are documented in the OpenAPI specification.

## Details

### What's New in v2.16.0

#### PATCH API Validation Enhancement

The PATCH API now validates whether incoming requests will actually modify the security configuration. If a PATCH request would result in no changes, the API responds with a message indicating no updates are required, avoiding unnecessary internal `TransportConfigUpdateAction` calls.

Example response when no changes are detected:
```json
{
  "status": "OK",
  "message": "No updates required"
}
```

#### REST API Test Refactoring

Several REST API test classes were refactored for improved maintainability and coverage:

| Original Test | Refactored Tests |
|---------------|------------------|
| `UserApiTest` | `InternalUsersRestApiIntegrationTest`, `InternalUsersRegExpPasswordRulesRestApiIntegrationTest`, `InternalUsersScoreBasedPasswordRulesRestApiIntegrationTest` |
| Role Mappings tests | `RoleMappingsRestApiIntegrationTest` |
| Tenants tests | `TenantsRestApiIntegrationTest` |
| Roles tests | `RolesRestApiIntegrationTest` |

#### Bug Fixes Included

- Added validation for security roles in PATCH operations (#4514)
- Fixed restricted characters in usernames - previously users could be created with restricted characters using URL encoding (#4513)
- Partial fixes for hidden security entities creation via REST API (#4166)

#### PR Template Update

The pull request template now includes a checkbox requiring contributors to document API changes in the OpenAPI specification, ensuring better API documentation consistency.

## Limitations

- The hidden security entities feature (#4166) received partial fixes; full implementation may require additional work in future releases.

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#4533](https://github.com/opensearch-project/security/pull/4533) | Update PR template for API spec changes | [opensearch-api-specification#387](https://github.com/opensearch-project/opensearch-api-specification/issues/387) |
| [#4530](https://github.com/opensearch-project/security/pull/4530) | PATCH API validation for no-op changes | [#4491](https://github.com/opensearch-project/security/issues/4491) |
| [#4481](https://github.com/opensearch-project/security/pull/4481) | Refactor InternalUsers REST API test | [#4166](https://github.com/opensearch-project/security/issues/4166), [#4514](https://github.com/opensearch-project/security/issues/4514), [#4513](https://github.com/opensearch-project/security/issues/4513) |
| [#4450](https://github.com/opensearch-project/security/pull/4450) | Refactor Role Mappings REST API test | [#4166](https://github.com/opensearch-project/security/issues/4166) |

### Issues

| Issue | Description |
|-------|-------------|
| [#4166](https://github.com/opensearch-project/security/issues/4166) | Add possibility to create hidden security entities via REST API |

### Documentation

- [Security REST API](https://docs.opensearch.org/2.16/security/access-control/api/)
