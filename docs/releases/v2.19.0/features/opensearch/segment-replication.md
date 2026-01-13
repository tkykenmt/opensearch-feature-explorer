---
tags:
  - opensearch
---
# Segment Replication

## Summary

OpenSearch v2.19.0 includes two improvements to segment replication: an increased default checkpoint limit for backpressure and new granular statistics for remote publication failures.

## Details

### What's New in v2.19.0

#### Increased Checkpoint Limit Default

The default value for `segrep.pressure.checkpoint.limit` has been increased from 4 to 30. This change aligns the checkpoint limit with the time limit setting (`segrep.pressure.time.limit` = 5 minutes) for remote-backed clusters.

**Rationale**: For remote-backed clusters, the recommended refresh interval is 10+ seconds (vs. 1 second default) due to segment upload costs. With the previous default of 4 checkpoints and a 10-second refresh interval, replicas could only lag 40 seconds before triggering backpressure rejections—far below the 5-minute time limit. The new default of 30 checkpoints allows approximately 300 seconds (5 minutes) of lag, matching the time limit.

| Setting | Old Default | New Default |
|---------|-------------|-------------|
| `segrep.pressure.checkpoint.limit` | 4 | 30 |

#### Granular Remote Publication Statistics

New statistics have been added to separate remote download failures from overall remote publication failures:

```json
{
  "remote_full_download": {
    "success_count": 1,
    "failed_count": 0,
    "total_time_in_millis": 4,
    "incoming_publication_failed_count": 0,
    "checksum_validation_failed_count": 0
  },
  "remote_diff_download": {
    "success_count": 2,
    "failed_count": 0,
    "total_time_in_millis": 12,
    "incoming_publication_failed_count": 0,
    "checksum_validation_failed_count": 0
  }
}
```

**New Metrics**:

| Metric | Description |
|--------|-------------|
| `incoming_publication_failed_count` | Count of failures during the incoming publication flow (separate from download failures) |
| `failed_count` | Now accurately reflects download-specific failures only |

### Technical Changes

- `RemoteDownloadStats` class extended with `incoming_publication_failed_count` field
- Download failure stats moved to `RemoteClusterStateService` download methods for accurate tracking
- New methods added: `fullIncomingPublicationFailed()` and `diffIncomingPublicationFailed()`

## Limitations

- The increased checkpoint limit may allow replicas to fall further behind before backpressure kicks in
- Users with custom checkpoint limits should review their settings after upgrade

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#16577](https://github.com/opensearch-project/OpenSearch/pull/16577) | Increase segrep pressure checkpoint default limit to 30 | - |
| [#16682](https://github.com/opensearch-project/OpenSearch/pull/16682) | Add stats for remote publication failure and move download failure stats to remote methods | - |
