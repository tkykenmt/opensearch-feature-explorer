---
tags:
  - domain/ml
  - component/dashboards
  - dashboards
  - observability
  - sql
---
# Dashboard Assistant (AI Chatbot)

## Summary

OpenSearch v3.1.0 brings significant UX improvements to the Dashboard Assistant (AI Chatbot), including enhanced text-to-visualization (t2viz) capabilities, improved streaming experience, persistent flyout state, and new admin UI settings for centralized feature control.

## Details

### What's New in v3.1.0

#### Text-to-Visualization Enhancements

1. **Single Metric Styling**: Improved visual presentation of single metric visualizations with descriptive text layers
2. **Time Range Support**: T2viz-generated visualizations now read time range from context, enabling time-aware charts
3. **Error Prevention**: Users are prevented from navigating to t2viz from Discover when PPL queries return no results or errors

#### UX Improvements

1. **Streaming Buffer for Special Characters**: Fixed hyperlink rendering during streaming by buffering special characters until complete
2. **Auto-scroll on Send**: User input messages now scroll to the top after sending for better conversation flow
3. **Persistent Flyout State**: Chatbot flyout visibility state is saved to local storage, keeping it open across page navigation

#### Admin Controls

1. **Centralized Feature Control**: New admin UI settings to control all Dashboard Assistant features:
   - `assistant.chatEnabled`: Controls the chatbot feature
   - `assistant.enabled`: Controls alert summary and anomaly detection features

#### Alert Summary

1. **Format Instructions**: Added format instructions for alert summaries to ensure consistent output formatting

### Technical Changes

#### New Configuration

| Setting | Description | Default |
|---------|-------------|--------|
| `assistant.chatEnabled` | Enable/disable chatbot via admin UI | `false` |
| `assistant.enabled` | Enable/disable alert summary and anomaly detection | `false` |

### Usage Example

```yaml
# opensearch_dashboards.yml
assistant.chat.enabled: true
assistant.next.enabled: true
```

Admin UI settings can be configured through OpenSearch Dashboards Management → Advanced Settings.

## Limitations

- T2viz requires PPL queries with valid results to generate visualizations
- Admin UI settings require OpenSearch Dashboards 3.1.0+ with corresponding backend support
- Streaming buffer may introduce slight delay for markdown content with special characters

## References

### Documentation
- [OpenSearch Assistant Documentation](https://docs.opensearch.org/3.1/dashboards/dashboards-assistant/index/)
- [Text to Visualization](https://docs.opensearch.org/3.1/dashboards/dashboards-assistant/text-to-visualization/)
- [dashboards-assistant Repository](https://github.com/opensearch-project/dashboards-assistant)

### Pull Requests
| PR | Description |
|----|-------------|
| [#539](https://github.com/opensearch-project/dashboards-assistant/pull/539) | Style single metric in text2vis |
| [#545](https://github.com/opensearch-project/dashboards-assistant/pull/545) | Improve chatbot UX by scrolling user input message to top after sending |
| [#546](https://github.com/opensearch-project/dashboards-assistant/pull/546) | Prevent user from navigating to t2viz from discover if PPL returns no results/error |
| [#549](https://github.com/opensearch-project/dashboards-assistant/pull/549) | Buffer for special characters when streaming |
| [#553](https://github.com/opensearch-project/dashboards-assistant/pull/553) | Save chatbot flyout visualize state to local storage |
| [#557](https://github.com/opensearch-project/dashboards-assistant/pull/557) | T2viz supports reading time range from context |
| [#568](https://github.com/opensearch-project/dashboards-assistant/pull/568) | Add format instruction for alert summary |
| [#578](https://github.com/opensearch-project/dashboards-assistant/pull/578) | Add admin UI setting option for control all dashboard assistant features |

## Related Feature Report

- [Full feature documentation](../../../../features/dashboards-assistant/dashboards-assistant-ai-assistant-chatbot.md)
