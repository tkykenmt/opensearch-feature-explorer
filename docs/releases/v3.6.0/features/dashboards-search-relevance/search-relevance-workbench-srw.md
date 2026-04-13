---
tags:
  - dashboards-search-relevance
---
# Search Relevance Workbench (SRW)

## Summary

OpenSearch v3.6.0 brings significant improvements to the Search Relevance Workbench (SRW) dashboards plugin, spanning new features, UX enhancements, and bug fixes. Key additions include manual Query Set creation with multi-format input support, a Help flyout for Query Set creation, multiple data source (MDS) support across all resource types, and an "Ask AI" button for the relevance tuning agent. UX improvements include resizable query editors, standardized tooltips, a rename from "Single Query Comparison" to "Query Analysis", and cleaner timestamp formatting. Several bug fixes address scheduler failures, judgment deletion errors, NDJSON parsing error messages, single-query execution, and result view alignment.

## Details

### New Features

#### Manual Query Set Creation (PR #754)
Users can now create Query Sets directly in the UI without file uploads. The text input parser supports three interchangeable formats with automatic fallback detection (NDJSON → Key-Value → Plain Text):
- Plain text: one query per line (e.g., `red bluejeans`)
- Key-value: `query: "capital of France?", answer: "Paris"`
- NDJSON: `{"queryText":"capital of France?","referenceAnswer":"Paris"}`

The `#` separator validation conflict was removed, allowing queries containing `#` characters.

#### Query Set Help Flyout (PR #767)
A Help button next to the Query Set input field opens a slide-in flyout panel providing:
- Text input format documentation with examples for all three formats
- File upload format documentation (NDJSON)
- Downloadable sample NDJSON files (basic queries and queries with reference answers)

Implemented as `QuerySetHelpButton` component, following the existing Help flyout pattern from Query Analysis.

#### Multiple Data Source Support (PR #802)
End-to-end `dataSourceId` support for all four resource types: Experiments, Judgments, Query Sets, and Search Configurations. Changes span the full stack:
- Server: routes accept `dataSourceId` as query parameter; `backendAction` routes to remote data source client when provided
- Services: all four service classes pass optional `dataSourceId` on every API call
- Hooks: list and view hooks forward `dataSourceId` to API calls
- UI: `DataSourceSelector` component rendered on listing, view, and create pages when MDS is enabled

Enable with `data_source.enabled: true` in `opensearch_dashboards.yml`.

#### Ask AI Button (PR #810)
A dismissible callout banner guides users to the relevance tuning agent when the chat plugin is activated. Provides a direct entry point for AI-assisted relevance tuning workflows.

### Enhancements

#### Resizable Query Editors (PR #791)
New `ResizableQueryEditor` component wraps `EuiCodeEditor` with drag handles for vertical expansion in Query Compare view. Both editors resize synchronously (160px min, 600px max) to maintain visual consistency. Supports controlled (synchronized) and uncontrolled (standalone) modes.

#### Rename to Query Analysis (PR #773)
"Single Query Comparison" renamed to "Query Analysis" across the codebase. The new name reflects that comparison is optional — users can run and evaluate a single query directly.

#### NDJSON/JSONL File Support (PR #775)
Sample query files renamed from `.txt` to `.ndjson`. File picker updated to accept `.ndjson` and `.jsonl` extensions with proper parsing.

#### Standardized Action Tooltips (PR #782)
Icon-only action buttons across all listing pages (Search Configurations, Experiments, Judgments, Query Sets) wrapped with `EuiToolTip` for descriptive hover text, improving accessibility.

#### Timestamp Format Cleanup (PR #799)
Milliseconds removed from timestamp display across all listing tables. Format changed from `MMM D, YYYY @ HH:mm:ss.SSS` to `MMM D, YYYY @ HH:mm:ss` in `date_format_context.tsx`.

### Bug Fixes

#### Scheduler Null Cron Fix (PR #808)
Fixed experiment scheduler failure when cron expression is null or empty by adding proper validation and handling. Also improved scheduling visibility and experiment execution information in the detail view.

#### Judgment Deletion Fix (PR #751)
Fixed inconsistent UI state after deleting judgment ratings. The judgments list now refreshes correctly and deleted entries are immediately removed from UI state, preventing "Error loading judgment data" and "Failed to delete judgment" errors.

#### Single Query Execution (PR #746)
Search Comparison UI now allows execution with only one configured setup instead of requiring two. Introduces single-result mode, skips validation for unconfigured optional setups, and updates UI text from "Query" to "Setup".

#### Query Analysis Alignment Fix (PR #752)
Fixed text alignment and excessive spacing in Query Analysis results view. Setup 1 (left column) uses right-aligned text; Setup 2 (right column) uses left-aligned text for a compact comparison layout.

#### NDJSON Error Message Fix (PR #776)
Malformed NDJSON uploads now surface specific `JSON.parse` error messages with exact line numbers instead of the generic "No valid queries found in file" message.

## Limitations

- Multiple data source support requires `data_source.enabled: true` in the Dashboards configuration
- The "Ask AI" button only appears when the chat plugin is activated
- Resizable query editors have a fixed range of 160px–600px

## References

### Pull Requests
| PR | Description | Category |
|----|-------------|----------|
| `https://github.com/opensearch-project/dashboards-search-relevance/pull/754` | Manual Query Set creation | feature |
| `https://github.com/opensearch-project/dashboards-search-relevance/pull/767` | Query Set Help flyout | feature |
| `https://github.com/opensearch-project/dashboards-search-relevance/pull/802` | Multiple data source support | feature |
| `https://github.com/opensearch-project/dashboards-search-relevance/pull/810` | Ask AI button for relevance tuning agent | feature |
| `https://github.com/opensearch-project/dashboards-search-relevance/pull/775` | NDJSON/JSONL file support | enhancement |
| `https://github.com/opensearch-project/dashboards-search-relevance/pull/791` | Resizable query editors | enhancement |
| `https://github.com/opensearch-project/dashboards-search-relevance/pull/782` | Standardized action tooltips | enhancement |
| `https://github.com/opensearch-project/dashboards-search-relevance/pull/799` | Timestamp format cleanup | enhancement |
| `https://github.com/opensearch-project/dashboards-search-relevance/pull/773` | Rename to Query Analysis | enhancement |
| `https://github.com/opensearch-project/dashboards-search-relevance/pull/808` | Scheduler null cron fix | bugfix |
| `https://github.com/opensearch-project/dashboards-search-relevance/pull/752` | Query Analysis alignment fix | bugfix |
| `https://github.com/opensearch-project/dashboards-search-relevance/pull/746` | Single query execution fix | bugfix |
| `https://github.com/opensearch-project/dashboards-search-relevance/pull/751` | Judgment deletion fix | bugfix |
| `https://github.com/opensearch-project/dashboards-search-relevance/pull/776` | NDJSON error message fix | bugfix |
