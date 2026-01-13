---
tags:
  - security
---
# Security Identity Plugin

## Summary

OpenSearch v2.19.0 introduces new extension points in the `IdentityPlugin` interface and adds `ContextProvidingPluginSubject` to strengthen system index protection in the plugin ecosystem. This enhancement allows plugins to securely access their own system indices using `pluginSubject.runAs()` while preventing unauthorized access to other plugins' system indices.

## Details

### What's New in v2.19.0

The security plugin now implements the `IdentityPlugin` interface from OpenSearch core, providing:

1. **ContextProvidingPluginSubject**: A new class that populates a header in the ThreadContext with the canonical class name of the plugin executing code using `pluginSubject.runAs()`.

2. **Plugin-Aware System Index Access**: Plugins can now perform index operations on their own registered system indices without requiring full admin privileges.

3. **Enhanced Privilege Evaluation**: The security plugin evaluates whether a plugin is authorized to access specific system indices based on the plugin's identity.

### Technical Changes

#### New Classes

| Class | Description |
|-------|-------------|
| `ContextProvidingPluginSubject` | Implements `PluginSubject` interface, manages plugin identity in ThreadContext |
| `UserSubjectImpl` | Implements `UserSubject` interface for authenticated users |
| `InMemorySecurityRoles` | Interface for dynamically created security roles |
| `InMemorySecurityRolesV7` | Implementation for plugin-specific security roles |

#### Key Implementation Details

- Plugins are identified by the convention `plugin:{canonical-class-name}` (e.g., `plugin:org.opensearch.security.systemindex.sampleplugin.SystemIndexPlugin1`)
- The `:` character is forbidden in regular usernames, ensuring plugin identities cannot be spoofed
- Plugin users can only perform index operations on system indices they registered via `SystemIndexPlugin.getSystemIndexDescriptors()`
- Cluster actions (like `cluster:monitor/health`) are not permitted for plugin subjects by default

#### Security Filter Changes

The `SecurityFilter` now:
- Skips automatic privilege bypass when a plugin user is detected
- Evaluates system index access based on plugin ownership
- Allows plugins to perform bulk operations on their own system indices

```java
// Example: Plugin accessing its own system index
pluginSubject.runAs(() -> {
    client.index(new IndexRequest(SYSTEM_INDEX_1)
        .source("{\"content\":1}", XContentType.JSON));
    return null;
});
```

### Migration from ThreadContext Stashing

Previously, plugins used `threadContext.stashContext()` to perform privileged operations:

```java
// Old approach (deprecated)
try (ThreadContext.StoredContext ctx = threadContext.stashContext()) {
    // Operations on system index
}
```

The new approach uses `pluginSubject.runAs()`:

```java
// New approach (v2.19.0+)
pluginSubject.runAs(() -> {
    // Operations on system index
    return null;
});
```

## Limitations

- Plugins cannot perform cluster-level actions (e.g., `cluster:monitor/health`) using `pluginSubject.runAs()`
- Plugins can only access system indices they explicitly registered
- Bulk operations targeting multiple system indices from different plugins will be rejected
- The feature requires `plugins.security.system_indices.enabled` to be `true` (default)

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#5028](https://github.com/opensearch-project/security/pull/5028) | Backport #4896 to 2.x - Implement new extension points in IdentityPlugin | - |
| [#5037](https://github.com/opensearch-project/security/pull/5037) | Implement IdentityPlugin extension points for legacy authz code path | [#4439](https://github.com/opensearch-project/security/issues/4439) |
| [#5032](https://github.com/opensearch-project/security/pull/5032) | Fix plugin search operations on system index with pluginSubject.runAs | - |
| [#5055](https://github.com/opensearch-project/security/pull/5055) | Fix plugin update operations on system index with pluginSubject.runAs | - |

### Related Issues

- [#4439](https://github.com/opensearch-project/security/issues/4439): RFC - Strengthen System Index Protection in the Plugin Ecosystem
