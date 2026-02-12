---
tags:
  - ml-commons
---
# ML Commons Agent & Connector

## Summary

Updates to the ML Commons agent and connector framework in v3.3.2 include MCP connector support in the agent update API and several bug fixes for tool execution, response streaming, conversation history, and JSON chunk handling.

## Details

### What's New in v3.3.2

#### MCP Connector in Agent Update API (ml-commons#4352)
The agent update API now supports updating MCP (Model Context Protocol) connectors. Users can update connector filters, remove connectors, or add new connectors to existing agents via the `PUT /_plugins/_ml/agents/{agent_id}` endpoint using the `mcp_connectors` parameter.

#### Bug Fixes

- **Execute Tool API Fix** (ml-commons#4325): Fixed `UnsupportedOperationException` when executing `ReadFromScratchPadTool` or `WriteToScratchPadTool` with empty parameters. The issue was caused by immutable map implementations being passed to tools that need to modify parameters. The fix creates a mutable copy of parameters before passing them to tools.

- **Filtered Output in Streaming** (ml-commons#4335): Fixed agent tool response streaming to use filtered output, ensuring consistent response formatting.

- **Return History Fix** (ml-commons#4310): Fixed an issue when `return_history` is set to `true` in agent execution.

- **JSON Chunk Combining** (ml-commons#4317): Fixed combining of JSON chunks from requests to handle fragmented payloads correctly.

## References

| PR | Description |
|----|-------------|
| [#4352](https://github.com/opensearch-project/ml-commons/pull/4352) | Support MCP connector in agent update API |
| [#4325](https://github.com/opensearch-project/ml-commons/pull/4325) | Fix unsupported operation exception in execute tool API |
| [#4335](https://github.com/opensearch-project/ml-commons/pull/4335) | Use filtered output in agent tool response streaming |
| [#4310](https://github.com/opensearch-project/ml-commons/pull/4310) | Fix when return_history is true |
| [#4317](https://github.com/opensearch-project/ml-commons/pull/4317) | Combine json chunks from requests |
| [#4321](https://github.com/opensearch-project/ml-commons/issues/4321) | Related issue: MCP connector in agent update |
