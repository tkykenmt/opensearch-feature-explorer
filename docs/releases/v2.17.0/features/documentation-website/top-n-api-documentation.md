# Query Insights Top N API Documentation Update

## Summary

This release item improves the documentation for the Query Insights Top N API. The changes clarify the API behavior, explain the `type` parameter usage, and add troubleshooting guidance for users who receive empty results.

## Details

### What's New in v2.17.0

Enhanced documentation for the GET top N queries API with clearer explanations and troubleshooting tips.

### Technical Changes

#### Documentation Improvements

| Section | Change |
|---------|--------|
| Introduction | Clarified that the feature provides visibility into queries with highest latency or resource consumption |
| API Default Behavior | Documented that the API returns `latency` results by default |
| Type Parameter | Explained that results are sorted in descending order based on the specified metric type |
| Troubleshooting | Added important note about ensuring monitoring is enabled and requests are within the time window |

#### Updated API Description

The documentation now clearly states:
- The Insights API returns top N `latency` results by default
- The `type` parameter can be used to retrieve results for other metric types (`cpu`, `memory`)
- Results are sorted in descending order based on the specified metric type

#### New Troubleshooting Guidance

Added an important note to help users troubleshoot empty results:
> If your query returns no results, ensure that top N query monitoring is enabled for the target metric type and that search requests were made within the current time window.

### Usage Example

```json
# Get top N queries (defaults to latency)
GET /_insights/top_queries

# Get top N queries by CPU usage
GET /_insights/top_queries?type=cpu

# Get top N queries by memory usage
GET /_insights/top_queries?type=memory
```

### Migration Notes

No migration required. This is a documentation improvement only.

## Limitations

None - this is a documentation update.

## References

### Documentation
- [PR #8139](https://github.com/opensearch-project/documentation-website/pull/8139): Main implementation
- [Top N Queries Documentation](https://opensearch.org/docs/latest/observing-your-data/query-insights/top-n-queries/): Official documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#8139](https://github.com/opensearch-project/documentation-website/pull/8139) | Update GET top N api documentation |

### Issues (Design / RFC)
- [Issue #80](https://github.com/opensearch-project/query-insights/issues/80): Related issue
- [Issue #83](https://github.com/opensearch-project/query-insights/issues/83): Related issue

## Related Feature Report

- [Full feature documentation](../../../../features/query-insights/query-insights.md)
