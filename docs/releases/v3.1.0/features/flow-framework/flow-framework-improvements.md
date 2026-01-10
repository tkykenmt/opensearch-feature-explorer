# Flow Framework Improvements

## Summary

This release includes three bug fixes for the Flow Framework plugin that improve the RegisterAgentStep functionality and error handling in workflow provisioning. The fixes address issues with LLM field processing, exception type reporting in workflow state errors, and LLM spec parameter passing.

## Details

### What's New in v3.1.0

Three bug fixes improve the reliability and usability of Flow Framework:

1. **LLM Field Processing Fix**: Corrected how the `llm` field is parsed in RegisterAgentStep when a model ID is provided
2. **Exception Type in Error Messages**: WorkflowState error field now consistently includes the exception type even when there's no cause
3. **LLM Spec Parameters Fix**: LLM spec parameters are now properly passed to the LLMSpec builder in RegisterAgentStep

### Technical Changes

#### RegisterAgentStep LLM Field Processing (PR #1151)

The RegisterAgentStep now correctly handles the `llm` field as a nested JSON object instead of flat parameters:

**Before (broken):**
```json
{
  "llm.model_id": "xyz",
  "llm.parameters": {
    "max_iteration": "5"
  }
}
```

**After (fixed):**
```json
{
  "llm": {
    "model_id": "xyz",
    "parameters": {
      "max_iteration": "5",
      "stop_when_no_tool_found": "true"
    }
  }
}
```

Key changes in `RegisterAgentStep.java`:
- Added `LLM` constant to `CommonValue.java` for the llm field
- Updated `WorkflowNode.java` to include `llm` in `MAP_FIELDS` set for proper parsing
- Refactored LLM field processing to parse as a JSON map using `XContentHelper.convertToMap()`
- Added validation for LLM parameters map (must be string-to-string)

#### Exception Type in WorkflowState Error (PR #1154)

Fixed inconsistent error message formatting in `ProvisionWorkflowTransportAction.java`:

**Before:**
- With cause: `"RuntimeException during step step_1, restStatus: INTERNAL_SERVER_ERROR"`
- Without cause: `"Error message during step step_1, restStatus: BAD_REQUEST"` (missing exception type)

**After:**
- Both cases now include exception type: `"WorkflowStepException during step step_1, Simulated failure, restStatus: BAD_REQUEST"`

The fix ensures the exception class name is always prepended to the error message for consistent debugging.

#### LLM Spec Parameters Passing (PR #1155)

Fixed a bug where LLM spec parameters were validated but not actually passed to the LLMSpec builder:

```java
// Before: Parameters validated but not used
if (llmParams != null) {
    validateLLMParametersMap(llmParams);
}

// After: Parameters validated AND added to builder
if (llmParams != null) {
    validateLLMParametersMap(llmParams);
    llmParameters.putAll((Map<String, String>) llmParams);
}
```

### Usage Example

```json
{
  "name": "my-agent",
  "type": "flow",
  "llm": {
    "model_id": "<model_id>",
    "parameters": {
      "max_iteration": "5",
      "system_instruction": "You are a helpful assistant.",
      "prompt": "${parameters.question}"
    }
  },
  "tools": [...]
}
```

## Limitations

- LLM parameters must be a string-to-string map; non-string values will cause validation errors
- These fixes are also backported to v2.19.3

## Related PRs

| PR | Description |
|----|-------------|
| [#1151](https://github.com/opensearch-project/flow-framework/pull/1151) | Fixing llm field processing in RegisterAgentStep |
| [#1154](https://github.com/opensearch-project/flow-framework/pull/1154) | Include exception type in WorkflowState error field even if no cause |
| [#1155](https://github.com/opensearch-project/flow-framework/pull/1155) | Pass llm spec params to builder |

## References

- [Issue #1153](https://github.com/opensearch-project/flow-framework/issues/1153): Workflow state error messages don't include FFE/WSE types
- [Register Agent API](https://docs.opensearch.org/3.0/ml-commons-plugin/api/agent-apis/register-agent/): Official documentation for agent registration
- [Flow Agents](https://docs.opensearch.org/3.0/ml-commons-plugin/agents-tools/agents/flow/): Flow agent documentation
- [Workflow Steps](https://docs.opensearch.org/3.0/automating-configurations/workflow-steps/): Workflow step reference

## Related Feature Report

- [Full feature documentation](../../../features/flow-framework/flow-framework.md)
