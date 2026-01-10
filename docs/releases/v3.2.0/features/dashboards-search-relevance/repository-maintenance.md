# Repository Maintenance

## Summary

This release item covers repository maintenance activities for the dashboards-search-relevance and security plugins in OpenSearch v3.2.0. The changes include maintainer updates, addition of issue templates, codecov integration for test coverage reporting, and GitHub Actions dependency bumps to improve CI/CD infrastructure.

## Details

### What's New in v3.2.0

#### Maintainer Updates (dashboards-search-relevance)

The dashboards-search-relevance repository received significant maintainer updates to ensure continued project health:

- Added @fen-qin and @epugh as new maintainers to recognize their contributions
- Updated maintainer list by moving inactive maintainers to Emeritus status
- New maintainer team committed to addressing open issues, adding features, and keeping the project active

#### Issue Templates and Test Coverage (dashboards-search-relevance)

As part of "Operation Enhancement":
- Added standardized issue templates for better issue tracking
- Integrated codecov for test coverage reporting
- Bumped binary OpenSearch version to 3.2

#### GitHub Actions Dependency Bumps (security)

Updated GitHub Actions dependencies to newer versions for improved security and functionality:

| Action | Previous Version | New Version |
|--------|------------------|-------------|
| `actions/checkout` | 2 | 4 |
| `codecov/codecov-action` | 4 | 5 |
| `actions/github-script` | 6 | 7 |
| `tibdex/github-app-token` | 1.5.0 | 2.1.0 |
| `stefanzweifel/git-auto-commit-action` | 5 | 6 |
| `derek-ho/start-opensearch` | 6 | 7 |
| `SvanBoxel/delete-merged-branch` | (older) | (newer) |

### Technical Changes

#### New Components

| Component | Description |
|-----------|-------------|
| Issue Templates | Standardized templates for bug reports and feature requests |
| Codecov Integration | Automated test coverage reporting in CI pipeline |

#### CI/CD Improvements

The GitHub Actions updates provide:
- Better security through updated action versions
- Improved compatibility with newer GitHub features
- More reliable CI/CD workflows

## Limitations

- These are infrastructure/maintenance changes with no user-facing feature impact
- GitHub Actions updates may require workflow file adjustments in forks

## Related PRs

| PR | Repository | Description |
|----|------------|-------------|
| [#569](https://github.com/opensearch-project/dashboards-search-relevance/pull/569) | dashboards-search-relevance | Adding @fen-qin and @epugh as maintainers |
| [#576](https://github.com/opensearch-project/dashboards-search-relevance/pull/576) | dashboards-search-relevance | Update maintainers list |
| [#601](https://github.com/opensearch-project/dashboards-search-relevance/pull/601) | dashboards-search-relevance | Add issue template and codecov |
| [#201](https://github.com/opensearch-project/dashboards-search-relevance/pull/201) | dashboards-search-relevance | Adding template for feature technical design |
| [#2260](https://github.com/opensearch-project/security/pull/2260) | security | Bump actions/checkout from 2 to 4 |
| [#2263](https://github.com/opensearch-project/security/pull/2263) | security | Bump codecov/codecov-action from 4 to 5 |
| [#2259](https://github.com/opensearch-project/security/pull/2259) | security | Bump actions/github-script from 6 to 7 |
| [#2262](https://github.com/opensearch-project/security/pull/2262) | security | Bump tibdex/github-app-token from 1.5.0 to 2.1.0 |
| [#2265](https://github.com/opensearch-project/security/pull/2265) | security | Bump SvanBoxel/delete-merged-branch |
| [#2267](https://github.com/opensearch-project/security/pull/2267) | security | Bump derek-ho/start-opensearch from 6 to 7 |
| [#2268](https://github.com/opensearch-project/security/pull/2268) | security | Bump stefanzweifel/git-auto-commit-action from 5 to 6 |

## References

- [Issue #562](https://github.com/opensearch-project/dashboards-search-relevance/issues/562): Request for issue templates and codecov

## Related Feature Report

- [Full feature documentation](../../../features/dashboards-search-relevance/repository-maintenance.md)
