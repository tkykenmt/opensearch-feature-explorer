---
tags:
  - opensearch-dashboards
---
# Navigation Next

## Summary

Updates and bug fixes for the new left navigation system in OpenSearch Dashboards v2.16.0. Key changes include renaming the "Detect" category to "Configure" with adjusted ordering, CSS styling fixes in Dev Tools, workspace integration improvements, and navigation behavior enhancements when workspaces are enabled.

## Details

### What's New in v2.16.0

#### Category Updates
Updated navigation categories in `default_app_categories.ts`:
- Renamed "Detect" category to "Configure" for better clarity
- Adjusted category ordering: Configure now has order 2000 (previously Detect was 3000)
- Visualize and Report category order changed to 3000 (previously 2000)
- Added deprecation markers for legacy category names (`dashboardAndReport`, `detect`)

| Category | Old Order | New Order |
|----------|-----------|-----------|
| Configure (was Detect) | 3000 | 2000 |
| Visualize and Report | 2000 | 3000 |

#### Dev Tools Tab CSS Fix
Updated CSS for Dev Tools tabs to work correctly with the new left navigation. Removed `justify-content: space-between` styling that caused incorrect tab spacing when Workbench was moved to Dev Tools.

#### Navigation-Next Integration Fixes
Multiple fixes for the navigation-next feature branch integration:
- Always collapse the new left navigation on home page when workspace is enabled
- Fixed typos in use case descriptions
- Declared `advanced_settings`, `dev_tools`, `data_administration_landing`, `settings_and_setup_landing` pages as features not visible within workspace
- Removed unnecessary `flushLeft` styling in workspace picker
- Show overview page in workspace of type "all" and hide home

#### Global Navigation Redirect
When workspace is enabled, users are redirected to home in global context to prevent creating objects in global scope:
- Changed "back" button to "home" when user is in Settings and Setup / Data Administration nav groups
- Changed navGroup to dataAdministration when navigating to devTools

### Technical Changes

| Change | Description |
|--------|-------------|
| Category rename | "Detect" → "Configure" in default_app_categories.ts |
| Category ordering | Configure: 2000, Visualize and Report: 3000 |
| Dev Tools CSS | Removed `justify-content: space-between` from dev tools tab styling |
| Workspace visibility | Marked admin pages as not visible within workspace |
| Navigation collapse | Auto-collapse left nav on home when workspace enabled |
| Global redirect | Redirect users to home in global context with workspace enabled |

## Limitations

- These fixes are specific to the new navigation system (feature flag required)
- Workspace feature must be enabled for some fixes to take effect
- Legacy category names (`dashboardAndReport`, `detect`) are deprecated but still available for backward compatibility

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#7339](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7339) | Update category: rename Detect to Configure, adjust ordering | - |
| [#7328](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7328) | Update dev tools tab css for new left navigation | - |
| [#7356](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7356) | Fix navigation-next integration issues | - |
| [#7551](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7551) | Redirect user to home in global when workspace is enabled | - |
