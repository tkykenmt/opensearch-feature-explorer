---
tags:
  - domain/ml
  - component/server
  - indexing
  - ml
  - performance
---
# Flow Framework Bugfixes

## Summary

OpenSearch v3.2.0 includes five bug fixes for the Flow Framework plugin addressing memory issues, exception handling, API compatibility, race conditions, and default use case templates. These fixes improve stability and reliability when using Flow Framework for AI/ML workflow automation.

## Details

### What's New in v3.2.0

This release focuses on bug fixes across several areas:

1. **ApiSpecFetcher Memory and Exception Handling** - Fixed heap space overflow when parsing large OpenAPI specifications
2. **Bad Request Status Handling** - Improved error messages for workflow steps that fail with 400 errors
3. **RegisterLocalCustomModelStep Update** - Compatibility fix for OpenSearch 3.1+ model registration API changes
4. **Encryption Key Race Condition** - Fixed concurrent template creation causing decryption failures
5. **Default Use Case Connector Name** - Fixed incorrect substitution field in default workflow templates

### Technical Changes

#### ApiSpecFetcher Memory Fix (PR #1185)

The `ApiSpecFetcher` class was experiencing Java heap space overflow when parsing large OpenAPI specifications (e.g., ML Commons API spec).

**Root Cause**: Full OpenAPI spec resolution consumed excessive memory.

**Solution**:
- Added static caches for OpenAPI specs and required fields
- Implemented optimized `ParseOptions` with minimal memory usage
- Fixed exception handling logic in `compareRequiredFields` method

#### Bad Request Status Handling (PR #1190)

Workflow steps that failed with `BAD_REQUEST` status (e.g., index already exists) returned unhelpful `INTERNAL_SERVER_ERROR` messages.

**Before**:
```
Failed to create the index workflow_dense during step create_index_node, restStatus: INTERNAL_SERVER_ERROR
```

**After**:
```
[workflow_dense] already exists
```

**Solution**: Added `OpenSearchException` with `BAD_REQUEST` status to the list of allowed exceptions in `WorkflowStepException`.

#### RegisterLocalCustomModelStep Update (PR #1194)

OpenSearch 3.1+ changed the `RegisterModelInput` API to require `model_type`, `embedding_dimension`, and `framework_type` to be nested under `model_config`.

**Changes**:
- Constructs `TextEmbeddingModelConfig` from user input
- Adds support for `additional_config.space_type` required for semantic fields

**Example** (now supported):
```yaml
- id: register_deploy_embedding_model
  type: register_local_custom_model
  user_inputs:
    deploy: true
    name: Local embedding model
    function_name: TEXT_EMBEDDING
    model_format: ONNX
    model_config:
      model_type: distilbert
      embedding_dimension: 768
      framework_type: sentence_transformers
      additional_config:
        space_type: l2
```

#### Encryption Key Race Condition (PR #1200)

When two templates were created simultaneously in different threads, both could attempt to initialize the encryption key, causing decryption failures.

**Root Cause**: Without `.overwriteIfExists(false)` on `PutDataObjectRequest`, the second thread could overwrite the key after the first thread stored it.

**Solution**: Added `.overwriteIfExists(false)` which produces `RestStatus.CONFLICT` on race condition, triggering a retry to GET the existing key.

#### Default Use Case Connector Name Fix (PR #1205)

Three default use cases had incorrect substitution field `create_connector` instead of `create_connector.name` for connector name.

**Affected Use Cases**:
- `conversational_search_with_llm_deploy`
- Other default templates using connector name substitution

**Before** (incorrect):
```json
"name": "${{create_connector}}"
```

**After** (correct):
```json
"name": "${{create_connector.name}}"
```

## Limitations

- Memory optimizations in ApiSpecFetcher use static caches which persist for the lifetime of the JVM
- Race condition fix may cause brief retry delays during concurrent template creation

## References

### Documentation
- [Workflow Settings Documentation](https://docs.opensearch.org/3.0/automating-configurations/workflow-settings/)
- [opensearch-remote-metadata-sdk PR #228](https://github.com/opensearch-project/opensearch-remote-metadata-sdk/pull/228): Related overwriteIfExists fix

### Pull Requests
| PR | Description |
|----|-------------|
| [#1185](https://github.com/opensearch-project/flow-framework/pull/1185) | Fix ApiSpecFetcher Memory Issues and Exception Handling |
| [#1190](https://github.com/opensearch-project/flow-framework/pull/1190) | Better handling of Workflow Steps with Bad Request status |
| [#1194](https://github.com/opensearch-project/flow-framework/pull/1194) | Update RegisterLocalCustomModelStep for 3.1+ compatibility |
| [#1200](https://github.com/opensearch-project/flow-framework/pull/1200) | Avoid race condition setting encryption key |
| [#1205](https://github.com/opensearch-project/flow-framework/pull/1205) | Fixing connector name in default use case |

### Issues (Design / RFC)
- [Issue #1180](https://github.com/opensearch-project/flow-framework/issues/1180): Migrate workflow custom model registration to 3.1
- [Issue #1189](https://github.com/opensearch-project/flow-framework/issues/1189): Error message for CreateIndexStep when index exists is unhelpful
- [Issue #1197](https://github.com/opensearch-project/flow-framework/issues/1197): create_connector issue with connector name validation in 3.1.0

## Related Feature Report

- Full feature documentation
