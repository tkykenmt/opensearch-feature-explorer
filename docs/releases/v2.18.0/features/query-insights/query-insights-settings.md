---
tags:
  - domain/observability
  - component/server
  - performance
  - search
---
# Query Insights Settings

## Summary

This bugfix changes the default values for the Query Insights grouping attribute settings `field_name` and `field_type` from `false` to `true`. This ensures that when queries are grouped by similarity, the query structure includes field names and field data types by default, providing more accurate and useful query grouping out of the box.

## Details

### What's New in v2.18.0

The Query Insights plugin's grouping feature allows similar queries to be grouped together based on their query structure. Prior to this change, the settings that control whether field names and field types are included in the query structure were disabled by default, which could result in overly broad query groupings.

### Technical Changes

#### Configuration Changes

| Setting | Old Default | New Default |
|---------|-------------|-------------|
| `search.insights.top_queries.grouping.attributes.field_name` | `false` | `true` |
| `search.insights.top_queries.grouping.attributes.field_type` | `false` | `true` |

#### Impact on Query Grouping

With these settings now enabled by default:

**Before (field_name=false, field_type=false):**
```
bool
  must
    term
  filter
    match
    range
```

**After (field_name=true, field_type=true):**
```
bool []
  must:
    term [field1, keyword]
  filter:
    match [field2, text]
    range [field4, long]
```

This provides more granular query grouping, distinguishing between queries that operate on different fields even if they have the same structure.

### Usage Example

The settings can still be disabled if broader grouping is desired:

```bash
PUT _cluster/settings
{
  "persistent": {
    "search.insights.top_queries.grouping.attributes.field_name": false,
    "search.insights.top_queries.grouping.attributes.field_type": false
  }
}
```

### Migration Notes

- Existing clusters upgrading to v2.18.0 will automatically use the new defaults
- Query groups may become more granular after upgrade due to field name/type inclusion
- No action required unless broader grouping behavior is preferred

## Limitations

- More granular grouping may result in more query groups being tracked
- Consider adjusting `max_groups_excluding_topn` if tracking limits are reached

## References

### Documentation
- [Grouping Top N Queries Documentation](https://docs.opensearch.org/2.18/observing-your-data/query-insights/grouping-top-n-queries/)
- [Query Insights Documentation](https://docs.opensearch.org/2.18/observing-your-data/query-insights/index/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#144](https://github.com/opensearch-project/query-insights/pull/144) | Set default true for field name and type setting |

## Related Feature Report

- Full feature documentation
