---
tags:
  - dashboards
  - indexing
  - observability
  - search
---

# TSVB Visualization

## Summary

The Time-Series Visual Builder (TSVB) is a powerful data visualization tool in OpenSearch Dashboards for creating detailed time-series visualizations. It supports multiple visualization types including Area, Line, Metric, Gauge, Markdown, and Data Table, with features for annotations, multiple data sources, and flexible axis configuration.

## Details

### Architecture

```mermaid
graph TB
    subgraph "OpenSearch Dashboards"
        subgraph "TSVB Plugin"
            UI[TSVB UI Components]
            Config[Panel Configuration]
            Vis[Visualization Renderer]
        end
        
        subgraph "Data Layer"
            Query[Query Builder]
            Agg[Aggregation Engine]
        end
    end
    
    subgraph "OpenSearch"
        Index[Index Data]
        Search[Search API]
    end
    
    UI --> Config
    Config --> Query
    Query --> Search
    Search --> Index
    Agg --> Vis
    Query --> Agg
```

### Visualization Types

| Type | Description |
|------|-------------|
| Time Series | Line/area charts with time on X-axis |
| Metric | Single value display |
| Gauge | Circular gauge visualization |
| Top N | Bar chart of top values |
| Table | Tabular data display |
| Markdown | Custom markdown with data variables |

### Axis Configuration

TSVB supports flexible axis configuration for time series visualizations:

| Setting | Description | Options |
|---------|-------------|---------|
| `axis_position` | Position of the Y-axis | `left`, `right`, `hidden` |
| `axis_scale` | Scale type for the axis | `normal`, `log` |
| `axis_min` | Minimum axis value | Number or empty |
| `axis_max` | Maximum axis value | Number or empty |
| `separate_axis` | Enable per-series axis | `0` (no), `1` (yes) |

#### Axis Position Constants

```javascript
export const AXIS_POSITION = {
  LEFT: 'left',
  RIGHT: 'right',
  HIDDEN: 'hidden',
};
```

### Aggregation Types

TSVB supports various aggregation types for data analysis:

| Aggregation | Description |
|-------------|-------------|
| Count | Document count |
| Average | Mean value |
| Sum | Total sum |
| Min/Max | Minimum/Maximum values |
| Cardinality | Unique value count |
| Percentile | Percentile calculations |
| Moving Average | Smoothed trend line |
| Serial Diff | Difference between time periods |
| Top Hit | Most recent document values |

### Multi-Data Source Support

Since v2.14, TSVB supports querying multiple data sources:

```yaml
# opensearch_dashboards.yml
data_source.enabled: true
vis_type_timeseries.enabled: true
```

### Usage Example

```json
{
  "type": "timeseries",
  "series": [
    {
      "id": "series-1",
      "chart_type": "line",
      "line_width": 1,
      "point_size": 1,
      "fill": 0.5,
      "separate_axis": 1,
      "axis_position": "right",
      "axis_scale": "log",
      "formatter": "number"
    }
  ],
  "axis_scale": "normal",
  "axis_position": "left"
}
```

## Limitations

- Axis scale setting requires "Separate Axis" to be enabled for per-series configuration
- Hidden axis position only available for time series with separate axis
- Some input fields use legacy HTML inputs due to type compatibility issues with EUI components

## Change History

- **v2.18.0** (2024-10-29): Added hidden axis option, per-axis scale setting, compressed UI input fields ([#8504](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8504))
- **v2.14.0**: Added multi-data source support for TSVB visualizations

## References

### Documentation
- [TSVB Documentation](https://docs.opensearch.org/latest/dashboards/visualize/tsvb/): Official documentation

### Blog Posts
- [Visualizing data from multiple data sources](https://opensearch.org/blog/vega-tsvb-mds-visualizations/): Blog post on TSVB with MDS

### Pull Requests
| Version | PR | Description | Related Issue |
|---------|-----|-------------|---------------|
| v2.18.0 | [#8504](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/8504) | Allow hiding axis, per-axis scale, compressed input fields | [#1929](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/1929) |
| v2.14.0 | - | Multi-data source support introduced |   |

### Issues (Design / RFC)
- [Issue #1929](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/1929): Axis scale override bug
