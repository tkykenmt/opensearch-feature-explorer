---
tags:
  - domain/core
  - component/dashboards
  - dashboards
  - search
  - sql
---
# Dashboards Features

## Summary

OpenSearch Dashboards v3.0.0 introduces several user experience improvements including autocomplete value suggestions for PPL and SQL queries, time field support for Vega visualizations with PPL, improved dependency license validation in CI, and enhanced scrolling behavior on the Discover page.

## Details

### What's New in v3.0.0

This release includes four key improvements to OpenSearch Dashboards:

1. **Autocomplete Value Suggestion** - Intelligent value suggestions for PPL and SQL queries
2. **Vega PPL Time Field Support** - Dashboard time range filters now work with Vega PPL visualizations
3. **Dependency License Validation** - Improved CI checks for dependency licensing compliance
4. **Discover Scrolling Improvements** - Better scrolling experience with sticky headers

### Technical Changes

#### Autocomplete Value Suggestion (PR #8275)

Adds intelligent value completion for PPL and SQL queries in binary comparison predicates and IN-predicates.

| Component | Description |
|-----------|-------------|
| `src/plugins/data/public/antlr/*` | Value suggestion logic using SQL aggregation queries |
| `src/plugins/data/server/ui_settings.ts` | New UI settings for value suggestion |
| `src/plugins/data/public/autocomplete/autocomplete_service.ts` | Value suggestion provider interface |

**New Configuration**

| Setting | Description | Default |
|---------|-------------|---------|
| `query:enhancements:suggestValues` | Enable/disable value suggestions | `true` |
| `query:enhancements:suggestValuesLimit` | Maximum values to query | `200` |

The feature queries the most popular column values using:
```sql
SELECT <column> FROM <table> GROUP BY <column> ORDER BY COUNT(<column>) DESC LIMIT <limit>
```

#### Vega PPL Time Field Support (PR #9152)

Enables Vega visualizations with PPL queries to respect dashboard time range filters using the `%timefield%` parameter.

**Before**: Vega PPL queries ignored dashboard time range settings.

**After**: Adding `"%timefield%": "timestamp"` applies the dashboard time filter automatically.

```json
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "data": {
        "url": {
            "%timefield%": "timestamp",
            "%type%": "ppl",
            "body": {
                "query": "source=opensearch_dashboards_sample_data_logs | stats count() as request_count by extension"
            }
        }
    }
}
```

#### Dependency License Validation (PR #9064)

Improves CI pipeline with additional checks:
- Out of sync lockfile detection
- Developer documentation validation
- Dependency license compliance validation
- Updated GitHub Actions workflow versions

#### Discover Scrolling Improvements (PR #9298)

Enhances the Discover page scrolling behavior:
- Vertical scrolling now occurs inside the table instead of the entire panel
- Horizontal scrollbar appears at the bottom of the viewport
- Table header is now sticky for better column visibility
- Users can see selected columns and query while scrolling

### Usage Example

**Vega PPL with Time Filter:**
```json
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "data": {
        "url": {
            "%timefield%": "timestamp",
            "%type%": "ppl",
            "body": {
                "query": "source=opensearch_dashboards_sample_data_logs | stats DISTINCT_COUNT(clientip) as unique_visitors by span(timestamp, 1d)"
            },
            "data_source_name": "default"
        }
    },
    "mark": "bar",
    "encoding": {
        "x": {"field": "timestamp", "type": "temporal"},
        "y": {"field": "unique_visitors", "type": "quantitative"}
    }
}
```

## Limitations

- Value suggestions only work for binary comparison predicates (`column = value`) and IN-predicates
- Vega time field support requires explicit `%timefield%` configuration
- Field-level security and masking are respected in value suggestions

## References

### Documentation
- [Vega Documentation](https://docs.opensearch.org/3.0/dashboards/visualize/vega/): Official Vega visualization docs

### Blog Posts
- [Improving ease of use in OpenSearch Dashboards with Vega visualizations](https://opensearch.org/blog/improving-dashboards-usability-with-vega/): Blog post on Vega improvements

### Pull Requests
| PR | Description |
|----|-------------|
| [#8275](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8275) | Autocomplete Value Suggestion for PPL & SQL |
| [#9064](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9064) | Improve CI checks and dependency license validation |
| [#9152](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9152) | Vega visualization with PPL time field support |
| [#9298](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/9298) | Improve scrolling experience on Discover page |

### Issues (Design / RFC)
- [Issue #9169](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/9169): Vega PPL %timefield% feature request

## Related Feature Report

- Full feature documentation
