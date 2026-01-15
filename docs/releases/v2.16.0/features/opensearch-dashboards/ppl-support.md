---
tags:
  - opensearch-dashboards
---
# PPL Support in Vega Visualization

## Summary

OpenSearch Dashboards v2.16.0 introduces PPL (Piped Processing Language) support in Vega visualizations. This feature enables users to query OpenSearch data using PPL syntax directly within Vega specifications, providing an alternative to the traditional OpenSearch Query DSL.

## Details

### What's New in v2.16.0

This release adds a new `ppl` data source type to Vega visualizations, allowing users to write PPL queries instead of OpenSearch DSL queries.

### Technical Changes

#### New PPL Query Parser

A new `PPLQueryParser` class was added to handle PPL queries in Vega specifications:

- Parses PPL query syntax from Vega `data.url.body.query`
- Validates that the query is a non-empty string
- Integrates with the existing Vega data model

#### PPL Raw Search Strategy

A new `pplraw` search strategy was registered in the query enhancements plugin:

- Executes PPL queries against OpenSearch
- Returns raw JSON data suitable for Vega consumption
- Supports multi-data-source configurations via `dataSourceId`

#### Search API Updates

The search API was enhanced to:

- Pass raw request context to search strategies
- Support the `pplraw` strategy option
- Handle PPL response inspection in the Vega inspector

### Usage Example

```hjson
{
  $schema: https://vega.github.io/schema/vega-lite/v5.json
  data: {
    url: {
      %context%: true
      %timefield%: @timestamp
      body: {
        query: "source=opensearch_dashboards_sample_data_logs | stats count() by response"
      }
    }
  }
  mark: bar
  encoding: {
    x: { field: response, type: nominal }
    y: { field: count(), type: quantitative }
  }
}
```

### Components Modified

| Component | Changes |
|-----------|---------|
| `vis_type_vega` | Added `PPLQueryParser`, integrated with `VegaParser` |
| `query_enhancements` | Added `pplraw` search strategy |
| `data` plugin | Updated search routes to pass raw request |

## Limitations

- PPL support in Vega requires the query enhancements plugin to be enabled
- UI changes for PPL in Vega are not included in this release (planned for future commits)
- Time filter injection for PPL queries requires explicit `%timefield%` configuration

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| [#7285](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7285) | Support PPL in vega visualization | - |

### Documentation

- [Vega Visualization](https://docs.opensearch.org/2.16/dashboards/visualize/vega/)
- [PPL Documentation](https://docs.opensearch.org/2.16/search-plugins/sql/ppl/index/)
