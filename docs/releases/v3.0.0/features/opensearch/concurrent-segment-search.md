---
tags:
  - indexing
  - k-nn
  - performance
  - search
---

# Concurrent Segment Search Auto Mode Default

## Summary

OpenSearch 3.0.0 enables concurrent segment search in `auto` mode by default, a significant change from previous versions where it was disabled. This enhancement improves search latency for aggregation workloads by searching Lucene segments in parallel during the query phase, without requiring manual configuration.

## Details

### What's New in v3.0.0

The key changes in this release:

1. **Default mode changed**: `search.concurrent_segment_search.mode` now defaults to `auto` instead of `none`
2. **Setting key renamed**: `CONCURRENT_SEGMENT_SEARCH_TARGET_MAX_SLICE_COUNT_KEY` → `CONCURRENT_SEGMENT_SEARCH_MAX_SLICE_COUNT_KEY`
3. **Default slice count formula**: `Math.min(vCPU / 2, 4)` - balances performance with resource utilization
4. **Pluggable decider support**: Plugins like k-NN can enable concurrent search for specific query types

### Technical Changes

#### Mode Behavior

| Mode | Behavior |
|------|----------|
| `auto` (new default) | Uses pluggable decider; enables for aggregation requests by default |
| `all` | Enables concurrent search for all requests |
| `none` | Disables concurrent search (previous default) |

#### Default Slice Count Calculation

```java
Math.max(1, Math.min(Runtime.getRuntime().availableProcessors() / 2, 4))
```

This formula ensures:
- Minimum of 1 slice
- Maximum of 4 slices
- Uses half of available vCPUs

#### Files Modified

| File | Change |
|------|--------|
| `IndexSettings.java` | Updated default mode to `auto`, renamed setting key |
| `DefaultSearchContext.java` | Updated slice count calculation |
| `SearchService.java` | Integrated new default behavior |
| `CHANGELOG.md` | Documented breaking change |

### Usage Example

The feature is enabled by default. To disable:

```json
PUT _cluster/settings
{
   "persistent": {
      "search.concurrent_segment_search.mode": "none"
   }
}
```

To enable for all requests (not just aggregations):

```json
PUT _cluster/settings
{
   "persistent": {
      "search.concurrent_segment_search.mode": "all"
   }
}
```

Configure slice count:

```json
PUT _cluster/settings
{
   "persistent": {
      "search.concurrent.max_slice_count": 4
   }
}
```

### Migration Notes

**Important**: After upgrading to OpenSearch 3.0, aggregation workloads may experience increased CPU utilization because concurrent search is now enabled by default in `auto` mode.

Recommendations:
- Monitor cluster resource usage after upgrade
- If CPU utilization exceeds 25% with aggregation workloads before upgrade, consider:
  - Scaling cluster resources
  - Disabling concurrent search if scaling is not feasible
- The legacy `search.concurrent_segment_search.enabled` setting is deprecated; migrate to `search.concurrent_segment_search.mode`

## Limitations

- Not supported with `terminate_after` search parameter
- Parent aggregations on join fields not supported
- `sampler` and `diversified_sampler` aggregations not supported
- Terms aggregations may have additional document count error due to slice-level `shard_size` application

## References

### Documentation
- [Documentation](https://docs.opensearch.org/3.0/search-plugins/concurrent-segment-search/): Official concurrent segment search docs

### Blog Posts
- [Blog: Exploring concurrent segment search performance](https://opensearch.org/blog/concurrent-search-follow-up/): Performance benchmarks and guidelines
- [Blog: Introducing concurrent segment search](https://opensearch.org/blog/concurrent_segment_search/): Original feature introduction

### Pull Requests
| PR | Description |
|----|-------------|
| [#17978](https://github.com/opensearch-project/OpenSearch/pull/17978) | Enable concurrent_segment_search auto mode by default |

### Issues (Design / RFC)
- [Issue #17981](https://github.com/opensearch-project/OpenSearch/issues/17981): Feature request for enabling auto mode by default

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/concurrent-segment-search.md)
