---
tags:
  - opensearch-dashboards
---
# Dashboards Data Plugin

## Summary

OpenSearch Dashboards v3.5.0 adds support for the `flat_object` field type in the Data plugin. Previously, fields mapped as `flat_object` in OpenSearch were not recognized by Dashboards, causing them to be displayed as unknown type in index patterns. With this change, `flat_object` fields are properly mapped to the OSD `string` field type, enabling correct display in index pattern management and search functionality in Discover.

## Details

### What's New in v3.5.0

The `flat_object` field type (introduced in OpenSearch 2.7) stores entire JSON objects as a single field without indexing subfields individually. This is useful for preventing mapping explosions when dealing with documents containing many dynamic keys. However, OpenSearch Dashboards did not recognize this field type, treating it as unknown.

This change registers `flat_object` as a recognized OpenSearch field type and maps it to the OSD `string` type, consistent with how other text-like types (`text`, `keyword`, `match_only_text`, `wildcard`) are handled.

### Technical Changes

Three files in the Data plugin's `osd_field_types` module were modified:

| File | Change |
|------|--------|
| `types.ts` | Added `FLAT_OBJECT = 'flat_object'` to the `OPENSEARCH_FIELD_TYPES` enum |
| `osd_field_types_factory.ts` | Added `OPENSEARCH_FIELD_TYPES.FLAT_OBJECT` to the `string` OSD field type's `esTypes` array |
| `osd_field_types.test.ts` | Added test verifying `flat_object` maps to `string` |

The mapping means `flat_object` fields are:
- **Sortable**: Yes (inherits from string type)
- **Filterable**: Yes (inherits from string type)
- **Displayed as**: `string` in index pattern field lists

## Limitations

- The `flat_object` type is mapped as a plain `string` in Dashboards. Subfield dot-path notation (e.g., `issue.labels.version`) is not surfaced as separate fields in index patterns.
- Aggregations on `flat_object` subfields using dot notation are not supported by the underlying OpenSearch engine, so Dashboards visualizations based on subfield aggregations are not available.

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#11085](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11085) | feat: support flat_object field type | [#9348](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/9348) |

### Documentation
- [Flat object field type](https://docs.opensearch.org/latest/mappings/supported-field-types/flat-object/)
