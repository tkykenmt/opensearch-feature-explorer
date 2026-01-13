---
tags:
  - domain/search
  - component/server
  - indexing
  - search
  - security
---
# Asynchronous Search GA Release Preparation

## Summary

This release item covers the version increment and release preparation for the asynchronous-search plugin for OpenSearch 3.0.0 GA. The changes are maintenance-focused, updating the plugin version from `3.0.0-beta1-SNAPSHOT` to `3.0.0-SNAPSHOT` to align with the OpenSearch 3.0.0 GA release.

## Details

### What's New in v3.0.0

The asynchronous-search plugin for v3.0.0 includes:

- **Version alignment**: Updated plugin version to match OpenSearch 3.0.0 GA release
- **JDK 21 baseline**: The plugin now requires JDK 21 as the minimum Java version (set in earlier 3.0 preparation)
- **Gradle 8.10.2**: Build system updated to use Gradle 8.10.2
- **JDK 23 support**: Added support for building with JDK 23

### Technical Changes

#### Build Configuration

| Setting | Previous Value | New Value |
|---------|----------------|-----------|
| `opensearch_version` | `3.0.0-beta1-SNAPSHOT` | `3.0.0-SNAPSHOT` |

#### Compatibility

The asynchronous-search plugin maintains full compatibility with OpenSearch 3.0.0 and continues to provide the same functionality:

- Background search execution for long-running queries
- Partial results retrieval during search execution
- Search result persistence for later examination
- Stats monitoring for asynchronous searches

### No Feature Changes

This release item contains no new features or API changes. The asynchronous-search plugin functionality remains unchanged from previous versions.

## Limitations

- No new features introduced in this release
- This is a maintenance release for GA version alignment

## References

### Documentation
- [Asynchronous Search Documentation](https://docs.opensearch.org/3.0/search-plugins/async/index/)
- [Asynchronous Search Security](https://docs.opensearch.org/3.0/search-plugins/async/security/)
- [Asynchronous Search Settings](https://docs.opensearch.org/3.0/search-plugins/async/settings/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#724](https://github.com/opensearch-project/asynchronous-search/pull/724) | Increment version to 3.0.0-SNAPSHOT |
| [#714](https://github.com/opensearch-project/asynchronous-search/pull/714) | Add 3.0.0.0-alpha1 release notes |
| [#698](https://github.com/opensearch-project/asynchronous-search/pull/698) | Update main branch for 3.0.0.0-alpha1 / gradle 8.10.2 / JDK23 |
| [#582](https://github.com/opensearch-project/asynchronous-search/pull/582) | Set JDK21 as the baseline for the 3.0 major version |

### Issues (Design / RFC)
- [Issue #318](https://github.com/opensearch-project/asynchronous-search/issues/318): 3.0.0 release tracking

## Related Feature Report

- [Full feature documentation](../../../features/asynchronous-search/asynchronous-search.md)
