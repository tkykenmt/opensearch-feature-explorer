---
tags:
  - performance-analyzer
---
# Performance Analyzer

## Summary

Maintenance update for the Performance Analyzer plugin in OpenSearch v3.5.0. The PA Commons dependency was bumped to version 2.1.0 with JDK 21 compatibility, and a build fix was applied to resolve a Jackson annotations version mismatch in the OpenSearch 3.5.0 snapshot.

## Details

### What's New in v3.5.0

This release contains dependency version bumps and a build configuration fix:

1. **PA Commons Upgrade (2.0.0 → 2.1.0)**: Updated the `performance-analyzer-commons` library dependency from 2.0.0 to 2.1.0, incorporating upstream changes from the commons repository ([PA Commons #118](https://github.com/opensearch-project/performance-analyzer-commons/pull/118)).

2. **Jackson Annotations Version Fix**: In OpenSearch 3.5.0, `jackson-core` and `jackson-annotations` have different minor versions. Previously, both used the same `jacksonVersion` variable, causing build failures. The fix introduces a separate `jacksonAnnotationsVersion` variable (using `versions.jackson_annotations`) to resolve the version mismatch.

3. **SNAPSHOT Build Fix**: Re-enabled the SNAPSHOT suffix for the PA Commons version during snapshot builds, which had been commented out.

### Technical Changes

| Change | Before | After |
|--------|--------|-------|
| PA Commons version | 2.0.0 | 2.1.0 |
| Jackson annotations version variable | `jacksonVersion` (shared) | `jacksonAnnotationsVersion` (separate) |
| SNAPSHOT suffix for PA Commons | Disabled (commented out) | Enabled |

## Limitations

No new limitations introduced.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#910](https://github.com/opensearch-project/performance-analyzer/pull/910) | Bump performance-analyzer-commons to v2.1.1 and fix Jackson annotations version | |
| [#911](https://github.com/opensearch-project/performance-analyzer/pull/911) | Fix performance-analyzer-commons version to 2.1.0 | |

### Related PRs (PA Commons)
| PR | Description |
|----|-------------|
| [PA Commons #118](https://github.com/opensearch-project/performance-analyzer-commons/pull/118) | Changes consumed in PA Commons 2.1.0 |
