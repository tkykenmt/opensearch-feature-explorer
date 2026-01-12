# Pull-based Ingestion Bugfixes

## Summary

This release fixes critical bugs in pull-based ingestion related to out-of-bounds offset handling and removes the persisted pointers concept. These changes improve reliability when dealing with Kafka retention expiration and consumer rewind scenarios, providing at-least-once processing guarantees.

## Details

### What's New in v3.4.0

Two key bugfixes improve pull-based ingestion reliability:

1. **Out-of-bounds offset handling**: Fixed scenarios where Kafka offsets become invalid (e.g., after retention period expiration)
2. **File-based ingestion flaky test fix**: Fixed the file-based consumer to properly track line numbers when start point exceeds file length

### Technical Changes

#### Removed Persisted Pointers

The persisted pointers concept has been removed to fix correctness issues during consumer rewind when versioning is not used:

| Before v3.4.0 | After v3.4.0 |
|---------------|--------------|
| Persisted pointers tracked processed offsets | No persisted pointer tracking |
| Duplicate detection based on stored offsets | At-least-once processing guarantee |
| Could skip latest messages on rewind | Consistent behavior on rewind |

#### Kafka Consumer Configuration Changes

| Setting | Before | After | Description |
|---------|--------|-------|-------------|
| `auto.offset.reset` | User-defined | `none` (default) | Throws error on out-of-bounds offsets |
| `max.poll.records` | Not used | Uses `poll.max_batch_size` | Controls batch size at consumer level |

#### API Changes

The `IngestionConsumerFactory.initialize()` method signature changed:

```java
// Before
void initialize(Map<String, Object> params);

// After  
void initialize(IngestionSource ingestionSource);
```

This allows consumer factories to access additional configuration like `maxPollSize` from the ingestion source.

#### Deprecated Metrics

| Metric | Status |
|--------|--------|
| `totalDuplicateMessageSkippedCount` | Deprecated (always 0) |

### Usage Example

When Kafka offsets become out-of-bounds (e.g., after retention expiration), the consumer now throws an error by default:

```json
PUT /my-index
{
  "settings": {
    "ingestion_source": {
      "type": "kafka",
      "pointer.init.reset": "earliest",
      "param": {
        "topic": "my-topic",
        "bootstrap_servers": "localhost:9092",
        "auto.offset.reset": "earliest"
      }
    }
  }
}
```

Users can override `auto.offset.reset` to `earliest` or `latest` to handle out-of-bounds offsets automatically.

### Migration Notes

1. **Versioning recommended**: Use document versioning (`_version` field) to ensure consistent document views on consumer rewind/replay
2. **Monitor consumer errors**: With `auto.offset.reset=none`, out-of-bounds offsets will cause errors that should be monitored
3. **Duplicate handling**: Without persisted pointers, duplicates may occur on rewind - use versioning for exactly-once semantics

## Limitations

- Pull-based ingestion provides at-least-once processing guarantees (not exactly-once without versioning)
- `totalDuplicateMessageSkippedCount` metric is deprecated and will be removed in a future version

## References

### Documentation
- [Documentation](https://docs.opensearch.org/3.0/api-reference/document-apis/pull-based-ingestion/): Pull-based ingestion

### Pull Requests
| PR | Description |
|----|-------------|
| [#19607](https://github.com/opensearch-project/OpenSearch/pull/19607) | Fix pull-based ingestion out-of-bounds offset scenarios and remove persisted offsets |
| [#19757](https://github.com/opensearch-project/OpenSearch/pull/19757) | Fix file-based ingestion consumer to handle start point beyond max line number |

### Issues (Design / RFC)
- [Issue #19591](https://github.com/opensearch-project/OpenSearch/issues/19591): Bug report for duplicate/old message skipping logic
- [Issue #19723](https://github.com/opensearch-project/OpenSearch/issues/19723): Flaky test report for FileBasedIngestionSingleNodeTests

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/pull-based-ingestion.md)
