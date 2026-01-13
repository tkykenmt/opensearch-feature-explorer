---
tags:
  - domain/core
  - component/server
  - indexing
  - observability
---
# Dynamic Mapping: false_allow_templates Option

## Summary

OpenSearch v3.3.0 introduces a new `dynamic` mapping parameter value: `false_allow_templates`. This option provides a middle ground between `dynamic: false` and `dynamic: true`, allowing fields that match predefined `dynamic_templates` to be indexed while silently ignoring fields that don't match any template or explicit mapping.

## Details

### What's New in v3.3.0

The `false_allow_templates` option addresses a common use case where users want to:
- Define explicit mappings for known fields
- Use dynamic templates for predictable naming patterns (e.g., `date_*`, `metric_*`)
- Silently ignore unexpected fields without throwing errors

Previously, users had to choose between:
- `dynamic: true` - indexes all fields (including unwanted ones)
- `dynamic: false` - disables dynamic templates entirely
- `dynamic: strict` - throws errors on unknown fields
- `dynamic: strict_allow_templates` - throws errors on fields not matching templates

### Technical Changes

#### New Dynamic Mapping Option

| Option | Behavior |
|--------|----------|
| `true` | All new fields are dynamically mapped |
| `false` | New fields are ignored, not indexed, but stored in `_source` |
| `strict` | Throws exception on unknown fields |
| `strict_allow_templates` | Maps fields matching templates, throws exception on others |
| `false_allow_templates` | Maps fields matching templates, silently ignores others |

#### Implementation Details

The feature modifies the `DocumentParser` class to handle the new dynamic option:
- When a field matches a `dynamic_template`, it creates the mapping as defined
- When a field doesn't match any template or explicit property, it skips indexing but preserves the field in `_source`
- Supports all field types: objects, arrays, strings, numbers, booleans, dates, and binary data

### Usage Example

```json
PUT my-index
{
  "mappings": {
    "dynamic": "false_allow_templates",
    "dynamic_templates": [
      {
        "dates": {
          "match": "date_*",
          "mapping": {
            "type": "date"
          }
        }
      }
    ],
    "properties": {
      "url": { "type": "keyword" }
    }
  }
}
```

Index a document with mixed fields:

```json
POST my-index/_doc/1
{
  "url": "https://example.com",
  "date_timestamp": "2024-01-01T00:00:00Z",
  "date_timezone": "2024-01-02T00:00:00Z",
  "author": "John Doe"
}
```

Resulting mapping:

```json
{
  "properties": {
    "url": { "type": "keyword" },
    "date_timestamp": { "type": "date" },
    "date_timezone": { "type": "date" }
  }
}
```

The `author` field is stored in `_source` but not indexed or searchable.

### Migration Notes

To adopt this feature:
1. Update index mappings to use `"dynamic": "false_allow_templates"`
2. Define `dynamic_templates` for fields that should be dynamically mapped
3. Existing indexes require reindexing to apply the new mapping behavior

## Limitations

- Fields not matching templates are stored in `_source` but cannot be searched or aggregated
- The feature requires OpenSearch 3.3.0 or later
- Cannot be combined with other dynamic values on the same mapping level

## References

### Documentation
- [Documentation: Dynamic mapping parameter](https://docs.opensearch.org/3.0/field-types/mapping-parameters/dynamic/): Official docs on dynamic mapping
- [Documentation PR #10388](https://github.com/opensearch-project/documentation-website/pull/10388): Documentation update
- [API Specification PR #944](https://github.com/opensearch-project/opensearch-api-specification/pull/944): API spec update

### Pull Requests
| PR | Description |
|----|-------------|
| [#19065](https://github.com/opensearch-project/OpenSearch/pull/19065) | Add `false_allow_templates` as a dynamic mapping option |

### Issues (Design / RFC)
- [Issue #18617](https://github.com/opensearch-project/OpenSearch/issues/18617): Feature request for `false_allow_templates`

## Related Feature Report

- [Full feature documentation](../../../features/opensearch/opensearch-dynamic-mapping.md)
