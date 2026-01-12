---
tags:
  - dashboards
  - performance
  - search
  - security
---

# Query Workbench Dashboards

## Summary

OpenSearch 3.0.0 includes maintenance updates for the Query Workbench Dashboards plugin, focusing on dependency updates, CI/CD improvements, and bug fixes. These changes ensure compatibility with OpenSearch 3.0.0 and improve build stability.

## Details

### What's New in v3.0.0

This release focuses on infrastructure and dependency maintenance rather than new features:

- **Dependency Updates**: Updated multiple npm packages including `glob-parent`, `@babel/helpers`, `@babel/runtime` to address security vulnerabilities and compatibility issues
- **CI/CD Improvements**: Upgraded GitHub Actions cache to v4 and improved Cypress test stability
- **Build Fixes**: Removed `package-lock.json` to resolve dependency conflicts and updated `package.json` configurations
- **Test Improvements**: Enhanced Cypress tests for dynamic column validation

### Technical Changes

#### Dependency Updates (dashboards-query-workbench)

| PR | Change | Purpose |
|----|--------|---------|
| #126 | Updated package.json | General package updates |
| #130 | Upgrade actions/cache to v4 | CI workflow improvement |
| #133 | Delete package-lock.json | Resolve dependency conflicts |
| #134 | Updated glob-parent version | Security fix |
| #139 | Update @babel/helpers | Compatibility update |
| #148 | Update default time range to 1h | UX improvement |
| #156 | Update babel/runtime version | Compatibility update |
| #168 | Improved Cypress test for dynamic column | Test stability |

#### CI/CD Updates (query-workbench)

| PR | Change | Purpose |
|----|--------|---------|
| #463 | Remove cypress version | Use OpenSearch Dashboards version |
| #460 | Remove download JSON feature | Feature removal |
| #459 | Minor CI updates and workflow fixes | Build stability |
| #441 | Update yarn.lock for cross-spawn | Dependency update |
| #453 | Update CIs to install job-scheduler plugin | Test environment fix |

### Migration Notes

No migration steps required. These are maintenance updates that do not change the Query Workbench user interface or functionality.

## Limitations

- No new features introduced in this release
- Changes are primarily infrastructure and dependency updates

## References

### Documentation
- [Query Workbench Documentation](https://docs.opensearch.org/3.0/dashboards/query-workbench/)

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#126](https://github.com/opensearch-project/dashboards-query-workbench/pull/126) | dashboards-query-workbench | Updated package.json |
| [#130](https://github.com/opensearch-project/dashboards-query-workbench/pull/130) | dashboards-query-workbench | Upgrade actions/cache to v4 |
| [#133](https://github.com/opensearch-project/dashboards-query-workbench/pull/133) | dashboards-query-workbench | Delete package-lock.json |
| [#134](https://github.com/opensearch-project/dashboards-query-workbench/pull/134) | dashboards-query-workbench | Updated glob-parent version |
| [#139](https://github.com/opensearch-project/dashboards-query-workbench/pull/139) | dashboards-query-workbench | Update @babel/helpers |
| [#148](https://github.com/opensearch-project/dashboards-query-workbench/pull/148) | dashboards-query-workbench | Update default time range to 1h |
| [#156](https://github.com/opensearch-project/dashboards-query-workbench/pull/156) | dashboards-query-workbench | Update babel/runtime version |
| [#168](https://github.com/opensearch-project/dashboards-query-workbench/pull/168) | dashboards-query-workbench | Improved Cypress test for dynamic column |

### Issues (Design / RFC)
- [GitHub Issue #205](https://github.com/tkykenmt/opensearch-feature-explorer/issues/205): Tracking issue

## Related Feature Report

- [Full feature documentation](../../../../features/dashboards-query-workbench/query-workbench.md)
