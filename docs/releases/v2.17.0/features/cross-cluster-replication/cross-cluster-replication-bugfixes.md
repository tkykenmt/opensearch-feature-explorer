---
tags:
  - domain/data
  - component/server
  - indexing
---
# Cross-Cluster Replication Bugfixes

## Summary

This release fixes the cross-cluster replication integration tests to use the correct cluster setting names after the Remote Store Migration feature was moved from experimental to GA in OpenSearch core. The setting names were updated from `remote_store.compatibility_mode` and `migration.direction` to `cluster.remote_store.compatibility_mode` and `cluster.migration.direction` respectively.

## Details

### What's New in v2.17.0

The integration test `test operations are fetched from lucene when leader is in mixed mode` was updated to use the correct cluster setting names following changes in OpenSearch core PR #14100.

### Technical Changes

#### Setting Name Updates

| Old Setting | New Setting |
|-------------|-------------|
| `remote_store.compatibility_mode` | `cluster.remote_store.compatibility_mode` |
| `migration.direction` | `cluster.migration.direction` |

#### Build Configuration Changes

1. Removed the experimental feature flag `opensearch.experimental.feature.remote_store.migration.enabled` from test configuration as it's no longer needed (feature is now GA)
2. Re-enabled the previously excluded integration test `test operations are fetched from lucene when leader is in mixed mode`

### Code Changes

The test file `StartReplicationIT.kt` was updated to use the new cluster-prefixed setting names:

```kotlin
val entityAsString = """
    {
      "persistent": {
        "cluster.remote_store.compatibility_mode": "mixed",
        "cluster.migration.direction" : "remote_store"
      }
    }""".trimMargin()
```

### Migration Notes

No user action required. This is an internal test fix that aligns with the Remote Store Migration GA changes in OpenSearch core.

## Limitations

- This change only affects integration tests, not production functionality

## References

### Documentation
- [Cross-cluster replication documentation](https://docs.opensearch.org/2.17/tuning-your-cluster/replication-plugin/index/)
- [Remote-backed storage migration](https://docs.opensearch.org/2.17/tuning-your-cluster/availability-and-recovery/remote-store/migrating-to-remote/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#1412](https://github.com/opensearch-project/cross-cluster-replication/pull/1412) | Updating remote-migration IT with correct setting name |
| [#14100](https://github.com/opensearch-project/OpenSearch/pull/14100) | Move Remote Store Migration from DocRep to GA (OpenSearch core) |

## Related Feature Report

- Full feature documentation
