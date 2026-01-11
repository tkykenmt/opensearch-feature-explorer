# WildcardFieldMapper

## Summary

OpenSearch v3.4.0 changes the default value of `doc_values` in `WildcardFieldMapper` from `false` to `true`. This aligns the wildcard field type with other field mappers and fixes a bug where nested queries on wildcard fields returned no results when `doc_values` was not explicitly enabled.

## Details

### What's New in v3.4.0

The `doc_values` parameter for wildcard fields now defaults to `true` instead of `false`. This change:

1. **Fixes nested query bug**: Wildcard fields inside nested objects now work correctly without explicit configuration
2. **Aligns with other field types**: Most field mappers default to `doc_values: true`
3. **Enables aggregations and sorting by default**: Users can now aggregate and sort on wildcard fields without additional configuration

### Technical Changes

#### Architecture Changes

```mermaid
graph TB
    subgraph "Before v3.4.0"
        A1[Wildcard Field] --> B1[doc_values: false]
        B1 --> C1[Nested Query]
        C1 --> D1[No stored field in sub-doc]
        D1 --> E1[No Results]
    end
    
    subgraph "After v3.4.0"
        A2[Wildcard Field] --> B2[doc_values: true]
        B2 --> C2[Nested Query]
        C2 --> D2[DocValueFetcher retrieves value]
        D2 --> E2[Correct Results]
    end
```

#### Code Changes

| File | Change |
|------|--------|
| `WildcardFieldMapper.java` | Changed `hasDocValues` default from `false` to `true` |
| `WildcardFieldMapper.java` | Added null check for `searchLookup` in `valueFetcher()` |

#### Root Cause

The wildcard field type retrieves field values from either:
- **DocValues** (if `doc_values: true`)
- **Stored field** (if `doc_values: false`)

For nested fields, sub-documents do not build stored indexes. When `doc_values` was `false` by default, nested wildcard queries could not retrieve values from sub-documents, causing queries to return no results.

### Usage Example

Before v3.4.0, nested wildcard queries required explicit `doc_values: true`:

```json
PUT wildcard_index
{
  "mappings": {
    "properties": {
      "outer_field": {
        "type": "nested",
        "properties": {
          "wildcard_field": {
            "type": "wildcard",
            "doc_values": true  // Required before v3.4.0
          }
        }
      }
    }
  }
}
```

After v3.4.0, the explicit setting is no longer needed:

```json
PUT wildcard_index
{
  "mappings": {
    "properties": {
      "outer_field": {
        "type": "nested",
        "properties": {
          "wildcard_field": {
            "type": "wildcard"  // doc_values: true by default
          }
        }
      }
    }
  }
}

PUT wildcard_index/_doc/1
{
  "outer_field": {
    "wildcard_field": "abcd"
  }
}

POST wildcard_index/_search
{
  "query": {
    "nested": {
      "path": "outer_field",
      "query": {
        "wildcard": {
          "outer_field.wildcard_field": "*bc*"
        }
      }
    }
  }
}
```

This query now returns the expected document.

### Migration Notes

- **Backward compatible**: The parameter is always serialized, so existing indexes with explicit `doc_values` settings are unaffected
- **New indexes**: Will have `doc_values: true` by default, which may slightly increase storage but enables more functionality
- **To disable**: Explicitly set `doc_values: false` if you want the previous behavior

## Limitations

- Indexes created before v3.4.0 without explicit `doc_values: true` will retain `doc_values: false`
- Slightly increased storage for new indexes due to doc values being enabled by default

## Related PRs

| PR | Description |
|----|-------------|
| [#19796](https://github.com/opensearch-project/OpenSearch/pull/19796) | Change the default value of doc_values in WildcardFieldMapper to true |

## References

- [Issue #18678](https://github.com/opensearch-project/OpenSearch/issues/18678): Bug report for nested query on wildcard type field returning no results
- [Wildcard Field Documentation](https://docs.opensearch.org/3.0/field-types/supported-field-types/wildcard/): Official documentation

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/wildcard-field.md)
