---
tags:
  - ml-commons
---

# AG-UI (Agent-User Interaction) Protocol

## Summary

AG-UI (Agent-User Interaction) is an open, event-based protocol that standardizes how AI agents connect to user-facing frontend applications. OpenSearch ml-commons implements AG-UI protocol support in its Agent Framework, enabling real-time streaming communication between conversational AI frontends and OpenSearch agents. This allows any AG-UI compatible frontend — including OpenSearch Dashboards — to interact with OpenSearch agents through standardized streaming events and hybrid tool execution.

AG-UI is positioned as a complementary protocol in the agentic ecosystem:
- **MCP (Model Context Protocol)**: Gives agents backend tools
- **A2A (Agent-to-Agent Protocol)**: Allows agents to communicate with other agents
- **AG-UI**: Brings agents into user-facing applications with frontend interaction tools

## Details

### Agent Type and Registration

AG-UI agents are registered with `"type": "AG_UI"` and use the `MLAGUIAgentRunner` class. This runner acts as a preprocessing layer that transforms AG-UI protocol requests into ml-commons compatible format, then delegates to `MLChatAgentRunner` for actual ReAct loop execution.

Key registration parameters:
- `type`: `"AG_UI"`
- `llm.model_id`: Reference to a deployed remote model (e.g., Bedrock Claude)
- `parameters._llm_interface`: LLM provider interface (e.g., `bedrock/converse/claude`)
- `tools[]`: Backend tools available to the agent
- `memory.type`: `"conversation_index"` for conversation persistence

### AG-UI Protocol Request Format

The AG-UI execute stream endpoint accepts:

| Field | Type | Description |
|-------|------|-------------|
| `threadId` | string | Conversation thread identifier |
| `runId` | string | Execution run identifier |
| `messages` | array | Conversation messages with roles: `user`, `assistant`, `tool` |
| `tools` | array | Frontend tool definitions with name, description, and JSON Schema parameters |
| `context` | array | Application context items (e.g., current page state, time range) |
| `state` | object | Shared state between agent and UI |
| `forwardedProps` | object | Additional forwarded properties |

### AG-UI Event Types

Responses are streamed as Server-Sent Events (SSE):

| Event Type | Description |
|------------|-------------|
| `RUN_STARTED` | Agent execution begins; includes threadId and runId |
| `TEXT_MESSAGE_START` | Start of assistant text response |
| `TEXT_MESSAGE_CONTENT` | Incremental text content delta |
| `TEXT_MESSAGE_END` | End of text response |
| `TOOL_CALL_START` | Agent requests tool execution; includes toolCallId and toolCallName |
| `TOOL_CALL_ARGS` | Tool call arguments as JSON delta |
| `TOOL_CALL_END` | Tool call definition complete |
| `TOOL_CALL_RESULT` | Backend tool execution result |
| `RUN_FINISHED` | Agent execution complete |
| `RUN_ERROR` | Error during execution |
| `MESSAGES_SNAPSHOT` | Reserved for memory integration |

### Hybrid Tool Execution

The AG-UI implementation supports a hybrid tool model within the ReAct loop:

1. **Backend tools** (e.g., `ListIndexTool`, `SearchIndexTool`, MCP tools): Execute server-side within the ReAct loop. Results feed back into the next LLM iteration.
2. **Frontend tools** (defined in request `tools[]`): When the LLM selects a frontend tool, the ReAct loop pauses and returns `TOOL_CALL_*` events to the client. The frontend executes the tool (e.g., updating a query bar, changing time range) and sends results back in a follow-up request with `tool` role messages.

The LLM sees all tools (backend + frontend) in a unified view, enabling seamless multi-tool reasoning across server and client boundaries.

### Frontend Integration

AG-UI compatible frontends can connect using the AG-UI client SDK:

```javascript
import { HttpAgent } from '@ag-ui/client';

const agent = new HttpAgent({
  url: 'https://your-opensearch-cluster/_plugins/_ml/agents/{agent_id}/_execute/stream'
});
```

OpenSearch Dashboards integrates AG-UI through its chat plugin, context provider framework, and page tools architecture, enabling context-aware chatbot experiences within the Explore application and other pages.

### Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `plugins.ml_commons.ag_ui_enabled` | `false` | Enable AG-UI agent feature |
| `plugins.ml_commons.stream_enabled` | `false` | Enable streaming responses |

### Supported LLM Providers

| Provider | `_llm_interface` Value |
|----------|----------------------|
| Amazon Bedrock (Claude) | `bedrock/converse/claude` |
| OpenAI-compatible APIs | `openai` (via HttpStreamingHandler) |

## Limitations

- AG-UI agent requires explicit feature flag enablement (`plugins.ml_commons.ag_ui_enabled`)
- Streaming with the unified agent interface is only supported for AG-UI agents; conversational agents registered via the new interface do not yet support `/_execute/stream`
- Multi-modal content (images) in streaming is supported but multi-modal content storage in `conversation_index` memory is limited
- The `MESSAGES_SNAPSHOT` event type is reserved but not yet fully integrated with memory

## Change History

### v3.5.0
- Initial AG-UI protocol support in Agent Framework (PR #4549, PR #4347)
- New `AG_UI` agent type with `MLAGUIAgentRunner`
- SSE streaming with 11 AG-UI event types
- Hybrid backend/frontend tool execution model
- `AGUIInputConverter` for protocol format detection and conversion
- Support for Bedrock Converse and OpenAI-compatible streaming handlers
- Feature flag `plugins.ml_commons.ag_ui_enabled`
- Tool message support in agent revamp for both Bedrock and OpenAI providers (PR #4596)
- Image support in streaming responses

## References

- PR: https://github.com/opensearch-project/ml-commons/pull/4549
- PR: https://github.com/opensearch-project/ml-commons/pull/4347
- PR: https://github.com/opensearch-project/ml-commons/pull/4596
- RFC: https://github.com/opensearch-project/ml-commons/issues/4409
- Issue: https://github.com/opensearch-project/ml-commons/issues/4211
- Issue: https://github.com/opensearch-project/ml-commons/issues/4548
- Issue: https://github.com/opensearch-project/ml-commons/issues/4604
- RFC: https://github.com/opensearch-project/ml-commons/issues/4552
- OSD RFC (AI Assistant Framework): https://github.com/opensearch-project/OpenSearch-Dashboards/issues/10585
- OSD RFC (Context & Page Tools): https://github.com/opensearch-project/OpenSearch-Dashboards/issues/10571
- OSD RFC (AI Toolkit): https://github.com/opensearch-project/OpenSearch-Dashboards/issues/10561
- AG-UI Protocol: https://github.com/ag-ui-protocol/ag-ui
- Docs Issue: https://github.com/opensearch-project/documentation-website/issues/11799
