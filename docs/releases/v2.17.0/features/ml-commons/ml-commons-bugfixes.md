# ML Commons Bugfixes

## Summary

OpenSearch 2.17.0 includes 13 bugfixes for the ML Commons plugin, addressing issues across model management, remote inference, agent execution, configuration APIs, and connector functionality. These fixes improve stability and reliability for machine learning workloads.

## Details

### What's New in v2.17.0

This release focuses on stability improvements across multiple ML Commons components:

- **Model Management**: Fixed race condition when deleting models rapidly
- **Remote Inference**: Improved input validation and parameter type handling for Cohere and other remote models
- **Agent Framework**: Enhanced error response formatting for better debugging
- **Configuration API**: Fixed breaking changes in config index fields for backward compatibility
- **Guardrails**: Set `local_regex` as the default guardrails type

### Technical Changes

#### Model Deletion Fix

Previously, deleting a model twice in quick succession would return a 500 error with `illegal_state_exception`. The fix ensures proper handling of concurrent delete requests, returning appropriate status codes instead of server errors.

**Before (v2.16.x)**:
```json
{
  "error": {
    "type": "illegal_state_exception",
    "reason": "Model is not all cleaned up, please try again. Model ID: ZVP1CJEBQj8N2F2ZqulZ"
  }
}
```

**After (v2.17.0)**: Returns 404 if model already deleted, or 200 if deletion succeeds.

#### Remote Inference Input Validation

Fixed an issue where the `RemoteInferenceInputDataset` parser converted all parameter values to strings, causing model interface validation failures. A new processing function converts parameters back to their original datatypes.

#### Cohere Model Interface Fix

Resolved intermittent validation failures when invoking Cohere models for the first time. The fix ensures consistent input validation across all invocations.

#### Agent Error Response Format

Agent execution errors are now returned in XContent (JSON) format for easier parsing and debugging. Falls back to plain text if JSON building fails.

**New error format**:
```json
{
  "error": {
    "type": "agent_execution_exception",
    "reason": "Agent execution failed: ..."
  }
}
```

#### Custom Prompt List Substitution

Fixed an issue in the ML inference search response processor where List values in custom prompts were not properly substituted. Users can now use `${parameters.context.toString()}` to convert lists to strings in prompts.

**Example configuration**:
```json
{
  "ml_inference": {
    "model_config": {
      "prompt": "Context: ${parameters.context.toString()}. Human: summarize the documents"
    }
  }
}
```

#### Configuration Index Backward Compatibility

Fixed breaking changes in config index fields to maintain backward compatibility. The get config API now outputs only the original field names.

#### Guardrails Default Type

When guardrails type is not specified, `local_regex` is now used as the default type, ensuring consistent behavior.

#### HTTP Dependency Fix

Fixed HTTP dependency issue in `CancelBatchJobTransportAction` that could cause runtime errors.

### Bug Categories

| Category | PRs | Description |
|----------|-----|-------------|
| Model Management | #2806 | Delete model race condition |
| Remote Inference | #2847, #2852 | Cohere validation, parameter type handling |
| Agent Framework | #2858 | JSON error responses |
| Search Processors | #2871 | List substitution in prompts |
| Configuration | #2882, #2892 | Config index backward compatibility |
| Guardrails | #2853 | Default type setting |
| Batch Jobs | #2898 | HTTP dependency fix |
| Connectors | #358 | Router response 500 fix |
| Code Quality | #2815, #2831, #356 | Spotless, test fixes, dependency bumps |

## Limitations

- The model deletion fix handles concurrent requests but does not prevent all race conditions in distributed environments
- Custom prompt `toString()` conversion may not preserve complex nested structures

## References

### Pull Requests
| PR | Description |
|----|-------------|
| [#2806](https://github.com/opensearch-project/ml-commons/pull/2806) | Fix delete local model twice quickly get 500 response issue |
| [#2847](https://github.com/opensearch-project/ml-commons/pull/2847) | Fix cohere model input interface cannot validate cohere input issue |
| [#2852](https://github.com/opensearch-project/ml-commons/pull/2852) | Add processed function for remote inference input dataset parameters |
| [#2853](https://github.com/opensearch-project/ml-commons/pull/2853) | Use local_regex as default type for guardrails |
| [#2858](https://github.com/opensearch-project/ml-commons/pull/2858) | Agent execution error in json format |
| [#2871](https://github.com/opensearch-project/ml-commons/pull/2871) | Fix custom prompt substitute with List issue in ml inference |
| [#2882](https://github.com/opensearch-project/ml-commons/pull/2882) | Fix breaking changes in config index fields |
| [#2892](https://github.com/opensearch-project/ml-commons/pull/2892) | Output only old fields in get config API |
| [#2898](https://github.com/opensearch-project/ml-commons/pull/2898) | Fix http dependency in CancelBatchJobTransportAction |
| [#358](https://github.com/opensearch-project/ml-commons/pull/358) | Fix connector router response 500 |
| [#2815](https://github.com/opensearch-project/ml-commons/pull/2815) | Applying spotless to common module |
| [#2831](https://github.com/opensearch-project/ml-commons/pull/2831) | Fix Cohere test |
| [#356](https://github.com/opensearch-project/ml-commons/pull/356) | Bump micromatch from 4.0.5 to 4.0.8 |

### Issues (Design / RFC)
- [Issue #2793](https://github.com/opensearch-project/ml-commons/issues/2793): Deleting a deleted model causes 500 error
- [Issue #2829](https://github.com/opensearch-project/ml-commons/issues/2829): Model interface validation issue
- [Issue #2839](https://github.com/opensearch-project/ml-commons/issues/2839): toString issue in parameters
- [Issue #2880](https://github.com/opensearch-project/ml-commons/issues/2880): List substitution in custom prompts

## Related Feature Report

- [Full ML Commons documentation](../../../features/ml-commons/ml-commons.md)
