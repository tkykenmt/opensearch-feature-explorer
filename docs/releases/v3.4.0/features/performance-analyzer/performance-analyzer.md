---
tags:
  - indexing
  - performance
---

# Performance Analyzer

## Summary

This release item restores Java 21 as the minimum compatible version for Performance Analyzer and removes Java 24 from the CI test matrix. This change ensures consistent build behavior and aligns with the broader OpenSearch ecosystem's Java compatibility requirements while maintaining support for JDK 25.

## Details

### What's New in v3.4.0

The Performance Analyzer plugin received a build configuration update that:

1. **Restores Java 21 minimum compatibility**: The `sourceCompatibility` and `targetCompatibility` in `build.gradle` are now explicitly set to `JavaVersion.VERSION_21`, removing the conditional logic that previously selected between Java 21 and Java 25.

2. **Updates GitHub Actions CI matrix**: The CI workflow now tests against Java 21 and Java 25, removing Java 24 from the test matrix.

### Technical Changes

#### Build Configuration Changes

The `build.gradle` file was simplified:

**Before:**
```groovy
def javaVersion = JavaVersion.current().isCompatibleWith(JavaVersion.VERSION_25) ?
        JavaVersion.VERSION_25 : JavaVersion.VERSION_21

java {
    sourceCompatibility = javaVersion
    targetCompatibility = javaVersion
}
```

**After:**
```groovy
java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21
}
```

#### CI Workflow Changes

| File | Change |
|------|--------|
| `.github/workflows/gradle.yml` | Changed Java matrix from `[24, 25]` to `[21, 25]` |
| `.github/workflows/maven-publish.yml` | Changed Java version from `25` to `21` |

### Migration Notes

No migration required. This is a build infrastructure change that does not affect runtime behavior or APIs.

## Limitations

- This change only affects the build and CI configuration
- Runtime Java version requirements remain unchanged (Java 21+)

## References

### Documentation
- [Performance Analyzer Documentation](https://docs.opensearch.org/latest/monitoring-your-cluster/pa/index/): Official documentation
- [PR #896](https://github.com/opensearch-project/performance-analyzer/pull/896): Upgrade to JDK25 and gradle 9.2.0

### Pull Requests
| PR | Description |
|----|-------------|
| [#902](https://github.com/opensearch-project/performance-analyzer/pull/902) | Restore java min compatible to 21 and remove 24 |

### Issues (Design / RFC)
- [Issue #883](https://github.com/opensearch-project/performance-analyzer/issues/883): [Release 3.4.0] Gradle 9.2.0 and GitHub Actions JDK 25 Upgrade

## Related Feature Report

- [Full feature documentation](../../../../features/performance-analyzer/performance-analyzer.md)
