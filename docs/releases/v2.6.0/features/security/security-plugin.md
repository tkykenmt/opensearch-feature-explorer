---
tags:
  - security
---
# Security Plugin

## Summary

OpenSearch 2.6.0 introduces 1 new feature(s) and 5 enhancement(s) to Security Plugin, along with 10 bug fixes.

## Details

### New Features

- **GetIndexMappings index pattern support**: Added in PR #265.

### Enhancements

- **Add actions cluster:admin/component_template/* to cluster_manage_index_templates**
- **Publish snapshots to maven**
- **Integrate k-NN functionality with security plugin**
- **Add indices:admin/close* to list of permissible index permissions**
- **Synchronize all permissions from latest OpenSearch**

### Bug Fixes

- Fix issue with jwt as url param after getAdditionalAuthHeader switched to async
- Update URLs referencing old docs-beta site
- Fix plugin configuration path
- Fixed security tests.
- Fix Node.js and Yarn installation in CI
- Added untriaged issue workflow
- Updates toString calls affected by change in method signature
- Updates DlsFlsFilterLeafReader with Lucene change and fix broken deprecation logger test
- Add CODEOWNERS
- Switch to maven to download plugin

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#265](https://github.com/opensearch-project/security/pull/265) | GetIndexMappings index pattern support | security |
| [#2409](https://github.com/opensearch-project/security/pull/2409) | Add actions cluster:admin/component_template/* to cluster_manage_index_templates | security |
| [#2438](https://github.com/opensearch-project/security/pull/2438) | Publish snapshots to maven | security |
| [#2274](https://github.com/opensearch-project/k-NN/pull/2274) | Integrate k-NN functionality with security plugin | k-NN |
| [#1323](https://github.com/opensearch-project/security/pull/1323) | Add indices:admin/close* to list of permissible index permissions | security |
| [#1333](https://github.com/opensearch-project/security/pull/1333) | Synchronize all permissions from latest OpenSearch | security |
| [#1292](https://github.com/opensearch-project/security/pull/1292) | Fix issue with jwt as url param after getAdditionalAuthHeader switched to async | security |
| [#1231](https://github.com/opensearch-project/security/pull/1231) | Update URLs referencing old docs-beta site | security |
| [#1304](https://github.com/opensearch-project/security/pull/1304) | Fix plugin configuration path | security |
| [#484](https://github.com/opensearch-project/security/pull/484) | Fixed security tests. | security |
| [#446](https://github.com/opensearch-project/security/pull/446) | Fix Node.js and Yarn installation in CI | security |
| [#410](https://github.com/opensearch-project/security/pull/410) | Added untriaged issue workflow | security |
| [#2418](https://github.com/opensearch-project/security/pull/2418) | Updates toString calls affected by change in method signature | security |
| [#2429](https://github.com/opensearch-project/security/pull/2429) | Updates DlsFlsFilterLeafReader with Lucene change and fix broken deprecation logger test | security |
| [#2445](https://github.com/opensearch-project/security/pull/2445) | Add CODEOWNERS | security |
| [#1331](https://github.com/opensearch-project/security/pull/1331) | Switch to maven to download plugin | security |
