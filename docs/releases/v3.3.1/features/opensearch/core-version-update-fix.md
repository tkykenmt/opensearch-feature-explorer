---
tags:
  - opensearch
---
# Core Version Update Fix

## Summary

Fixed a build failure that occurred when bumping the OpenSearch core version to a patch number other than 0 (e.g., 3.3.1). The `GlobalBuildInfoPlugin` was reading legacy Elasticsearch version definitions from `LegacyESVersion.java`, which introduced version numbers from more than two major versions ago. The `BwcVersions` validation then rejected the build because it found more than 2 major versions.

## Details

### What's New in v3.3.1

When attempting to version-bump the core to 3.3.1 and run `./gradlew localDistro`, the build failed with:

```
Expected exactly 2 majors in parsed versions but found: [2, 3, 6, 7]
```

The root cause was in `GlobalBuildInfoPlugin.resolveBwcVersions()`, which concatenated version lines from both `Version.java` and `LegacyESVersion.java`. The legacy file contained Elasticsearch 6.x and 7.x version constants. When `BwcVersions.assertNoOlderThanTwoMajors()` ran — a check only triggered when both minor and patch are non-zero — it found 4 major versions instead of the expected 2.

The fix removes the legacy version file reading entirely from `resolveBwcVersions()`, so only `Version.java` (containing OpenSearch 2.x and 3.x versions) is parsed. This is safe because the legacy ES versions are more than two major versions behind and are no longer relevant for backward compatibility testing.

### Technical Changes

| File | Change |
|------|--------|
| `buildSrc/.../GlobalBuildInfoPlugin.java` | Removed `LegacyESVersion.java` file reading from `resolveBwcVersions()` |

The `DEFAULT_LEGACY_VERSION_JAVA_FILE_PATH` constant remains in the class but is no longer used in `resolveBwcVersions()`.

### Trigger Condition

The bug only manifested when both `minor != 0` and `patch != 0` (e.g., 3.3.1), because `BwcVersions.assertNoOlderThanTwoMajors()` skips the check when either is zero:

```java
if (majors.size() != numSupportedMajors
    && currentVersion.getMinor() != 0
    && currentVersion.getRevision() != 0) {
    throw new IllegalStateException(...);
}
```

This is why the issue was never encountered during regular minor releases (e.g., 3.3.0).

## Limitations

- The `DEFAULT_LEGACY_VERSION_JAVA_FILE_PATH` constant is still defined in the class but unused by `resolveBwcVersions()`. It may be referenced elsewhere.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [opensearch-project/OpenSearch#19377](https://github.com/opensearch-project/OpenSearch/pull/19377) | Fix issue with updating core with a patch number other than 0 | [opensearch-build#5720](https://github.com/opensearch-project/opensearch-build/issues/5720) |

### Related Issues
- [opensearch-build#5720](https://github.com/opensearch-project/opensearch-build/issues/5720) — Discussion: Patch releases currently take a lot of effort
