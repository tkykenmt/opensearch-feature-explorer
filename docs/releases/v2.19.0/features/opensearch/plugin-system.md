---
tags:
  - opensearch
---
# Plugin System

## Summary

OpenSearch v2.19.0 introduces support for optional extended plugins, allowing plugins to declare dependencies on other plugins as optional rather than required. This enables plugins to extend functionality from other plugins (like the Security plugin) without requiring those plugins to be installed.

## Details

### What's New in v2.19.0

This release adds a new syntax for declaring optional plugin dependencies in the `extendedPlugins` configuration. Previously, when a plugin extended another plugin through SPI (Service Provider Interface), the extended plugin was required to be installed. Now plugins can mark extended plugins as optional.

### Configuration

Plugins can declare optional dependencies using the new syntax in their build configuration:

```groovy
opensearchplugin {
    name 'opensearch-plugin'
    description 'OpenSearch Plugin'
    classname 'org.opensearch.example.ExamplePlugin'
    extendedPlugins = ['opensearch-security;optional=true']
}
```

The `;optional=true` suffix indicates that the dependency is optional.

### Technical Changes

| Component | Change |
|-----------|--------|
| `PluginInfo` | Added `optionalExtendedPlugins` field to track which extended plugins are optional |
| `PluginInfo` | Added `isExtendedPluginOptional(String)` method to check if a specific extended plugin is optional |
| `PluginsService` | Modified to warn instead of fail when optional dependencies are missing |
| `PluginsService` | Updated JAR hell checking to skip optional missing plugins |
| `PluginsService` | Updated plugin loading to skip optional missing plugins |

### Behavior

When installing a plugin with optional dependencies:

1. If the optional dependency is not installed, a warning is displayed:
   ```
   WARN  org.opensearch.plugins.PluginsService - Missing plugin [opensearch-security], dependency of [my-plugin]
   WARN  org.opensearch.plugins.PluginsService - Some features of this plugin may not function without the dependencies being installed.
   ```

2. Installation proceeds successfully
3. Features requiring the optional dependency will not be available

When the optional dependency is installed, all features work normally.

### Use Case: Plugin Resource Sharing

The primary motivation for this feature is to enable the Security plugin to offer a SPI for resource sharing. Other plugins can extend the Security plugin to share resources, but since Security is optional, plugins need to work both with and without it installed.

This enables scenarios like:
- Plugins sharing resources through Security's SPI when Security is installed
- Same plugins functioning (without resource sharing) when Security is not installed

## Limitations

- Optional dependencies only affect installation and loading behavior
- Features requiring the optional plugin will not work if the plugin is not installed
- The plugin developer must handle the case where optional dependencies are missing

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16909](https://github.com/opensearch-project/OpenSearch/pull/16909) | Allow extended plugins to be optional | Enables plugin resource sharing use-case |
