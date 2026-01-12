---
tags:
  - security
---

# Geospatial Infrastructure

## Summary

This release updates the Geospatial plugin's build infrastructure by upgrading Gradle to version 8.14.3 and enabling CI checks with JDK 24. These changes ensure compatibility with the latest Java runtime and improve build tooling.

## Details

### What's New in v3.2.0

The Geospatial plugin build infrastructure has been modernized with the following updates:

1. **Gradle Upgrade**: Updated from 8.10.2 to 8.14.3
2. **JDK 24 Support**: CI workflows now run tests with JDK 21 and JDK 24 (replacing JDK 23)
3. **Lombok Plugin Update**: Upgraded to version 8.14 with new plugin DSL syntax
4. **Test Fix**: Improved test reliability for duplicate key handling

### Technical Changes

#### Build Configuration Updates

| Component | Previous | New |
|-----------|----------|-----|
| Gradle | 8.10.2 | 8.14.3 |
| CI JDK Matrix | 21, 23 | 21, 24 |
| Lombok Plugin | 8.4 (classpath) | 8.14 (plugins DSL) |

#### CI Workflow Changes

The following workflow files were updated to use JDK 24:

- `.github/workflows/CI.yml` - Main CI workflow
- `.github/workflows/test_security.yml` - Security tests

#### Gradle Plugin Migration

The Lombok plugin declaration was migrated from classpath-based to plugins DSL:

```groovy
// Before (classpath in buildscript)
classpath "io.freefair.gradle:lombok-plugin:8.4"
apply plugin: 'io.freefair.lombok'

// After (plugins DSL)
plugins {
    id "io.freefair.lombok" version "8.14"
}
```

This change applies to both the main `build.gradle` and `client/build.gradle`.

#### Test Improvements

Fixed a flaky test in `UploadStatsServiceTests.java` that could fail due to duplicate random keys by adding deduplication logic.

## Limitations

- JDK 24 is the latest supported version; older JDK versions below 21 are not supported
- Gradle 8.14.3 requires compatible plugin versions

## References

### Documentation
- [Gradle 8.14.3 Release Notes](https://docs.gradle.org/8.14.3/release-notes.html): Gradle release information
- [JDK 24 Release](https://openjdk.org/projects/jdk/24/): OpenJDK 24 project page
- [Lombok Gradle Plugin](https://plugins.gradle.org/plugin/io.freefair.lombok): Lombok plugin for Gradle

### Pull Requests
| PR | Description |
|----|-------------|
| [#776](https://github.com/opensearch-project/geospatial/pull/776) | Upgrade gradle to 8.14.3 and run CI checks with JDK24 |

## Related Feature Report

- [Full feature documentation](../../../../features/geospatial/geospatial-plugin.md)
