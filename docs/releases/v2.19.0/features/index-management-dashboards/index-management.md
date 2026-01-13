---
tags:
  - index-management-dashboards
---
# Index Management

## Summary

OpenSearch v2.19.0 includes bug fixes and performance improvements for the Index Management Dashboards plugin, focusing on snapshot management functionality. Key changes include using the Cat Snapshot API for improved repository page performance and fixes for snapshot restore and policy editing issues.

## Details

### What's New in v2.19.0

#### Performance Improvements

**Cat Snapshot API for Repository Page**
- Replaced Get Snapshot API with Cat Snapshot API for retrieving snapshot counts
- Cat Snapshot API uses minimal information from backend storage calls
- Significantly reduces load time when loading repository information with many snapshots

#### Bug Fixes

**Snapshot Restore Alias Handling**
- Fixed issue where snapshot restore always restored index aliases regardless of user selection
- The "Restore aliases" checkbox now correctly controls whether aliases are restored
- Default value for `include_aliases` parameter set to `true` per API documentation

**Snapshot Policy Schedule Editing**
- Fixed issue where users could not modify snapshot schedule time during policy editing
- Schedule times can now be successfully updated and saved

**Index Expression Display**
- Fixed problem where index expressions displayed as `[Object][Object]` instead of actual values
- Snapshot details page now properly shows index expressions as strings
- Snapshots now correctly include the specified indices

#### Maintenance

**Integration Test Improvements**
- Updated integration tests to use `adminClient` when searching system indexes
- Addresses test failures when running with Security plugin enabled
- Aligns with security changes in v2.18.0 that protect system indices

**Build Fixes**
- Fixed 2.x build issues related to update settings requests on read-only indices
- Addresses compatibility with OpenSearch core bug fix in PR #16568

**Dependency Updates**
- Updated Cypress version
- Fixed CVE-2024-21538 security vulnerability

## Limitations

- Cat Snapshot API performance improvement is most noticeable with repositories containing many snapshots
- Snapshot restore alias behavior change may affect existing automation scripts that relied on previous behavior

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1242](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1242) | Use Cat Snapshot API for repository snapshot count | Performance |
| [#1193](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1193) | Fix snapshot restore alias handling | Bug fix |
| [#1213](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1213) | Fix snapshot restore default alias value | Bug fix |
| [#1207](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1207) | Fix snapshot policy schedule editing and index expression display | [#947](https://github.com/opensearch-project/index-management-dashboards-plugin/issues/947) |
| [#1286](https://github.com/opensearch-project/index-management/pull/1286) | Use adminClient for system index searches in tests | [#1269](https://github.com/opensearch-project/index-management/issues/1269) |
| [#1315](https://github.com/opensearch-project/index-management/pull/1315) | Fix 2.x build for read-only index settings | [#1304](https://github.com/opensearch-project/index-management/issues/1304), [#1305](https://github.com/opensearch-project/index-management/issues/1305) |
