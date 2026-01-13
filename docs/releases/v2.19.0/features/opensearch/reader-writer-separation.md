---
tags:
  - opensearch
---
# Reader Writer Separation

## Summary

In v2.19.0, Reader-Writer Separation is now limited to remote-store-enabled clusters only. This change simplifies the architecture by removing support for document replication-based search replicas and updates the recovery flow for search replicas to use empty store recovery instead of peer recovery, eliminating primary shard communication during recovery.

## Details

### What's New in v2.19.0

This release introduces significant changes to how search replicas are initialized and managed:

1. **Remote Store Requirement**: Search replicas now require remote store to be enabled. The validation error message changed from requiring `SEGMENT` replication type to requiring `remote_store.enabled = true`.

2. **Empty Store Recovery**: Search replicas now recover using `EmptyStoreRecoverySource` instead of `PeerRecoverySource`, syncing segments directly from remote store without primary communication.

3. **In-Sync Allocation ID Exclusion**: Search replicas are excluded from the in-sync allocation ID set, ensuring primaries don't track or validate search replica presence.

4. **Throttling Decider Updates**: The throttling allocation decider now handles search replicas specially, allowing remote-based search replicas to bypass outgoing recovery limits.

### Technical Changes

```mermaid
flowchart TB
    subgraph "Before v2.19.0"
        A1[Search Replica] -->|Peer Recovery| P1[Primary Shard]
        P1 -->|Segment Transfer| A1
    end
    
    subgraph "v2.19.0+"
        A2[Search Replica] -->|Empty Store Recovery| RS[Remote Store]
        RS -->|Direct Segment Sync| A2
        P2[Primary Shard] -.->|No Communication| A2
    end
```

### Key Implementation Details

| Change | Description |
|--------|-------------|
| Recovery Source | Changed from `PeerRecoverySource` to `EmptyStoreRecoverySource` for search replicas |
| Validation | Now checks `SETTING_REMOTE_STORE_ENABLED` instead of `INDEX_REPLICATION_TYPE_SETTING` |
| Allocation IDs | Search replicas excluded from `allAllocationIds` set in routing table |
| Throttling | Remote-based search replicas bypass primary outgoing recovery limits |
| Retention Leases | Search replicas filtered from peer recovery retention lease renewal |

### Recovery Flow Changes

The recovery flow for search replicas has been updated:

1. **Initial Recovery**: Uses `EmptyStoreRecoverySource` to bootstrap from remote store
2. **Existing Store Recovery**: After restart, uses `ExistingStoreRecoverySource` with local data
3. **Remote Store Restore**: During restore operations, search replicas maintain their assignment if already allocated

## Limitations

- Search replicas are only supported on remote-store-enabled clusters
- Document replication clusters cannot use search replicas
- Search replicas cannot be promoted to primary shards
- Requires segment replication to be enabled (implicit with remote store)

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16760](https://github.com/opensearch-project/OpenSearch/pull/16760) | Limit RW separation to remote store enabled clusters and update recovery flow | [#15952](https://github.com/opensearch-project/OpenSearch/issues/15952) |

### Related Issues
- [#15952](https://github.com/opensearch-project/OpenSearch/issues/15952): [RW Separation] Change search replica recovery flow
