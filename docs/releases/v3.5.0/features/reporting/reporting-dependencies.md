---
tags:
  - reporting
---
# Reporting Dependencies

## Summary

In v3.5.0, the Reporting plugin updated its mockito-core test dependency to align with the version provided by the OpenSearch core framework, resolving a build conflict that caused compilation failures.

## Details

### What's New in v3.5.0

The `mockito-core` dependency was updated to use `${versions.mockito}` from the OpenSearch version catalog instead of a hardcoded version. This resolved a version conflict between mockito-core 5.2.0 (from OpenSearch core) and 5.1.0 (previously pinned in the reporting plugin), which caused `compileTestKotlin` task failures.

### Technical Changes

- Replaced hardcoded mockito-core version with `${versions.mockito}` to fetch the version from OpenSearch core
- Resolved `testCompileClasspath` dependency conflict between mockito-core 5.2.0 and 5.1.0

## Limitations

- This is a test-only dependency change with no runtime impact

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#678](https://github.com/opensearch-project/reporting/pull/678) | Bump mockito-core version to align with OpenSearch core | Build failure due to version conflict |
