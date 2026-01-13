---
tags:
  - opensearch
---
# Snapshot Restore Settings

## Summary

OpenSearch v2.19.0 introduces a new `UnmodifiableOnRestore` setting property that prevents certain index settings from being modified or removed during snapshot restore operations. This enhancement provides better data integrity protection by ensuring critical settings remain unchanged when restoring indexes from snapshots.

## Details

### What's New in v2.19.0

A new `Setting.Property.UnmodifiableOnRestore` property has been added to the OpenSearch settings framework. Settings marked with this property cannot be:
- Modified via `index_settings` parameter during restore
- Removed via `ignore_index_settings` parameter during restore

### Technical Changes

#### New Setting Property

The `UnmodifiableOnRestore` property is added to the `Setting.Property` enum:

```java
/**
 * Mark this setting as immutable on snapshot restore
 * i.e. the setting will not be allowed to be removed or modified during restore
 */
UnmodifiableOnRestore
```

#### Settings Now Protected

The following settings are now marked as `UnmodifiableOnRestore`:

| Setting | Description |
|---------|-------------|
| `index.number_of_shards` | Number of primary shards for the index |
| `index.version.created` | Version of OpenSearch that created the index |

#### Validation Rules

- `UnmodifiableOnRestore` settings must have `IndexScope` property
- `UnmodifiableOnRestore` settings cannot be `Dynamic`
- Attempting to modify or remove these settings during restore throws `SnapshotRestoreException`

### Error Messages

When attempting to modify an `UnmodifiableOnRestore` setting:
```
cannot modify UnmodifiableOnRestore setting [index.number_of_shards] on restore
```

When attempting to remove an `UnmodifiableOnRestore` setting:
```
cannot remove UnmodifiableOnRestore setting [index.number_of_shards] on restore
```

### Use Case

This feature was primarily introduced to support the k-NN plugin's requirement to make `index.knn` setting immutable during snapshot restore. The k-NN plugin can now mark its settings with `UnmodifiableOnRestore` to prevent users from accidentally changing the k-NN configuration when restoring indexes.

## Limitations

- Only applies to index-scoped settings
- Cannot be combined with `Dynamic` property
- Existing `USER_UNREMOVABLE_SETTINGS` and `USER_UNMODIFIABLE_SETTINGS` lists in `RestoreService` continue to function independently

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16957](https://github.com/opensearch-project/OpenSearch/pull/16957) | Added new Setting property UnmodifiableOnRestore to prevent updating settings on restore snapshot | [k-NN#2334](https://github.com/opensearch-project/k-NN/issues/2334) |

### Related Issues

- [k-NN#2334](https://github.com/opensearch-project/k-NN/issues/2334) - Original issue requesting immutable k-NN settings
- [#17019](https://github.com/opensearch-project/OpenSearch/issues/17019) - Related OpenSearch issue

### Documentation

- [Snapshot Restore Documentation](https://docs.opensearch.org/2.19/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/)
