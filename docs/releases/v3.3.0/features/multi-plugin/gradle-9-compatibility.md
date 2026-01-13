---
tags:
  - domain/infra
  - component/server
  - indexing
  - search
---
# Gradle 9 Compatibility

## Summary

This bugfix updates Gradle build files across 16 OpenSearch plugin repositories to fix compatibility with Gradle 9. The change replaces the deprecated `$System.env.VARIABLE_NAME` syntax with the `System.getenv()` method for accessing environment variables, specifically for Sonatype credentials used in SNAPSHOT publication.

## Details

### What's New in v3.3.0

Gradle 9 introduced breaking changes in how environment variables are accessed in build scripts. The previous syntax using string interpolation (`$System.env.VARIABLE_NAME`) no longer works and causes build failures during SNAPSHOT publication workflows.

### Technical Changes

#### Syntax Change

| Before (Gradle 8 and earlier) | After (Gradle 9 compatible) |
|-------------------------------|------------------------------|
| `"$System.env.SONATYPE_USERNAME"` | `System.getenv("SONATYPE_USERNAME")` |
| `"$System.env.SONATYPE_PASSWORD"` | `System.getenv("SONATYPE_PASSWORD")` |

#### Code Change Example

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

### Affected Repositories

| Repository | PR |
|------------|-----|
| alerting | [#1920](https://github.com/opensearch-project/alerting/pull/1920) |
| asynchronous-search | [#763](https://github.com/opensearch-project/asynchronous-search/pull/763) |
| common-utils | [#867](https://github.com/opensearch-project/common-utils/pull/867) |
| cross-cluster-replication | [#1575](https://github.com/opensearch-project/cross-cluster-replication/pull/1575) |
| custom-codecs | [#273](https://github.com/opensearch-project/custom-codecs/pull/273) |
| geospatial | [#791](https://github.com/opensearch-project/geospatial/pull/791) |
| index-management | [#1474](https://github.com/opensearch-project/index-management/pull/1474) |
| job-scheduler | [#821](https://github.com/opensearch-project/job-scheduler/pull/821) |
| opensearch-system-templates | [#95](https://github.com/opensearch-project/opensearch-system-templates/pull/95) |
| query-insights | [#407](https://github.com/opensearch-project/query-insights/pull/407) |
| reporting | [#1120](https://github.com/opensearch-project/reporting/pull/1120) |
| notifications | [#1069](https://github.com/opensearch-project/notifications/pull/1069) |
| opensearch-learning-to-rank-base | [#219](https://github.com/opensearch-project/opensearch-learning-to-rank-base/pull/219) |
| user-behavior-insights | [#122](https://github.com/opensearch-project/user-behavior-insights/pull/122) |
| dashboards-search-relevance | [#227](https://github.com/opensearch-project/dashboards-search-relevance/pull/227) |
| skills | [#630](https://github.com/opensearch-project/skills/pull/630) |

### Migration Notes

No user action required. This is an internal build system fix that ensures CI/CD pipelines continue to work with Gradle 9.

## Limitations

- This fix only addresses the Sonatype credentials syntax; other uses of `$System.env` may require similar updates in the future.

## References

### Documentation
- [Gradle 9 Release Notes](https://docs.gradle.org/9.0/release-notes.html): Breaking changes in Gradle 9
- [Example failed workflow](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/actions/runs/17023398832/job/48255946880#step:5:74): CI failure demonstrating the issue

### Pull Requests
| PR | Description |
|----|-------------|
| [#1920](https://github.com/opensearch-project/alerting/pull/1920) | alerting: Update System.env syntax |
| [#763](https://github.com/opensearch-project/asynchronous-search/pull/763) | asynchronous-search: Update System.env syntax |
| [#867](https://github.com/opensearch-project/common-utils/pull/867) | common-utils: Update System.env syntax |
| [#245](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/245) | opensearch-remote-metadata-sdk: Original fix example |

## Related Feature Report

- [Full feature documentation](../../../../features/multi-plugin/multi-plugin-gradle-9-compatibility.md)
