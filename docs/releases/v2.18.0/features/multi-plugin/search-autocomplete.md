---
tags:
  - domain/infra
  - component/server
  - dashboards
  - search
---
# Search Autocomplete

## Summary

OpenSearch v2.18.0 brings two improvements to search autocomplete functionality: a bug fix for `search_as_you_type` field type to support multi-fields in OpenSearch core, and enhanced autocomplete UX in OpenSearch Dashboards with persistent suggestion windows and user hints.

## Details

### What's New in v2.18.0

This release includes improvements across both OpenSearch and OpenSearch Dashboards:

1. **search_as_you_type Multi-Fields Support (OpenSearch)**: Fixed a bug where `search_as_you_type` fields silently ignored the `fields` parameter in mapping definitions. Now multi-fields (subfields) are properly created and indexed.

2. **Autocomplete UX Improvements (Dashboards)**: Enhanced the query editor autocomplete experience with persistent suggestion windows, user hints, and improved operator styling.

### Technical Changes

#### OpenSearch: search_as_you_type Multi-Fields Fix

The `SearchAsYouTypeFieldMapper` was not resolving the `fields` parameter, causing multi-fields to be silently ignored. The fix modifies the mapper to properly build and pass multi-fields to the parent constructor.

**Before (Bug)**:
```java
return new SearchAsYouTypeFieldMapper(
    name, ft, copyTo.build(), prefixFieldMapper, shingleFieldMappers, this);
```

**After (Fixed)**:
```java
return new SearchAsYouTypeFieldMapper(
    name, ft, multiFieldsBuilder.build(this, context), copyTo.build(),
    prefixFieldMapper, shingleFieldMappers, this);
```

#### New Mapping Capability

You can now define multi-fields on `search_as_you_type` fields:

```json
PUT my_index
{
  "mappings": {
    "properties": {
      "title": {
        "type": "search_as_you_type",
        "fields": {
          "sortable": {
            "type": "keyword",
            "normalizer": "lowercase_normalizer"
          }
        }
      }
    }
  }
}
```

#### OpenSearch Dashboards: Autocomplete UX Enhancements

| Change | Description |
|--------|-------------|
| Persistent suggestion window | Suggestion window stays open when editor is focused, after typing space, and after selecting a suggestion |
| User hints | Added "Tab to insert, ESC to close window" hint below suggestion window |
| Operator styling | DQL operators (AND, OR, NOT) now display with distinct operator icon and styling |
| Trigger on focus | Suggestions automatically appear when clicking into the query editor |

**Key Implementation Details**:

- Added `triggerSuggestOnFocus` prop to `CodeEditor` component
- Added `triggerCharacters: [' ']` to trigger suggestions after space
- Added command to trigger next suggestion after selection: `{ id: 'editor.action.triggerSuggest', title: 'Trigger Next Suggestion' }`
- Added CSS pseudo-element for user hints via `.suggest-widget.visible::after`

### Usage Example

**Using search_as_you_type with multi-fields**:

```json
// Create index with search_as_you_type and keyword subfield
PUT products
{
  "mappings": {
    "properties": {
      "name": {
        "type": "search_as_you_type",
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      }
    }
  }
}

// Search with bool_prefix for autocomplete
GET products/_search
{
  "query": {
    "multi_match": {
      "query": "lap",
      "type": "bool_prefix",
      "fields": ["name", "name._2gram", "name._3gram"]
    }
  }
}

// Use keyword subfield for exact match or sorting
GET products/_search
{
  "query": { "term": { "name.keyword": "Laptop Pro" } },
  "sort": [{ "name.keyword": "asc" }]
}
```

## Limitations

- The `search_as_you_type` multi-fields fix is available in v2.18.0+ and v3.0.0+
- Dashboards autocomplete improvements apply to DQL queries; PPL and SQL may require additional modifications for optimal behavior

## References

### Documentation
- [search_as_you_type Documentation](https://docs.opensearch.org/2.18/field-types/supported-field-types/search-as-you-type/): Official field type documentation
- [Autocomplete Documentation](https://docs.opensearch.org/2.18/search-plugins/searching-data/autocomplete/): Autocomplete functionality guide

### Pull Requests
| PR | Repository | Description |
|----|------------|-------------|
| [#15988](https://github.com/opensearch-project/OpenSearch/pull/15988) | OpenSearch | Fix search_as_you_type not supporting multi-fields |
| [#7991](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/7991) | OpenSearch-Dashboards | Keep Autocomplete suggestion window open and put user hints below the suggestion window |

### Issues (Design / RFC)
- [Issue #5035](https://github.com/opensearch-project/OpenSearch/issues/5035): Original bug report for search_as_you_type multi-fields

## Related Feature Report

- [Full feature documentation](../../../../features/multi-plugin/multi-plugin-search-autocomplete.md)
