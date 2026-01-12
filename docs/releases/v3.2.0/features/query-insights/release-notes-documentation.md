---
tags:
  - indexing
  - observability
  - performance
  - search
---

# Release Notes & Documentation

## Summary

This release item covers the automated release notes generation for the Query Insights plugin in OpenSearch v3.2.0. The release notes document enhancements, infrastructure updates, and maintenance changes included in this version.

## Details

### What's New in v3.2.0

The Query Insights plugin v3.2.0 release includes:

1. **Enhancements**: Increased reader search limit to 500 and fixed sort by metric type
2. **Infrastructure Updates**: Maven endpoint migration, Gradle and Java version bumps
3. **CI/CD Improvements**: Codecov configuration fixes

### Technical Changes

#### Enhancements

| Change | PR | Description | Related Issue |
|--------|-----|-------------|---------------|
| Reader Search Limit | [#381](https://github.com/opensearch-project/query-insights/pull/381) | Increase reader search limit from default to 500 and fix sort by metric type |   |

#### Infrastructure

| Change | PR | Description | Related Issue |
|--------|-----|-------------|---------------|
| Build System | [#392](https://github.com/opensearch-project/query-insights/pull/392) | Update Maven endpoint and bump Gradle/Java versions |   |
| Codecov Fix | [#393](https://github.com/opensearch-project/query-insights/pull/393) | Fix codecov configuration |   |
| Codecov v3 | [#394](https://github.com/opensearch-project/query-insights/pull/394) | Migrate to codecov v3 |   |

#### Maintenance

| Change | PR | Description | Related Issue |
|--------|-----|-------------|---------------|
| Version Increment | [#380](https://github.com/opensearch-project/query-insights/pull/380) | Increment version to 3.2.0-SNAPSHOT |   |
| Release Notes | [#395](https://github.com/opensearch-project/query-insights/pull/395) | Add release notes for 3.2.0 |   |

## Limitations

- This is a documentation-only release item
- No functional changes to the Query Insights plugin core functionality

## References

### Documentation
- [Query Insights Plugin Repository](https://github.com/opensearch-project/query-insights)
- [Release Notes 3.2.0](https://github.com/opensearch-project/query-insights/blob/main/release-notes/opensearch-query-insights.release-notes-3.2.0.0.md)

### Pull Requests
| PR | Description |
|----|-------------|
| [#380](https://github.com/opensearch-project/query-insights/pull/380) | Version increment to 3.2.0-SNAPSHOT |
| [#381](https://github.com/opensearch-project/query-insights/pull/381) | Increase reader search limit to 500 |
| [#392](https://github.com/opensearch-project/query-insights/pull/392) | Maven endpoint and build updates |
| [#393](https://github.com/opensearch-project/query-insights/pull/393) | Codecov fix |
| [#394](https://github.com/opensearch-project/query-insights/pull/394) | Codecov v3 migration |
| [#395](https://github.com/opensearch-project/query-insights/pull/395) | Release notes for 3.2.0 |

## Related Feature Report

- [Query Insights Feature Documentation](../../../../features/query-insights/query-insights.md)
