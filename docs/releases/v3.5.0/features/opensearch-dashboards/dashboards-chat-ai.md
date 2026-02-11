---
tags:
  - opensearch-dashboards
---
# Dashboards Chat/AI

## Summary

OpenSearch Dashboards v3.5.0 brings significant enhancements to the AI Chat feature, including new UX capabilities (slash commands, thinking indicators, "Ask AI" context menu), improved PPL query tool execution, plugin action registration API, and multiple bug fixes for page context handling, error messages, and conversation timeline rendering.

## Details

### What's New in v3.5.0

#### New Features

- **Slash Command System** ([#11194](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11194)): Extensible command registry with autocomplete UI, ghost text hints, keyboard navigation, and user confirmation workflow for sensitive tool executions. Includes `ConfirmationService` using RxJS `BehaviorSubject` for reactive confirmation state, and automatic restoration of unfinished tool calls on page reload.

- **"Thinking..." Loading Message** ([#11157](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11157)): Displays a "Thinking..." indicator immediately after sending a message, replacing the previous blank wait. Uses temporary loading messages with `loading-` ID prefix that are removed when the first response arrives, on error, or on completion.

- **"Ask AI" Context Menu for Explore Visualizations** ([#11134](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11134)): Right-click action on visualizations in the Explore plugin that captures the visualization as an image using `html2canvas` and opens the chat window with the image and a default message. Adds multimodal support (text + binary image content) to chat messages.

- **Plugin Action Registration API** ([#11131](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11131)): Exposes `registerAction`/`unregisterAction` methods allowing plugins to register permanent chat actions at plugin start time, without requiring component rendering. Enables use cases like creating investigation actions that persist across navigation.

- **Enhanced PPL Query Tool** ([#11023](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11023)): The `execute_ppl_query` tool now passes query results back to the backend agent with configurable timeout and polling intervals. Returns structured feedback with success, error, or timeout status.

- **Gradient Chat Button** ([#11066](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11066)): Updated chat header button with gradient SVG icon (cyan-blue-purple sparkles), gradient background/border effects, and internationalization support via `FormattedMessage`.

- **Hide "Ask AI" in Explore Visualization** ([#11214](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11214)): Conditionally hides the "Ask AI" context menu action in certain Explore visualization contexts.

#### Bug Fixes

- **Stale Network Error Cleanup** ([#11025](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11025)): Removes trailing "network error" system messages from restored conversations after page refresh via `removeTrailingErrorMessages()`.

- **Page Context Replacement** ([#11027](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11027)): Standardized page context categories to `['page', 'static']` and added `extractDataSourceIdFromPageContext()` for correct data source ID resolution.

- **Suggested Actions Service** ([#11029](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11029)): Fixed `suggestedActionsService is undefined` error.

- **Page Context Cleanup on Navigation** ([#11036](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11036)): Fixed page context not being cleaned up when navigating to pages without page context.

- **mlClient Undefined** ([#11064](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11064)): Fixed `mlClient is not defined` error for chatbot.

- **ML Router Error Format** ([#11103](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11103)): Fixed ML router error response format.

- **PPL Execution Tool Status** ([#11112](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11112)): Fixed incorrect status reporting in PPL execution tool.

- **Tool Call Timeline Positioning** ([#11115](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11115)): Fixed tool call positioning in conversation timeline.

- **Auto Scroll** ([#10977](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10977)): Added auto-scroll when new lines are added to the chat.

## Limitations

- Slash command system requires AG-UI chatbot feature flag enabled
- "Ask AI" visualization capture depends on `html2canvas` which may not render all CSS accurately
- Confirmation workflow is currently limited to investigation-type tool executions

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#11023](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11023) | Enhance execute_ppl_query tool execution result | |
| [#11066](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11066) | Add gradient icon and styling to chat header button | |
| [#11131](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11131) | Expose action register method for permanent actions | |
| [#11134](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11134) | Add "Ask AI" Context Menu Action to explore visualizations | |
| [#11157](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11157) | Add thinking message in chat conversation | |
| [#11194](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11194) | Add slash command system with autocomplete and confirmations | |
| [#11214](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11214) | Hide "Ask AI" in explore visualization | |
| [#11025](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11025) | Remove stale network error messages after page refresh | |
| [#11027](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11027) | Fix page context replacement and dataSourceId extraction | |
| [#11029](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11029) | Fix suggested actions service undefined | |
| [#11036](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11036) | Fix page context cleanup on navigation | |
| [#11064](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11064) | Fix mlClient undefined for chatbot | |
| [#11103](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11103) | Fix ML router error response format | |
| [#11112](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11112) | Fix PPL execution tool incorrect status | |
| [#11115](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/11115) | Fix tool call positioning in conversation timeline | |
| [#10977](https://github.com/opensearch-project/OpenSearch-Dashboards/pull/10977) | Add auto scroll when new line is added | |
