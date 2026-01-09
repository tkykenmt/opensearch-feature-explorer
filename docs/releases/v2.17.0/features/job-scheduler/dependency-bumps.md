# Dependency Bumps (Job Scheduler)

## Summary

Routine dependency updates for the Job Scheduler plugin in v2.17.0, including updates to Gradle plugins, logging libraries, and build tools to maintain security and compatibility.

## Details

### What's New in v2.17.0

The Job Scheduler plugin received 4 dependency updates via Dependabot:

| Dependency | From | To | Type |
|------------|------|-----|------|
| org.gradle.test-retry | 1.5.9 | 1.5.10 | Gradle Plugin |
| com.google.googlejavaformat:google-java-format | - | Latest | Code Formatting |
| org.slf4j:slf4j-api | 2.0.13 | 2.0.16 | Logging |
| com.netflix.nebula.ospackage | 11.9.1 | 11.10.0 | Packaging |

### Technical Changes

#### Gradle Test Retry Plugin (1.5.9 → 1.5.10)
- Minor bug fixes and improvements for test retry functionality
- Enhances CI reliability by retrying flaky tests

#### SLF4J API (2.0.13 → 2.0.16)
- Logging framework update with bug fixes
- Maintains compatibility with existing logging configuration

#### Nebula OS Package (11.9.1 → 11.10.0)
- Gradle plugin for building OS packages (RPM, DEB)
- Improvements to package generation

#### Google Java Format
- Code formatting tool update
- Ensures consistent code style across the codebase

## Limitations

- These are maintenance updates with no functional changes
- No migration required

## Related PRs

| PR | Description |
|----|-------------|
| [#653](https://github.com/opensearch-project/job-scheduler/pull/653) | Bump org.gradle.test-retry from 1.5.9 to 1.5.10 |
| [#663](https://github.com/opensearch-project/job-scheduler/pull/663) | Bump com.google.googlejavaformat:google-java-format |
| [#666](https://github.com/opensearch-project/job-scheduler/pull/666) | Bump org.slf4j:slf4j-api from 2.0.13 to 2.0.16 |
| [#668](https://github.com/opensearch-project/job-scheduler/pull/668) | Bump com.netflix.nebula.ospackage from 11.9.1 to 11.10.0 |

## References

- [Job Scheduler Repository](https://github.com/opensearch-project/job-scheduler)

## Related Feature Report

- [Dependency Management](../../../../features/multi-plugin/dependency-bumps.md)
