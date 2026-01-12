# Query Insights Plugin (Batch 2)

## Summary

OpenSearch v3.0.0 includes additional bug fixes and improvements for the Query Insights plugin. This batch focuses on fixing default exporter settings, improving local index management, optimizing query retrieval limits, and adding integration tests for the exporter and reader components.

## Details

### What's New in v3.0.0

#### Fix Default Exporter Settings

The default settings for exporters were broken after changes in PR #217, causing no data to be exported to the local index when running OpenSearch with Query Insights. This fix deeply refactors the exporter logic to ensure proper functionality:

- Data is now correctly exported to `top_queries-*` local indices
- Exporter can be properly disabled and re-enabled via cluster settings
- Debug mode works correctly when switching exporter types

**Testing the fix:**
```bash
# Enable local index exporter
curl -X PUT 'localhost:9200/_cluster/settings' -H 'Content-Type: application/json' -d'
{
    "persistent": {
        "search.insights.top_queries.exporter.type": "local_index"
    }
}'

# Verify indices are created after search queries
curl -X GET "localhost:9200/_cat/indices?v&s=index" | grep top_queries
```

#### Local Index Replica Count Changed to 0

The default replica count for `top_queries-*` indices has been changed from 1 to 0. This ensures that Query Insights local indices show as `green` health status on single-node domains instead of `yellow`.

**Before (yellow on single-node):**
```
yellow open top_queries-2025.03.07-21637 ... 1 1 ...
```

**After (green on single-node):**
```
green  open top_queries-2025.03.07-21637 ... 1 0 ...
```

#### Improved Expired Index Deletion

When searching for expired local indices to delete, the plugin now uses `ClusterStateRequest` with an index pattern (`top_queries-*`) instead of scanning all indices on the domain. This improvement:

- Reduces computation on domains with many indices
- Minimizes risk of accidental deletion of unrelated indices
- Applies stricter validation including index name pattern (`top_queries-<date>-<5 digits>`), creation time, and metadata checks

**Configuration:**
```bash
# Set retention period for local indices
curl -X PUT "localhost:9200/_cluster/settings" -H 'Content-Type: application/json' -d'
{
  "persistent": {
    "search.insights.top_queries.exporter.delete_after_days": "7"
  }
}'
```

#### Reduced MAX_TOP_N_INDEX_READ_SIZE to 50

The maximum number of Top N queries that can be fetched from the local index has been reduced from a higher value to 50. Results are now sorted by descending latency by default. This change:

- Improves performance when reading from local indices
- Provides more relevant results by default sorting
- Aligns with Query Insights Dashboards requirements

#### Integration Tests for Exporter and Reader

Comprehensive integration tests have been added for the Query Insights exporter and reader components, covering:

1. Document creation
2. Top Queries exporter configuration
3. Search operations
4. Latency window size settings
5. Local index creation verification
6. Exporter disable/re-enable functionality
7. Debug mode switching

### Technical Changes

#### Configuration Changes

| Setting | Description | New Default |
|---------|-------------|-------------|
| `search.insights.top_queries.exporter.delete_after_days` | Days to retain exported data | `7` |

#### Index Settings Changes

| Setting | Old Value | New Value |
|---------|-----------|-----------|
| `number_of_replicas` | `1` | `0` |

### Usage Examples

**Check local index health:**
```bash
curl -X GET "localhost:9200/_cat/indices?v&s=index" | grep top_queries
```

**Configure retention period:**
```bash
curl -X PUT "localhost:9200/_cluster/settings" -H 'Content-Type: application/json' -d'
{
  "persistent": {
    "search.insights.top_queries.exporter.delete_after_days": "10"
  }
}'
```

**Disable and re-enable exporter:**
```bash
# Disable
curl -X PUT 'localhost:9200/_cluster/settings' -H 'Content-Type: application/json' -d'
{
    "persistent": {
        "search.insights.top_queries.exporter.type": "none"
    }
}'

# Re-enable
curl -X PUT 'localhost:9200/_cluster/settings' -H 'Content-Type: application/json' -d'
{
    "persistent": {
        "search.insights.top_queries.exporter.type": "local_index"
    }
}'
```

## Limitations

- Local index exporter must be enabled for historical query lookups
- Expired index deletion runs once per day at 00:05 UTC

## Related PRs

| PR | Description |
|----|-------------|
| [#234](https://github.com/opensearch-project/query-insights/pull/234) | Fix default exporter settings |
| [#257](https://github.com/opensearch-project/query-insights/pull/257) | Change local index replica count to 0 |
| [#262](https://github.com/opensearch-project/query-insights/pull/262) | Use ClusterStateRequest with index pattern when searching for expired local indices |
| [#281](https://github.com/opensearch-project/query-insights/pull/281) | Reduce MAX_TOP_N_INDEX_READ_SIZE to 50, sort by desc latency |
| [#267](https://github.com/opensearch-project/query-insights/pull/267) | Integration tests for exporter and reader |

## References

- [Issue #232](https://github.com/opensearch-project/query-insights/issues/232): Default exporter settings bug
- [Issue #256](https://github.com/opensearch-project/query-insights/issues/256): Local index replica count issue
- [Issue #261](https://github.com/opensearch-project/query-insights/issues/261): Expired index deletion improvement
- [Issue #233](https://github.com/opensearch-project/query-insights/issues/233): Integration tests request
- [Issue #105](https://github.com/opensearch-project/query-insights-dashboards/issues/105): Related dashboards issue for read size
- [Top N Queries Documentation](https://docs.opensearch.org/3.0/observing-your-data/query-insights/top-n-queries/): Official documentation

## Related Feature Report

- [Full feature documentation](../../../features/query-insights/query-insights.md)
