# Flow Framework Bugfixes

## Summary

This release fixes an incorrect default value for the output dimension in the semantic search with local model workflow template. The `paraphrase-MiniLM-L3-v2` model outputs 384-dimensional vectors, but the template incorrectly specified 768 dimensions, causing vector dimension mismatch errors during document ingestion.

## Details

### What's New in v3.4.0

Fixed the `text_embedding.field_map.output.dimension` default value in the `semantic-search-with-local-model-defaults.json` template from 768 to 384 to match the actual output dimension of the `paraphrase-MiniLM-L3-v2` model.

### Technical Changes

#### Bug Description

When using the `semantic_search_with_local_model` workflow template, users encountered the following error when uploading documents to the vector index:

```json
{
  "caused_by": {
    "type": "illegal_argument_exception",
    "reason": "Vector dimension mismatch. Expected: 768, Given: 384"
  }
}
```

The root cause was that the default configuration file specified an incorrect output dimension (768) that did not match the actual output dimension (384) of the `huggingface/sentence-transformers/paraphrase-MiniLM-L3-v2` model.

#### Configuration Change

| Setting | Before | After |
|---------|--------|-------|
| `text_embedding.field_map.output.dimension` | `768` | `384` |

#### Affected File

- `src/main/resources/defaults/semantic-search-with-local-model-defaults.json`

### Usage Example

The semantic search with local model workflow can now be used without overriding the dimension parameter:

```bash
# Create and provision the workflow (now works correctly)
POST /_plugins/_flow_framework/workflow?use_case=semantic_search_with_local_model&provision=true

# Ingest documents (no longer causes dimension mismatch error)
PUT /my-nlp-index/_doc/1
{
  "passage_text": "Hello world",
  "id": "s1"
}
```

### Migration Notes

Users who previously worked around this issue by manually overriding the dimension parameter can now remove that override:

```json
// No longer needed
{
  "text_embedding.field_map.output.dimension": "384"
}
```

## Limitations

- This fix only affects the `semantic_search_with_local_model` workflow template
- Existing workflows created with the incorrect dimension will need to be recreated

## References

### Documentation
- [Hugging Face Model](https://huggingface.co/sentence-transformers/paraphrase-MiniLM-L3-v2): Model documentation confirming 384-dimensional output
- [Workflow Templates Documentation](https://docs.opensearch.org/3.0/automating-configurations/workflow-templates/): Official documentation for workflow templates

### Pull Requests
| PR | Description |
|----|-------------|
| [#1270](https://github.com/opensearch-project/flow-framework/pull/1270) | Fix incorrect field map output dimensions in default values |

### Issues (Design / RFC)
- [Issue #1254](https://github.com/opensearch-project/flow-framework/issues/1254): Bug report for incorrect output dimensions

## Related Feature Report

- [Full feature documentation](../../../features/flow-framework/flow-framework.md)
