---
tags:
  - domain/ml
  - component/dashboards
  - dashboards
  - indexing
  - search
---
# Data Ingestion Dashboards

## Summary

This release item includes bug fixes and enhancements to the data ingestion experience in OpenSearch Flow (dashboards-flow-framework plugin). Key improvements include fine-grained error handling for ingest and search pipelines, JSON Lines format support for data ingestion, local cluster version detection fixes, and various UX improvements.

## Details

### What's New in v3.0.0

The Data Ingestion Dashboards improvements in v3.0.0 focus on enhancing the user experience when building AI search workflows through OpenSearch Flow. These changes make it easier to ingest data, debug pipeline errors, and work with local clusters.

### Technical Changes

#### Fine-Grained Error Handling (#598)

Surfaces processor-level errors for both ingest and search flows:

- **Ingest errors**: Uses the `verbose` parameter from the simulate pipeline API to check for errors before data ingestion
- **Search errors**: Passes `verbose_pipeline=true` to the search API to fetch processor-level results
- Errors are displayed in two places:
  1. The `Errors` tab in the Inspector with details about failed processors
  2. Error icons next to processors in the form with hover tooltips

#### JSON Lines Format Support (#639)

Changed the ingestion input format from JSON array to JSON Lines format (https://jsonlines.org/):

- New `JsonLinesField` component with specific error handling and formatting
- File upload now accepts `*.jsonl` extension
- New JSON Lines config field type with corresponding schema/value presets
- Updated all ingest docs parsing to handle JSON Lines strings

#### Local Cluster Version Detection (#606)

Fixed an issue where selecting a local data source showed a loading state without rendering presets:

- Now correctly retrieves version from the datasource
- Renders presets based on the data source version

#### UX Improvements

| PR | Description |
|----|-------------|
| #613 | Added prompt message when no compatible datasource; index configurations retained in configure ingest page |
| #618 | Fixed `Get started` accordion visibility; BWC 2.17 datasource support; processor error reformatting; model refresh buttons |
| #630 | Loading state improvements when switching datasources; fixed "Transform query" section visibility |
| #644 | Description fields changed to textarea; unsaved changes confirmation modal; normalization processor UI updates |
| #654 | Fixed Search Index bug in Local Cluster scenario |
| #672 | Fixed UI autofilling edge cases after JSON Lines format change |

### Usage Example

Data ingestion now uses JSON Lines format:

```jsonl
{"title": "Document 1", "content": "First document content"}
{"title": "Document 2", "content": "Second document content"}
{"title": "Document 3", "content": "Third document content"}
```

### Migration Notes

- If you have existing workflows using JSON array format for ingestion, you'll need to convert your data to JSON Lines format
- File uploads now require `.jsonl` extension instead of `.json`

## Limitations

- JSON Lines format requires one JSON object per line with no trailing commas
- Error handling requires models with properly defined interfaces for best results

## References

### Documentation
- [Documentation: Building AI search workflows](https://docs.opensearch.org/3.0/vector-search/ai-search/workflow-builder/): Official OpenSearch Flow documentation
- [JSON Lines specification](https://jsonlines.org/): JSON Lines format specification

### Pull Requests
| PR | Description |
|----|-------------|
| [#598](https://github.com/opensearch-project/dashboards-flow-framework/pull/598) | Add fine-grained error handling; misc bug fixes |
| [#639](https://github.com/opensearch-project/dashboards-flow-framework/pull/639) | Change ingestion input to JSON lines format |
| [#606](https://github.com/opensearch-project/dashboards-flow-framework/pull/606) | Fix error that local cluster cannot get version |
| [#613](https://github.com/opensearch-project/dashboards-flow-framework/pull/613) | UX fit-n-finish updates XI |
| [#618](https://github.com/opensearch-project/dashboards-flow-framework/pull/618) | UX fit-n-finish updates XII |
| [#630](https://github.com/opensearch-project/dashboards-flow-framework/pull/630) | Bug fixes XIII |
| [#644](https://github.com/opensearch-project/dashboards-flow-framework/pull/644) | Various bug fixes & improvements |
| [#654](https://github.com/opensearch-project/dashboards-flow-framework/pull/654) | Fixed bug related to Search Index in Local Cluster scenario |
| [#672](https://github.com/opensearch-project/dashboards-flow-framework/pull/672) | Fix missed UI autofilling after JSON Lines change |

### Issues (Design / RFC)
- [Issue #571](https://github.com/opensearch-project/dashboards-flow-framework/issues/571): Fine-grained error handling feature request
- [Issue #627](https://github.com/opensearch-project/dashboards-flow-framework/issues/627): Various bug fixes request
- [Issue #653](https://github.com/opensearch-project/dashboards-flow-framework/issues/653): Search Index Local Cluster bug

## Related Feature Report

- Full feature documentation
