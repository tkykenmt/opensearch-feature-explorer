---
tags:
  - opensearch
---
# System Index Registry

## Summary

The System Index Registry is a centralized mechanism in OpenSearch for managing and querying system index descriptors registered by plugins. It provides static helper methods to determine if index expressions match system index patterns, enabling plugin-aware system index protection and access control.

## Details

### Architecture

```mermaid
graph TB
    subgraph "Node Startup"
        Node[Node.java] --> |collect descriptors| Plugins[SystemIndexPlugin instances]
        Plugins --> |getSystemIndexDescriptors| SIM[SystemIndexDescriptorMap]
        SIM --> |register| SIR[SystemIndexRegistry]
    end
    
    subgraph "SystemIndexRegistry"
        SIR --> SMAP[Descriptor Map<br/>pluginClassName → Collection&lt;Descriptor&gt;]
        SIR --> SPAT[Pattern Array<br/>String[]]
        SIR --> TASK[Task Index Descriptor<br/>.tasks*]
    end
    
    subgraph "Runtime Queries"
        SEC[Security Plugin] --> |matchesSystemIndexPattern| SIR
        SEC --> |matchesPluginSystemIndexPattern| SIR
        SI[SystemIndices] --> |getAllDescriptors| SIR
    end
```

### Components

| Component | Description |
|-----------|-------------|
| `SystemIndexRegistry` | Central registry holding all system index descriptors and providing query methods |
| `SystemIndexDescriptor` | Describes a system index with pattern and description |
| `SystemIndices` | Facade class that delegates to SystemIndexRegistry for index matching |

### Key Methods

| Method | Description |
|--------|-------------|
| `matchesSystemIndexPattern(Set<String>)` | Returns indices matching any registered system index pattern |
| `matchesPluginSystemIndexPattern(String, Set<String>)` | Returns indices matching a specific plugin's system index patterns |
| `getAllDescriptors()` | Returns all registered system index descriptors |

### Configuration

Plugins register system indices by implementing `SystemIndexPlugin`:

```java
public class MyPlugin extends Plugin implements SystemIndexPlugin {
    @Override
    public Collection<SystemIndexDescriptor> getSystemIndexDescriptors(Settings settings) {
        return Collections.singletonList(
            new SystemIndexDescriptor(".my-plugin-index*", "My Plugin System Index")
        );
    }
}
```

### Usage Example

```java
// Check if indices are system indices
Set<String> indices = Set.of(".opendistro_security", "my-data-index");
Set<String> systemIndices = SystemIndexRegistry.matchesSystemIndexPattern(indices);
// Returns: {".opendistro_security"}

// Check if indices belong to a specific plugin
Set<String> pluginIndices = SystemIndexRegistry.matchesPluginSystemIndexPattern(
    "org.opensearch.security.OpenSearchSecurityPlugin",
    indices
);
// Returns: {".opendistro_security"}
```

### Built-in System Indices

The registry automatically includes the Task Result Index:

| Pattern | Description |
|---------|-------------|
| `.tasks*` | Task Result Index for storing async task results |

## Limitations

- The `SystemIndexRegistry` is marked as `@ExperimentalApi` and may change in future versions
- Pattern overlap between plugins is detected at registration time and throws `IllegalStateException`
- Plugin class names must be unique; duplicate source names cause `IllegalArgumentException`

## Change History

- **v2.16.0** (2024-08-06): Initial implementation
  - Created `SystemIndexRegistry` class with `matchesSystemIndexPattern` method
  - Added `matchesPluginSystemIndexPattern` for plugin-specific matching
  - Changed method signatures from `List` to `Set` for better performance
  - Promoted `SystemIndexDescriptor` to `@PublicApi`
  - Changed plugin key from `getSimpleName()` to `getCanonicalName()` for uniqueness

## References

### Documentation

- [System indexes](https://docs.opensearch.org/2.16/security/configuration/system-indices/) - OpenSearch documentation on system index configuration

### Pull Requests

| Version | PR | Description |
|---------|-----|-------------|
| v2.16.0 | [#14415](https://github.com/opensearch-project/OpenSearch/pull/14415) | Create SystemIndexRegistry with helper method matchesSystemIndex |
| v2.16.0 | [#14750](https://github.com/opensearch-project/OpenSearch/pull/14750) | Add matchesPluginSystemIndexPattern to SystemIndexRegistry |

### Related Issues

- [security#4439](https://github.com/opensearch-project/security/issues/4439) - RFC: Strengthen System Index Protection in the Plugin Ecosystem
