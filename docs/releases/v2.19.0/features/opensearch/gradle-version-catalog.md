---
tags:
  - opensearch
---
# Gradle Version Catalog

## Summary

OpenSearch v2.19.0 expands the Gradle version catalog (`gradle/libs.versions.toml`) by adding `[libraries]` and `[bundles]` sections for server dependencies. This enables Dependabot to perform automated dependency upgrades and simplifies dependency management across the project.

## Details

### What's New in v2.19.0

This PR migrates dependencies from `server/build.gradle` to the centralized Gradle version catalog, building on the initial version catalog work from PR #16284.

### Technical Changes

#### Version Catalog Structure

The `gradle/libs.versions.toml` file now includes three sections:

| Section | Purpose |
|---------|---------|
| `[versions]` | Centralized version definitions |
| `[libraries]` | Library dependency declarations |
| `[bundles]` | Grouped dependencies for common use cases |

#### New Library Definitions

Added library entries for core server dependencies:

- **Lucene libraries**: `lucene-core`, `lucene-analysis-common`, `lucene-backward-codecs`, `lucene-grouping`, `lucene-highlighter`, `lucene-join`, `lucene-memory`, `lucene-misc`, `lucene-queries`, `lucene-queryparser`, `lucene-sandbox`, `lucene-spatial-extras`, `lucene-spatial3d`, `lucene-suggest`
- **Logging**: `log4japi`, `log4jjul`, `log4jcore`
- **Utilities**: `jodatime`, `tdigest`, `hdrhistogram`, `jna`, `jzlib`, `roaringbitmap`
- **Spatial**: `spatial4j`, `jtscore`
- **Reactive**: `reactorcore`, `reactivestreams`
- **Serialization**: `protobuf`, `jakartaannotation`

#### Lucene Bundle

A new `lucene` bundle groups all Lucene dependencies:

```toml
[bundles]
lucene = [
    "lucene-core",
    "lucene-analysis-common",
    "lucene-backward-codecs",
    "lucene-grouping",
    "lucene-highlighter",
    "lucene-join",
    "lucene-memory",
    "lucene-misc",
    "lucene-queries",
    "lucene-queryparser",
    "lucene-sandbox",
    "lucene-spatial-extras",
    "lucene-spatial3d",
    "lucene-suggest"
]
```

#### Build.gradle Migration

Dependencies in `server/build.gradle` now use catalog references:

```groovy
// Before
api "org.apache.lucene:lucene-core:${versions.lucene}"
api "joda-time:joda-time:${versions.joda}"

// After
api libs.bundles.lucene
api libs.jodatime
```

### Benefits

1. **Automated Dependency Updates**: Dependabot can now create PRs for dependency upgrades
2. **Centralized Version Management**: Single source of truth for dependency versions
3. **Simplified Build Files**: Cleaner `build.gradle` files using catalog references
4. **Bundle Support**: Group related dependencies for easier management

## Limitations

- This PR covers `server/build.gradle` dependencies only; other modules may still use traditional dependency declarations
- Plugins and other subprojects may need separate migration efforts

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16707](https://github.com/opensearch-project/OpenSearch/pull/16707) | Make entries for dependencies from server/build.gradle to gradle version catalog | Follow-up to #16284 |
| [#16284](https://github.com/opensearch-project/OpenSearch/pull/16284) | Switch from buildSrc/version.properties to Gradle version catalog | Resolves #3782 |
