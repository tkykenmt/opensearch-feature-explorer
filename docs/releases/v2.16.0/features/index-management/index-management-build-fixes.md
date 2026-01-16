---
tags:
  - index-management
---
# Index Management Build Fixes

## Summary

Build and CI/CD fixes for the Index Management plugin in v2.16.0, including SPI Maven publishing support, GitHub Actions updates for Java 21, and a security vulnerability fix for the braces package (CVE-2024-4068) in the dashboards plugin.

## Details

### What's New in v2.16.0

#### SPI Maven Publishing (Backend)

Added Maven publishing support for the Index Management SPI module, enabling other plugins to consume the SPI as a dependency:

```groovy
compileOnly "org.opensearch:opensearch-index-management-spi:${opensearch_version}"
```

This allows plugins like Cross-Cluster Replication to extend ISM functionality by depending on the published SPI artifact.

**Changes:**
- Added `maven-publish` plugin to `spi/build.gradle`
- Configured shadow publication with sources and javadoc JARs
- Added `publishShadowPublicationToSnapshotsRepository` task to maven-publish workflow
- Fixed build dependency ordering for POM file generation

#### GitHub Actions Java 21 Update (Backend)

Updated GitHub Actions workflows to use Java 21 (from Java 17) to align with OpenSearch's JDK requirements:

- `bwc-test-workflow.yml`: Java 17 → 21
- `docker-security-test-workflow.yml`: Java 17 → 21
- `security-test-workflow.yml`: Java 17 → 21
- Added `ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION: true` environment variable to workflows using older Node.js versions

#### CVE-2024-4068 Fix (Dashboards)

Updated the `braces` package in the Index Management Dashboards Plugin to address [CVE-2024-4068](https://github.com/advisories/GHSA-grv7-fg5c-xmjg), a high-severity vulnerability in the braces package that could cause uncontrolled resource consumption via crafted input.

**Fix:** Updated `yarn.lock` to use braces v3.0.3 which patches the vulnerability.

## Limitations

- The SPI publishing change only affects the build/release process; no runtime behavior changes
- GitHub Actions changes are CI-only and do not affect plugin functionality

## References

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#1207](https://github.com/opensearch-project/index-management/pull/1207) | index-management | Add publish in spi build.gradle |
| [#1208](https://github.com/opensearch-project/index-management/pull/1208) | index-management | Fix github action |
| [#1091](https://github.com/opensearch-project/index-management-dashboards-plugin/pull/1091) | index-management-dashboards-plugin | Bumped up braces package version to address CVE-2024-4068 |

### Related PRs
| PR | Repository | Description |
|----|------------|-------------|
| [#1562](https://github.com/opensearch-project/alerting/pull/1562) | alerting | Reference for SPI publishing pattern |
| [#1604](https://github.com/opensearch-project/alerting/pull/1604) | alerting | Reference for SPI publishing pattern |
| [#1795](https://github.com/opensearch-project/k-NN/pull/1795) | k-NN | Reference for GitHub Actions fix |

### Security Advisory
- [GHSA-grv7-fg5c-xmjg](https://github.com/advisories/GHSA-grv7-fg5c-xmjg): CVE-2024-4068 - Uncontrolled resource consumption in braces
