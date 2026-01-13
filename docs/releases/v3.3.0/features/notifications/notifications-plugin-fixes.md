---
tags:
  - domain/observability
  - component/server
  - dashboards
  - indexing
---
# Notifications Plugin Fixes

## Summary

This release includes two build infrastructure fixes for the OpenSearch Notifications plugin that resolve Maven snapshot publication issues. These fixes ensure compatibility with Gradle 9 and resolve SLF4J version conflicts that were preventing successful snapshot builds.

## Details

### What's New in v3.3.0

Two critical build fixes were merged to restore snapshot publication functionality:

1. **Gradle 9 Compatibility**: Updated environment variable access syntax from deprecated `$System.env.VARIABLE_NAME` to `System.getenv("VARIABLE_NAME")`
2. **SLF4J Version Conflict Resolution**: Forced SLF4J version from Gradle version catalog to resolve dependency conflicts

### Technical Changes

#### Gradle 9 Environment Variable Syntax Fix

The previous syntax for accessing environment variables in Gradle build files was incompatible with Gradle 9:

```gradle
// Before (incompatible with Gradle 9)
credentials {
    username "$System.env.SONATYPE_USERNAME"
    password "$System.env.SONATYPE_PASSWORD"
}

// After (Gradle 9 compatible)
credentials {
    username System.getenv("SONATYPE_USERNAME")
    password System.getenv("SONATYPE_PASSWORD")
}
```

This change was applied to both `notifications/core/build.gradle` and `notifications/notifications/build.gradle`.

#### SLF4J Version Conflict Resolution

A version conflict between SLF4J 2.0.17 and 1.7.36 was causing build failures when publishing Maven snapshots. The fix forces the SLF4J version from the Gradle version catalog:

```gradle
configurations.all {
    resolutionStrategy {
        force "org.slf4j:slf4j-api:${versions.slf4j}"
    }
}
```

### Files Changed

| File | Change |
|------|--------|
| `notifications/core/build.gradle` | Updated Sonatype credentials syntax |
| `notifications/notifications/build.gradle` | Updated Sonatype credentials syntax, added SLF4J version forcing |

## Limitations

- These are build infrastructure fixes only; no runtime behavior changes
- Requires Gradle version catalog to define `versions.slf4j`

## References

### Documentation
- [Failed workflow example](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/actions/runs/17023398832/job/48255946880#step:5:74): Gradle 9 syntax failure
- [Related fix in opensearch-remote-metadata-sdk](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/245): Similar Gradle 9 fix
- [Snapshot publication failure](https://github.com/opensearch-project/notifications/actions/runs/17410029596/job/50618172116): SLF4J conflict error

### Pull Requests
| PR | Description |
|----|-------------|
| [#1069](https://github.com/opensearch-project/notifications/pull/1069) | Fix: Update System.env syntax for Gradle 9 compatibility |
| [#1074](https://github.com/opensearch-project/notifications/pull/1074) | Fix issue publishing maven snapshots by forcing slf4j version |

## Related Feature Report

- Full feature documentation
