---
tags:
  - observability
---
# GenAI Agent Tracing

## Summary

OpenSearch Dashboards v3.6.0 delivers a major UX overhaul for the GenAI Agent Tracing feature, including a migration from EuiBasicTable to the Discover-based DataTable, a new Visualization tab with dashboard integration, improved trace map rendering via Celestial Map, and numerous styling and usability refinements across the agent traces plugin.

## Details

### What's New in v3.6.0

#### Discover Data Table Migration (OSD #11513)

The Traces and Spans tabs were refactored from `EuiBasicTable` to the Discover-based `DataTable` component. This brings:

- Custom column add/remove via the Fields sidebar
- Horizontal scrolling for wide datasets
- Infinite scrolling instead of pagination
- Filter-for and filter-out values directly from cells
- Wrap cell text toggle
- Info bar showing count, total, and query elapsed time

The metrics bar was replaced with `EuiStats` components, and error count filtering was added to the metrics bar. The Fields sidebar now uses `attributes.gen_ai.operation.name` and `status.code` as facet fields, with `gen_ai` attributes lifted to the top.

Agent traces are now enabled in analytics workspaces.

#### Visualization Tab (OSD #11564)

A new Visualization tab was added alongside Traces and Spans. Key capabilities:

- Runs the original user query without hidden `parentSpanId` or `gen_ai.operation.name` filters
- Supports PPL `stats` aggregation queries with automatic tab detection
- Integrates with the Explore plugin's visualization components
- Includes a resizable style settings panel for chart configuration
- "Add to Dashboard" functionality to save visualizations as embeddable panels on new or existing dashboards
- Keyboard shortcut (`a`) for quick dashboard export

The `detectAndSetOptimalTab` logic now automatically switches to the Visualization tab when a `stats` pipe is detected in the query, and preserves the user's tab choice on time-only refreshes.

#### Celestial Map Graph Library (OSD #11450)

The trace map (formerly "agent graph") was migrated from React Flow to Celestial Map, providing improved rendering performance and tighter node spacing (`rankSep: 80`, `nodeSep: 40`).

#### Kind Label Colors and Flyout Styling (OSD #11520)

- Span category badge colors updated: Tool → gray, Retrieval → mauve
- Badges switched from solid background to pastel background with colored text
- Icon removed from trace map `TypeBadge`, replaced with pastel pill style
- Error tooltips added on warning icons in trace tree and timeline
- `statusMessage` field added to `BaseRow` from span data
- Multi-column sorting removed for simplicity (single-column sort only)

#### Usability Improvements (OSD #11432)

- Updated colors and label texts for "Kind" categories
- Column sorting support added (Tokens sorts by `output_tokens` via PPL)
- "Agent graph" renamed to "Trace map"
- Extra table margins fixed
- Cypress end-to-end tests added

#### Styles and Saved Search Fix (OSD #11532)

- "Tool" kind color updated
- Emdash used as fallback for "Operation" in flyout instead of "Other"
- Fixed bug where loading a saved search showed empty results until user clicks update
- Support for both flattened (`gen_ai.operation.name: 'xxx'`) and nested (`gen_ai: { operation: { name: 'xxx' } }`) attribute formats via `unflattenSource` utility

#### Observability Plugin (observability #11387)

A new `agent_traces` plugin was created in the observability repository for GenAI agent tracing in the observability workspace.

### Technical Changes

- New constants: `AGENT_TRACES_VISUALIZATION_TAB_ID`, `AGENT_TRACES_DEFAULT_COLUMNS`, `AGENT_TRACES_COLUMN_DISPLAY_NAMES`, `AGENT_TRACES_SORTABLE_COLUMNS`, `AGENT_TRACES_VIRTUAL_COLUMN_SOURCE_FIELDS`
- `splitPplWhereAndTail()` utility separates user WHERE clauses from tail commands (head, sort, dedup, eval) for correct query assembly
- `queryEndsWithHead()` detects head commands to hide "of X total" in info bar
- `hitToBaseRow()` converts OpenSearch hits to `BaseRow` via `unflattenSource` + `traceHitToAgentSpan`
- PPL query request format changed to use `queries` array instead of flat query object
- `executePPLQuery` now accepts an optional `AbortSignal` for cancellation
- `TracePPLService.fetchTraceSpans` passes abort signal through
- Metrics queries split into 3 parallel queries: unfiltered counts, filtered stats, filtered counts
- `dataset_change_middleware` now dispatches `LOADING` status immediately and initializes default sort for new datasets
- `TraceExpansionContext` added for row expansion state management in DataTable
- Token tooltips in trace tree show input/output token breakdown
- `inputTokens` and `outputTokens` fields added to `BaseRow`

## Limitations

- Multi-column sorting is not supported in the DataTable integration with PPL; only single-column sorting is available
- The observability plugin PR (#11387) could not be fully investigated (repository access issue)

## References

### Pull Requests
| PR | Description | Repository |
|----|-------------|------------|
| `https://github.com/opensearch-project/observability/pull/11387` | Create agent_traces plugin for GenAI agent tracing | observability |
| `https://github.com/opensearch-project/opensearch-dashboards/pull/11564` | Support visualizations tab in agent traces | opensearch-dashboards |
| `https://github.com/opensearch-project/opensearch-dashboards/pull/11520` | Update colors for Kind labels and flyout styling | opensearch-dashboards |
| `https://github.com/opensearch-project/opensearch-dashboards/pull/11513` | Improve UX with discover data table, metrics bar, workspace support | opensearch-dashboards |
| `https://github.com/opensearch-project/opensearch-dashboards/pull/11450` | Update agent graph library to celestial map | opensearch-dashboards |
| `https://github.com/opensearch-project/opensearch-dashboards/pull/11532` | Update styles and fix loading saved search | opensearch-dashboards |
| `https://github.com/opensearch-project/opensearch-dashboards/pull/11432` | Improve usability with sorting, color updates, Cypress tests | opensearch-dashboards |
