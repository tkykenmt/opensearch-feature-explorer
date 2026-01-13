---
tags:
  - domain/ml
  - component/server
  - indexing
  - ml
  - observability
  - sql
---
# Skills Tools

## Summary

OpenSearch v3.3.0 introduces two new analysis tools to the Skills plugin: the Log Pattern Analysis Tool and the Data Distribution Tool. These tools enable intelligent log analysis and data distribution comparison capabilities through the ML Commons agent framework. Additionally, this release includes enhancements to the PPL Tool and bug fixes for the WebSearchTool and DataDistributionTool.

## Details

### What's New in v3.3.0

#### Log Pattern Analysis Tool (LogPatternAnalysisTool)

A new tool for intelligent log analysis that detects patterns and sequences across log messages using PPL's patterns command and hierarchical clustering algorithms.

**Key Features:**
- Log pattern detection using configurable thresholds
- Log sequence analysis across trace IDs to identify exceptional sequences
- Time-based comparison between baseline and selection periods
- Pattern vectorization using IDF and sigmoid functions for similarity calculations

**Analysis Modes:**

| Mode | Description | Use Case |
|------|-------------|----------|
| Log Insight | Basic pattern extraction from selection time range | Find errors/exceptions/outliers |
| Pattern Diff | Compare patterns between baseline and selection periods | Identify pattern changes |
| Sequence Analysis | Trace-based sequence analysis with clustering | Identify new log sequences |

**Usage Example:**
```json
POST /_plugins/_ml/agents/{agent_id}/_execute
{
  "parameters": {
    "index": "logs-2025.06.24",
    "logFieldName": "body",
    "selectionTimeRangeStart": "2025-06-24T07:50:26.999Z",
    "selectionTimeRangeEnd": "2025-06-24T07:55:56Z"
  }
}
```

#### Data Distribution Tool (DataDistributionTool)

A new tool for analyzing field value distributions using statistical methods with configurable sample sizes.

**Key Features:**
- Statistical distribution analysis with configurable sample sizes
- Time-based comparison between baseline and selection periods
- Statistical divergence calculation to quantify differences
- Automatic field type detection (keyword, numeric, boolean, text)
- Support for both DSL and PPL query modes

**Analysis Modes:**

| Mode | Description |
|------|-------------|
| Single Period | Basic distribution analysis within a specific time range |
| Comparative | Compare distributions between baseline and selection periods |
| Custom Filtering | Advanced analysis with DSL or PPL filters |

**Usage Example:**
```json
POST /_plugins/_ml/agents/{agent_id}/_execute
{
  "parameters": {
    "index": "logs-2025.01.15",
    "timeField": "@timestamp",
    "baselineTimeRangeStart": "2025-01-15 08:00:00",
    "baselineTimeRangeEnd": "2025-01-15 09:00:00",
    "selectionTimeRangeStart": "2025-01-15 10:00:00",
    "selectionTimeRangeEnd": "2025-01-15 11:00:00"
  }
}
```

### Technical Changes

#### New Components

| Component | Description |
|-----------|-------------|
| `LogPatternAnalysisTool` | Main implementation for log pattern/sequence analysis |
| `DataDistributionTool` | Main implementation for data distribution analysis |
| `ClusteringHelper` | Utility for clustering operations |
| `HierarchicalAgglomerativeClustering` | Clustering algorithm implementation |

#### New Dependencies

- Apache Commons Math3 for statistical computations

### Bug Fixes

| PR | Description |
|----|-------------|
| [#641](https://github.com/opensearch-project/skills/pull/641) | Fixed DataDistributionTool output to remove baselinePercentage values when no baseline time is provided |
| [#639](https://github.com/opensearch-project/skills/pull/639) | Fixed WebSearchTool by using AsyncHttpClient from ml-commons; fixed CVE-2025-48924; fixed DataDistributionToolIT and PPLTool IT failures |

### Enhancements

| PR | Description |
|----|-------------|
| [#636](https://github.com/opensearch-project/skills/pull/636) | Enhanced PPLTool to include additional context (mappings, current_time, os_version) when passing requests to SageMaker |

## Limitations

- LogPatternAnalysisTool requires PPL plugin for pattern detection
- DataDistributionTool performance depends on sample size configuration
- Both tools require appropriate index permissions

## References

### Documentation
- [LogPatternTool Documentation](https://docs.opensearch.org/3.0/ml-commons-plugin/agents-tools/tools/log-pattern-tool/): Official documentation
- [Tools Documentation](https://docs.opensearch.org/3.0/ml-commons-plugin/agents-tools/tools/index/): Tools overview
- [Skills Repository](https://github.com/opensearch-project/skills): Source code

### Pull Requests
| PR | Description |
|----|-------------|
| [#625](https://github.com/opensearch-project/skills/pull/625) | Log patterns analysis tool |
| [#634](https://github.com/opensearch-project/skills/pull/634) | Data Distribution Tool |
| [#636](https://github.com/opensearch-project/skills/pull/636) | Add more information in PPL tool when passing to SageMaker |
| [#641](https://github.com/opensearch-project/skills/pull/641) | Delete-single-baseline (DataDistributionTool fix) |
| [#639](https://github.com/opensearch-project/skills/pull/639) | Fix WebSearchTool issue |

## Related Feature Report

- [Full feature documentation](../../../../features/skills/skills-tools.md)
