---
tags:
  - domain/ml
  - component/dashboards
  - dashboards
  - ml
  - search
---
# Dashboards Agent & Assistant

## Summary

OpenSearch v3.4.0 introduces significant enhancements to the Dashboards Flow Framework plugin for agent configuration and management. These changes improve the user experience for creating and managing AI agents by adding agent summary visualization, memory integration for conversational search, simplified agent configuration, automatic response filter configuration, and various UI fixes.

## Details

### What's New in v3.4.0

This release focuses on improving the agent configuration experience in OpenSearch Dashboards through the Flow Framework plugin. Key additions include:

1. **Agent Summary Visualization** - View agent execution steps and reasoning
2. **Memory Integration** - Support for conversational search with memory persistence
3. **Simplified Agent Configuration** - Cleaner UI with auto-inferred settings
4. **Automatic Response Filters** - Auto-configuration for supported model providers
5. **UI/UX Improvements** - Firefox compatibility fixes and cleaner tool configurations

### Technical Changes

#### Agent Summary Feature

A new "View agent summary" button displays agent execution steps in a modal dialog. This helps users understand how the agent processes queries and which tools are used.

```typescript
// Agent summary is extracted from search response
// Only appears when agentic_context search response processor is configured
{
  "ext": {
    "agent_steps_summary": "I have these tools available: [ListIndexTool, IndexMappingTool, query_planner_tool]...",
    "memory_id": "2GMahJkBlF3USoHtuIpW"
  }
}
```

#### Memory Integration for Conversational Search

Users can now inject `memory_id` into queries to maintain conversation context across searches:

- **Continue conversation** button - Injects `memory_id` from previous response
- **Remove conversation** button - Clears `memory_id` for fresh context
- Automatic clearing when switching to flow agents (which don't support memory)

#### Simplified Agent Configuration

| Change | Description |
|--------|-------------|
| Unified model field | Single "model" field replaces separate LLM configuration |
| Auto-inferred LLM interface | Automatically detects interface from connector URL and parameters |
| Hidden advanced settings | LLM interface moved under "Advanced settings" |
| Removed memory delete button | Memory is required, so delete option removed |

#### Automatic Response Filters

For flow agents, response filters are now automatically configured based on the model provider:

| Provider | Response Filter |
|----------|-----------------|
| OpenAI | Auto-configured |
| Bedrock Claude | Auto-configured |
| Unknown/Custom | Empty value (manual configuration required) |

### Usage Example

Creating an agent with memory support:

```json
{
  "query": {
    "agentic": {
      "query_text": "top-rated nike shoes",
      "memory_id": "2GMahJkBlF3USoHtuIpW"
    }
  }
}
```

Follow-up query using conversation context:

```json
{
  "query": {
    "agentic": {
      "query_text": "only black ones",
      "memory_id": "2GMahJkBlF3USoHtuIpW"
    }
  }
}
```

### Migration Notes

- Existing agent configurations continue to work without changes
- Users can now simplify configurations by removing explicit LLM interface settings if using supported models
- Flow agents automatically get response filters for OpenAI and Bedrock Claude models

## Limitations

- Memory integration only works with conversational agents, not flow agents
- Automatic LLM interface inference may not work for custom connectors
- Response filter auto-configuration limited to OpenAI and Bedrock Claude providers
- Firefox EuiSelect rendering issues require bundled builds (not reproducible in local development)

## References

### Documentation
- [OpenSearch Assistant for OpenSearch Dashboards](https://docs.opensearch.org/3.0/dashboards/dashboards-assistant/index/)
- [Flow Agents Documentation](https://docs.opensearch.org/latest/vector-search/ai-search/agentic-search/flow-agent/)
- [Agents and Tools](https://docs.opensearch.org/3.0/ml-commons-plugin/agents-tools/index/)

### Pull Requests
| PR | Description |
|----|-------------|
| [#626](https://github.com/opensearch-project/dashboards-assistant/pull/626) | Disable dashboards assistant chatbot if investigation feature flag enabled |
| [#801](https://github.com/opensearch-project/dashboards-flow-framework/pull/801) | Add agent summary |
| [#796](https://github.com/opensearch-project/dashboards-flow-framework/pull/796) | Clean up / hide complex fields on agent configuration |
| [#803](https://github.com/opensearch-project/dashboards-flow-framework/pull/803) | Clean up agent summary formatting |
| [#809](https://github.com/opensearch-project/dashboards-flow-framework/pull/809) | Integrate with memory |
| [#817](https://github.com/opensearch-project/dashboards-flow-framework/pull/817) | Automatically add response filters to flow agents when possible |
| [#820](https://github.com/opensearch-project/dashboards-flow-framework/pull/820) | Remove default empty tool field values; fix EuiSelect values in Firefox |

## Related Feature Report

- Full feature documentation
