---
tags:
  - dashboards
  - indexing
---

# Reporting Release Maintenance

## Summary

Standard release maintenance for the OpenSearch Reporting plugin for v3.1.0. This includes automated version increment to 3.1.0-SNAPSHOT and the addition of release notes documenting the changes in this version.

## Details

### What's New in v3.1.0

This release contains maintenance updates to prepare the Reporting plugin for the v3.1.0 release cycle:

1. **Version Increment**: Automated version bump from 3.0.0-beta1 to 3.1.0-SNAPSHOT
2. **Release Notes**: Added release notes documenting the v3.1.0.0 changes

### Technical Changes

#### Build Configuration Updates

| File | Change | Description |
|------|--------|-------------|
| `build.gradle` | Version update | `opensearch_version` changed from `3.0.0-beta1-SNAPSHOT` to `3.1.0-SNAPSHOT` |
| `build.gradle` | Qualifier removal | `buildVersionQualifier` changed from `beta1` to empty string |
| `.github/workflows/draft-release-notes-workflow.yml` | Version update | Draft release notes version changed from `3.0.0.0` to `3.1.0.0` |

#### Release Notes Content

The release notes file `release-notes/opensearch-reporting.release-notes-3.1.0.0.md` was added with:

- Compatibility statement: Compatible with OpenSearch 3.1.0
- Maintenance section listing the version increment PR

### Migration Notes

No migration required. This is a maintenance release with no breaking changes.

## Limitations

None specific to this release.

## References

### Documentation
- [Reporting Repository](https://github.com/opensearch-project/reporting): Export and automate PNG, PDF, and CSV reports in OpenSearch Dashboards

### Pull Requests
| PR | Description |
|----|-------------|
| [#1092](https://github.com/opensearch-project/reporting/pull/1092) | [AUTO] Increment version to 3.1.0-SNAPSHOT |
| [#1101](https://github.com/opensearch-project/reporting/pull/1101) | Adding release notes for 3.1.0 |

### Issues (Design / RFC)
- [Issue #1095](https://github.com/opensearch-project/reporting/issues/1095): [RELEASE] Release version 3.1.0

## Related Feature Report

- [Full feature documentation](../../../../features/reporting/release-maintenance.md)
