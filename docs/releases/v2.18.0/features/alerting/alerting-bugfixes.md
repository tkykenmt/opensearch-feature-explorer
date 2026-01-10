# Alerting Bugfixes

## Summary

OpenSearch v2.18.0 includes 8 bug fixes for the Alerting plugin, addressing backend query index management, bucket-level monitor optimization, and multiple UX improvements in the Alerting Dashboards plugin. These fixes improve reliability, performance, and user experience for alerting workflows.

## Details

### What's New in v2.18.0

This release focuses on two main areas:
1. **Backend fixes** for query index lifecycle and bucket-level monitor performance
2. **Dashboard UX improvements** including fit-and-finish updates and MDS (Multi Data Source) compatibility fixes

### Technical Changes

#### Backend Fixes (alerting)

| Fix | Description | Impact |
|-----|-------------|--------|
| Query index deletion timing | Delete query index only when put mappings throws an exception | Prevents accidental data loss during index creation |
| Bucket-level monitor optimization | Resolve alias to query only time-series indices within range query timeframe | Improved query performance for time-series data |
| Query index shard settings | Set number of shards to 0 and auto expand replicas to 0-1 | Better resource utilization and availability |

#### Dashboard UX Fixes (alerting-dashboards-plugin)

| Fix | Description | Impact |
|-----|-------------|--------|
| Fit and Finish UX | Consistent spacing, pagination placement, button labels, breadcrumb fixes | Improved visual consistency |
| Fit and Finish UX Pt 2 | Alert links to monitor page, data source query fixes, monitor name display | Better navigation and data handling |
| Recent alerts card width | Set width to 16 (1/3 of row) after removing "What's New" card | Proper layout balance |
| Assistant plugin override | Fix optional plugin override issue, return dataSourceId in context | Correct plugin initialization |
| MDS ui_metadata fetch | Fix ui_metadata not fetched when MDS client is used | Proper metadata display with MDS |

### Usage Example

The bucket-level monitor optimization automatically applies when using time-series indices with aliases:

```json
POST _plugins/_alerting/monitors
{
  "type": "monitor",
  "name": "time-series-bucket-monitor",
  "monitor_type": "bucket_level_monitor",
  "enabled": true,
  "schedule": {
    "period": {
      "interval": 5,
      "unit": "MINUTES"
    }
  },
  "inputs": [{
    "search": {
      "indices": ["logs-*"],
      "query": {
        "size": 0,
        "query": {
          "bool": {
            "filter": [{
              "range": {
                "@timestamp": {
                  "gte": "now-1h",
                  "lte": "now"
                }
              }
            }]
          }
        },
        "aggs": {
          "by_host": {
            "terms": {
              "field": "host.keyword"
            },
            "aggs": {
              "error_count": {
                "filter": {
                  "term": { "level": "ERROR" }
                }
              }
            }
          }
        }
      }
    }
  }],
  "triggers": [{
    "bucket_level_trigger": {
      "name": "high-error-host",
      "severity": "1",
      "condition": {
        "buckets_path": {
          "error_count": "error_count._count"
        },
        "script": {
          "source": "params.error_count > 100",
          "lang": "painless"
        }
      }
    }
  }]
}
```

With the optimization in v2.18.0, this monitor will only query indices that contain documents within the specified time range, significantly improving performance for large time-series datasets.

## Limitations

- Query index shard settings changes apply only to newly created query indices
- Bucket-level monitor optimization requires proper timestamp field configuration in the range query

## Related PRs

| PR | Repository | Description |
|----|------------|-------------|
| [#1685](https://github.com/opensearch-project/alerting/pull/1685) | alerting | Delete query index only if put mappings throws an exception |
| [#1701](https://github.com/opensearch-project/alerting/pull/1701) | alerting | Optimize bucket level monitor to resolve alias to query only time-series indices within timeframe |
| [#1702](https://github.com/opensearch-project/alerting/pull/1702) | alerting | Fix number of shards of query index to 0 and auto expand replicas to 0-1 |
| [#1092](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1092) | alerting-dashboards-plugin | Fit and Finish UX Fixes |
| [#1099](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1099) | alerting-dashboards-plugin | Fit and Finish UX changes Pt 2 |
| [#1102](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1102) | alerting-dashboards-plugin | Fix assistant plugin override issue and return dataSourceId in context |
| [#1117](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1117) | alerting-dashboards-plugin | Add width for recent alerts card |
| [#1124](https://github.com/opensearch-project/alerting-dashboards-plugin/pull/1124) | alerting-dashboards-plugin | Fix ui_metadata is not fetched when MDS client is used |

## References

- [Monitors Documentation](https://docs.opensearch.org/2.18/observing-your-data/alerting/monitors/): Monitor types and configuration
- [Alerting Documentation](https://docs.opensearch.org/2.18/observing-your-data/alerting/index/): Official alerting documentation
- [Issue #1710](https://github.com/opensearch-project/alerting/issues/1710): Related issue for bucket-level monitor optimization
- [Issue #1123](https://github.com/opensearch-project/alerting-dashboards-plugin/issues/1123): Related issue for MDS ui_metadata fix
- [PR #1674](https://github.com/opensearch-project/alerting/pull/1674): Related PR for query index creation timing

## Related Feature Report

- [Full feature documentation](../../../../features/alerting/alerting.md)
