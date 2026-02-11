---
tags:
  - opensearch-dashboards
---
# Data Importer

## Summary

In v3.5.0, the Data Importer plugin gains integration with the Discover/Explore page and receives several UI polish fixes. Users can now import data directly from within Explore via a new "Import data" button in the widget panel, and the importer UI has been refined with improved styling, layout consistency, and better embedded modal behavior.

## Details

### What's New in v3.5.0

#### Discover/Explore Integration (PR #11180)

The Data Importer is now accessible directly from the Explore page. When the plugin is enabled (`data_importer.enabled: true`), an "Import data" button appears in the Explore widget panel. Clicking it opens the importer in a modal dialog, allowing users to upload CSV, JSON, or NDJSON files and create indexes without leaving the Explore context.

This integration supports a key workflow for log analysts: supplementing log data with additional human-readable context. For example, users can import a CSV lookup table containing host metadata, then use PPL's `lookup` command to enrich their log queries with that data.

If the Data Importer plugin is not enabled, the button is not shown.

#### UI Fixes (PR #10961)

- Fixed text capitalization inconsistencies
- Renamed "Create new index" title for clarity
- Fixed spacing issues between input elements
- Unified font sizes with other Dashboards pages
- Updated data source selection behavior

#### Embedded Modal Style Improvements (PR #11241)

Follow-up to the Discover integration addressing code review feedback:

- Replaced inline styles with CSS classes for maintainability
- Fixed TypeScript type usage in `import_data_modal.tsx`
- Replaced radio buttons with a button group in `ImportTypeSelector`
- Fixed embedded modal layout and overflow issues
- Added ESLint rule to prevent future inline style usage

### Technical Changes

The integration adds a new `embedded` rendering mode to the Data Importer plugin, allowing it to be rendered inside a modal rather than as a standalone page. Key files changed:

- `src/plugins/data_importer/public/components/import_data_modal.tsx` - New modal wrapper component
- `src/plugins/explore/public/` - Widget panel integration with "Import data" button
- `src/plugins/data_importer/public/components/import_type_selector.tsx` - Refactored to use button group

## Limitations

- The "Import data" button only appears when `data_importer.enabled: true` is set in configuration
- The embedded modal inherits the same file size and text limits as the standalone importer

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#11180](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11180) | Integrate data importer with Discover/Explore | - |
| [#10961](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10961) | Fix UI changes for data importer | - |
| [#11241](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11241) | Improve style and overflow behavior for embedded data importers | - |
