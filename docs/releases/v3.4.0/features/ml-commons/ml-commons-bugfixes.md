# ML Commons Bugfixes

## Summary

OpenSearch v3.4.0 includes 7 bug fixes for the ML Commons plugin, focusing on agent framework stability, agentic memory improvements, tool configuration handling, and security-related logging fixes. These fixes improve reliability for conversational agents, agentic search, and remote model integrations.

## Details

### What's New in v3.4.0

This release addresses critical bugs in the agent framework and agentic memory features:

1. **Agent Type Update Validation** - Properly reject attempts to change agent type during updates
2. **QueryPlanningTool Model ID Parsing** - Fix model ID propagation for agentic search
3. **Tool Config Empty Values** - Handle empty name/description in tool configurations
4. **Agentic Memory Multi-node Support** - Fix index creation in multi-node clusters
5. **Memory Search NPE Fix** - Handle null user during memory container search
6. **Error Message Escaping** - Properly escape special characters in agent error messages
7. **Sensitive Log Removal** - Remove request body from error logs during connector invocation

### Technical Changes

#### Agent Framework Fixes

| Fix | Description | Impact |
|-----|-------------|--------|
| Agent Type Update | Agent type is now immutable; update attempts return 400 error | Prevents silent failures when changing agent type |
| Model ID Parsing | QueryPlanningTool uses agent's LLM model_id as fallback | Fixes "Model ID can't be null" errors after agent updates |
| Error Message Escaping | `StringUtils.processTextDoc()` escapes exception messages | Prevents JSON parsing errors from special characters |

#### Agentic Memory Fixes

| Fix | Description | Impact |
|-----|-------------|--------|
| Default Index Settings | Added default settings for memory indices | Fixes index creation exceptions in multi-node clusters |
| Context Stashing | Fixed context stashing for non-system indices | Proper thread context handling |
| Null User Handling | Skip backend-role filtering when user is null | Prevents NPE during memory search |

#### Tool Configuration Fixes

| Fix | Description | Impact |
|-----|-------------|--------|
| Empty Values Handling | Omit empty name/description/parameters from serialization | Fixes Bedrock Claude validation errors |

#### Security Improvements

| Fix | Description | Impact |
|-----|-------------|--------|
| Sensitive Log Removal | Remove request body from connector error logs | Prevents credential exposure in logs |

### Usage Example

Agent type is now immutable - attempting to change it returns an error:

```json
// Create flow agent
POST /_plugins/_ml/agents/_register
{
  "name": "test",
  "type": "flow"
}

// Attempt to update to conversational - now returns 400 error
PUT /_plugins/_ml/agents/<agent-id>
{
  "name": "test",
  "type": "conversational"
}

// Response
{
  "error": {
    "type": "illegal_argument_exception",
    "reason": "Agent type cannot be updated"
  },
  "status": 400
}
```

QueryPlanningTool now automatically uses the agent's LLM model_id:

```json
// Agent with QueryPlanningTool - no explicit model_id needed
POST /_plugins/_ml/agents/_register
{
  "name": "agentic-search-agent",
  "type": "conversational",
  "tools": [
    {
      "type": "QueryPlanningTool"
    }
  ],
  "llm": {
    "model_id": "my-model-id"
  }
}
```

### Migration Notes

- **Agent Type Changes**: If you need to change an agent's type, delete and recreate the agent
- **Tool Configs**: Empty `description` or `parameters` fields are now automatically omitted from serialization - no action required
- **Error Handling**: Applications parsing agent error responses should continue to work as JSON structure is preserved

## Limitations

- Agent type remains immutable once created
- Empty tool config fields are silently omitted rather than validated at registration time

## References

### Documentation
- [ML Commons Agents and Tools Documentation](https://docs.opensearch.org/3.0/ml-commons-plugin/agents-tools/index/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#4341](https://github.com/opensearch-project/ml-commons/pull/4341) | Fix agent type update - make type immutable |
| [#4458](https://github.com/opensearch-project/ml-commons/pull/4458) | Fix model ID parsing for QueryPlanningTool in agentic search |
| [#4479](https://github.com/opensearch-project/ml-commons/pull/4479) | Handle edge case of empty values in tool configs |
| [#4476](https://github.com/opensearch-project/ml-commons/pull/4476) | Fix several bugs on agentic memory (multi-node, context, NPE) |
| [#4410](https://github.com/opensearch-project/ml-commons/pull/4410) | Fix tool error message escaping in MLChatAgentRunner |
| [#4450](https://github.com/opensearch-project/ml-commons/pull/4450) | Remove sensitive error log on request body |
| [#4472](https://github.com/opensearch-project/ml-commons/pull/4472) | Fix OpenAI RAG integration tests (test-only) |

### Issues (Design / RFC)
- [Issue #4340](https://github.com/opensearch-project/ml-commons/issues/4340): Update agent API silently fails when changing agent type
- [Issue #4424](https://github.com/opensearch-project/ml-commons/issues/4424): Updating conversational agents causes agentic search to fail
- [Issue #4477](https://github.com/opensearch-project/ml-commons/issues/4477): Conversational agent execution fails with remote Claude models for certain tool configs

## Related Feature Report

- [Full feature documentation](../../../../features/ml-commons/ml-commons-bugfixes.md)
