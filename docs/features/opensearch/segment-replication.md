---
tags:
  - indexing
  - search
---

# Segment Replication

## Summary

Segment replication is an alternative replication strategy in OpenSearch that copies Lucene segment files directly from primary shards to replica shards, instead of re-indexing documents on each replica. This approach significantly improves indexing throughput (up to 40% higher) and reduces CPU/memory utilization on replica nodes, at the cost of increased network bandwidth usage. Segment replication is particularly beneficial for write-heavy workloads with lower search requirements.

## Details

### Architecture

```mermaid
graph TB
    subgraph "Primary Shard"
        PS[Primary Shard]
        IDX[Indexing]
        SEG[Segment Files]
        CP[Checkpoint]
        IDX --> SEG
        SEG --> CP
    end
    
    subgraph "Segment Replicator"
        SR[SegmentReplicator]
        RCS[ReplicationCheckpointStats]
        SR --> RCS
    end
    
    subgraph "Replica Shards"
        RS1[Replica 1]
        RS2[Replica 2]
    end
    
    CP --> |Checkpoint Notification| SR
    SR --> |Copy Segments| RS1
    SR --> |Copy Segments| RS2
```

### Data Flow

```mermaid
flowchart TB
    A[Primary Refresh] --> B[Create Checkpoint]
    B --> C[Notify Replicas]
    C --> D[SegmentReplicator.startReplication]
    D --> E[Fetch Segment Files]
    E --> F[Apply to Replica]
    F --> G[Update Checkpoint Stats]
    G --> H[Prune Old Checkpoints]
```

### Components

| Component | Description |
|-----------|-------------|
| `SegmentReplicator` | Manages segment replication events on replicas, tracks checkpoint stats |
| `ReplicationCheckpoint` | Represents a point-in-time state of segments on primary shard |
| `ReplicationCheckpointStats` | Tracks bytes behind and timestamp for each checkpoint |
| `SegmentReplicationTarget` | Orchestrates a single replication event |
| `SegmentReplicationSource` | Source for fetching segment files (node-to-node or remote store) |

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `index.replication.type` | Replication type: `SEGMENT` or `DOCUMENT` | `DOCUMENT` |
| `cluster.indices.replication.strategy` | Default replication type for new indexes | `DOCUMENT` |
| `cluster.index.restrict.replication.type` | Enforce cluster-level replication type | `false` |
| `segrep.pressure.enabled` | Enable segment replication backpressure | `false` |
| `cluster.routing.allocation.balance.prefer_primary` | Balance primary shards across nodes | `false` |
| `indices.publish_check_point.retry_timeout` | Retry timeout for publish checkpoint action (v3.0.0+) | `5m` |

### Replication Metrics

| Metric | Description |
|--------|-------------|
| `max_bytes_behind` | Maximum bytes replica is behind primary |
| `total_bytes_behind` | Total bytes behind across all replicas |
| `max_replication_lag` | Maximum time (ms) replica is behind primary |

### Usage Example

Create an index with segment replication:

```json
PUT /my-index
{
  "settings": {
    "index": {
      "replication.type": "SEGMENT",
      "number_of_replicas": 1
    }
  }
}
```

Enable recommended settings for segment replication:

```json
PUT /_cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.balance.prefer_primary": true,
    "segrep.pressure.enabled": true
  }
}
```

Check segment replication status:

```
GET _cat/segment_replication?v
```

## Limitations

- Requires reindexing to enable on existing indexes
- Does not support `refresh=wait_for` or `refresh=true` policies
- Cross-cluster replication does not use segment replication
- Increased network bandwidth usage on primary shards (node-to-node mode)
- Get/MultiGet/TermVector operations route to primary for strong reads

## Change History

- **v3.3.0** (2025-09-09): Fixed NullPointerException in SegmentReplicator.getSegmentReplicationStats() caused by race condition; Fixed reference count control in NRTReplicationEngine#acquireLastIndexCommit to prevent NoSuchFileException
- **v3.2.0** (2025-07-01): Fixed replication lag computation to use epoch-based timestamps and corrected checkpoint pruning logic
- **v3.0.0** (2025-05-13): Implemented shard-level stats computation on replicas; Fixed skewed lag metric when same checkpoint published twice; Increased default segment counter step size from 10 to 100,000; Added configurable publish checkpoint retry timeout setting

## References

### Documentation
- [Segment Replication Documentation](https://docs.opensearch.org/3.0/tuning-your-cluster/availability-and-recovery/segment-replication/index/): Official documentation
- [Segment Replication Backpressure](https://docs.opensearch.org/3.0/tuning-your-cluster/availability-and-recovery/segment-replication/backpressure/): Backpressure mechanism
- [CAT Segment Replication API](https://docs.opensearch.org/3.0/api-reference/cat/cat-segment-replication/): API for viewing metrics

### Blog Posts
- [Segment Replication Blog](https://opensearch.org/blog/segment-replication/): Introduction blog post

### Pull Requests
| Version | PR | Description | Related Issue |
|---------|-----|-------------|---------------|
| v3.3.0 | [#19214](https://github.com/opensearch-project/OpenSearch/pull/19214) | Add reference count control in NRTReplicationEngine#acquireLastIndexCommit | [#19213](https://github.com/opensearch-project/OpenSearch/issues/19213) |
| v3.3.0 | [#18997](https://github.com/opensearch-project/OpenSearch/pull/18997) | Fix NullPointerException in segment replicator |   |
| v3.2.0 | [#18602](https://github.com/opensearch-project/OpenSearch/pull/18602) | Fix bugs in replication lag computation | [#18437](https://github.com/opensearch-project/OpenSearch/issues/18437) |
| v3.0.0 | [#17055](https://github.com/opensearch-project/OpenSearch/pull/17055) | Implemented computation of segment replication stats at shard level | [#16801](https://github.com/opensearch-project/OpenSearch/issues/16801) |
| v3.0.0 | [#17831](https://github.com/opensearch-project/OpenSearch/pull/17831) | Avoid skewed segment replication lag metric | [#10764](https://github.com/opensearch-project/OpenSearch/issues/10764) |
| v3.0.0 | [#17568](https://github.com/opensearch-project/OpenSearch/pull/17568) | Increase the default segment counter step size when replica promoting | [#17566](https://github.com/opensearch-project/OpenSearch/issues/17566) |
| v3.0.0 | [#17749](https://github.com/opensearch-project/OpenSearch/pull/17749) | Add cluster setting for retry timeout of publish checkpoint tx action | [#17595](https://github.com/opensearch-project/OpenSearch/issues/17595) |

### Issues (Design / RFC)
- [Issue #19213](https://github.com/opensearch-project/OpenSearch/issues/19213): Bug report for NRTReplicationEngine file deletion issue
- [Issue #18437](https://github.com/opensearch-project/OpenSearch/issues/18437): Bug report for lag metric issue
- [Issue #16801](https://github.com/opensearch-project/OpenSearch/issues/16801): Feature request for redefining segment replication metrics computation
- [Issue #10764](https://github.com/opensearch-project/OpenSearch/issues/10764): Bug report for skewed lag metric
- [Issue #17566](https://github.com/opensearch-project/OpenSearch/issues/17566): Feature request for increased segment counter step size
- [Issue #17595](https://github.com/opensearch-project/OpenSearch/issues/17595): Bug report for segment replication stopping when publish checkpoint fails
