---
tags:
  - opensearch-dashboards
---
# Dashboard Visualization Editing

## Summary

OpenSearch Dashboards v3.6.0 introduces the in-context visualization editor, allowing users to create and edit visualizations directly within dashboards without navigating away. This release also includes several bug fixes that improve the editor's stability, including fixes for state transfer during visualization creation, scope history management, empty state component imports, and UI issues with the dropdown and edit URL routing.

## Details

### What's New in v3.6.0

The in-context visualization editor is a new feature that enables quick editing of visualizations directly within the Dashboard view. Key capabilities include:

- Quick editing: switch datasets, rewrite PPL queries, and re-configure visualizations without leaving the dashboard. Saved changes apply directly to the dashboard panel.
- Create new visualizations from the Dashboard's "Add Panel" flow with context-aware dataset filtering:
  - PPL Mode: shows datasets with Logs or Traces signal types
  - PromQL Mode: filters to show only Prometheus datasets
  - AI Mode: dataset-driven activation based on selected dataset
- Edit routing based on creation origin:
  - Visualizations created in Explore open the full Explore app when edited
  - Visualizations created in Dashboard open the in-context editor when edited

The editor is registered as a separate application (`visualization-editor`) within the Explore plugin, with its own URL tracker, scoped history, and embeddable factory integration.

### Technical Changes

The in-context visualization editor is implemented under `src/plugins/explore/public/application/in_context_vis_editor/` with the following key components:

| Component | Description |
|-----------|-------------|
| `VisualizationEditorPage` | Main page component with resizable panels for query, visualization, and style options |
| `QueryBuilder` | Singleton class managing query state, URL sync, dataset resolution, and query execution |
| `VisualizationBuilder` | Manages visualization configuration, chart rendering, and style panel |
| `SaveVisButton` | Handles save/discard with `stateTransfer` for dashboard round-trip navigation |
| `ExploreEmbeddableFactory` | Updated to route edit actions to the visualization editor for in-context-created visualizations |

Bug fixes in this release:

1. State transfer for dashboard visualization dropdown (PR #11551): Fixed `stateTransfer` not being passed when creating visualizations from the dashboard dropdown. The `new_vis_actions.tsx` in the visualizations plugin now uses `stateTransfer.navigateToEditor()` with `originatingApp` to ensure proper back-navigation to the dashboard.

2. Scope history and initialization refactor (PR #11596): Refactored `useInitialSaveExplore` to separate saved state parsing from initialization logic. The `QueryBuilder` now handles URL state restoration, dataset resolution, and URL sync internally in its `init()` method, fixing race conditions between previous `visData` and `visConfig`. Renamed "In context editor" to "visualization editor" throughout the codebase.

3. Empty state component import fix (PR #11613): Replaced imports of `DiscoverNoResults`, `DiscoverUninitialized`, and `LoadingSpinner` from legacy Discover with dedicated visualization editor components (`VisEditorNoResults`, `VisEditorUninitialized`, `VisEditorLoadingState`), removing the dependency on the legacy Discover app.

4. UI fixes for dropdown and edit URL (PR #11574): Added "Visualize with Discover" back to the create visualization dropdown by registering a separate `DiscoverVisualization` alias alongside the new `VisualizationEditor` alias. Fixed the embeddable `editUrl` to correctly route to the visualization editor app for in-context-created visualizations (those without a `type` field).

## Limitations

- The in-context editor is a complement to the Explore app, not a replacement. Complex analysis workflows still benefit from the full Explore feature set.
- Visualizations created in Explore cannot be edited in the in-context editor; they always open in the full Explore app.
- After a page reload, the `originatingApp` context may be lost, so the editor falls back to saving without navigating back to the dashboard.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| `https://github.com/opensearch-project/opensearch-dashboards/pull/11528` | Add in-context visualization editor | - |
| `https://github.com/opensearch-project/opensearch-dashboards/pull/11551` | Fix stateTransfer not added when creating visualization from dashboard dropdown | - |
| `https://github.com/opensearch-project/opensearch-dashboards/pull/11596` | Fix scope history out of scope for in-context visualization editor | - |
| `https://github.com/opensearch-project/opensearch-dashboards/pull/11613` | Fix visualization editor empty state component import | - |
| `https://github.com/opensearch-project/opensearch-dashboards/pull/11574` | Fix visualization editor UI issues including dropdown and edit URL | - |
