---
tags:
  - indexing
  - ml
---

# Build/Test Infrastructure

## Summary

This bugfix updates the backward compatibility (BWC) test infrastructure in the custom-codecs plugin to align with OpenSearch v3.1.0. The change ensures BWC tests use the correct OpenSearch version dependency and includes the required Java agent plugin for compatibility with the SecurityManager replacement.

## Details

### What's New in v3.1.0

The BWC test configuration was updated to:
1. Update the default OpenSearch version from `3.0.0-alpha1-SNAPSHOT` to `3.1.0-SNAPSHOT`
2. Add the `opensearch.java-agent` plugin required for Java 21+ compatibility

### Technical Changes

#### Configuration Updates

| Setting | Before | After |
|---------|--------|-------|
| `opensearch_version` | `3.0.0-alpha1-SNAPSHOT` | `3.1.0-SNAPSHOT` |
| `opensearch.java-agent` plugin | Not applied | Applied |

#### Build Configuration

The `bwc-test/build.gradle` file was modified:

```groovy
apply plugin: 'opensearch.build'
apply plugin: 'opensearch.java-agent'  // Added for Java 21+ support
apply plugin: 'opensearch.rest-test'
apply plugin: 'java'
```

```groovy
buildscript {
    ext {
        opensearch_version = System.getProperty("opensearch.version", "3.1.0-SNAPSHOT")
        opensearch_group = "org.opensearch"
    }
}
```

### Migration Notes

No migration required. This is an internal build infrastructure change that does not affect plugin functionality or user-facing APIs.

## Limitations

- BWC tests require the appropriate plugin artifacts to be available in the `src/test/resources/` directory for the versions being tested

## References

### Documentation
- [PR #255](https://github.com/opensearch-project/custom-codecs/pull/255): Main implementation
- [custom-codecs repository](https://github.com/opensearch-project/custom-codecs): OpenSearch custom Lucene codecs plugin

### Pull Requests
| PR | Description |
|----|-------------|
| [#255](https://github.com/opensearch-project/custom-codecs/pull/255) | Fix version on bwc test dependency |
| [#256](https://github.com/opensearch-project/custom-codecs/pull/256) | Backport to 3.1 branch |

## Related Feature Report

- [Full feature documentation](../../../features/custom-codecs/custom-codecs.md)
