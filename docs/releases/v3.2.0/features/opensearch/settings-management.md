---
tags:
  - indexing
---

# Settings Management

## Summary

This bugfix resolves a critical issue where cluster settings updates would fail if archived settings were present, even when attempting to update unrelated settings. Prior to this fix, users who upgraded from older OpenSearch versions could become completely blocked from modifying any cluster settings.

## Details

### What's New in v3.2.0

OpenSearch now ignores archived settings when validating settings updates. This allows users to modify cluster and index settings without first having to clear archived settings.

### Technical Changes

#### Problem Background

When OpenSearch encounters unknown settings (typically from plugins that were removed or settings that were deprecated), it moves them to an "archived" namespace. For example, `plugins.index_state_management.template_migration.control` becomes `archived.plugins.index_state_management.template_migration.control`.

Before this fix, the settings validation logic would fail on these archived settings when attempting to update any setting, resulting in errors like:

```json
{
  "error": {
    "root_cause": [{
      "type": "settings_exception",
      "reason": "unknown setting [archived.plugins.index_state_management.metadata_migration.status] please check that any required plugins are installed, or check the breaking changes documentation for removed settings"
    }]
  },
  "status": 400
}
```

#### Solution

The fix modifies `MetadataUpdateSettingsService` to pass `ignoreArchivedSettings: true` when validating settings updates. This allows the validation to skip archived settings while still validating all other settings.

#### Code Changes

| File | Change |
|------|--------|
| `MetadataUpdateSettingsService.java` | Added `ignoreArchivedSettings` parameter to `indexScopedSettings.validate()` calls |
| `ArchivedIndexSettingsIT.java` | Added test to verify unrelated settings can be updated when archived settings are present |

### Usage Example

After this fix, users can update settings normally even with archived settings present:

```bash
# This now works even if archived settings exist
PUT /_cluster/settings
{
  "persistent": {
    "cluster.max_shards_per_node": 500
  }
}
```

### Migration Notes

No migration required. This fix is automatically applied when upgrading to v3.2.0.

## Limitations

- Archived settings themselves still cannot be modified on open indices (must close the index first)
- This fix only addresses the validation blocking issue; archived settings remain in the cluster state until explicitly cleared

## References

### Documentation
- [Cluster Settings API](https://docs.opensearch.org/3.2/api-reference/cluster-api/cluster-settings/): Official documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#18885](https://github.com/opensearch-project/OpenSearch/pull/18885) | Ignore archived settings on update |

### Issues (Design / RFC)
- [Issue #8714](https://github.com/opensearch-project/OpenSearch/issues/8714): Original bug report - Unable to change any cluster setting
- [Issue #18515](https://github.com/opensearch-project/OpenSearch/issues/18515): Cannot update cluster settings after upgrading to 3.0.0

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/settings-management.md)
