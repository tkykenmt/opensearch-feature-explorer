---
tags:
  - ml-commons
---
# ML Commons Agents & Memory

## Summary

OpenSearch v3.6.0 delivers major enhancements to the ML Commons Agent Framework and Agentic Memory system. The headline feature is the V2 Chat Agent (`conversational_v2`), which introduces a unified interface with single-step registration, multi-modal support, and standardized Strands-style I/O. Alongside this, new semantic and hybrid search APIs simplify long-term memory retrieval, token usage tracking enables cost monitoring across all agent types, and the post-memory hook now supports structured messages for context management. Multiple bug fixes improve error handling, context restoration, and AG-UI compatibility.

## Details

### What's New in v3.6.0

#### V2 Chat Agent (conversational_v2)

A new `conversational_v2` agent type that simplifies agent registration from a 4-step process (create connector → register model → deploy model → create agent) to a single API call with auto-generated connectors and models.

Key capabilities:
- Three input types: TEXT (simple string), CONTENT_BLOCKS (multi-modal array with images/videos/documents), and MESSAGES (full conversation array)
- Requires `agentic_memory` (not `conversation_index`) — preserves multi-modal content in `structured_data_blob`
- Standardized output format with `stop_reason`, `message`, `memory_id`, and `metrics`
- New `AbstractV2AgentRunner` base class for code reuse across future V2 agent types
- Supports Bedrock, OpenAI, and Gemini providers via abstraction
- Full backward compatibility — zero changes to existing V1 agents

#### Semantic and Hybrid Search APIs for Long-Term Memory

Two new REST endpoints that abstract away the complexity of searching long-term memories:

- `POST /_plugins/_ml/memory_containers/{id}/memories/long-term/_semantic_search` — constructs neural/neural_sparse queries automatically from plain text
- `POST /_plugins/_ml/memory_containers/{id}/memories/long-term/_hybrid_search` — combines BM25 keyword + neural vector search with configurable weights (`bm25_weight`, `neural_weight`)

Both support namespace filtering, tag filtering, `min_score` threshold, and generic OpenSearch query DSL filters. Hybrid search pipeline is auto-created at memory container creation time.

#### Token Usage Tracking

New `AgentTokenTracker` provides per-execution token usage tracking across Conversational, AG-UI, and Plan-Execute-Reflect agents. Tracks input, output, cache read/write, and reasoning tokens per turn and per model. Enabled via `include_token_usage` flag in agent execute requests. Supports provider-specific extraction for Bedrock Converse, OpenAI, and Gemini.

#### Post-Memory Hook with Structured Messages

The POST_MEMORY hook now supports structured messages (`List<Message>`) used by unified interface agents. Context managers (SlidingWindowManager, SummarizationManager) can compress structured chat history before LLM prompt formatting. Includes safe-cut-point logic that avoids splitting tool-call/tool-result pairs.

### Enhancements

- Context management overwrite at execute time: agents registered with inline context management can override with a different `context_management_name` parameter during execution
- AG-UI context restoration for legacy interface agents
- Improved agent workflow logging for debugging and metric collection
- Tool name and description escaping to handle quotation marks in frontend tool definitions (e.g., Dashboards `update_time_range` tool)

### Bug Fixes

- Fixed `agent_id` parameter conflict causing infinite loop in AgentTool — renamed to `agent_id_log` for logging
- Fixed MCP connector setting not being respected for Agent V2 — moved V2 execution post MCP setting check
- Fixed incorrect error codes (500 → 404) when deleting memory containers and context management templates
- Fixed context restoration bug where user information was missing
- Fixed unsupported operation exception when putting agent ID into immutable map in `MLAgentExecutor`
- Fixed `RestChatAgentIT` teardown failure when AWS credentials are absent
- Fixed LLM customized prompt template in Dashboards

## Limitations

- V2 agents do not yet support streaming
- V2 agents do not yet support hooks and context management
- V1 agents registered with unified interface format only support text input
- V2 agents can only be registered with `agentic_memory`
- Hybrid search weight tuning at the container level (normalization technique, combination technique) is planned for a follow-up

## References

### Pull Requests
| PR | Description | Category |
|----|-------------|----------|
| `https://github.com/opensearch-project/ml-commons/pull/4732` | Introduce V2 Chat Agent with unified interface, multi-modal support, and simplified registration | feature |
| `https://github.com/opensearch-project/ml-commons/pull/4658` | Add semantic and hybrid search APIs for long-term memory retrieval | feature |
| `https://github.com/opensearch-project/ml-commons/pull/4683` | Add token usage tracking for Conversational, AG_UI, and PER agents | feature |
| `https://github.com/opensearch-project/ml-commons/pull/4645` | Support messages array in all memory types and chat history in AGUI agent | feature |
| `https://github.com/opensearch-project/ml-commons/pull/4687` | Add post-memory hook with structured message support for context managers | feature |
| `https://github.com/opensearch-project/ml-commons/pull/4681` | Add detailed logging to Agent Workflow | enhancement |
| `https://github.com/opensearch-project/ml-commons/pull/4637` | Allow overwrite during execute for inline context management | enhancement |
| `https://github.com/opensearch-project/ml-commons/pull/4720` | Restore AGUI context for legacy interface agent | enhancement |
| `https://github.com/opensearch-project/ml-commons/pull/4747` | Escape tool name and description to handle quotation marks | enhancement |
| `https://github.com/opensearch-project/ml-commons/pull/4762` | Fix agent_id parameter conflict by renaming to agent_id_log | bugfix |
| `https://github.com/opensearch-project/ml-commons/pull/4739` | Fix MCP connector setting not being respected for Agent V2 | bugfix |
| `https://github.com/opensearch-project/ml-commons/pull/4723` | Fix incorrect error codes when deleting memory containers | bugfix |
| `https://github.com/opensearch-project/ml-commons/pull/4701` | Fix error code for delete context management template API (404 instead of 500) | bugfix |
| `https://github.com/opensearch-project/ml-commons/pull/4730` | Fix context restoration bug where user information was missing | bugfix |
| `https://github.com/opensearch-project/ml-commons/pull/4733` | Fix unsupported operation when putting agent ID into immutable map | bugfix |
| `https://github.com/opensearch-project/ml-commons/pull/4772` | Fix RestChatAgentIT teardown failure when AWS credentials are absent | bugfix |
| `https://github.com/opensearch-project/dashboards/pull/811` | Fix LLM customized prompt template | bugfix |

### Related Issues
- `https://github.com/opensearch-project/ml-commons/issues/4552` — RFC: Unified Agent Interface with Multi-Modal Support
- `https://github.com/opensearch-project/ml-commons/issues/4647` — Semantic and hybrid search for long-term memory
- `https://github.com/opensearch-project/ml-commons/issues/4662` — Token usage tracking
- `https://github.com/opensearch-project/ml-commons/issues/4583` — Post-memory hook for structured messages
- `https://github.com/opensearch-project/ml-commons/issues/4688` — AGUI context for legacy interface agent
- `https://github.com/opensearch-project/ml-commons/issues/4706` — Wrong error code when deleting memory container
