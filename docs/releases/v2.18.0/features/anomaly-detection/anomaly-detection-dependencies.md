# Anomaly Detection Dependencies

## Summary

This release updates several dependencies in the Anomaly Detection plugin to address security vulnerabilities and improve compatibility. The update also removes the unused `javassist` dependency to reduce the plugin's footprint.

## Details

### What's New in v2.18.0

Consolidated dependency updates that were previously tracked in separate dependabot PRs, making maintenance and rebasing easier.

### Technical Changes

#### Dependency Updates

| Dependency | Previous Version | New Version | Notes |
|------------|------------------|-------------|-------|
| jackson-databind | 2.16.1 | 2.18.0 | Core serialization |
| jackson-annotations | 2.16.1 | 2.18.0 | Core serialization |
| jackson-core | 2.16.0 | 2.18.0 | Core serialization (forced) |
| mockito-core | 5.9.0 | 5.14.1 | Test framework |
| junit-jupiter-api | 5.10.0 | 5.11.2 | Test framework |
| junit-jupiter-params | 5.10.0 | 5.11.2 | Test framework |
| junit-jupiter-engine | 5.10.0 | 5.11.2 | Test framework |
| junit-platform-launcher | 1.10.0 | 1.11.2 | Test framework |
| org.gradle.test-retry | 1.5.7 | 1.6.0 | Gradle plugin |
| release-drafter | v5 | v6 | GitHub Actions |
| actions/setup-java | v4 | v3 | GitHub Actions (downgrade) |

#### Removed Dependencies

| Dependency | Version | Reason |
|------------|---------|--------|
| javassist | 3.28.0-GA | Unused - all tests pass without it |

### Migration Notes

No migration required. This is a transparent dependency update with no API changes.

## Limitations

None identified.

## References

### Documentation
- [Anomaly Detection Documentation](https://docs.opensearch.org/2.18/observing-your-data/ad/index/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#1337](https://github.com/opensearch-project/anomaly-detection/pull/1337) | Updating several dependencies |

## Related Feature Report

- [Full feature documentation](../../../../features/anomaly-detection/anomaly-detection-dependencies.md)
