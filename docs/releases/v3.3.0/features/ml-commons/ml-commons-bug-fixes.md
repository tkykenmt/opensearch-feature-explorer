# ML Commons Bug Fixes

## Summary

OpenSearch v3.3.0 includes 29 bug fixes for the ML Commons plugin, addressing issues across the Agent Framework, Agentic Memory, multi-tenancy, RAG responses, and various parsing and validation problems. These fixes improve stability and reliability for ML workloads.

## Details

### What's New in v3.3.0

This release focuses on stability improvements across multiple ML Commons subsystems:

- **Agent Framework**: Fixed exception handling, tool parsing, and LLM response processing
- **Agentic Memory**: Improved memory container management, validation, and security
- **Multi-tenancy**: Fixed NPE and access validation issues
- **RAG/Generative QA**: Fixed missing responses in search templates
- **Model Management**: Fixed deployment issues and embedding type updates

### Technical Changes

#### Agent Framework Fixes

| Issue | Fix | PR |
|-------|-----|-----|
| Empty LLM content causes NPE | Added null check before tool use processing | [#4138](https://github.com/opensearch-project/ml-commons/pull/4138) |
| Steps with commas break parsing | Return original JSON instead of double conversion | [#4138](https://github.com/opensearch-project/ml-commons/pull/4138) |
| Nested JSON in tool parameters fails | Fall back to string with clearer exception | [#4138](https://github.com/opensearch-project/ml-commons/pull/4138) |
| Runtime exceptions not marked as failures | Task now marked failed with proper error message | [#4263](https://github.com/opensearch-project/ml-commons/pull/4263) |
| Invalid `_llm_interface` not validated | Added validation for this parameter | [#4263](https://github.com/opensearch-project/ml-commons/pull/4263) |
| JSON parsing error in long-term memory | Extract JSON processor to handle invalid LLM output | [#4278](https://github.com/opensearch-project/ml-commons/pull/4278) |
| LLM result path errors | Fixed path extraction and prompt conversion | [#4283](https://github.com/opensearch-project/ml-commons/pull/4283), [#4292](https://github.com/opensearch-project/ml-commons/pull/4292) |

#### Agentic Memory Fixes

| Issue | Fix | PR |
|-------|-----|-----|
| Missing validation for strategies without LLM | Throw exception when strategies declared without LLM/embedding model | [#4284](https://github.com/opensearch-project/ml-commons/pull/4284) |
| Embedding model conflict on existing index | Throw exception when updating with different embedding model | [#4284](https://github.com/opensearch-project/ml-commons/pull/4284) |
| New strategies without index setup | Initiate indices with proper validation | [#4284](https://github.com/opensearch-project/ml-commons/pull/4284) |
| Non-owner can delete memory container | Only container owner can delete | [#4258](https://github.com/opensearch-project/ml-commons/pull/4258) |
| Delete by query response parsing | Use builtin BulkByScrollResponse parser | [#4237](https://github.com/opensearch-project/ml-commons/pull/4237) |
| Cannot update from TEXT_EMBEDDING to SPARSE_ENCODING | Auto-clear dimension when switching to SPARSE_ENCODING | [#4297](https://github.com/opensearch-project/ml-commons/pull/4297) |
| Wrong field name in working memory API | Fixed field name | [#4255](https://github.com/opensearch-project/ml-commons/pull/4255) |
| LLM not verified before session summarize | Added LLM verification | [#4300](https://github.com/opensearch-project/ml-commons/pull/4300) |

#### Multi-tenancy Fixes

| Issue | Fix | PR |
|-------|-----|-----|
| NPE when executing flow agent with multi-tenancy off | Handle null `tenant_id` in serialization | [#4189](https://github.com/opensearch-project/ml-commons/pull/4189) |
| Validate access broken for multi-tenancy | Fixed validation logic | [#4196](https://github.com/opensearch-project/ml-commons/pull/4196) |

#### RAG/Generative QA Fixes

| Issue | Fix | PR |
|-------|-----|-----|
| Missing RAG response in search templates | Override `innerToXContent()` to include ext block | [#4118](https://github.com/opensearch-project/ml-commons/pull/4118) |

#### Other Fixes

| Issue | Fix | PR |
|-------|-----|-----|
| Metrics correlation algorithm broken | Fixed index mapping for model group index | [#4200](https://github.com/opensearch-project/ml-commons/pull/4200) |
| Model deploy issues | Fixed deployment flow | [#4003](https://github.com/opensearch-project/ml-commons/pull/4003) |
| Batch predict model interface validation | Skip validation for batch predict | [#4219](https://github.com/opensearch-project/ml-commons/pull/4219) |
| MLTaskState enum serialization errors | Fixed serialization | [#4158](https://github.com/opensearch-project/ml-commons/pull/4158) |
| Approver matching not exact | Changed to exact match | [#4247](https://github.com/opensearch-project/ml-commons/pull/4247) |
| Approver parsing bug in require-approval workflow | Fixed parsing | [#4259](https://github.com/opensearch-project/ml-commons/pull/4259) |
| MLSdkAsyncHttpResponseHandler exception type | Return IllegalArgumentException | [#4182](https://github.com/opensearch-project/ml-commons/pull/4182) |

### New Processors Added

The release also adds new processors to support Agentic Memory:

- **Extract JSON Processor**: Extracts valid JSON from LLM output that may contain invalid JSON
- **For Each Processor**: Processes each item in an array (useful for adding required fields to messages)
- **Input Processor Support**: Allows configuring input processors for models

### Usage Example

Memory container deletion with selective memory deletion:

```json
DELETE /_plugins/_ml/memory_containers/{container_id}?delete_memories=sessions,working

// Or with request body
DELETE /_plugins/_ml/memory_containers/{container_id}
{
    "delete_memories": ["sessions", "long-term", "history"]
}
```

Strategy-level LLM override:

```json
PUT _plugins/_ml/memory_containers/{container_id}
{
  "llm_id": "default_llm_id",
  "strategies": [
    {
      "id": "semantic_f904644b",
      "enabled": true,
      "configuration": {
        "llm_id": "override_llm_id"
      }
    }
  ]
}
```

## Limitations

- Some fixes are specific to the new Agentic Memory feature which is experimental
- Multi-tenancy fixes require proper configuration of the multi-tenancy feature

## Related PRs

| PR | Description |
|----|-------------|
| [#4138](https://github.com/opensearch-project/ml-commons/pull/4138) | Agent/Tool Parsing Fixes |
| [#4189](https://github.com/opensearch-project/ml-commons/pull/4189) | Fix NPE when execute flow agent with multi tenancy is off |
| [#4263](https://github.com/opensearch-project/ml-commons/pull/4263) | Exception handling for runtime exceptions during async execution |
| [#4284](https://github.com/opensearch-project/ml-commons/pull/4284) | Add validations during create and update memory container |
| [#4258](https://github.com/opensearch-project/ml-commons/pull/4258) | Allow only container owner to delete memory container |
| [#4118](https://github.com/opensearch-project/ml-commons/pull/4118) | Fix missing RAG response from generative_qa_parameters |
| [#4278](https://github.com/opensearch-project/ml-commons/pull/4278) | Fix json parsing error; add for each processor |
| [#4297](https://github.com/opensearch-project/ml-commons/pull/4297) | Fix dimension update flow to allow embedding type update |
| [#4200](https://github.com/opensearch-project/ml-commons/pull/4200) | Fixing metrics correlation algorithm |
| [#4196](https://github.com/opensearch-project/ml-commons/pull/4196) | Fixing validate access for multi-tenancy |
| [#4237](https://github.com/opensearch-project/ml-commons/pull/4237) | Use builtin BulkByScrollResponse parser |
| [#4167](https://github.com/opensearch-project/ml-commons/pull/4167) | Fix claude model it |
| [#4214](https://github.com/opensearch-project/ml-commons/pull/4214) | Fix error_prone_annotations jar hell |
| [#4132](https://github.com/opensearch-project/ml-commons/pull/4132) | Fix failing UTs and increment version |
| [#4151](https://github.com/opensearch-project/ml-commons/pull/4151) | Fix jdt formatter error |
| [#4003](https://github.com/opensearch-project/ml-commons/pull/4003) | Fix model deploy issue |
| [#4234](https://github.com/opensearch-project/ml-commons/pull/4234) | Refactor memory delete by query API |
| [#4158](https://github.com/opensearch-project/ml-commons/pull/4158) | Fix MLTaskState enum serialization errors |
| [#4233](https://github.com/opensearch-project/ml-commons/pull/4233) | Fix connector tool IT |
| [#4210](https://github.com/opensearch-project/ml-commons/pull/4210) | Fixing build issue in ml-commons |
| [#4182](https://github.com/opensearch-project/ml-commons/pull/4182) | Make MLSdkAsyncHttpResponseHandler return IllegalArgumentException |
| [#4219](https://github.com/opensearch-project/ml-commons/pull/4219) | Skip model interface validation for batch predict |
| [#4255](https://github.com/opensearch-project/ml-commons/pull/4255) | Fix wrong field name in get working memory API |
| [#4283](https://github.com/opensearch-project/ml-commons/pull/4283) | Fix llm result path; convert message to user prompt string |
| [#4292](https://github.com/opensearch-project/ml-commons/pull/4292) | Fix llm result path error |
| [#4300](https://github.com/opensearch-project/ml-commons/pull/4300) | Verify llm before summarize session |
| [#4247](https://github.com/opensearch-project/ml-commons/pull/4247) | Update approver matching to be exact match |
| [#4259](https://github.com/opensearch-project/ml-commons/pull/4259) | Fix approver parsing bug in require-approval workflow |
| [#4174](https://github.com/opensearch-project/ml-commons/pull/4174) | Fix Cohere IT |

## References

- [Issue #4135](https://github.com/opensearch-project/ml-commons/issues/4135): Agent parsing issue
- [Issue #4136](https://github.com/opensearch-project/ml-commons/issues/4136): Empty LLM content issue
- [Issue #4137](https://github.com/opensearch-project/ml-commons/issues/4137): Steps with commas issue
- [Issue #4186](https://github.com/opensearch-project/ml-commons/issues/4186): NPE with multi-tenancy off
- [Issue #4018](https://github.com/opensearch-project/ml-commons/issues/4018): Missing RAG response issue

## Related Feature Report

- [ML Commons Bug Fixes](../../../features/ml-commons/ml-commons-bug-fixes.md)
