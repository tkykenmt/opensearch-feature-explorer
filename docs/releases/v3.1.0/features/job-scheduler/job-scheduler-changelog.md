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
## [Unreleased 3.x]
### Added
### Changed
### Dependencies
### Deprecated
### Removed
### Fixed
### Security
```

#### Workflow Configuration

```yaml
name: "Changelog Verifier"
on:
  pull_request:
    types: [opened, edited, reopened]

jobs:
  verify-changelog:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: dangoslen/changelog-enforcer@v3
        with:
          skipLabels: "autocut, skip-changelog"
```

### Usage Example

When contributing to Job Scheduler, add an entry to the appropriate section in CHANGELOG.md:

```markdown
### Added
- Add new feature X ([#123](https://github.com/opensearch-project/job-scheduler/pull/123))

### Dependencies
- Bump dependency Y from 1.0 to 2.0 ([#124](https://github.com/opensearch-project/job-scheduler/pull/124))
```

PRs with `autocut` or `skip-changelog` labels bypass the changelog requirement.

### Benefits

- **Iterative release notes**: Changes are documented as they're merged, reducing release preparation overhead
- **Dependabot integration**: Dependabot can automatically update changelog entries when bumping the same dependency multiple times
- **Consistent format**: Enforced structure ensures uniform release notes across versions

## Limitations

- The workflow condition references `security-dashboards-plugin` repository instead of `job-scheduler` (copy-paste issue from template)
- PRs must include changelog entries unless labeled with `autocut` or `skip-changelog`

## Related PRs

| PR | Description |
|----|-------------|
| [#778](https://github.com/opensearch-project/job-scheduler/pull/778) | Add a CHANGELOG and changelog_verifier workflow |

## References

- [Issue #777](https://github.com/opensearch-project/job-scheduler/issues/777): Add a CHANGELOG to assemble release notes as PRs are merged
- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/): Changelog format specification
- [Geospatial PR #238](https://github.com/opensearch-project/geospatial/pull/238): Reference implementation in geospatial repo
- [OpenSearch PR #17262](https://github.com/opensearch-project/OpenSearch/pull/17262): Example of Dependabot changelog integration

## Related Feature Report

- [Full feature documentation](../../../../features/job-scheduler/job-scheduler.md)
