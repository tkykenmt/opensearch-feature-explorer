# Job Scheduler Bug Fixes

## Summary

OpenSearch 3.0.0 includes several bug fixes for the Job Scheduler plugin focused on CI/CD improvements and compatibility with OpenSearch core refactoring. These changes ensure the plugin builds correctly with the new JPMS (Java Platform Module System) architecture and modernize the GitHub Actions workflows.

## Details

### What's New in v3.0.0

The Job Scheduler plugin received three key bug fixes to maintain compatibility with OpenSearch 3.0.0 and improve the development workflow:

1. **GitHub Actions Modernization**: Updated CI workflows to use newer action versions
2. **JPMS Compatibility**: Fixed compile issues from OpenSearch's Java module system refactoring
3. **Security Test Optimization**: Conditional demo certificate downloads for integration tests

### Technical Changes

#### GitHub Actions Updates (PR #702)

Updated the CI workflow to resolve deprecation warnings and compatibility issues:

| Component | Old Version | New Version |
|-----------|-------------|-------------|
| `actions/checkout` | v2 | v4 |
| `actions/upload-artifact` | v3 | v4 |
| `codecov/codecov-action` | v3 | v4 |

The workflow now uses custom start commands from the CI image configuration instead of hardcoded options.

#### JPMS Refactoring Compatibility (PR #730)

OpenSearch 3.0.0 introduced JPMS (Java Platform Module System) refactoring that moved client classes to new packages. The Job Scheduler plugin was updated to use the new import paths:

| Old Import | New Import |
|------------|------------|
| `org.opensearch.client.Client` | `org.opensearch.transport.client.Client` |
| `org.opensearch.client.node.NodeClient` | `org.opensearch.transport.client.node.NodeClient` |

Files updated include:
- `JobSchedulerPlugin.java`
- `JobSweeper.java`
- `LockService.java`
- `JobDetailsService.java`
- REST action handlers
- Sample extension plugin classes

The `build.gradle` was also updated to properly handle version qualifiers in the OpenSearch build version.

#### Conditional Demo Certificate Downloads (PR #737)

Optimized the build process to only download demo certificates when running integration tests with security enabled:

```groovy
// Before: Always downloaded certificates
['esnode.pem', 'esnode-key.pem', ...].forEach { file ->
    download.run { ... }
}

// After: Only download when security.enabled=true
runIntegTestWithSecurityPlugin = System.getProperty("security.enabled")
if (runIntegTestWithSecurityPlugin == "true") {
    ['esnode.pem', 'esnode-key.pem', ...].forEach { file ->
        download.run { ... }
    }
}
```

The system property was also renamed from `-Dsecurity` to `-Dsecurity.enabled` for consistency.

### Migration Notes

- If you have custom CI/CD pipelines that run Job Scheduler integration tests with security, update the flag from `-Dsecurity=true` to `-Dsecurity.enabled=true`
- Plugin developers extending Job Scheduler should update their imports to use the new `org.opensearch.transport.client` package

## Limitations

These are internal build and compatibility fixes with no user-facing limitations.

## Related PRs

| PR | Description |
|----|-------------|
| [#702](https://github.com/opensearch-project/job-scheduler/pull/702) | Enable custom start commands and options to resolve GHA issues |
| [#730](https://github.com/opensearch-project/job-scheduler/pull/730) | Fix JS compile issues caused by OpenSearch JPMS Refactoring |
| [#737](https://github.com/opensearch-project/job-scheduler/pull/737) | Only download demo certs when integTest run with -Dsecurity.enabled=true |

## References

- [Issue #698](https://github.com/opensearch-project/job-scheduler/issues/698): GitHub Action Deprecation: actions/upload-artifact@v3
- [Issue #715](https://github.com/opensearch-project/job-scheduler/issues/715): [Release 3.0] Planned Breaking Changes for 3.0 in Plugin
- [OpenSearch Issue #8110](https://github.com/opensearch-project/OpenSearch/issues/8110): JPMS Refactoring tracking issue
- [Documentation](https://docs.opensearch.org/3.0/monitoring-your-cluster/job-scheduler/index/): Job Scheduler official docs

## Related Feature Report

- [Full feature documentation](../../../features/job-scheduler/job-scheduler.md)
