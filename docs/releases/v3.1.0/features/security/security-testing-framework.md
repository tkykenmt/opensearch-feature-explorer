---
tags:
  - domain/security
  - component/server
  - indexing
  - security
---
# Security Testing Framework

## Summary

This release item updates the Security plugin's integration test framework to use the `extendedPlugins` mechanism introduced in OpenSearch core PR #16908. This replaces the previous workaround for testing the sample-resource-plugin, enabling proper plugin extension loading in integration tests. Additionally, the resource sharing flow was refactored to modify sharing info in memory instead of using Painless scripts.

## Details

### What's New in v3.1.0

The Security plugin's sample-resource-plugin integration tests now leverage the core OpenSearch Plugin Testing Framework's `extendedPlugins` support. This change:

1. Removes manual workarounds for loading plugin extensions in tests
2. Enables proper `ExtensiblePlugin` and extension relationships via `PluginInfo`
3. Refactors resource sharing to use in-memory modifications instead of Painless scripts

### Technical Changes

#### Architecture Changes

```mermaid
graph TB
    subgraph "Before v3.1.0"
        A1[Test] --> B1[Manual Resource Sharing Entry]
        B1 --> C1[Painless Script Update]
        C1 --> D1[Resource Sharing Index]
    end
    
    subgraph "After v3.1.0"
        A2[Test] --> B2[PluginInfo with extendedPlugins]
        B2 --> C2[Automatic Extension Loading]
        C2 --> D2[In-Memory Sharing Update]
        D2 --> E2[Direct Index Write]
    end
```

#### New Components

| Component | Description |
|-----------|-------------|
| `ResourceSharing.docId` | New field to track document ID for in-memory updates |
| `ResourceSharing.share()` | New method to modify sharing info in memory |
| `ShareWith.accessLevels()` | Helper to get all access levels from share configuration |
| `ShareWith.atAccessLevel()` | Helper to get sharing config at specific access level |
| `SharedWithActionGroup.share()` | Method to merge sharing targets |

#### API Changes

The `ResourceSharing` class now includes:

```java
// New field for document tracking
private String docId;

// New methods for in-memory sharing
public void share(String accessLevel, SharedWithActionGroup target) {
    if (shareWith == null) {
        shareWith = new ShareWith(Set.of(target));
    } else {
        SharedWithActionGroup sharedWith = shareWith.atAccessLevel(accessLevel);
        sharedWith.share(target);
    }
}
```

### Usage Example

```java
// Integration test using extendedPlugins
@ClassRule
public static LocalCluster cluster = new LocalCluster.Builder()
    .clusterManager(ClusterManager.SINGLENODE)
    .plugin(PainlessModulePlugin.class)
    .plugin(
        new PluginInfo(
            SampleResourcePlugin.class.getName(),
            "classpath plugin",
            "NA",
            Version.CURRENT,
            "1.8",
            SampleResourcePlugin.class.getName(),
            null,
            List.of(OpenSearchSecurityPlugin.class.getName()),  // extendedPlugins
            false
        )
    )
    .anonymousAuth(true)
    .authc(AUTHC_HTTPBASIC_INTERNAL)
    .users(USER_ADMIN, SHARED_WITH_USER)
    .build();
```

### Migration Notes

For plugin developers using the Security plugin's test framework:

1. Replace manual resource-sharing index entries with proper `PluginInfo` configuration
2. Use `extendedPlugins` list to declare plugin extension relationships
3. Remove `ResourceSharingClientAccessor` manual setup - extensions are now loaded automatically

## Limitations

- Requires OpenSearch core v3.1.0+ with PR #16908 merged
- Only applicable to integration tests using the Security plugin's test framework

## References

### Documentation
- [Security Plugin Documentation](https://docs.opensearch.org/3.1/security/index/): OpenSearch Security plugin docs
- [PR #5322](https://github.com/opensearch-project/security/pull/5322): Main implementation
- [PR #16908](https://github.com/opensearch-project/OpenSearch/pull/16908): Core Plugin Testing Framework enhancement

### Pull Requests
| PR | Description |
|----|-------------|
| [#5322](https://github.com/opensearch-project/security/pull/5322) | Use extendedPlugins in integrationTest framework for sample resource plugin testing |
| [#16908](https://github.com/opensearch-project/OpenSearch/pull/16908) | Enable testing for ExtensiblePlugins using classpath plugins (core dependency) |

## Related Feature Report

- Plugin Testing Framework
- Security Testing Framework
