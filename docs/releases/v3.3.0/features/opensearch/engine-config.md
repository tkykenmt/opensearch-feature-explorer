---
tags:
  - search
---

# Engine Config toBuilder Method

## Summary

This release adds a `toBuilder()` method to the `EngineConfig` class, enabling plugin developers to easily create modified copies of engine configurations. This is particularly useful for plugins that need to customize specific engine settings (like translog factory) while preserving all other configuration values.

## Details

### What's New in v3.3.0

The `EngineConfig` class now includes a `toBuilder()` method that creates a new `Builder` instance pre-populated with all values from the current configuration. This allows selective modification of specific fields while preserving all others.

Additionally, both `EngineConfig.Builder` and `CodecService` have been promoted to public API status (`@PublicApi(since = "3.3.0")`).

### Technical Changes

#### New Method

```java
/**
 * Creates a new Builder pre-populated with all values from this EngineConfig.
 * This allows for easy modification of specific fields while preserving all others.
 *
 * @return a new Builder instance with all current configuration values
 */
public Builder toBuilder() {
    return new Builder()
        .shardId(this.shardId)
        .threadPool(this.threadPool)
        .indexSettings(this.indexSettings)
        // ... all 28+ fields copied
        .translogFactory(this.translogFactory)
        .clusterApplierService(this.clusterApplierService);
}
```

#### API Visibility Changes

| Class | Previous Status | New Status |
|-------|-----------------|------------|
| `EngineConfig.Builder` | `@opensearch.internal` | `@PublicApi(since = "3.3.0")` |
| `CodecService` | `@opensearch.internal` | `@PublicApi(since = "3.3.0")` |

### Usage Example

Before this change, modifying a single field required manually copying all 25+ fields:

```java
// Old approach - error-prone and verbose
EngineConfig cryptoConfig = new EngineConfig.Builder()
    .shardId(config.getShardId())
    .threadPool(config.getThreadPool())
    .indexSettings(config.getIndexSettings())
    // ... 20+ more manual field copies
    .translogFactory(cryptoTranslogFactory)  // The only field we want to change
    .build();
```

With the new `toBuilder()` method:

```java
// New approach - clean and maintainable
EngineConfig cryptoConfig = config.toBuilder()
    .translogFactory(cryptoTranslogFactory)
    .build();
```

### Motivation

This change was driven by the [opensearch-storage-encryption](https://github.com/opensearch-project/opensearch-storage-encryption) plugin, which needed to create an `EngineConfig` identical to the original except for the `translogFactory` field to enable encrypted translogs.

The previous approach of manually copying all fields was:
- Error-prone: Easy to miss fields when copying
- Maintenance burden: Any new fields added to `EngineConfig.Builder` would require updates to all plugins using this pattern
- Verbose: Required 25+ lines of boilerplate code

## Limitations

- The `toBuilder()` method creates a shallow copy of all configuration values
- Mutable objects within the configuration are shared between the original and the copy

## References

### Documentation
- [opensearch-storage-encryption PR #39](https://github.com/opensearch-project/opensearch-storage-encryption/pull/39#discussion_r2257070134): Original discussion that motivated this change

### Pull Requests
| PR | Description |
|----|-------------|
| [#19054](https://github.com/opensearch-project/OpenSearch/pull/19054) | Add toBuilder() method in EngineConfig |

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/opensearch-engine-config.md)
