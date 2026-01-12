---
tags:
  - search
---

# User Behavior Insights Bugfixes

## Summary

This release includes three bug fixes for the User Behavior Insights (UBI) plugin addressing ActionFilter interface compatibility with OpenSearch core changes, CI build script fixes for shallow git checkouts, and plugin zip publishing errors.

## Details

### What's New in v3.4.0

Three bug fixes improve plugin compatibility and build reliability:

1. **ActionFilter Interface Adaptation** - Updated `UbiActionFilter` to implement the new `apply()` method signature with `ActionRequestMetadata` parameter
2. **CI Build Script Fix** - Export `CI=true` environment variable to skip git diff on depth=1 checkouts during release builds
3. **Plugin Zip Publishing Fix** - Remove duplicate `bundlePlugin` artifact from Maven publication to fix publishing errors

### Technical Changes

#### ActionFilter Interface Update

The OpenSearch core PR [#18523](https://github.com/opensearch-project/OpenSearch/pull/18523) changed the `ActionFilter` interface by adding a new `apply()` method with an additional `ActionRequestMetadata` parameter. The old method is now deprecated.

```java
// Updated method signature in UbiActionFilter.java
public <Request extends ActionRequest, Response extends ActionResponse> void apply(
    Task task,
    String action,
    Request request,
    ActionRequestMetadata<Request, Response> actionRequestMetadata,  // New parameter
    ActionListener<Response> listener,
    ActionFilterChain<Request, Response> chain
)
```

#### CI Build Script Fix

When building with depth=1 checkout (used in release builds), git diff fails because the main branch reference is not available:

```
fatal: ambiguous argument 'refs/remotes/origin/main': unknown revision or path not in the working tree.
```

The fix exports `CI=true` in `scripts/build.sh` to skip the git diff check:

```bash
export CI=true
```

#### Plugin Zip Publishing Fix

The `opensearch.pluginzip` Gradle plugin automatically creates a `pluginZip` publication and adds `bundlePlugin` as its artifact. The manual addition of `bundlePlugin` in `build.gradle` caused duplicate artifact errors:

```
Execution failed for task ':publishPluginZipPublicationToMavenLocal'.
> Failed to publish publication 'pluginZip' to repository 'mavenLocal'
   > Invalid publication 'pluginZip': multiple artifacts with the identical extension and classifier ('zip', 'null').
```

The fix removes the redundant `artifact bundlePlugin` line from the publications block.

### Files Changed

| PR | Files | Changes |
|----|-------|---------|
| #142 | `UbiActionFilter.java`, `UbiActionFilterTests.java` | +5 lines |
| #146 | `scripts/build.sh` | +2 lines |
| #151 | `build.gradle`, license files | -1 line, dependency update |

## Limitations

- The ActionFilter interface change requires OpenSearch 3.4.0 or later
- The CI fix is specific to the opensearch-build release process

## References

### Documentation
- [UBI Documentation](https://docs.opensearch.org/3.0/search-plugins/ubi/index/): Official OpenSearch UBI documentation
- [OpenSearch PR #18523](https://github.com/opensearch-project/OpenSearch/pull/18523): ActionFilter interface change in core

### Blog Posts
- [Plugin Zip Publishing Blog](https://opensearch.org/blog/opensearch-plugin-zips-now-in-maven-repo/): OpenSearch plugin zip Maven publishing

### Pull Requests
| PR | Description |
|----|-------------|
| [#142](https://github.com/opensearch-project/user-behavior-insights/pull/142) | Adapt ActionFilter interface implementation to core change |
| [#146](https://github.com/opensearch-project/user-behavior-insights/pull/146) | Export CI env var as true to skip git diff on depth=1 checkout |
| [#151](https://github.com/opensearch-project/user-behavior-insights/pull/151) | Fix the plugin publish zip errors |

### Issues (Design / RFC)
- [Issue #138](https://github.com/opensearch-project/user-behavior-insights/issues/138): Release version 3.4.0 tracking issue
- [Issue #5764](https://github.com/opensearch-project/opensearch-build/issues/5764): Build system issue for plugin zip publishing

## Related Feature Report

- [Full feature documentation](../../../features/user-behavior-insights/user-plugin-fixes.md)
