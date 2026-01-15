---
tags:
  - opensearch-dashboards
---
# UI Improvements

## Summary

OpenSearch Dashboards v2.16.0 introduces several UI improvements including accessibility enhancements, navigation group interfaces, application description fields, and button styling consistency.

## Details

### What's New in v2.16.0

#### Accessibility Improvements
Added missing `aria-label` attributes to the Discover page to improve screen reader support and WCAG compliance (1.1.1 Non-text Content Level A).

#### Navigation Group Interface
Introduced new interfaces in the Chrome service for organizing applications and categories into groups:
- `addNavToGroup`: Register features into specific groups
- `getGroupsMap$`: Observable to retrieve registered groups

This foundational change enables plugins to organize their features within logical groups, supporting the new navigation experience.

#### Application Description Field
Added a `description` field to the App interface, allowing plugins to provide descriptions for their features. This supports the new overview page where feature descriptions are displayed.

```typescript
// Example: Registering an app with description
core.application.register({
  id: 'myPlugin',
  title: 'My Plugin',
  description: 'Description shown in overview page',
  // ...
});
```

#### Button Styling Consistency
Addressed styling inconsistencies for non-primary buttons by changing them to secondary or empty buttons:
- Discover Open Flyout button → secondary
- Dashboard Embed Code button → secondary
- Dashboard Permalinks button → secondary
- Dashboard controls visual button → secondary
- Visualize Control Builder button → secondary

## Limitations

- Navigation group interfaces are foundational and require additional PRs to fully implement the new navigation experience
- Application description field requires plugins to update their registrations to provide descriptions

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#6898](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6898) | Add missing aria-label for discover page | [#6897](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/6897) |
| [#7060](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7060) | Introduce new interface for group | [#7061](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/7061) |
| [#7152](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7152) | Add description field in App | |
| [#7211](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7211) | Address styling of non-primary buttons by making secondary/empty | |
