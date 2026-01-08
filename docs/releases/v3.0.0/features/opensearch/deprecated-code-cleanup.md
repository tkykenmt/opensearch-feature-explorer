# Deprecated Code Cleanup

## Summary

OpenSearch 3.0.0 includes a comprehensive cleanup of deprecated code, removing legacy settings, APIs, and terminology that were deprecated in earlier versions. This is a breaking change that affects users upgrading from 2.x versions who may still be using deprecated features.

## Details

### What's New in v3.0.0

This release removes deprecated code across multiple categories:

1. **Thread Pool Settings**: Deprecated `thread_pool.test.max_queue_size` and `thread_pool.test.min_queue_size` settings removed
2. **Index Store Settings**: `index.store.hybrid.mmap.extensions` setting removed in favor of improved hybridfs file handling
3. **Transport Plugin**: `transport-nio` plugin removed; Netty remains the standard network framework
4. **Locale Provider**: COMPAT locale provider replaced with CLDR for JDK 21+ compatibility
5. **Tokenizer Naming**: CamelCase `PathHierarchy` tokenizer name deprecated in favor of snake_case `path_hierarchy`
6. **Module Renaming**: Classes ending with `Plugin` under `modules` directory renamed to `Module`
7. **JodaCompatibleZonedDateTime**: Deprecated methods removed from scripts
8. **Feature Flags**: Experimental feature flags removed for GA features (PLUGGABLE_CACHE, APPROXIMATE_POINT_RANGE_QUERY)
9. **Legacy Version Constants**: LegacyESVersion constants (V_7_0 through V_7_10, V_1_) removed
10. **Non-inclusive Terminology**: "blacklist/whitelist" replaced with "allow list/deny list"

### Technical Changes

#### Removed Settings

| Setting | Replacement | PR |
|---------|-------------|-----|
| `thread_pool.test.max_queue_size` | None (removed) | [#2595](https://github.com/opensearch-project/OpenSearch/pull/2595) |
| `thread_pool.test.min_queue_size` | None (removed) | [#2595](https://github.com/opensearch-project/OpenSearch/pull/2595) |
| `index.store.hybrid.mmap.extensions` | Auto-detection | [#9392](https://github.com/opensearch-project/OpenSearch/pull/9392) |

#### Removed Components

| Component | Reason | PR |
|-----------|--------|-----|
| `transport-nio` plugin | Netty is standard | [#16887](https://github.com/opensearch-project/OpenSearch/issues/16887) |
| COMPAT locale provider | JDK 21 deprecation | [#13988](https://github.com/opensearch-project/OpenSearch/pull/13988) |
| LegacyESVersion constants | Version cleanup | Multiple PRs |

#### Removed Feature Flags

| Feature Flag | Status | PR |
|--------------|--------|-----|
| `PLUGGABLE_CACHE` | GA in 3.0 | [#17344](https://github.com/opensearch-project/OpenSearch/pull/17344) |
| `APPROXIMATE_POINT_RANGE_QUERY_SETTING` | GA in 3.0 | [#17769](https://github.com/opensearch-project/OpenSearch/pull/17769) |

### Migration Notes

#### Thread Pool Settings
Remove any references to deprecated thread pool settings from your configuration:
```yaml
# Remove these settings from opensearch.yml
# thread_pool.test.max_queue_size: ...
# thread_pool.test.min_queue_size: ...
```

#### Index Store Settings
The `index.store.hybrid.mmap.extensions` setting is no longer needed. OpenSearch now automatically determines which file extensions use mmap vs nio:
```yaml
# Remove this setting - no longer supported
# index.store.hybrid.mmap.extensions: ...
```

#### Tokenizer Naming
Update analyzer configurations to use snake_case tokenizer names:
```json
// Before (deprecated)
{
  "tokenizer": {
    "type": "PathHierarchy"
  }
}

// After (recommended)
{
  "tokenizer": {
    "type": "path_hierarchy"
  }
}
```

#### Locale Changes
If your application relies on locale-specific date/time formatting, be aware that CLDR locale data may have minor differences from COMPAT. For example, German short day/month names may include a trailing period.

#### Script Updates
Update any Painless scripts that use deprecated `JodaCompatibleZonedDateTime` methods. These methods were causing performance overhead due to deprecation warnings.

## Limitations

- No backward compatibility for removed settings
- Scripts using deprecated datetime methods will fail
- Plugins depending on `transport-nio` must migrate to Netty

## Related PRs

| PR | Description |
|----|-------------|
| [#3346](https://github.com/opensearch-project/OpenSearch/pull/3346) | Remove deprecated JodaCompatibleZonedDateTime methods |
| [#9392](https://github.com/opensearch-project/OpenSearch/pull/9392) | Remove mmap.extensions setting |
| [#13988](https://github.com/opensearch-project/OpenSearch/pull/13988) | Remove COMPAT locale provider |
| [#17344](https://github.com/opensearch-project/OpenSearch/pull/17344) | Remove PLUGGABLE_CACHE feature flag |
| [#17769](https://github.com/opensearch-project/OpenSearch/pull/17769) | Remove ApproximatePointRangeQuery feature flag |
| [#4042](https://github.com/opensearch-project/OpenSearch/pull/4042) | Rename Plugin classes to Module |
| [#10894](https://github.com/opensearch-project/OpenSearch/pull/10894) | Deprecate CamelCase PathHierarchy tokenizer |

## References

- [Breaking Changes Documentation](https://docs.opensearch.org/3.0/breaking-changes/)
- [Issue #2773](https://github.com/opensearch-project/OpenSearch/issues/2773): List of deprecated code removal in 3.0
- [Issue #3156](https://github.com/opensearch-project/OpenSearch/issues/3156): JodaCompatibleZonedDateTime deprecation
- [Issue #8297](https://github.com/opensearch-project/OpenSearch/issues/8297): mmap.extensions removal
- [Issue #11550](https://github.com/opensearch-project/OpenSearch/issues/11550): COMPAT locale provider removal
- [Issue #17343](https://github.com/opensearch-project/OpenSearch/issues/17343): Tiered caching GA

## Related Feature Report

- [Full feature documentation](../../../../features/opensearch/deprecated-code-cleanup.md)
