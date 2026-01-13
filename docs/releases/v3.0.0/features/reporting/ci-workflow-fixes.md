---
tags:
  - domain/infra
  - component/server
  - dashboards
---
# CI/Workflow Fixes

## Summary

This release item includes minor CI updates and workflow fixes for the dashboards-reporting plugin. The changes modernize GitHub Actions workflows by upgrading to newer action versions, consolidating duplicate build jobs, and fixing documentation links.

## Details

### What's New in v3.0.0

The PR introduces several maintenance improvements to the CI/CD infrastructure:

1. **GitHub Actions Version Upgrades**: Updated `actions/checkout` from v1/v2/v3 to v4 across all workflow files
2. **Build Job Consolidation**: Merged separate Windows and macOS build jobs into a single matrix-based job
3. **Documentation Fixes**: Corrected broken links in README and DEVELOPER_GUIDE
4. **Maintainer Updates**: Updated maintainer GitHub handle

### Technical Changes

#### Workflow Files Modified

| File | Changes |
|------|---------|
| `cypress-e2e-reporting-test.yml` | Upgraded checkout actions to v4, removed invalid filter parameter |
| `dashboards-reports-test-and-build-workflow.yml` | Consolidated Windows/macOS builds into matrix job, fixed path references |
| `ftr-e2e-reporting-test.yml` | Upgraded checkout actions to v4, removed invalid filter parameter |
| `link-checker.yml` | Upgraded checkout action to v4, formatting cleanup |
| `lint.yml` | Upgraded checkout actions to v4, formatting cleanup |
| `verify-binary-installation.yml` | Upgraded checkout action to v4 |

#### Build Job Consolidation

Before v3.0.0, Windows and macOS builds were separate jobs with duplicated configuration:

```yaml
# Before: Separate jobs
windows-build:
  runs-on: windows-latest
  steps: [...]

macos-build:
  runs-on: macos-latest
  steps: [...]
```

After v3.0.0, they are consolidated using a matrix strategy:

```yaml
# After: Matrix-based job
windows-mac-builds:
  runs-on: ${{ matrix.os }}
  strategy:
    matrix:
      os: [windows-latest, macos-latest]
  steps: [...]
```

#### Path Reference Fixes

Fixed incorrect path references in the build workflow:

| Setting | Before | After |
|---------|--------|-------|
| node-version-file | `'../OpenSearch-Dashboards/.nvmrc'` | `'OpenSearch-Dashboards/.nvmrc'` |
| yarn version path | `'../OpenSearch-Dashboards/package.json'` | `'./OpenSearch-Dashboards/package.json'` |
| bootstrap command | `yarn osd bootstrap` | `cd OpenSearch-Dashboards && yarn osd bootstrap` |

#### Documentation Fixes

| File | Fix |
|------|-----|
| `README.md` | Fixed cypress code link path |
| `README.md` | Removed outdated Notifications integration section |
| `DEVELOPER_GUIDE.md` | Fixed backport.yml link to use absolute URL |
| `MAINTAINERS.md` | Updated vamsi-amazon handle to vamsimanohar |

## Limitations

- These are infrastructure-only changes with no impact on plugin functionality
- The changes are specific to the dashboards-reporting repository CI/CD

## References

### Documentation
- [PR #548](https://github.com/opensearch-project/dashboards-reporting/pull/548): Main implementation
- [dashboards-reporting repository](https://github.com/opensearch-project/dashboards-reporting): Source repository

### Pull Requests
| PR | Description |
|----|-------------|
| [#548](https://github.com/opensearch-project/dashboards-reporting/pull/548) | Minor CI updates and workflow fixes |
| [#547](https://github.com/opensearch-project/dashboards-reporting/pull/547) | Related: Upgrade dashboards-reporting to node version 20 (closed, not merged) |

## Related Feature Report

- Full feature documentation
