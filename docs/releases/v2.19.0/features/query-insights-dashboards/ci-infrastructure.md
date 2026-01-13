---
tags:
  - query-insights-dashboards
---
# Query Insights Dashboards CI/Infrastructure Fixes

## Summary

This release includes foundational CI/CD and infrastructure improvements for the Query Insights Dashboards plugin. These changes establish the build pipeline, linting configuration, backport workflows, and 2.x branch support for the newly created dashboards repository.

## Details

### What's New in v2.19.0

The Query Insights Dashboards repository was bootstrapped with essential development infrastructure:

#### CI/CD Pipeline Setup
- Basic CI workflow for automated testing and builds
- GitHub Actions configuration for the 2.x release branch
- Backport workflow for automated cherry-picking to maintenance branches
- Post-build target in package.json for artifact renaming

#### Code Quality
- ESLint configuration with proper linting rules
- Fixed linting issues across the codebase

#### Security Integration
- Mend (WhiteSource) integration for vulnerability scanning
- Automated security issue creation for detected vulnerabilities

### Technical Changes

| Change | Description |
|--------|-------------|
| ESLint Setup | Configured `.eslintrc` with project-specific rules and fixed existing linting violations |
| CI Workflow | Added `.github/workflows/ci.yml` for automated testing on pull requests |
| 2.x Branch CI | Set up GitHub Actions specifically for the 2.x maintenance branch |
| Backport Workflow | Added `.github/workflows/backport.yml` for automated backporting with labels |
| Build Target | Added `postbuild` script in `package.json` to rename build artifacts |
| Mend Integration | Added `.whitesource` configuration for dependency vulnerability scanning |

## Limitations

- These are infrastructure-only changes with no user-facing functionality
- Query grouping dashboard changes included in PR #48 are primarily test additions

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1](https://github.com/opensearch-project/query-insights-dashboards/pull/1) | Configure Mend for GitHub.com | - |
| [#20](https://github.com/opensearch-project/query-insights-dashboards/pull/20) | Fix ESLint config and related linting issues | [#19](https://github.com/opensearch-project/query-insights-dashboards/issues/19) |
| [#23](https://github.com/opensearch-project/query-insights-dashboards/pull/23) | Add GitHub workflow for backport | [#19](https://github.com/opensearch-project/query-insights-dashboards/issues/19) |
| [#36](https://github.com/opensearch-project/query-insights-dashboards/pull/36) | Set up GitHub Actions for 2.x | - |
| [#48](https://github.com/opensearch-project/query-insights-dashboards/pull/48) | Add post build target | - |

### Query Insights Plugin PRs
| PR | Description |
|----|-------------|
| [#171](https://github.com/opensearch-project/query-insights/pull/171) | Fix 2.x GitHub checks |
| [#181](https://github.com/opensearch-project/query-insights/pull/181) | Fix GitHub CI by adding eclipse dependency in build.gradle |
