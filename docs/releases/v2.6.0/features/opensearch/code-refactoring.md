---
tags:
  - opensearch
---
# Code Refactoring

## Summary

OpenSearch 2.6.0 introduces 1 new feature(s) and 0 enhancement(s) to Code Refactoring, along with 1 bug fixes.

## Details

### New Features

- **Remove deprecated org.gradle.util.DistributionLocator usage**: The [org.gradle.util.DistributionLocator](https://docs.gradle.org/current/javadoc/org/gradle/util/DistributionLocator.html) class is deprecated and will be removed in Gradle 9.0. This PR replaces that usage in `build.gradle` with `wrapper.getDistributionUrl()` which [implements the identical logic i

### Bug Fixes

- Refactor layer properties as own interface

## References

### Pull Requests

| PR | Description | Repository |
|----|-------------|------------|
| [#225](https://github.com/opensearch-project/dashboards-maps/pull/225) | Refactor layer properties as own interface | dashboards-maps |
| [#6212](https://github.com/opensearch-project/OpenSearch/pull/6212) | Remove deprecated org.gradle.util.DistributionLocator usage | OpenSearch |
