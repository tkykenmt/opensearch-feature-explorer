# User Plugin Fixes

## Summary

This release fixes dependency version conflicts in the User Behavior Insights (UBI) plugin that were causing integration test failures. The fix forces a specific version of the `error_prone_annotations` library to resolve conflicts between different dependencies.

## Details

### What's New in v3.3.0

This bugfix resolves dependency resolution errors that occurred during UBI integration tests. The issue was caused by version conflicts in the `com.google.errorprone:error_prone_annotations` library.

### Technical Changes

#### Dependency Resolution Fix

The fix adds a resolution strategy to the Gradle build configuration that forces a specific version of the error_prone_annotations library:

```groovy
configurations.all {
    resolutionStrategy {
        force("com.google.errorprone:error_prone_annotations:2.41.0")
    }
}
```

#### Changed Files

| File | Change |
|------|--------|
| `build.gradle` | Added resolution strategy to force error_prone_annotations version |

### Impact

- Integration tests now pass successfully
- No functional changes to the UBI plugin behavior
- No API changes

## Limitations

- This is a build-time fix only; no runtime behavior changes

## Related PRs

| PR | Description |
|----|-------------|
| [#128](https://github.com/opensearch-project/user-behavior-insights/pull/128) | Pass Integration tests - fixes dependency errors |

## References

- [User Behavior Insights Plugin](https://github.com/opensearch-project/user-behavior-insights): Main UBI repository
- [UBI Documentation](https://docs.opensearch.org/3.0/search-plugins/ubi/index/): Official OpenSearch UBI documentation

## Related Feature Report

- [UBI Data Generator](../../../../features/user-behavior-insights/user-behavior-insights-data-generator.md)
