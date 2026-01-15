---
tags:
  - opensearch
---
# Dynamic Mapping

## Summary

OpenSearch v2.16.0 introduces the `strict_allow_templates` dynamic mapping option. This new option provides a middle ground between `strict` and `true` modes, allowing new fields to be dynamically added only if they match predefined dynamic templates, while rejecting fields that don't match any template.

## Details

### What's New in v2.16.0

The `strict_allow_templates` option addresses a common use case where users want to:
- Prevent arbitrary fields from being added to the mapping
- Still allow controlled dynamic field creation through templates
- Get clear error messages when unmapped fields are encountered

### Dynamic Mapping Options Comparison

| Option | New Fields Indexed | Template Support | Unknown Fields |
|--------|-------------------|------------------|----------------|
| `true` | Yes | Yes | Auto-mapped |
| `false` | No | No | Stored in `_source` only |
| `strict` | No | No | Throws exception |
| `strict_allow_templates` | Template matches only | Yes | Throws exception |

### Technical Changes

The implementation adds a new `STRICT_ALLOW_TEMPLATES` enum value to `ObjectMapper.Dynamic` and modifies `DocumentParser` to:
1. Check if a field matches any dynamic template when `strict_allow_templates` is set
2. Allow the field to be indexed if a template match is found
3. Throw `StrictDynamicMappingException` if no template matches

Key files modified:
- `ObjectMapper.java`: Added `STRICT_ALLOW_TEMPLATES` enum value
- `DocumentParser.java`: Updated parsing logic to handle the new mode
- `StrictDynamicMappingException.java`: Updated error message to include dynamic mode name

### Usage Example

```json
PUT testindex
{
  "mappings": {
    "dynamic": "strict_allow_templates",
    "dynamic_templates": [
      {
        "strings": {
          "match": "room*",
          "match_mapping_type": "string",
          "mapping": {
            "type": "keyword"
          }
        }
      }
    ],
    "properties": {
      "patient": {
        "properties": {
          "id": { "type": "keyword" },
          "name": { "type": "keyword" }
        }
      }
    }
  }
}
```

With this configuration:
- `room1`, `room2` fields are allowed (match template)
- `patient.id`, `patient.name` are allowed (explicit mapping)
- `floor`, `unknown_field` will throw an exception

### Error Message

When a field doesn't match any template:
```json
{
  "error": {
    "type": "strict_dynamic_mapping_exception",
    "reason": "mapping set to strict_allow_templates, dynamic introduction of [field_name] within [_doc] is not allowed"
  },
  "status": 400
}
```

## Limitations

- The `strict_allow_templates` setting applies at the object level and can be set differently for nested objects
- Fields that don't match templates will cause the entire document indexing to fail
- Template matching follows the same rules as regular dynamic templates (first match wins)

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#14555](https://github.com/opensearch-project/OpenSearch/pull/14555) | Add `strict_allow_templates` dynamic mapping option | [#11276](https://github.com/opensearch-project/OpenSearch/issues/11276) |

### Documentation
- [Dynamic parameter](https://docs.opensearch.org/2.16/field-types/dynamic/)
- [Object field type](https://docs.opensearch.org/2.16/field-types/supported-field-types/object/)
