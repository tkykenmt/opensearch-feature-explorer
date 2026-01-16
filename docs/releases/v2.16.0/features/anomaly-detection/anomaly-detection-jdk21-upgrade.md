---
tags:
  - anomaly-detection
---
# Anomaly Detection JDK21 Upgrade

## Summary

The Anomaly Detection plugin upgraded its baseline JDK version from JDK 11/17 to JDK 21 in v2.16.0. This change aligns the plugin with OpenSearch core's JDK 21 baseline requirement for the 3.0.0 release track and ensures CI/CD pipelines use consistent Java versions across backend and frontend components.

## Details

### What's New in v2.16.0

The JDK 21 upgrade involved changes to both the backend plugin and the dashboards plugin:

**Backend Plugin (anomaly-detection)**
- Updated `build.gradle` to set `sourceCompatibility` and `targetCompatibility` to `JavaVersion.VERSION_21`
- Modified CI workflow matrices to test only with JDK 21 (previously tested JDK 11, 17, and 21)
- Updated GitHub Actions workflows:
  - `maven-publish.yml`: JDK 17 → JDK 21
  - `test_build_multi_platform.yml`: Spotless check and build matrix updated to JDK 21
  - `test_bwc.yml`: Backward compatibility tests updated to JDK 21
  - `test_security.yml`: Security tests updated to JDK 21

**Frontend Plugin (anomaly-detection-dashboards-plugin)**
- Updated `remote-integ-tests-workflow.yml` to use JDK 21 for integration tests
- This change was required because the backend baseline change caused CI failures with "error: release version 21 not supported"

### Technical Changes

| Component | Before | After |
|-----------|--------|-------|
| Source compatibility | Java 11 | Java 21 |
| Target compatibility | Java 11 | Java 21 |
| CI test matrix | JDK 11, 17, 21 | JDK 21 only |
| Maven publish JDK | 17 | 21 |
| Frontend CI JDK | 11 | 21 |

### Motivation

This change was part of the broader OpenSearch initiative to set JDK 21 as the baseline for the 3.0.0 release. The tracking issues were:
- [OpenSearch #10745](https://github.com/opensearch-project/OpenSearch/issues/10745): JDK 21 baseline discussion
- [OpenSearch #14011](https://github.com/opensearch-project/OpenSearch/issues/14011): JDK 21 baseline implementation

## Limitations

- Environments running older JDK versions (11, 17) are no longer supported for building or testing the plugin
- Users must ensure JDK 21 is available in their development and CI environments

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [anomaly-detection#1228](https://github.com/opensearch-project/anomaly-detection/pull/1228) | Set baseline JDK version to JDK-21 | [#1223](https://github.com/opensearch-project/anomaly-detection/issues/1223) |
| [anomaly-detection-dashboards-plugin#798](https://github.com/opensearch-project/anomaly-detection-dashboards-plugin/pull/798) | Update Frontend CI to use JDK21 | - |

### Related Issues
| Issue | Description |
|-------|-------------|
| [anomaly-detection#1223](https://github.com/opensearch-project/anomaly-detection/issues/1223) | Set anomaly-detection plugin 3.0.0 baseline JDK version to JDK-21 |
| [OpenSearch#10745](https://github.com/opensearch-project/OpenSearch/issues/10745) | JDK 21 baseline discussion |
| [OpenSearch#14011](https://github.com/opensearch-project/OpenSearch/issues/14011) | JDK 21 baseline implementation |
