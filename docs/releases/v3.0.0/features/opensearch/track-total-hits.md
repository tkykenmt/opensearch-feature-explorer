---
tags:
  - performance
  - search
---

# Track Total Hits

## Summary

This release item adds logic to skip the Approximation Framework's early termination optimization when `track_total_hits` is set to `true`. When users explicitly request accurate total hit counts, the system now correctly falls back to standard query execution to ensure all matching documents are counted.

## Details

### What's New in v3.0.0

The Approximation Framework was enhanced to detect when `track_total_hits: true` is specified and automatically disable approximation in those cases. This ensures users receive accurate total hit counts when explicitly requested.

### Technical Changes

#### Behavior Change

When `track_total_hits` is set to `true`, the search context's `trackTotalHitsUpTo()` returns `SearchContext.TRACK_TOTAL_HITS_ACCURATE` (equivalent to `Integer.MAX_VALUE`). The approximation queries now check for this condition and skip early termination.

| `track_total_hits` Value | Behavior | Approximation |
|--------------------------|----------|---------------|
| `true` | Count all matching documents | Disabled |
| `false` | Count up to 10,000 documents | Enabled |
| Not specified | Count up to 10 documents (default) | Enabled |
| Integer (e.g., `1000`) | Count up to specified number | Enabled |

#### Modified Components

| Component | Change |
|-----------|--------|
| `ApproximatePointRangeQuery` | Added check for `TRACK_TOTAL_HITS_ACCURATE` in `canApproximate()` |
| `ApproximateMatchAllQuery` | Added check for `TRACK_TOTAL_HITS_ACCURATE` in `canApproximate()` |

### Usage Example

```json
// Approximation DISABLED - accurate total count required
GET logs/_search
{
  "track_total_hits": true,
  "query": {
    "range": {
      "@timestamp": {
        "gte": "2023-01-01T00:00:00",
        "lt": "2023-01-03T00:00:00"
      }
    }
  }
}

// Response includes accurate total
{
  "hits": {
    "total": {
      "value": 1523847,
      "relation": "eq"
    }
  }
}
```

```json
// Approximation ENABLED - default behavior
GET logs/_search
{
  "query": {
    "range": {
      "@timestamp": {
        "gte": "2023-01-01T00:00:00",
        "lt": "2023-01-03T00:00:00"
      }
    }
  }
}

// Response may have approximate total
{
  "hits": {
    "total": {
      "value": 10000,
      "relation": "gte"
    }
  }
}
```

### Migration Notes

No migration required. This change ensures correct behavior when `track_total_hits: true` is specified. Users who rely on accurate total hit counts should continue using `track_total_hits: true` as before.

## Limitations

- When `track_total_hits: true` is set, queries will not benefit from the Approximation Framework's performance optimizations
- For large result sets, queries with `track_total_hits: true` may have higher latency

## References

### Documentation
- [Search API Documentation](https://docs.opensearch.org/3.0/api-reference/search-apis/search/): `track_total_hits` parameter reference

### Blog Posts
- [OpenSearch Approximation Framework Blog](https://opensearch.org/blog/opensearch-approximation-framework/): Framework overview

### Pull Requests
| PR | Description |
|----|-------------|
| [#18017](https://github.com/opensearch-project/OpenSearch/pull/18017) | Skip approximation when `track_total_hits` is set to `true` |

### Issues (Design / RFC)
- [Issue #14406](https://github.com/opensearch-project/OpenSearch/issues/14406): Expand ApproximatePointRangeQuery to other numeric types

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/approximation-framework.md)
