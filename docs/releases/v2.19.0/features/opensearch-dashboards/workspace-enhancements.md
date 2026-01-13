---
tags:
  - opensearch-dashboards
---
# Workspace Enhancements

## Summary

OpenSearch Dashboards v2.19.0 introduces several workspace enhancements focused on user experience improvements, including dismissible get started sections, optimized recent items handling, improved permission error handling, privacy level settings, and enhanced search functionality by category name.

## Details

### What's New in v2.19.0

#### Dismissible Get Started Section
Users can now dismiss the "Get Started" section on workspace overview pages (Search, Essential, and Analytics use cases). This provides a cleaner interface for experienced users who no longer need onboarding guidance.

#### Optimized Recent Items
- Internal users now emit app updaters, reducing extra requests for recent items
- Items from deleted workspaces are automatically filtered out from the recent items list
- Improved performance by eliminating unnecessary API calls

#### Improved Permission Error Handling
The `bulk_get` handler in the permission wrapper has been refactored to return responses with errors instead of throwing exceptions. This fixes index pattern fetch errors in the Discover dataset modal, providing a better user experience when accessing resources with permission restrictions.

#### Privacy Levels for Workspaces
New privacy settings allow workspace administrators to configure user permissions at multiple touchpoints:
- Workspace creation page
- Workspace details page
- Collaborators page

Additionally, collaborator input validation now prevents single `*` wildcard input for security purposes.

#### Category-Based Search for Dev Tools
Users can now search for Dev Tools applications by their category name. For example, searching "dev tools" will match all sub-applications under the Dev Tools category, making it easier to discover related functionality.

### Technical Changes

| Change | Description |
|--------|-------------|
| Get Started Dismissal | Added settings button to overview pages for dismissing get started cards |
| Recent Items Optimization | Updated internal users to emit app updaters; added workspace deletion filtering |
| Permission Wrapper Refactor | Changed `bulk_get` handler to return error responses instead of throwing |
| Privacy Settings | Added privacy level configuration to workspace create/details/collaborators pages |
| Category Search | Extended search functionality to match applications by category name |

## Limitations

- Privacy settings require the Security plugin to be properly configured
- Category search only works when workspace and new home page features are enabled
- Dismissed get started sections are stored per-user and cannot be reset through the UI

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#8874](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8874) | Support dismiss get started for search/essential/analytics overview page | |
| [#8900](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8900) | Optimize recent items and filter out items whose workspace is deleted | |
| [#8906](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8906) | Refactor bulk_get handler in permission wrapper when item has permission error | |
| [#8907](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8907) | Add privacy levels to the workspace | |
| [#8920](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8920) | Support search dev tools by its category name | |
