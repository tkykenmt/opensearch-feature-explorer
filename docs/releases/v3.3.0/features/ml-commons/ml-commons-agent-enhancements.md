# ML Commons Agent Enhancements

## Summary

OpenSearch v3.3.0 introduces several enhancements to the ML Commons agent framework, including a new Get Agent API in the ML Client, agent metrics collection via OpenTelemetry, and improved error handling for agent execution failures. These changes improve observability, debugging capabilities, and developer experience when working with ML agents.

## Details

### What's New in v3.3.0

This release adds three key enhancements to the ML Commons agent framework:

1. **Get Agent API in ML Client** - Programmatic access to retrieve agent configurations
2. **Agent Metrics via OpenTelemetry** - Telemetry data collection for agent monitoring
3. **Failure Message Updates** - Improved error handling with interaction updates on failures

### Technical Changes

#### New Components

| Component | Description |
|-----------|-------------|
| `MachineLearningClient.getAgent()` | New method to retrieve agent by ID |
| `MLAgentGetRequest` | Request class for Get Agent API |
| `MLAgentGetResponse` | Response class containing agent details |
| `MLAgent.getTags()` | Method to generate telemetry tags for agents |
| `AdoptionMetric.AGENT_COUNT` | New metric for tracking agent counts |

#### Agent Metrics Collection

The agent metrics feature captures the following telemetry data via OpenTelemetry:

```
{
  _llm_interface: "bedrock/converse/claude",
  model_deployment: "remote",
  is_hidden: false,
  model_service_provider: "bedrock",
  model_type: "llm",
  memory_type: "conversation_index",
  model: "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
  type: "CONVERSATIONAL"
}
```

Tags captured include:
- `is_hidden` - Whether the agent is hidden
- `type` - Agent type (e.g., CONVERSATIONAL, FLOW)
- `memory_type` - Memory configuration type if configured
- `_llm_interface` - LLM interface parameter if specified
- Model information (model, provider, deployment type) from linked models

#### Failure Message Handling

When an agent execution fails, the interaction is now updated with the failure message:

**Before (v3.2.x):**
```json
{
    "memory_id": "Uw_ufZkBE5GN_tuwO2KT",
    "message_id": "Wg_yfZkBE5GN_tuwuGI9",
    "create_time": "2025-09-24T22:58:02.939633Z",
    "input": "give me index mapping of any index"
}
```

**After (v3.3.0):**
```json
{
    "memory_id": "Uw_ufZkBE5GN_tuwO2KT",
    "message_id": "Wg_yfZkBE5GN_tuwuGI9",
    "create_time": "2025-09-24T22:58:02.939633Z",
    "input": "give me index mapping of any index",
    "response": "Agent execution failed: failed to run"
}
```

### Usage Example

#### Get Agent API

```java
// Using the ML Client to get an agent
MachineLearningNodeClient mlClient = new MachineLearningNodeClient(client);

// Synchronous call
MLAgentGetResponse response = mlClient.getAgent("agent-id").actionGet();
MLAgent agent = response.getMlAgent();

// Asynchronous call
mlClient.getAgent("agent-id", ActionListener.wrap(
    response -> {
        MLAgent agent = response.getMlAgent();
        // Process agent
    },
    error -> {
        // Handle error
    }
));
```

#### REST API

```bash
GET /_plugins/_ml/agents/<agent_id>
```

### Migration Notes

- No breaking changes - all enhancements are additive
- Existing agent workflows continue to work without modification
- Agent metrics collection is automatic when the metrics framework is enabled

## Limitations

- Agent metrics are collected periodically via the stats job processor, not in real-time
- Model tags cache is cleared on each metrics collection run
- Batch size for agent metrics collection is limited to 10,000 agents

## References

### Documentation
- [Agent APIs Documentation](https://docs.opensearch.org/3.0/ml-commons-plugin/api/agent-apis/index/): Official agent API documentation
- [Get Agent API](https://docs.opensearch.org/3.0/ml-commons-plugin/api/agent-apis/get-agent/): Get agent endpoint documentation

### Pull Requests
| PR | Description |
|----|-------------|
| [#4180](https://github.com/opensearch-project/ml-commons/pull/4180) | Add Get Agent to ML Client |
| [#4221](https://github.com/opensearch-project/ml-commons/pull/4221) | Introduce agent metrics & Add is_hidden tag for model metrics |
| [#4198](https://github.com/opensearch-project/ml-commons/pull/4198) | Update interaction with failure message on agent execution failure |

### Issues (Design / RFC)
- [Issue #4197](https://github.com/opensearch-project/ml-commons/issues/4197): Feature request for failure message updates

## Related Feature Report

- [Full feature documentation](../../../features/ml-commons/ml-commons-agent-framework.md)
