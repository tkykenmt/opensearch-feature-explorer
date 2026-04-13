---
tags:
  - opensearch-dashboards
---
# AI Assistant / Chatbot

## Summary

OpenSearch Dashboards v3.6.0 delivers a major update to the AI Chat feature with 39 PRs spanning new capabilities, architectural improvements, and extensive bug fixes. Key additions include conversation history with agentic memory, dashboard screenshot capture for multimodal AI interactions, "Ask AI" for legacy visualizations, a time range tool for natural language time updates, "On Behalf Of" (OBO) bearer token integration for secure AG-UI authorization, and chat interaction metrics tracking. The architecture was refactored to a single window model with a dedicated `ChatMountService`, and numerous stability fixes address streaming, conversation restore, tool call handling, and error management.

## Details

### New Features

- **Conversation History List**: Added a pluggable `ConversationMemoryProvider` interface with a history list panel in the chatbot, enabling plugins to provide custom memory backends (#11348)
- **Agentic Memory Provider**: New `AgenticMemoryProvider` implementation that stores and retrieves conversation history using ML Commons Agent Memory APIs. Configuration is managed server-side, and conversation state is automatically persisted by the agent (#11380)
- **Dashboard Screenshot Capture**: New `usePageContainerCapture` hook leveraging `html2canvas-pro` to capture visual snapshots of dashboard pages and send them to the AI as base64-encoded images (#11287). Screenshots are scaled to stay under 8k pixel limit (#11585). The capture option is hidden on dashboard pages where it's not applicable (#11587)
- **"Ask AI" for Legacy Visualizations**: Extended the "Ask AI" action to legacy visualizations via `ask_ai_embeddable_action`, with the action hidden in Explore visualization until multimodal support is available (#11338, #11214)
- **Time Range Tool**: New frontend tool allowing users to update the dashboard time range using natural language within the chatbot (#11331)
- **Default Page Context**: The context provider plugin now provides default context (appId and path) for all pages, while still allowing per-page overrides (#11502)
- **Chat Interaction Metrics**: Added metrics tracking for chat interactions including success/failure counts and interaction duration (#11575)
- **Tool Call Parameter Display**: Tool call parameters are now displayed in the chat tool call row for better transparency (#11552)
- **Grouped Tool Calls**: Consecutive completed tool calls from assistant messages are grouped into a single visual unit, reducing UI clutter (#11332)
- **CSP Nonce Support**: Switched to `html2canvas-pro` to support Content Security Policy nonce for screenshot capture (#11329)

### Architecture & Security

- **Single Window Architecture**: Refactored chat to use a single window architecture with a dedicated `ChatMountService` that handles sidecar open/close/toggle operations and chrome visibility integration. `ChatHeaderButton` simplified to only render the toggle button (#11483)
- **OBO Bearer Token Integration**: Integrated "On Behalf Of" bearer token flow with AG-UI authorization, enabling secure identity propagation through the chain: OSD → Chat → Security Plugin OBO → Chat → Agent Server → MCP Tools → OpenSearch. Configured via `chat.forwardCredentials: true` (#11524)
- **AG-UI Error Handling**: Fixed ag-ui error function invocation — the library returns `() => Error` which must be invoked to get the actual error (#11569)

### UI/UX Improvements

- **Chat Header Update**: Updated chat header look and feel (#11330)
- **Input & Message Layout**: Improved chatbot input and message bubble layout for better density (#11327)
- **Enhanced Error Handling**: Improved error handling for chat ML client responses (#11543)
- **Input Focus During Streaming**: Chat input stays focused during response streaming (#11379)
- **Auto-load Conversation**: Latest conversation is automatically loaded and restored when the chat window opens (#11396)
- **Scrolling During Streaming**: Enabled scrolling while chat response is streaming (#11549)
- **Flat History List**: Removed grouped conversation sections from chat history panel for a simpler flat list (#11474)

### Bug Fixes

- **Dev Tools Modal Padding**: Fixed padding when sidecar is hidden (#11542)
- **Confirmation Bar Removal**: Removed confirmation bar and excluded customized tool output render from tool group (#11414)
- **AskAIEmbeddableAction Undefined**: Fixed undefined error for `AskAIEmbeddableAction` (#11508)
- **Race Condition Prevention**: Disabled chat input during tool result sending to prevent race conditions (#11510)
- **Conversation Restore Stuck**: Fixed chat window stuck on loading when restoring conversation with unfinished tool calls (#11576)
- **Auto-load History**: Auto-load conversation history when content doesn't fill container (#11517)
- **Multi-data-source Support**: Pass data source ID to agentic memory provider for multi-data-source support (#11529)
- **Failed Conversation Restore**: Fixed failed conversation restore after chat window unmount by resetting thread ID (#11526)
- **Thinking Message Disappearing**: Fixed loading ("Thinking...") message disappearing prematurely during chat streaming (#11459)
- **Thread Creation on Clear**: Fixed `sendMessageWithWindow` to properly create new thread when clearing conversation (#11507)
- **User Confirmation Input Lock**: Disabled chat input when tool call requires user confirmation (#11588)
- **Typing Re-renders**: Fixed chat input typing triggering unnecessary chat message re-renders (#11467)
- **Array Content Handling**: Handle assistant message content in array type to prevent chat rendering failures (#11473)
- **Minor UX Issues**: Fixed sidecar overlap, button overflow, and error messages (#11408)
- **Chat UX Improvements**: Stop button, scroll bar fix, and text area height increase (#11266)
- **Hide Delete Button**: Hidden conversation delete button when using agentic memory provider (#11418)

### New Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `chat.forwardCredentials` | Forward OBO bearer token to AG-UI agent server | `false` |
| `chat.agUiUrl` | URL for the AG-UI agent server runs endpoint | - |

## References

### Pull Requests
| PR | Description |
|----|-------------|
| [#11348](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11348) | Add conversation history list support in chatbot |
| [#11380](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11380) | Add agentic memory provider for ML Commons Agent Memory APIs |
| [#11338](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11338) | Add "Ask AI" action for legacy visualizations |
| [#11287](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11287) | Add screenshot capture support in chatbot for dashboard pages |
| [#11575](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11575) | Add metrics tracking for chat interactions |
| [#11332](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11332) | Group consecutive completed tool calls in chat interface |
| [#11418](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11418) | Hide conversation delete button when using agentic memory provider |
| [#11587](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11587) | Hide screenshot capture option on dashboard pages |
| [#11396](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11396) | Load and restore latest conversation automatically |
| [#11552](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11552) | Display tool call parameters in chat tool call row |
| [#11379](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11379) | Keep chat input focused during response streaming |
| [#11330](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11330) | Update chat header look and feel |
| [#11331](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11331) | Add time range tool to chatbot |
| [#11502](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11502) | Add default page context in context provider plugin |
| [#11329](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11329) | Use html2canvas-pro to support CSP nonce |
| [#11214](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11214) | Hide "Ask AI" in Explore visualization |
| [#11327](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11327) | Improve chatbot input and message bubble layout |
| [#11543](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11543) | Enhance error handling for chat ML client responses |
| [#11542](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11542) | Fix dev tools modal padding when sidecar is hidden |
| [#11414](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11414) | Remove confirmation bar and fix tool output render |
| [#11508](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11508) | Fix AskAIEmbeddableAction undefined error |
| [#11510](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11510) | Disable chat input during tool result sending |
| [#11576](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11576) | Fix chat window stuck on loading with unfinished tool calls |
| [#11517](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11517) | Auto-load conversation history when content doesn't fill container |
| [#11529](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11529) | Pass data source ID to agentic memory provider |
| [#11526](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11526) | Fix failed conversation restore by resetting thread ID |
| [#11459](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11459) | Fix "Thinking..." message disappearing prematurely |
| [#11585](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11585) | Scale screenshots to stay under 8k pixel limit |
| [#11507](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11507) | Fix sendMessageWithWindow thread creation on clear |
| [#11588](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11588) | Disable chat input when tool call requires confirmation |
| [#11474](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11474) | Remove grouped conversation sections for flat list |
| [#11467](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11467) | Fix chat input typing triggering re-renders |
| [#11473](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11473) | Handle assistant message content in array type |
| [#11408](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11408) | Fix minor chat UX issues |
| [#11549](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11549) | Enable scrolling while chat response is streaming |
| [#11524](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11524) | Integrate OBO bearer token with AG-UI authorization |
| [#11569](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11569) | Support ag-ui error function invocation |
| [#11266](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11266) | Chat UX improvements: stop button, scroll bar, text area |
| [#11483](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11483) | Refactor chat to single window architecture with mount service |
