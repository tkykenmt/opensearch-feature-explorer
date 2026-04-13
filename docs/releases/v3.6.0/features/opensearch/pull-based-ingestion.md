---
tags:
  - opensearch
---
# Pull-based Ingestion

## Summary

In v3.6.0, pull-based ingestion graduates from experimental to generally available (GA) as a public API. This release also introduces a warmup phase to prevent serving stale data after node restarts or shard relocations, and adds the `field_mapping` message mapper type that extracts document metadata from configurable fields in raw stream messages.

## Details

### What's New in v3.6.0

#### GA Status — Experimental Tag Removed

All pull-based ingestion classes have been promoted from `@ExperimentalApi` to `@PublicApi(since = "3.6.0")`. This includes the core `IngestionSource`, `IngestionShardPointer`, `IngestionShardConsumer`, `IngestionConsumerFactory`, `Message`, `IngestionErrorStrategy`, `IngestionSettings`, `IngestionStatus`, and all ingestion management API request/response classes (pause, resume, get state, update state). The `BroadcastRequest` base class was also marked as `@PublicApi` since its implementations were already public.

#### Warmup Phase

A new warmup mechanism prevents shards from serving search queries until they have caught up with the streaming source after node restart or shard relocation. This addresses the problem of stale data being served while the consumer catches up from the last checkpoint offset.

State machine:

```
Index Created → WARMING_UP → (lag ≤ threshold OR timeout) → POLLING → STARTED
```

During warmup:
- The poller actively ingests from the source (internally POLLING/PROCESSING)
- Externally reports state as `WARMING_UP` via `GET /{index}/ingestion/_state`
- The shard remains in `INITIALIZING` and does not serve search queries
- If the poller is paused, warmup is skipped immediately
- On timeout, warmup completes with a warning log and the shard proceeds

New settings:

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `ingestion_source.warmup.timeout` | TimeValue | `-1` (disabled) | Maximum warmup wait time. `-1` = disabled, `>=0` = enabled |
| `ingestion_source.warmup.lag_threshold` | long | `100` | Acceptable pointer-based lag for warmup completion |

Both settings are Final (set at index creation, cannot be changed later).

Usage example:

```json
PUT /my-index
{
  "settings": {
    "ingestion_source": {
      "type": "kafka",
      "warmup": {
        "timeout": "5m",
        "lag_threshold": 50
      },
      "param": {
        "topic": "my-topic",
        "bootstrap_servers": "localhost:9092"
      }
    }
  }
}
```

Implementation details:
- `WarmupConfig` record class added to `IngestionSource` with `timeout` and `lagThreshold` fields
- Warmup blocking occurs in `IndexShard.postRecovery()` before transitioning to `POST_RECOVERY` state
- Uses `CountDownLatch` for thread-safe blocking/signaling in `DefaultStreamPoller`
- `cachedPointerBasedLag` initialized to `-1` to prevent premature warmup completion before lag data is available
- `IngestionEngine.awaitWarmupComplete()` encapsulates timeout and error handling

#### Field Mapping Message Mapper

A new `field_mapping` mapper type allows extracting `_id`, `_version`, and `_op_type` from configurable top-level fields in raw stream messages. Extracted fields are removed from `_source`. This is useful for CDC (Change Data Capture) and other scenarios where metadata is embedded in the message payload rather than in a structured envelope.

New mapper type: `field_mapping` (added to `MapperType` enum alongside `default` and `raw_payload`)

New settings prefix: `ingestion_source.mapper_settings.*`

| Mapper Setting | Description |
|----------------|-------------|
| `id_field` | Source field to use as document `_id`. If absent, ID is auto-generated |
| `version_field` | Source field to use as document `_version` with external versioning. Must be present in every message when configured |
| `op_type_field` | Source field to determine operation type |
| `op_type_field.delete_value` | Value that indicates a delete operation |
| `op_type_field.create_value` | Value that indicates a create operation |

Operation type resolution: if the field value matches `delete_value` → delete, if it matches `create_value` → create, otherwise → index (default).

Usage example:

```json
PUT /cdc-index
{
  "settings": {
    "ingestion_source": {
      "type": "kafka",
      "mapper_type": "field_mapping",
      "mapper_settings": {
        "id_field": "user_id",
        "version_field": "timestamp",
        "op_type_field": "action",
        "op_type_field.delete_value": "DELETE",
        "op_type_field.create_value": "INSERT"
      },
      "param": {
        "topic": "cdc-events",
        "bootstrap_servers": "localhost:9092"
      }
    }
  }
}
```

With this configuration, a message like:
```json
{"user_id": "abc", "timestamp": 1234567890, "action": "DELETE", "name": "alice"}
```
Would be processed as a delete operation for document `abc` with external version `1234567890`.

Validation rules:
- `field_mapping` mapper type requires all cluster nodes to be on v3.6.0 or later (mixed-cluster version check)
- `mapper_settings` keys are validated against the set of known keys for the mapper type
- `delete_value` and `create_value` require `op_type_field` to be configured
- `delete_value` and `create_value` cannot be the same
- Extracted field values must be scalar types (string, number, or boolean)

### Technical Changes

- `IngestionSource` class and related classes promoted from `@ExperimentalApi` to `@PublicApi(since = "3.6.0")`
- New `WarmupConfig` record class in `IngestionSource`
- New `WARMING_UP` state added to `StreamPoller.State` enum
- `DefaultStreamPoller` gains warmup-aware state management with `CountDownLatch`-based blocking
- `IndexShard.postRecovery()` calls `handlePullBasedIngestionWarmup()` before state transition
- New `FieldMappingIngestionMessageMapper` class implementing `IngestionMessageMapper`
- `IngestionMessageMapper.create()` factory method extended to accept `mapperSettings` parameter
- `MetadataCreateIndexService.validateIngestionSourceSettings()` validates mapper type version compatibility and settings
- New `INGESTION_SOURCE_MAPPER_SETTINGS` prefix setting in `IndexMetadata`
- `INGESTION_SOURCE_WARMUP_TIMEOUT_SETTING` and `INGESTION_SOURCE_WARMUP_LAG_THRESHOLD_SETTING` added to `IndexMetadata`

## Limitations

- Warmup uses pointer-based lag only; sources that do not support offset-based lag will rely on timeout for warmup completion
- `field_mapping` mapper type requires all cluster nodes to be on v3.6.0+ (no mixed-cluster support)
- Warmup settings are Final and cannot be changed after index creation
- `field_mapping` mapper only extracts from top-level fields (no nested field path support)

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#20704](https://github.com/opensearch-project/OpenSearch/pull/20704) | Remove experimental tag, mark as public API since 3.6.0 | |
| [#20526](https://github.com/opensearch-project/OpenSearch/pull/20526) | Add warmup phase for pull-based ingestion | [#20506](https://github.com/opensearch-project/OpenSearch/issues/20506) |
| [#20722](https://github.com/opensearch-project/OpenSearch/pull/20722) | Add mapper_settings support and field_mapping mapper type | [#20721](https://github.com/opensearch-project/OpenSearch/issues/20721) |
| [#20729](https://github.com/opensearch-project/OpenSearch/pull/20729) | Implement FieldMappingIngestionMessageMapper | [#20728](https://github.com/opensearch-project/OpenSearch/issues/20728) |

### Documentation
- [Pull-based ingestion](https://docs.opensearch.org/latest/api-reference/document-apis/pull-based-ingestion/)
- [Pull-based ingestion management](https://docs.opensearch.org/latest/api-reference/document-apis/pull-based-ingestion-management/)
