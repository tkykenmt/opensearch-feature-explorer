# Segment Warmer

## Summary

Segment Warmer is an optimization feature for segment replication that pre-copies merged segments to replica shards before the primary shard's refresh completes. By leveraging Lucene's `IndexWriter.IndexReaderWarmer` interface, this feature significantly reduces the visibility delay between primary and replica shards, improving data consistency and search freshness in segment replication deployments. The feature supports both local segment replication (node-to-node transfer) and remote-store-enabled clusters (via remote storage).

## Details

### Architecture

```mermaid
graph TB
    subgraph "Primary Shard"
        IW[IndexWriter]
        SM[SegmentMerger]
        MSW[MergedSegmentWarmer]
        UP[RemoteStoreUploader]
    end
    
    subgraph "MergedSegmentWarmerFactory"
        MF[Factory]
    end
    
    subgraph "Remote Store"
        RS[(Remote Segment Store)]
    end
    
    subgraph "Replication Targets"
        R1[Replica Shard 1]
        R2[Replica Shard N]
    end
    
    SM -->|merge complete| IW
    IW -->|warm callback| MSW
    MF -->|creates| MSW
    MSW -->|local segrep| R1
    MSW -->|local segrep| R2
    MSW -->|remote store| UP
    UP -->|upload| RS
    RS -.->|fetch| R1
    RS -.->|fetch| R2
```

### Data Flow

```mermaid
flowchart TB
    subgraph "Without Pre-copy"
        A1[Merge] --> A2[Refresh]
        A2 --> A3[Segment Replication]
        A3 --> A4[Replica Visible]
    end
    
    subgraph "With Pre-copy"
        B1[Merge] --> B2[Pre-copy to Replicas]
        B2 --> B3[Refresh]
        B3 --> B4[Segment Replication]
        B4 --> B5[Replica Visible]
        B2 -.->|files already present| B4
    end
```

### Components

| Component | Description |
|-----------|-------------|
| `MergedSegmentWarmerFactory` | Factory that creates appropriate `IndexReaderWarmer` implementations based on index replication settings |
| `MergedSegmentWarmer` | Unified implementation handling both local and remote segment warming |
| `RemoteStorePublishMergedSegmentAction` | Replication action for uploading merged segments to remote store and publishing checkpoints |
| `RemoteStoreMergedSegmentCheckpoint` | Checkpoint containing local-to-remote filename mappings for merged segments |
| `PublishMergedSegmentAction` | Replication action for local segment replication pre-copy |
| `MergedSegmentCheckpoint` | Checkpoint representing merged segment information |

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `opensearch.experimental.feature.merged_segment_warmer.enabled` | Feature flag to enable merged segment warmer | `false` |
| `index.replication.type` | Must be set to `SEGMENT` for segment warmer to activate | `DOCUMENT` |
| `max_remote_low_priority_download_bytes_per_sec` | Rate limit for low-priority downloads (merged segments) | `0` (unlimited) |

### Metrics (v3.3.0+)

The segment warmer exposes comprehensive metrics under `merges.warmer` in stats APIs:

| Metric | Type | Description |
|--------|------|-------------|
| `total_invocations_count` | Cumulative | Total number of warm operations invoked |
| `total_time_millis` | Cumulative | Total wallclock time spent in warming operations |
| `total_failure_count` | Cumulative | Number of failed warming attempts |
| `total_bytes_sent` | Cumulative | Total data volume uploaded by primary shards |
| `total_bytes_received` | Cumulative | Total data volume downloaded by replica shards |
| `total_send_time_millis` | Cumulative | Time spent uploading segments |
| `total_receive_time_millis` | Cumulative | Time spent downloading segments |
| `ongoing_count` | Point-in-time | Current number of active warming operations |

Access metrics via:
- Node Stats: `GET /_nodes/stats/indices/merge`
- Index Stats: `GET /_stats/merge`
- CAT Shards: `GET /_cat/shards?h=merges.warmer.*`
- CAT Nodes: `GET /_cat/nodes?h=merges.warmer.*`

### Usage Example

Enable the feature flag in `opensearch.yml`:

```yaml
opensearch.experimental.feature.merged_segment_warmer.enabled: true
```

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

### How Pre-copy Works

1. **Standard Segment Replication Flow**: Without pre-copy, merged segments wait for the next refresh cycle before being replicated to replicas, causing visibility delays proportional to segment size

2. **Pre-copy Flow**:
   - Primary shard completes segment merge
   - `IndexWriter` invokes `IndexReaderWarmer.warm()` callback
   - `MergedSegmentWarmer` initiates segment transfer to replicas
   - Replicas receive segment files before primary refresh
   - On refresh, segment replication finds files already present on replicas
   - Replication completes with minimal network transfer

3. **Failover**: If pre-copy fails or times out, the system falls back to standard segment replication behavior

## Limitations

- Requires segment replication (`replication.type: SEGMENT`)
- Experimental feature requiring explicit feature flag enablement
- Increases network utilization during merge operations
- Not applicable to document replication indexes
- Failures during warming are logged but do not block merge operations

## Related PRs

| Version | PR | Description |
|---------|-----|-------------|
| v3.3.0 | [#18929](https://github.com/opensearch-project/OpenSearch/pull/18929) | Add metrics for merged segment warmer operations |
| v3.2.0 | [#18683](https://github.com/opensearch-project/OpenSearch/pull/18683) | Remote store support for merged segment warming |
| v3.0.0 | [#18255](https://github.com/opensearch-project/OpenSearch/pull/18255) | Local merged segment warmer implementation |
| v3.0.0 | [#17881](https://github.com/opensearch-project/OpenSearch/pull/17881) | Initial implementation - MergedSegmentWarmerFactory infrastructure |

## References

- [Issue #17528](https://github.com/opensearch-project/OpenSearch/issues/17528): RFC - Introduce Pre-copy Merged Segment into Segment Replication
- [Issue #18625](https://github.com/opensearch-project/OpenSearch/issues/18625): META - Merged segment pre-copy tracking issue
- [Issue #1694](https://github.com/opensearch-project/OpenSearch/issues/1694): Original Segment Replication feature request
- [Segment Replication Documentation](https://docs.opensearch.org/3.0/tuning-your-cluster/availability-and-recovery/segment-replication/index/): Official docs
- [Remote-backed Storage Documentation](https://docs.opensearch.org/3.0/tuning-your-cluster/availability-and-recovery/remote-store/index/): Official docs

## Change History

- **v3.3.0** (2025-10-14): Added comprehensive metrics for monitoring segment warmer operations - `MergedSegmentTransferTracker` and `MergedSegmentWarmerStats` expose invocation counts, timing, bytes transferred, and failure counts via stats APIs
- **v3.2.0** (2025-08-05): Added remote store support - merged segments are uploaded to remote store and replicated to replicas via `RemoteStorePublishMergedSegmentAction`
- **v3.0.0** (2025-05-06): Initial implementation - introduced `MergedSegmentWarmerFactory` with `LocalMergedSegmentWarmer` and `RemoteStoreMergedSegmentWarmer` infrastructure
