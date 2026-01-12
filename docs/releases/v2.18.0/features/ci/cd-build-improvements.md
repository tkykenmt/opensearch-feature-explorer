---
tags:
  - indexing
  - ml
  - observability
  - security
---

# CI/CD & Build Improvements

## Summary

OpenSearch v2.18.0 includes various CI/CD and build infrastructure improvements across multiple plugins. These changes focus on updating baseline JDK versions, fixing CI workflows, improving test security, and streamlining the backport process.

## Details

### What's New in v2.18.0

This release includes 12 PRs across 5 repositories addressing CI/CD and build infrastructure:

#### JDK Version Updates

- **index-management**: Updated baseline JDK version from JDK-17 to JDK-21 to align with OpenSearch core requirements

#### CI Workflow Fixes

- **notifications**: Fixed CI failures caused by Node 20 compatibility issues in GitHub Actions workflows
- **observability**: Added compile step before Cypress runs in CI to ensure proper build order

#### Security Improvements

- **ml-commons**: Removed API keys from integration test logs to prevent credential exposure in CI output

#### Backport Process Improvements

- **ml-commons**: Allowed backport PRs to skip approval requirements for faster release cycles
- **ml-commons**: Updated approval requirements to trigger correctly for opensearch-trigger-bot
- **ml-commons**: Unblocked integration test pipeline for release by removing obsolete tests

#### Dependency Security

- **observability**: Bumped lint-staged from 13.1.0 to 15.2.10 to address CVE vulnerabilities

#### Maintainer Updates

- **index-management**: Moved non-active maintainer to emeritus status
- **index-management**: Removed wildcard imports introduced in previous changes

### Technical Changes

#### Repository: index-management

| PR | Description |
|----|-------------|
| [#1276](https://github.com/opensearch-project/index-management/pull/1276) | Update baseline JDK to JDK-21 |
| [#1263](https://github.com/opensearch-project/index-management/pull/1263) | Move non-active maintainer to emeritus |
| [#1251](https://github.com/opensearch-project/index-management/pull/1251) | Remove wildcard imports |

#### Repository: ml-commons

| PR | Description |
|----|-------------|
| [#3112](https://github.com/opensearch-project/ml-commons/pull/3112) | Remove API keys from integration test logs |
| [#3132](https://github.com/opensearch-project/ml-commons/pull/3132) | Allow backport PRs to skip approval |
| [#3148](https://github.com/opensearch-project/ml-commons/pull/3148) | Update approval requirements for trigger bot |
| [#3159](https://github.com/opensearch-project/ml-commons/pull/3159) | Unblock integration test pipeline for release |

#### Repository: notifications

| PR | Description |
|----|-------------|
| [#965](https://github.com/opensearch-project/notifications/pull/965) | Fix CI workflows for Node 20 compatibility |

#### Repository: observability

| PR | Description |
|----|-------------|
| [#2138](https://github.com/opensearch-project/observability/pull/2138) | Bump lint-staged to 15.2.10 (CVE fix) |
| [#2187](https://github.com/opensearch-project/observability/pull/2187) | Add compile step before Cypress runs |

## Limitations

- These changes are infrastructure-focused and do not affect runtime behavior
- JDK-21 baseline requires users building from source to have JDK-21 installed

## References

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#1263](https://github.com/opensearch-project/index-management/pull/1263) | index-management | Move non-active maintainer to emeritus |
| [#1251](https://github.com/opensearch-project/index-management/pull/1251) | index-management | Remove wildcard imports |
| [#1276](https://github.com/opensearch-project/index-management/pull/1276) | index-management | Update baseline JDK to JDK-21 |
| [#3112](https://github.com/opensearch-project/ml-commons/pull/3112) | ml-commons | Remove API keys from integration test logs |
| [#3132](https://github.com/opensearch-project/ml-commons/pull/3132) | ml-commons | Allow backport PRs to skip approval |
| [#3148](https://github.com/opensearch-project/ml-commons/pull/3148) | ml-commons | Update approval requirements |
| [#3159](https://github.com/opensearch-project/ml-commons/pull/3159) | ml-commons | Unblock integration test pipeline |
| [#965](https://github.com/opensearch-project/notifications/pull/965) | notifications | Fix CI workflows |
| [#2138](https://github.com/opensearch-project/observability/pull/2138) | observability | CVE fix for lint-staged |
| [#2187](https://github.com/opensearch-project/observability/pull/2187) | observability | Add compile step before Cypress |

### Issues (Design / RFC)
- [ml-commons Issue #2915](https://github.com/opensearch-project/ml-commons/issues/2915): API keys in integration test logs

## Related Feature Report

- [Full feature documentation](../../../../features/ci/cd-build-improvements.md)
