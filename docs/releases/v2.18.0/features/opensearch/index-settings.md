---
tags:
  - domain/core
  - component/server
  - indexing
---
# Index Settings

## Summary

This release fixes two bugs related to index settings default value handling when settings are explicitly set to `null`. Previously, setting `index.number_of_replicas` or `index.number_of_routing_shards` to `null` did not properly honor cluster-level defaults or calculate correct values.

## Details

### What's New in v2.18.0

Two bug fixes improve the consistency of index settings behavior when users explicitly set values to `null`:

1. **Replica count default handling**: When updating `index.number_of_replicas` to `null`, the system now correctly uses the `cluster.default_number_of_replicas` setting instead of always defaulting to `1`.

2. **Routing shards default handling**: When creating an index with `index.number_of_routing_shards` set to `null`, the system now calculates the correct default value (same as when the setting is omitted) instead of incorrectly using `number_of_shards`.

### Technical Changes

#### Fix 1: Replica Count Default (PR #14948)

**Problem**: When calling the Update Settings API with `index.number_of_replicas: null`, the replica count always reset to `1`, ignoring the `cluster.default_number_of_replicas` cluster setting.

**Solution**: Modified `MetadataUpdateSettingsService` to read the cluster's default replica count setting and use it as the fallback value.

```java
// Before: Always used hardcoded default of 1
indexSettings.put(
    IndexMetadata.SETTING_NUMBER_OF_REPLICAS,
    IndexMetadata.INDEX_NUMBER_OF_REPLICAS_SETTING.get(Settings.EMPTY)
);

// After: Uses cluster setting as default
final int defaultReplicaCount = clusterService.getClusterSettings()
    .get(Metadata.DEFAULT_REPLICA_COUNT_SETTING);
indexSettings.put(IndexMetadata.SETTING_NUMBER_OF_REPLICAS, defaultReplicaCount);
```

#### Fix 2: Routing Shards Default (PR #16331)

**Problem**: When creating an index with `index.number_of_routing_shards: null`, the value incorrectly defaulted to `number_of_shards` instead of the calculated optimal value for index splitting.

**Solution**: Modified `MetadataCreateIndexService.getIndexNumberOfRoutingShards()` to check if the setting value is actually `null` rather than just checking if the setting exists.

```java
// Before: Checked if setting exists (true even for null value)
if (IndexMetadata.INDEX_NUMBER_OF_ROUTING_SHARDS_SETTING.exists(indexSettings)) {
    routingNumShards = IndexMetadata.INDEX_NUMBER_OF_ROUTING_SHARDS_SETTING.get(indexSettings);
}

// After: Checks if actual value is non-null
if (indexSettings.get(IndexMetadata.INDEX_NUMBER_OF_ROUTING_SHARDS_SETTING.getKey()) != null) {
    routingNumShards = IndexMetadata.INDEX_NUMBER_OF_ROUTING_SHARDS_SETTING.get(indexSettings);
}
```

### Usage Example

#### Setting Replica Count to Null

```bash
# Set cluster default
PUT _cluster/settings
{
  "persistent": {
    "cluster.default_number_of_replicas": 3
  }
}

# Create index with custom replica count
PUT my-index
{
  "settings": {
    "number_of_replicas": 2
  }
}

# Reset to cluster default (now correctly uses 3, not 1)
PUT my-index/_settings
{
  "index": {
    "number_of_replicas": null
  }
}
```

#### Setting Routing Shards to Null

```bash
# Create index with null routing shards (now correctly calculates optimal value)
PUT my-index
{
  "settings": {
    "number_of_routing_shards": null,
    "number_of_shards": 2
  }
}

# Verify routing_num_shards is calculated (e.g., 1024), not equal to number_of_shards (2)
GET _cluster/state/metadata/my-index
```

## Limitations

- These fixes only affect new operations after upgrading to v2.18.0
- Existing indexes with incorrect settings are not automatically corrected

## References

### Documentation
- [Index Settings Documentation](https://docs.opensearch.org/2.18/install-and-configure/configuring-opensearch/index-settings/): Official documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#14948](https://github.com/opensearch-project/OpenSearch/pull/14948) | Fix update settings with null replica not honoring cluster setting |
| [#16331](https://github.com/opensearch-project/OpenSearch/pull/16331) | Fix wrong default value when setting `index.number_of_routing_shards` to null |

### Issues (Design / RFC)
- [Issue #14810](https://github.com/opensearch-project/OpenSearch/issues/14810): Bug report for replica count default
- [Issue #16327](https://github.com/opensearch-project/OpenSearch/issues/16327): Bug report for routing shards default

## Related Feature Report

- Full feature documentation
