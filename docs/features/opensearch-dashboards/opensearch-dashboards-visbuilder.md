---
tags:
  - opensearch-dashboards
---
# VisBuilder

## Summary

VisBuilder is a drag-and-drop visualization tool in OpenSearch Dashboards that allows users to create data visualizations without preselecting the visualization output type. It provides an immediate view of data with intuitive field-based configuration. Starting from v2.16.0, VisBuilder includes enhanced drag-and-drop functionality and experimental Vega specification generation.

## Details

### Architecture

```mermaid
graph TB
    subgraph "VisBuilder Plugin"
        subgraph "UI Components"
            DND[Drag & Drop Interface]
            CONFIG[Configuration Pane]
            PREVIEW[Visualization Preview]
        end
        
        subgraph "Visualization Types"
            METRIC[Metric Vis]
            TABLE[Table Vis]
            BAR[Bar Chart]
            LINE[Line Chart]
            AREA[Area Chart]
        end
        
        subgraph "Expression Renderer"
            EXPR[ReactExpressionRenderer]
            VEGA[Vega Renderer]
            CONTAINER[VisualizationContainer]
        end
    end
    
    subgraph "Data Layer"
        INDEX[Index Pattern]
        DS[Data Source]
    end
    
    DND --> CONFIG
    CONFIG --> PREVIEW
    PREVIEW --> EXPR
    PREVIEW --> VEGA
    EXPR --> METRIC
    EXPR --> TABLE
    EXPR --> BAR
    EXPR --> LINE
    EXPR --> AREA
    INDEX --> EXPR
    INDEX --> VEGA
    DS --> INDEX
```

### Components

| Component | Description |
|-----------|-------------|
| Drag & Drop Interface | Field selector with drag-and-drop to axis wells, supports cross-axis movement |
| Configuration Pane | Side panel for configuring visualization options |
| Visualization Preview | Real-time preview of the visualization |
| ReactExpressionRenderer | Expression-based rendering engine |
| Vega Spec Builder | Dynamic Vega/Vega-Lite specification generator (v2.16.0+) |
| VisualizationContainer | Wrapper component for loading states and error handling |

### Supported Visualization Types

| Type | Description |
|------|-------------|
| Metric | Single value display with optional comparison |
| Table | Tabular data display with sorting |
| Bar Chart | Vertical/horizontal bar visualizations |
| Line Chart | Time-series line visualizations |
| Area Chart | Stacked or overlapping area visualizations |

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| Index Pattern | Data source for visualization | Required |
| Metrics | Aggregation fields (Y-axis) | Count |
| Buckets | Grouping fields (X-axis) | None |
| Legend | Show/hide legend | Visible |
| `visbuilder:enableVega` | Enable Vega rendering (v2.16.0+) | false |

### Drag & Drop Operations (v2.16.0+)

| Operation | Description |
|-----------|-------------|
| Add field | Drag from field selector to an axis |
| Replace field | Drag and drop onto an existing field |
| Move between axes | Drag a configured field to a different axis |
| Reorder | Drag fields within the same axis to reorder |

### Usage Example

1. Navigate to Visualize → Create visualization → VisBuilder
2. Select an index pattern
3. Drag fields from the field list to Metrics or Buckets wells
4. Configure aggregation options in the configuration pane
5. Save the visualization

## Limitations

- Vega rendering is experimental and must be enabled via advanced settings
- Vega integration currently supports line, area, and bar chart types
- Some complex aggregation configurations may not translate perfectly to Vega specifications

## Change History

- **v2.16.0** (2024-08-06): Enhanced drag-and-drop with cross-axis movement, field replacement, and reordering; Added experimental Vega specification generation; Bug fixes for Metric/Table rendering, configuration pane scrolling, legend toggle, and data source compatibility

## References

### Documentation
- [VisBuilder Documentation](https://docs.opensearch.org/latest/dashboards/visualize/visbuilder/)

### Pull Requests
| Version | PR | Description |
|---------|-----|-------------|
| v2.16.0 | [#7107](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7107) | Enhance Drag & Drop functionality in Vis Builder |
| v2.16.0 | [#7288](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7288) | Add capability to generate dynamic Vega |
| v2.16.0 | [#6674](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6674) | Fix flat render structure in Metric and Table Vis |
| v2.16.0 | [#6811](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6811) | Bug fixes for config pane scroll and legend toggle |
| v2.16.0 | [#6948](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/6948) | Fix vis-builder not rendering with data source |
