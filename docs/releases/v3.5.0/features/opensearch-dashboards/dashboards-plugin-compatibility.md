---
tags:
  - opensearch-dashboards
---
# Dashboards Plugin Compatibility

## Summary

In v3.5.0, OpenSearch Dashboards relaxes plugin version compatibility enforcement. Previously, plugins with a version mismatch would cause errors that prevented server startup or plugin installation. Now, version mismatches produce warnings instead of errors, and the default validation mode is changed from `strict` to `ignore` across all components.

## Details

### What's New in v3.5.0

Two complementary changes make plugin version compatibility more permissive:

1. **Server-side manifest parser now warns instead of errors** (PR #11179): The `plugin_manifest_parser.ts` no longer throws a `PluginDiscoveryError.incompatibleVersion` when a plugin's version doesn't match the OSD version. Instead, it logs a warning and allows the plugin to load. This means OSD can run with older plugin versions without being blocked at startup.

2. **Default validation mode changed to `ignore`** (PR #11183): The default value of `--single-version` is changed from `strict` to `ignore` across multiple components:

| Component | Setting | Before | After |
|-----------|---------|--------|-------|
| CLI plugin install (`index.js`) | `--single-version` default | `strict` | `ignore` |
| Settings parser (`settings.js`) | `singleVersion` fallback | `strict` | `ignore` |
| OpenSearch config (`opensearch_config.ts`) | `ignoreVersionMismatch` | `false` | `true` |
| Dependency validator (`validate_dependencies.ts`) | `singleVersionResolution` | `STRICT` | `IGNORE` |

### Technical Changes

In `plugin_manifest_parser.ts`, the version check was changed from:
```typescript
throw PluginDiscoveryError.incompatibleVersion(manifestPath, new Error(...));
```
to:
```typescript
log.warn(`Plugin "${manifest.id}" is version "${expectedVersion}", but used OpenSearch Dashboards version is "${packageInfo.version}".`);
```

This allows incompatible plugins to be discovered and loaded, with a warning logged to the console for debugging purposes.

## Limitations

- Version mismatch warnings do not guarantee that the plugin will function correctly with a different OSD version
- Plugins with `opensearchDashboardsVersion: "opensearchDashboards"` continue to bypass all version checks
- Users can still enforce strict mode by explicitly passing `--single-version strict`

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#11179](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11179) | Allow external plugins to be a different version from OSD (warn instead of error) | - |
| [#11183](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11183) | Make single-version=ignore as default | Follow-up to #11179 |
