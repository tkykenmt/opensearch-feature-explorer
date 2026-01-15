---
tags:
  - opensearch
---
# Remote Store

## Summary

OpenSearch v2.16.0 introduces three enhancements to Remote Store: a rate limiter for low priority uploads, refactored remote routing table service aligned with remote state interfaces, and shard-diff path support in diff manifests to reduce remote store read calls.

## Details

### What's New in v2.16.0

#### Rate Limiter for Low Priority Uploads

A new rate limiter has been added specifically for low priority remote store uploads. Previously, the existing rate limiter applied to both high and low priority uploads without distinction. This enhancement allows operators to control low priority upload bandwidth separately, preventing low priority operations from consuming resources needed for critical uploads.

**Configuration**:
```yaml
# Repository settings
max_remote_low_priority_upload_bytes_per_sec: <value>
```

The rate limiter applies to operations like clone index uploads that are marked as low priority. When content length exceeds 15GB, uploads are automatically treated as low priority.

#### Remote Routing Table Service Refactoring

The `RemoteRoutingTableService` has been refactored to implement remote table entities, aligning with the remote state interfaces pattern. Key changes include:

- Introduction of `RemoteRoutingTableBlobStore` for managing routing table blob storage
- New `RemoteIndexRoutingTable` class extending `AbstractRemoteWritableBlobEntity`
- Simplified API with `getAsyncIndexRoutingWriteAction` and `getAsyncIndexRoutingReadAction` methods
- Settings moved to `RemoteRoutingTableBlobStore`:
  - `cluster.remote_store.routing_table.path_type` (default: `HASHED_PREFIX`)
  - `cluster.remote_store.routing_table.path_hash_algo` (default: `FNV_1A_BASE64`)

#### Shard-Diff Path in Diff Manifest

A new shard-diff path has been added to the diff manifest to reduce the number of read calls to remote store. This optimization stores incremental routing table differences rather than full routing tables when only shard-level changes occur.

Key components:
- `RoutingTableIncrementalDiff`: Represents differences between routing tables
- `RemoteRoutingTableDiff`: Remote store entity for routing table diffs
- New manifest codec version `CODEC_V3` with `indicesRoutingDiffPath` field

## Limitations

- Rate limiter for low priority uploads requires repository reconfiguration to take effect
- Remote routing table feature requires experimental feature flag `REMOTE_PUBLICATION_EXPERIMENTAL` to be enabled

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14374](https://github.com/opensearch-project/OpenSearch/pull/14374) | Rate limiter for remote store low priority uploads | [#14373](https://github.com/opensearch-project/OpenSearch/issues/14373) |
| [#14668](https://github.com/opensearch-project/OpenSearch/pull/14668) | Refactor remote-routing-table service inline with remote state interfaces | [#14067](https://github.com/opensearch-project/OpenSearch/issues/14067) |
| [#14684](https://github.com/opensearch-project/OpenSearch/pull/14684) | Add shard-diff path to diff manifest to reduce number of read calls remote store | [#15125](https://github.com/opensearch-project/OpenSearch/issues/15125) |

### Documentation
- [Remote-backed storage](https://docs.opensearch.org/2.16/tuning-your-cluster/availability-and-recovery/remote-store/index/)
- [Remote cluster state](https://docs.opensearch.org/2.16/tuning-your-cluster/availability-and-recovery/remote-store/remote-cluster-state/)
