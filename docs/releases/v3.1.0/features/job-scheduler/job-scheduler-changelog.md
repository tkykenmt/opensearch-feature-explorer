---
tags:
  - domain/data
  - component/server
  - dashboards
  - indexing
  - neural-search
  - security
---
# Job Scheduler Changelog

## Summary

This release adds a CHANGELOG file and changelog_verifier GitHub Actions workflow to the Job Scheduler plugin. This enables iterative release note assembly as PRs are merged and integrates with Dependabot for automatic changelog entry updates when dependencies are bumped.

## Details

### What's New in v3.1.0

The Job Scheduler plugin now includes:

1. **CHANGELOG file**: A structured changelog following the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format
2. **Changelog Verifier workflow**: A GitHub Actions workflow that enforces changelog updates on every pull request

### Technical Changes

#### New Files

| File | Description |
|------|-------------|
| `CHANGELOG.md` | Structured changelog with sections for Added, Changed, Dependencies, Deprecated, Removed, Fixed, and Security |
| `.github/workflows/changelog_verifier.yml` | GitHub Actions workflow using `dangoslen/changelog-enforcer@v3` |

#### Changelog Structure

The CHANGELOG follows semantic versioning and includes these sections:

```markdown

## Limitations

- The workflow condition references `security-dashboards-plugin` repository instead of `job-scheduler` (copy-paste issue from template)
- PRs must include changelog entries unless labeled with `autocut` or `skip-changelog`

## References

### Documentation
- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/): Changelog format specification
- [Geospatial PR #238](https://github.com/opensearch-project/geospatial/pull/238): Reference implementation in geospatial repo
- [OpenSearch PR #17262](https://github.com/opensearch-project/OpenSearch/pull/17262): Example of Dependabot changelog integration

### Pull Requests
| PR | Description |
|----|-------------|
| [#778](https://github.com/opensearch-project/job-scheduler/pull/778) | Add a CHANGELOG and changelog_verifier workflow |

### Issues (Design / RFC)
- [Issue #777](https://github.com/opensearch-project/job-scheduler/issues/777): Add a CHANGELOG to assemble release notes as PRs are merged

## Related Feature Report

- [Full feature documentation](../../../../features/job-scheduler/job-scheduler.md)
