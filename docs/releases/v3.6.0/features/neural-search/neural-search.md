---
tags:
  - neural-search
---
# Neural Search

## Summary

OpenSearch v3.6.0 includes two bug fixes for the neural-search plugin: fixing the rerank processor's inability to extract text from nested and dot-notation fields in `document_fields`, and removing an invalid validation that blocked remote symmetric embedding models from being used with the `semantic` field type.

## Details

### What's New in v3.6.0

#### Fix: Rerank Processor Nested and Dot-Notation Field Extraction

The `DocumentContextSourceFetcher` in the rerank processor had a bug where `hit.getSourceAsMap().containsKey(field)` was used as a guard before calling `ObjectPath.eval()`. For dot-notation paths like `content.text`, `containsKey()` checks for the literal key in the top-level map and returns `false`, so the field value was never extracted. The reranker received empty strings, making reranking have no effect on documents with nested or dot-notation fields.

Additionally, for nested type fields where `_source` contains an array of objects, the previous code did not handle list traversal.

The fix replaces the broken field extraction logic with `ProcessorUtils.getValueFromSource()`, which already existed in the codebase and correctly handles:
- Dot-notation traversal through nested maps (e.g., `metadata.author`)
- Array-of-objects traversal (e.g., `content.text` where `content` is a list of objects)
- Concatenation of multiple values from array fields into a single space-separated string

This utility was already used by `ByFieldRerankProcessor`, so the fix aligns `DocumentContextSourceFetcher` with the same proven approach.

#### Fix: Remote Symmetric Model Support

An invalid validation in `NeuralSearchMLInputBuilder.createTextEmbeddingInput()` threw an `IllegalArgumentException` ("Remote models are only supported for asymmetric E5 text embedding") when a remote model was detected as non-asymmetric. This was a regression introduced in a prior version that prevented users from using remote symmetric embedding models (e.g., `ext-embedding-ada-002`) with the `semantic` field type.

The fix removes the incorrect validation check and allows remote symmetric models to pass through to the standard `MLInput` construction path, using `FunctionName.TEXT_EMBEDDING` directly instead of routing through `createLocalInput()`.

### Technical Changes

| Component | Change | File |
|-----------|--------|------|
| `DocumentContextSourceFetcher` | Replaced `containsKey()` + `ObjectPath.eval()` with `ProcessorUtils.getValueFromSource()` for correct nested/dot-notation field extraction; added `List` concatenation support | `DocumentContextSourceFetcher.java` |
| `NeuralSearchMLInputBuilder` | Removed invalid `RemoteModelConfig` + `!isAsymmetric` validation; changed non-asymmetric path to use `new MLInput()` directly | `NeuralSearchMLInputBuilder.java` |

## Limitations

- The rerank processor fix depends on `ProcessorUtils.getValueFromSource()` behavior; deeply nested structures beyond what this utility supports may still not work
- Remote symmetric models must still be properly deployed and configured in ML Commons

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#1805](https://github.com/opensearch-project/neural-search/pull/1805) | Fix rerank processor unable to extract text from nested and dot-notation fields in document_fields | [#657](https://github.com/opensearch-project/neural-search/issues/657) |
| [#1767](https://github.com/opensearch-project/neural-search/pull/1767) | Fix issue where remote symmetric models are not supported | [#1765](https://github.com/opensearch-project/neural-search/issues/1765) |
