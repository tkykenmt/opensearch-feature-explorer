---
tags:
  - skills
---
# Agent Skills/Tools

## Summary

OpenSearch v3.6.0 adds two new agent tools (SearchAroundDocumentTool and MetricChangeAnalysisTool), adds filter support to LogPatternAnalysisTool, and improves default tool descriptions for better LLM usability. A new shared DataFetchingHelper utility was extracted to reduce code duplication across tools.

## Details

### What's New in v3.6.0

#### New Tool: SearchAroundDocumentTool

A new tool that retrieves N documents before and N documents after a specific document, ordered by a timestamp field. This is useful for investigating log entries surrounding a known event.

- Uses `search_after` pagination for efficient retrieval
- Sorts by timestamp + `_doc` for deterministic ordering
- Returns documents in chronological order (before docs are reversed from DESC to ASC)
- Accepts parameters via direct fields or JSON `input` string

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `index` | string | Yes | OpenSearch index name |
| `doc_id` | string | Yes | Target document ID |
| `timestamp_field` | string | Yes | Timestamp field for ordering |
| `count` | integer | Yes | Number of documents before and after the target |

**Response format:** JSON array of documents in chronological order: `[before_docs..., target_doc, after_docs...]`. Each document includes `_index`, `_id`, `_score`, `_source`, and `sort` values.

#### New Tool: MetricChangeAnalysisTool

A new tool for detecting and analyzing metric changes by comparing percentile distributions (P50, P90) between a baseline and selection time period. Fields are ranked by a log-ratio change score to identify the most significant changes.

- Compares P50 and P90 percentiles between baseline and selection periods
- Uses log-ratio scoring (scale-independent) to rank fields by significance
- Skips fields with near-zero baselines to avoid inflated scores
- Returns top N fields (default: 10) ranked by change score
- Shares data fetching logic with DataDistributionTool via new `DataFetchingHelper`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `index` | string | Yes | Target OpenSearch index name |
| `timeField` | string | Yes | Date/time field for filtering |
| `selectionTimeRangeStart` | string | Yes | Start of target period (yyyy-MM-dd HH:mm:ss) |
| `selectionTimeRangeEnd` | string | Yes | End of target period (yyyy-MM-dd HH:mm:ss) |
| `baselineTimeRangeStart` | string | Yes | Start of baseline period (yyyy-MM-dd HH:mm:ss) |
| `baselineTimeRangeEnd` | string | Yes | End of baseline period (yyyy-MM-dd HH:mm:ss) |
| `size` | integer | No | Max documents to analyze (default: 1000, max: 10000) |
| `topN` | integer | No | Number of top fields to return (default: 10) |

#### LogPatternAnalysisTool: Filter Support

A new `filter` parameter enables log pattern analysis for specific services or conditions. The filter is a PPL boolean expression applied as an additional `where` clause.

- Applies to pattern diff mode and log insight mode
- Ignored in sequence analysis mode (requires all logs within a trace for accurate analysis)
- Example: `serviceName='ts-auth-service'` or `severity='ERROR'`

#### Improved Tool Descriptions

Default descriptions for LogPatternAnalysisTool, DataDistributionTool, and MetricChangeAnalysisTool were rewritten to be more concise and structured, helping LLMs select the right tool:

- **LogPatternAnalysisTool**: Now describes three modes (sequence analysis, pattern diff, log insight) with clear trigger conditions
- **DataDistributionTool**: Now describes two modes (comparison with baseline, single analysis) with clearer parameter descriptions
- **MetricChangeAnalysisTool**: Shortened description focusing on core capability

Input schema field descriptions were also simplified with consistent formatting (e.g., `format: yyyy-MM-dd HH:mm:ss`). The `DEFAULT_ATTRIBUTES` for all three tools now serialize the input schema via Gson for consistent JSON formatting.

### Technical Changes

#### DataFetchingHelper Utility

A new `DataFetchingHelper` class was extracted from `DataDistributionTool` to share data fetching logic:

- `AnalysisParameters`: Shared parameter parsing and validation
- `fetchIndexData()`: Fetches data via DSL or PPL queries with time range filtering
- `getFieldTypes()`: Retrieves index field type mappings
- `getNumberFields()`: Filters numeric fields from mappings
- `getFlattenedValue()`: Extracts nested field values using dot notation
- `buildFilterQuery()`: Builds BoolQueryBuilder with time range and custom filters

`DataDistributionTool` was refactored to delegate data fetching, field type detection, and query building to this helper, reducing ~250 lines of duplicated code.

#### DataDistributionTool: timeField Now Required

The `timeField` parameter was added to the `required` array in the input schema for `DataDistributionTool`, making it explicitly required instead of defaulting silently.

## Limitations

- SearchAroundDocumentTool requires the target document to exist and have valid sort values for the specified timestamp field
- MetricChangeAnalysisTool works best with short, focused time ranges (15-30 minutes) of similar duration
- LogPatternAnalysisTool filter is ignored in sequence analysis mode (when `traceFieldName` is provided with baseline)

## References

### Pull Requests

| PR | Description | Related Issue |
|----|-------------|---------------|
| `https://github.com/opensearch-project/skills/pull/702` | Add SearchAroundDocumentTool | |
| `https://github.com/opensearch-project/skills/pull/698` | Add MetricChangeAnalysisTool with DataFetchingHelper refactor | |
| `https://github.com/opensearch-project/skills/pull/707` | Add filter support for LogPatternAnalysisTool | |
| `https://github.com/opensearch-project/skills/pull/703` | Update default tool descriptions for LogPatternAnalysisTool and DataDistributionTool | |
