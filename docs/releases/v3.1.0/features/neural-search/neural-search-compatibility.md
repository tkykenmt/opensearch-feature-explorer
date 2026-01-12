---
tags:
  - indexing
  - neural-search
  - search
---

# Neural Search Compatibility

## Summary

This release item updates the neural-search plugin for OpenSearch 3.0 beta compatibility. The change updates version qualifiers in the build configuration from `alpha1` to `beta1`, ensuring the plugin builds correctly against the OpenSearch 3.0 beta release.

## Details

### What's New in v3.1.0

This is a maintenance/infrastructure change that updates the neural-search plugin's build configuration to target OpenSearch 3.0 beta1 instead of alpha1.

### Technical Changes

#### Build Configuration Update

The `build.gradle` file was updated to change the version qualifiers:

```groovy
// Before
opensearch_version = System.getProperty("opensearch.version", "3.0.0-alpha1-SNAPSHOT")
buildVersionQualifier = System.getProperty("build.version_qualifier", "alpha1")

// After
opensearch_version = System.getProperty("opensearch.version", "3.0.0-beta1-SNAPSHOT")
buildVersionQualifier = System.getProperty("build.version_qualifier", "beta1")
```

#### Files Changed

| File | Changes |
|------|---------|
| `build.gradle` | Version qualifier update (alpha1 → beta1) |
| `CHANGELOG.md` | Added entry for this PR |

### Migration Notes

No migration required. This is a build infrastructure change that does not affect runtime behavior or APIs.

## Limitations

- This change is specific to the 3.0 beta release cycle
- No functional changes to neural search capabilities

## References

### Documentation
- [Neural Search Documentation](https://docs.opensearch.org/3.1/vector-search/ai-search/neural-sparse-search/): Official docs

### Pull Requests
| PR | Description |
|----|-------------|
| [#1245](https://github.com/opensearch-project/neural-search/pull/1245) | Update neural-search for OpenSearch 3.0 beta compatibility |

### Issues (Design / RFC)
- [Issue #225](https://github.com/opensearch-project/neural-search/issues/225): Release version 3.0.0
- [Issue #3747](https://github.com/opensearch-project/opensearch-build/issues/3747): Release version 3.0.0 (build)

## Related Feature Report

- [Full feature documentation](../../../../features/neural-search/neural-search-compatibility.md)
