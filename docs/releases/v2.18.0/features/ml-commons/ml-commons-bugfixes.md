# ML Commons Bugfixes

## Summary

OpenSearch v2.18.0 includes 11 bugfixes for the ML Commons plugin, addressing issues across RAG pipelines, ML inference processors, connector management, model deployment, and agent execution. These fixes improve stability and reliability for machine learning workloads.

## Details

### What's New in v2.18.0

This release focuses on stability improvements and bug fixes across multiple ML Commons components.

### Technical Changes

#### RAG Pipeline Fixes

Two critical fixes address null pointer exceptions (NPE) in RAG pipelines:

1. **Missing generative_qa_parameters handling** ([#3100](https://github.com/opensearch-project/ml-commons/pull/3100)): Gracefully handles errors when required `generative_qa_parameters` is not provided for a RAG pipeline, preventing crashes and providing meaningful error messages.

2. **Optional parameters NPE fix** ([#3057](https://github.com/opensearch-project/ml-commons/pull/3057)): Explicitly checks if parameters are null before serializing field names and values in the RAG processor.

#### ML Inference Processor Fix

**JsonPath return format consistency** ([#2985](https://github.com/opensearch-project/ml-commons/pull/2985)): Fixed inconsistent behavior where the ML inference ingest processor always returned lists when using JsonPath in `input_maps`. The fix standardizes the JsonPath configuration across ML inference search processors and ingest processors, returning the original format of the object instead of always wrapping in a list.

Before fix:
```json
{
  "input": ["red shoes"]  // Always returned as list
}
```

After fix:
```json
{
  "input": "red shoes"  // Returns original string format
}
```

#### Connector Time Fields

**Populate time fields for connectors** ([#2922](https://github.com/opensearch-project/ml-commons/pull/2922)): Fixed an issue where `created_time` and `last_updated_time` fields were always null for connectors. Now these fields are properly populated when creating and updating connectors via the API.

| Operation | created_time | last_updated_time |
|-----------|--------------|-------------------|
| Create connector | ✅ Set | ✅ Set |
| Update connector | ✅ Preserved | ✅ Updated |

#### Model Deployment Stability

1. **Model stuck in deploying state** ([#3137](https://github.com/opensearch-project/ml-commons/pull/3137)): Fixed an issue where models could get stuck in "deploying" state during node crashes or cluster restarts. The fix ensures proper state cleanup and recovery.

2. **Remote model auto-redeployment filter** ([#2976](https://github.com/opensearch-project/ml-commons/pull/2976)): Filters out remote model auto-redeployment in `MLModelAutoRedeployer` since remote models support auto-deployment on first prediction request.

#### Master Key Race Condition

**Increased wait timeout for master key** ([#3151](https://github.com/opensearch-project/ml-commons/pull/3151)): Fixed a race condition during master key initialization when encrypting/decrypting credentials in connectors. The encrypt/decrypt thread could previously get a null key even if the key was successfully fetched from the config index in another thread.

#### Bedrock Integration

**BWC for Bedrock Converse API** ([#3173](https://github.com/opensearch-project/ml-commons/pull/3173)): Handles backward compatibility for serialization and deserialization of newly added fields for the Bedrock Converse API.

#### Agent Logging

**Correct agent type in error logs** ([#2809](https://github.com/opensearch-project/ml-commons/pull/2809)): Fixed error logging in `MLAgentExecutor` to show the correct agent type instead of always showing "flow agent".

Before:
```
[ERROR] Failed to run flow agent
```

After:
```
[ERROR] Failed to run conversational agent
```

#### Documentation

**Bedrock multimodal documentation** ([#3073](https://github.com/opensearch-project/ml-commons/pull/3073)): Added usage examples for Bedrock multimodal built-in functions in documentation.

## Limitations

- Connectors created before v2.18.0 will not have `created_time` populated (remains null), but `last_updated_time` will be set on next update
- The JsonPath fix may require updates to existing pipelines that relied on the previous list-wrapping behavior

## Related PRs

| PR | Description |
|----|-------------|
| [#3100](https://github.com/opensearch-project/ml-commons/pull/3100) | Gracefully handle error when generative_qa_parameters is not provided |
| [#3057](https://github.com/opensearch-project/ml-commons/pull/3057) | Fix RAG processor NPE when optional parameters not provided |
| [#2985](https://github.com/opensearch-project/ml-commons/pull/2985) | Fix ML inference ingest processor JsonPath return format |
| [#2922](https://github.com/opensearch-project/ml-commons/pull/2922) | Populate time fields for connectors on return |
| [#3137](https://github.com/opensearch-project/ml-commons/pull/3137) | Fix model stuck in deploying state during node crash/cluster restart |
| [#2976](https://github.com/opensearch-project/ml-commons/pull/2976) | Filter out remote model auto-redeployment |
| [#3151](https://github.com/opensearch-project/ml-commons/pull/3151) | Increase wait timeout to fetch master key |
| [#3173](https://github.com/opensearch-project/ml-commons/pull/3173) | Handle BWC for Bedrock Converse API |
| [#2809](https://github.com/opensearch-project/ml-commons/pull/2809) | Fix error log to show correct agent type |
| [#3073](https://github.com/opensearch-project/ml-commons/pull/3073) | Add Bedrock multimodal built-in function usage example |
| [#369](https://github.com/opensearch-project/ml-commons/pull/369) | Fix category order and description in data administration |

## References

- [Issue #3092](https://github.com/opensearch-project/ml-commons/issues/3092): RAG pipeline error handling
- [Issue #2983](https://github.com/opensearch-project/ml-commons/issues/2983): RAG processor NPE
- [Issue #2974](https://github.com/opensearch-project/ml-commons/issues/2974): ML inference processor JsonPath issue
- [Issue #2890](https://github.com/opensearch-project/ml-commons/issues/2890): Connector time fields not implemented
- [Issue #2970](https://github.com/opensearch-project/ml-commons/issues/2970): Model stuck in deploying state
- [Issue #3126](https://github.com/opensearch-project/ml-commons/issues/3126): Bedrock Converse API BWC
- [Issue #3060](https://github.com/opensearch-project/ml-commons/issues/3060): Bedrock multimodal documentation

## Related Feature Report

- [Full feature documentation](../../../../features/ml-commons/ml-commons-bugfixes.md)
