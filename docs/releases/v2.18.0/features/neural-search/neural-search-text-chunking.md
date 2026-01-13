---
tags:
  - domain/search
  - component/server
  - neural-search
  - search
---
# Neural Search Text Chunking Enhancement

## Summary

This release adds the `ignore_missing` parameter to text chunking processors in the neural-search plugin. When enabled, the processor skips fields that don't exist in the document instead of outputting an empty list, providing more flexible handling of optional text fields during ingestion.

## Details

### What's New in v2.18.0

The text chunking processor now supports an `ignore_missing` boolean parameter that controls how the processor handles missing or null input fields.

### Technical Changes

#### New Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `ignore_missing` | When `true`, missing fields are skipped and no output field is created. When `false`, missing fields result in an empty list in the output field. | `false` |

#### Behavior Comparison

**With `ignore_missing: false` (default):**
- Input document without the mapped field produces an empty list in the output field
- Maintains backward compatibility with existing pipelines

**With `ignore_missing: true`:**
- Input document without the mapped field is passed through unchanged
- No output field is created for missing input fields
- Useful for pipelines processing documents with optional text fields

### Usage Example

```json
PUT _ingest/pipeline/text-chunking-pipeline
{
  "description": "Text chunking with ignore_missing enabled",
  "processors": [
    {
      "text_chunking": {
        "ignore_missing": true,
        "field_map": {
          "body": "body_chunk"
        },
        "algorithm": {
          "fixed_token_length": {
            "token_limit": 10,
            "tokenizer": "letter"
          }
        }
      }
    }
  ]
}
```

**Input document (missing `body` field):**
```json
{
  "name": "OpenSearch"
}
```

**Output with `ignore_missing: true`:**
```json
{
  "name": "OpenSearch"
}
```

**Output with `ignore_missing: false` (default):**
```json
{
  "name": "OpenSearch",
  "body_chunk": []
}
```

### Migration Notes

- Existing pipelines are unaffected as the default value is `false`
- To adopt this feature, add `"ignore_missing": true` to your text chunking processor configuration

## Limitations

- The `ignore_missing` parameter only affects null/missing fields; empty strings are still processed and produce empty chunk results

## References

### Documentation
- [Documentation](https://docs.opensearch.org/2.18/ingest-pipelines/processors/text-chunking/): Text chunking processor documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#907](https://github.com/opensearch-project/neural-search/pull/907) | Add ignore_missing field to text chunking processors |

### Issues (Design / RFC)
- [Issue #906](https://github.com/opensearch-project/neural-search/issues/906): Feature request for ignore_missing field

## Related Feature Report

- Full feature documentation
