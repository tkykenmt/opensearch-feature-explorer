---
tags:
  - opensearch
---
# CI Fixes

## Summary

Fixed failing CI builds caused by Eclipse JDT formatter download failures by configuring a P2 mirror for the Spotless Gradle plugin.

## Details

### What's New in v2.19.0

The CI pipeline was experiencing intermittent failures with the error `Failed to load eclipse jdt formatter`. This occurred because the Spotless Gradle plugin was unable to download the Eclipse JDT formatter from the primary Eclipse download server (`download.eclipse.org`).

### Technical Changes

The fix adds a P2 mirror configuration to the Spotless Eclipse formatter setup in `gradle/formatting.gradle`:

```groovy
// Before
eclipse().configFile rootProject.file('buildSrc/formatterConfig.xml')

// After
eclipse().withP2Mirrors(Map.of("https://download.eclipse.org/", "https://mirror.umd.edu/eclipse/")).configFile rootProject.file('buildSrc/formatterConfig.xml')
```

This change redirects Eclipse artifact downloads to the University of Maryland mirror, which provides more reliable availability than the primary Eclipse download server.

### Root Cause

The issue was tracked in the Spotless project (diffplug/spotless#1783). The primary Eclipse download server occasionally experiences connectivity issues or timeouts, causing CI builds to fail when attempting to download the Eclipse JDT formatter artifacts.

## Limitations

- The fix relies on a single mirror (mirror.umd.edu). If this mirror becomes unavailable, CI builds could still fail.
- This is a workaround for upstream infrastructure issues in the Eclipse download servers.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#17172](https://github.com/opensearch-project/OpenSearch/pull/17172) | Fix failing CI's with `Failed to load eclipse jdt formatter` | [diffplug/spotless#1783](https://github.com/diffplug/spotless/issues/1783) |
