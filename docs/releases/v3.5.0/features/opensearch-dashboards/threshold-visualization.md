---
tags:
  - opensearch-dashboards
---
# Threshold Visualization

## Summary

OpenSearch Dashboards v3.5.0 introduces improved threshold visualization capabilities in the Explore Vis framework. The changes simplify threshold logic for gauge and metric visualizations, add threshold color support for bar charts (regular and stacked), and extend threshold visual maps to scatter charts. These improvements provide users with more consistent and flexible data-driven color coding across chart types.

## Details

### What's New in v3.5.0

#### Simplified Threshold Logic (PR #10909)
The threshold processing pipeline was refactored to improve consistency across gauge and metric visualizations. Key changes include:
- Enhanced threshold generation, filtering, range handling, and deduplication
- Improved support for undefined values and edge cases
- Better color consistency across threshold boundaries
- Comprehensive unit tests added for threshold utility functions

#### Threshold Colors for Bar Charts (PR #11106)
Threshold color functionality was extended to bar chart visualizations:
- Data processing layer added to pivot data for 2-dimension scenarios
- "Use threshold colors" option is now always accessible in bar chart settings (previously conditionally hidden)
- Supports both regular bar charts and stacked bar charts
- Colors are applied based on metric values crossing threshold boundaries

#### Scatter Chart Threshold Visual Map (PR #11268)
Threshold colors were extended to scatter chart visualizations:
- Added ECharts `visualMap` component for scatter charts to enable threshold-based coloring
- Ensured color consistency between dark mode and light mode
- Scatter points are colored based on their Y-axis values relative to defined thresholds

### Technical Changes

The changes primarily affect the Explore Vis plugin within OpenSearch Dashboards, specifically:

| Component | Change |
|-----------|--------|
| Threshold utilities | Refactored generation, filtering, range handling, deduplication |
| Bar chart renderer | Added threshold color data processing with data pivoting |
| Bar chart settings | "Use threshold colors" toggle always visible |
| Scatter chart renderer | Added `visualMap` for threshold-based point coloring |
| Theme handling | Consistent threshold colors across dark/light modes |

## Limitations

- Threshold color support is part of the Explore Vis framework (experimental); not available in legacy visualization types
- Data pivoting for 2-dimension bar charts may have performance implications with very large datasets

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#10909](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10909) | Simplify threshold logic | - |
| [#11106](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11106) | Data processing for applying threshold colors | - |
| [#11045](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11045) | Fix flaky test for global threshold custom value | - |
| [#11268](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11268) | Add thresholds visual map for scatter | - |
