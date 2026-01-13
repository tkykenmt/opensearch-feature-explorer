---
tags:
  - dashboards-assistant
---
# AI Assistant UI

## Summary

OpenSearch v2.19.0 introduces significant UI improvements to the AI Assistant (Chatbot) in OpenSearch Dashboards. Key changes include a responsive chatbot entry button redesign, new feature flags for controlling UI elements, improved in-context summarization UI for alerts, and enhanced dropdown list functionality.

## Details

### What's New in v2.19.0

#### Chatbot Entry UI Redesign
The chatbot entry point has been redesigned for better responsiveness:
- Button displays as icon-only when screen width is less than 1200px
- Full button with text shown on wider screens
- Improved integration with application header

#### Feature Flags for UI Control
New configuration flags allow administrators to control visibility of UI elements:
- `assistant.chat.trace.enabled` - Controls trace view button visibility in message bubbles
- `assistant.chat.feedback.enabled` - Controls feedback button visibility in message bubbles
- `assistant.chat.stopGeneration.enabled` - Controls stop generation button visibility
- `assistant.chat.regenerate.enabled` - Controls regenerate button visibility
- `assistant.chat.deleteConversation.enabled` - Controls delete conversation API availability
- `assistant.chat.renameConversation.enabled` - Controls rename conversation API availability

#### In-context Summarization UI Update
The alert summarization UI has been improved:
- Removed blue dashed underline from alert links
- Added icon next to alerts
- Hover effect now shows gradient instead of previous styling

#### Dropdown List Improvements
- Updated button label for clarity
- Removed popover title for cleaner appearance
- Added query assistant summary switch to dropdown list

#### Logo Configuration
New capability to configure custom logo for the assistant through configuration settings.

#### Pipeline Architecture for Multi-Agent Execution
Introduced a `Pipeline` architecture for executing asynchronous operations:
- Each operator encapsulates a specific function
- Pipeline orchestrates operators, processing input sequentially
- Allows adding, reusing, or rearranging steps with minimal code changes
- Replaced monolithic Text2Vega class with Pipeline

#### Error Handling Improvements
- Returns HTTP 404 instead of 500 for missing agent config name
- Extracted error handling logic to reusable function
- For 5xx errors, returns original error code instead of generic 500

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `assistant.chat.trace.enabled` | Show trace view button | `true` |
| `assistant.chat.feedback.enabled` | Show feedback buttons | `true` |
| `assistant.chat.stopGeneration.enabled` | Show stop generation button | `true` |
| `assistant.chat.regenerate.enabled` | Show regenerate button | `true` |
| `assistant.chat.deleteConversation.enabled` | Enable delete conversation API | `true` |
| `assistant.chat.renameConversation.enabled` | Enable rename conversation API | `true` |

## Limitations

- Feature flags require plugin restart to take effect
- Logo configuration requires proper asset path setup

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
| [#396](https://github.com/opensearch-project/dashboards-assistant/pull/396) | Chatbot entry UI redesign | - |
| [#379](https://github.com/opensearch-project/dashboards-assistant/pull/379) | Add feature flags for traces and feedback | - |
| [#394](https://github.com/opensearch-project/dashboards-assistant/pull/394) | Hide stop/regenerate buttons via feature flag | - |
| [#392](https://github.com/opensearch-project/dashboards-assistant/pull/392) | Update UI for in-context summarization in Alerts table | - |
| [#407](https://github.com/opensearch-project/dashboards-assistant/pull/407) | Update dropdown list button label | - |
| [#395](https://github.com/opensearch-project/dashboards-assistant/pull/395) | Add query assistant summary to dropdown list | - |
| [#401](https://github.com/opensearch-project/dashboards-assistant/pull/401) | Set logo config in assistant | - |
| [#409](https://github.com/opensearch-project/dashboards-assistant/pull/409) | Feature flag for delete conversation API | - |
| [#410](https://github.com/opensearch-project/dashboards-assistant/pull/410) | Feature flag for rename conversation API | - |
| [#376](https://github.com/opensearch-project/dashboards-assistant/pull/376) | Refactor multi agents execution with Pipeline | - |
| [#384](https://github.com/opensearch-project/dashboards-assistant/pull/384) | Return 404 instead of 500 for missing agent config | - |
| [#368](https://github.com/opensearch-project/dashboards-assistant/pull/368) | Visual editor alerts navigation to discover | - |

### Documentation
- [OpenSearch Assistant Documentation](https://docs.opensearch.org/2.19/dashboards/dashboards-assistant/index/)
- [Build Your Own Chatbot Tutorial](https://docs.opensearch.org/2.19/tutorials/gen-ai/chatbots/build-chatbot/)
