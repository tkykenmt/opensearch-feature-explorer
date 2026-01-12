---
tags:
  - dashboards
  - indexing
  - observability
  - search
  - security
---

# Security Dashboards Enhancements

## Summary

OpenSearch v3.2.0 introduces usability improvements to the Security Dashboards plugin's role management interface. These enhancements address long-standing issues where index permission panels displayed truncated information with no way to view the complete list, and where certain index-level permissions were missing from the UI selection options.

## Details

### What's New in v3.2.0

Two key improvements enhance the role management experience:

1. **Full Index Pattern Display**: The Index Permission panel in the Role View page now displays all index patterns, permissions, and anonymizations without truncation
2. **Missing Index Permissions Added**: Several commonly-used index permissions are now available in the index permissions dropdown

### Technical Changes

#### UI Component Changes

The `index-permission-panel.tsx` component was refactored to remove the row expansion pattern and display all values directly:

| Change | Before | After |
|--------|--------|-------|
| Index patterns display | Max 3 items with "..." | Full list displayed |
| Permissions display | Max 3 items, expandable | PermissionTree component inline |
| Anonymizations display | Max 3 items with "..." | Full list displayed |
| Row expansion arrow | Present | Removed |

#### New Index Permissions

The following permissions were added to `constants.tsx`:

```typescript
// Read permissions
'indices:data/read/mget*'
'indices:data/read/mtv*'

// Write permissions  
'indices:data/write/bulk*'
```

These permissions can now be selected when configuring index-level permissions through the Dashboards UI.

### Usage Example

When viewing a role with multiple index patterns, all patterns are now visible:

```
Role: data-analyst
Index Permissions:
├── Index: logs-*, metrics-*, traces-*, events-*, audit-*
│   Permissions: read, search
│   Field Level Security: timestamp, message, level
│   Anonymizations: user_id, ip_address
```

Previously, only the first 3 index patterns would be shown with no way to see the rest without editing the role.

### Migration Notes

No migration required. The changes are purely UI improvements that take effect immediately upon upgrading to v3.2.0.

## Limitations

- The full list display may result in longer page layouts for roles with many index patterns
- No pagination or virtual scrolling for very large permission lists

## References

### Documentation
- [Documentation: Defining users and roles](https://docs.opensearch.org/3.2/security/access-control/users-roles/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#2254](https://github.com/opensearch-project/security-dashboards-plugin/pull/2254) | Show all index patterns in index permission panel |
| [#2255](https://github.com/opensearch-project/security-dashboards-plugin/pull/2255) | Add missing index permissions to the list |

### Issues (Design / RFC)
- [Issue #1303](https://github.com/opensearch-project/security-dashboards-plugin/issues/1303): Index permissions view abbreviated with no way to expand
- [Issue #1969](https://github.com/opensearch-project/security-dashboards-plugin/issues/1969): Permissions not displayed in index permissions category
- [Issue #1891](https://github.com/opensearch-project/security-dashboards-plugin/issues/1891): Related truncation issue

## Related Feature Report

- [Full feature documentation](../../../../features/security-dashboards-plugin/security-dashboards-role-management.md)
