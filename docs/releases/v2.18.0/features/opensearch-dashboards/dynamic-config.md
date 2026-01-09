# Dynamic Config Bugfixes

## Summary

This release fixes several bugs related to dynamic configuration management in OpenSearch Dashboards, particularly around workspace integration and index/alias handling during startup.

## Details

### What's New in v2.18.0

Three key bugfixes were introduced to improve the reliability of dynamic configuration:

1. **Config saved objects no longer auto-append workspaces** - When creating config saved objects, the system no longer automatically appends workspace IDs, ensuring global configs remain accessible across all workspaces.

2. **Global config discovery during upgrades** - The advanced settings config upgrade process now correctly finds global configs by using the `sortField: 'buildNum'` parameter.

3. **Dynamic config index/alias validation** - Fixed a bug where the system could fail if the `.opensearch_dashboards_dynamic_config` alias existed but pointed to an invalid or missing index.

### Technical Changes

#### Index and Alias Handling

The `OpenSearchConfigStoreClient` now properly handles various edge cases during startup:

| Scenario | Alias Present? | Index State | Behavior |
|----------|---------------|-------------|----------|
| Fresh install | No | No index | Create new index with alias |
| Orphaned index | No | Index exists | Update index with alias |
| Valid setup | Yes | Valid index | Do nothing |
| Invalid alias | Yes | Multiple/wrong indices | Throw error |

#### New Utility Functions

| Function | Description |
|----------|-------------|
| `isDynamicConfigIndex()` | Validates if an index name matches the dynamic config pattern |
| `extractVersionFromDynamicConfigIndex()` | Extracts version number from index name |
| `searchLatestConfigIndex()` | Finds the most recent dynamic config index |

#### Workspace Integration Fix

The `WorkspaceIdConsumerWrapper` was updated to:
- Skip workspace ID injection for `config` type saved objects
- Allow global config discovery when searching with `sortField: 'buildNum'`

```typescript
// Config type objects bypass workspace filtering
if (this.isConfigType(type)) {
  return options; // Don't append workspace ID
}
```

### Usage Example

The fixes are transparent to users. The dynamic config system now correctly handles:

```bash
# Valid index patterns
.opensearch_dashboards_dynamic_config_1
.opensearch_dashboards_dynamic_config_4

# Invalid patterns (will be ignored)
.opensearch_dashboards_dynamic_config_foo
.opensearch_dashboards_dynamic_config_
```

## Limitations

- If the alias points to multiple indices or a non-dynamic-config index, the server will fail to start with an error message instructing the user to remove the invalid alias.

## Related PRs

| PR | Description |
|----|-------------|
| [#8160](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8160) | Fix config related issues and dedup category in landing page |
| [#8184](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8184) | Fix bug when dynamic config index and alias are checked |

## References

- [PR #8160](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8160): Config related issues fix
- [PR #8184](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8184): Dynamic config index/alias validation fix
- [Dynamic configuration in OpenSearch Dashboards](https://docs.opensearch.org/2.18/security/multi-tenancy/dynamic-config/): Official documentation

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch-dashboards/dynamic-config.md)
