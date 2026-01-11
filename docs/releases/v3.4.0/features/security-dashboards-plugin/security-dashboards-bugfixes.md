# Security Dashboards Bugfixes

## Summary

This release fixes a bug in the Security Dashboards Plugin where blank backend roles could be inadvertently saved when creating or editing internal users. The fix filters out empty or whitespace-only backend role entries before submitting the user creation/update request.

## Details

### What's New in v3.4.0

A bug fix that prevents blank backend roles from being saved to internal users in the Security Dashboards Plugin.

### Technical Changes

#### Bug Fix: Filter Blank Backend Roles

When creating or editing an internal user through the Security Dashboards UI, users can add multiple backend roles. Previously, if a user left a backend role field empty or containing only whitespace, this blank value would be saved to the user's configuration.

The fix adds a filter to remove blank backend roles before the user update request is submitted:

```typescript
const updateObject: InternalUserUpdate = {
  backend_roles: backendRoles.filter((role) => role.trim() !== ''),
  attributes: unbuildAttributeState(validAttributes),
};
```

#### Changed Files

| File | Change |
|------|--------|
| `public/apps/configuration/panels/internal-user-edit/internal-user-edit.tsx` | Filter blank backend roles before creating/updating user |

### Impact

- Prevents invalid empty backend roles from being stored in user configurations
- Improves data quality for internal user management
- Consistent with existing validation for user attributes (which already filters empty keys)

## Limitations

- This fix only applies to the Dashboards UI; direct REST API calls to the security plugin can still create users with blank backend roles if not validated server-side

## Related PRs

| PR | Description |
|----|-------------|
| [#2330](https://github.com/opensearch-project/security-dashboards-plugin/pull/2330) | Filter blank backend role before creating internal user |

## References

- [PR #2330](https://github.com/opensearch-project/security-dashboards-plugin/pull/2330): Main implementation
- [Defining users and roles](https://docs.opensearch.org/3.0/security/access-control/users-roles/): OpenSearch Security documentation

## Related Feature Report

- [Full feature documentation](../../../../features/security-dashboards-plugin/security-dashboards-bugfixes.md)
