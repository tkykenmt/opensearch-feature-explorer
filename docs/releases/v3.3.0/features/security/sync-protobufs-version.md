---
tags:
  - security
---

# Sync `org.opensearch:protobufs` Version with Core

## Summary

This bugfix synchronizes the `org.opensearch:protobufs` dependency version in the Security plugin with the version defined in OpenSearch core. Previously, the Security plugin maintained its own hardcoded protobufs version, requiring manual PRs to update it whenever core updated the dependency. This change automates version synchronization, reducing maintenance overhead and ensuring compatibility.

## Details

### What's New in v3.3.0

The Security plugin now dynamically references the protobufs version from OpenSearch core's version catalog (`versions.opensearchprotobufs`) instead of maintaining a separate `protobuf_plugin_version` variable.

### Technical Changes

#### Build Configuration Changes

| Before | After |
|--------|-------|
| `protobuf_plugin_version = '0.13.0'` (hardcoded) | Uses `versions.opensearchprotobufs` from core |
| Manual PR required for each version update | Automatic sync with core |

#### Modified Files

| File | Change |
|------|--------|
| `build.gradle` | Removed `protobuf_plugin_version` variable, updated dependency reference |

#### Dependency Reference Change

```groovy
// Before
integrationTestImplementation "org.opensearch:protobufs:${protobuf_plugin_version}"

// After
integrationTestImplementation "org.opensearch:protobufs:${versions.opensearchprotobufs}"
```

### Benefits

1. **Reduced maintenance**: No manual PRs needed when core updates protobufs version
2. **Guaranteed compatibility**: Security plugin always uses the same protobufs version as core
3. **Build consistency**: Eliminates version mismatch issues between core and Security plugin

### Version Reference

The protobufs version is defined in OpenSearch core at:
- File: `gradle/libs.versions.toml`
- Key: `opensearchprotobufs`
- Current value: `1.1.0` (as of OpenSearch 3.x)

## Limitations

- If a breaking change is introduced in protobufs, the Security plugin build will fail until compatibility is restored
- Requires the Security plugin to be built against a compatible OpenSearch core version

## References

### Documentation
- [OpenSearch core libs.versions.toml](https://github.com/opensearch-project/OpenSearch/blob/main/gradle/libs.versions.toml#L25): Protobufs version definition

### Pull Requests
| PR | Description |
|----|-------------|
| [#5659](https://github.com/opensearch-project/security/pull/5659) | Sync `org.opensearch:protobufs` version with core |

## Related Feature Report

- [Full feature documentation](../../../../features/security/protobufs-version-sync.md)
