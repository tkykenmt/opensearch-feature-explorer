# AI Assistant / Chatbot

## Summary

The OpenSearch AI Assistant (Chatbot) is an AI-powered conversational interface integrated into OpenSearch Dashboards. It enables users to interact with their data through natural language, generate visualizations from text descriptions, receive alert insights, and get data summaries without requiring specialized query skills. The assistant leverages ML Commons agents and tools to provide intelligent responses.

## Details

### Architecture

```mermaid
graph TB
    subgraph "OpenSearch Dashboards"
        Entry[Entry Point Button]
        ChatUI[Chat Interface]
        T2V[Text-to-Visualization]
        AlertInsight[Alert Insights]
        DataSummary[Data Summary]
    end
    
    subgraph "Backend"
        Router[Request Router]
        Stream[Streaming Handler]
        Memory[Conversation Memory]
    end
    
    subgraph "ML Commons"
        RootAgent[Root Chat Agent]
        Tools[Agent Tools]
        Models[ML Models]
    end
    
    Entry --> ChatUI
    ChatUI --> Router
    Router --> Stream
    Stream --> RootAgent
    RootAgent --> Tools
    Tools --> Models
    ChatUI --> Memory
    T2V --> RootAgent
    AlertInsight --> RootAgent
    DataSummary --> RootAgent
```

### Data Flow

```mermaid
flowchart TB
    User[User Input] --> UI[Chat UI]
    UI --> API[Backend API]
    API --> Agent[ML Agent]
    Agent --> LLM[LLM Model]
    LLM --> Stream[Streaming Response]
    Stream --> UI
    UI --> Display[Display Response]
```

### Components

| Component | Description |
|-----------|-------------|
| Chat Interface | Main conversational UI with message history and input |
| Entry Point Button | Single button in header for accessing the chatbot |
| Streaming Handler | Processes real-time response chunks for smooth UX |
| Conversation Memory | Stores and retrieves conversation history |
| Text-to-Visualization | Generates visualizations from natural language |
| Alert Insights | Provides AI-generated insights for alerts |
| Data Summary | Generates summaries of data patterns |
| Auto Aggregation | Suggests appropriate aggregations for visualizations |

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `assistant.chat.enabled` | Enable/disable the chatbot feature | `false` |
| `assistant.next.enabled` | Enable experimental features (text-to-viz) | `false` |

### Usage Example

1. Enable the assistant in `opensearch_dashboards.yml`:

```yaml
assistant.chat.enabled: true
assistant.next.enabled: true
```

2. Configure the root agent via API:

```json
PUT .plugins-ml-config/_doc/os_chat
{
    "type": "os_chat_root_agent",
    "configuration": {
        "agent_id": "your_root_agent_id"
    }
}
```

3. Access the chatbot via the button in the OpenSearch Dashboards header.

### Key Features

- **Natural Language Interaction**: Ask questions in plain English
- **Streaming Responses**: Real-time response display for better UX
- **Conversation History**: Resume previous conversations
- **Text-to-Visualization**: Generate charts from text descriptions
- **Alert Insights**: AI-powered alert analysis
- **Data Summaries**: Automatic data pattern summaries
- **Notebook Integration**: Save conversations to Notebooks

## Limitations

- Requires ML Commons plugin with configured agents and models
- Streaming output requires compatible backend support
- Text-to-visualization requires PPL queries with aggregations
- Response quality depends on the underlying LLM model

## Related PRs

| Version | PR | Description |
|---------|-----|-------------|
| v3.0.0 | [#398](https://github.com/opensearch-project/dashboards-assistant/pull/398) | Expose chatEnabled flag to capabilities |
| v3.0.0 | [#435](https://github.com/opensearch-project/dashboards-assistant/pull/435) | Update chatbot UI to align with new look |
| v3.0.0 | [#493](https://github.com/opensearch-project/dashboards-assistant/pull/493) | Support streaming output |
| v3.0.0 | [#505](https://github.com/opensearch-project/dashboards-assistant/pull/505) | Generate visualization on t2v page mount |
| v3.0.0 | [#514](https://github.com/opensearch-project/dashboards-assistant/pull/514) | Add auto aggregation suggest for t2v |
| v3.0.0 | [#540](https://github.com/opensearch-project/dashboards-assistant/pull/540) | Change chatbot entry point to single button |
| v2.18.0 | [#267](https://github.com/opensearch-project/dashboards-assistant/pull/267) | Add assistant capabilities to control rendering components |
| v2.18.0 | [#307](https://github.com/opensearch-project/dashboards-assistant/pull/307) | Expose API to check if agent config name has agent ID configured |

## References

- [OpenSearch Assistant Documentation](https://docs.opensearch.org/3.0/dashboards/dashboards-assistant/index/)
- [Build Your Own Chatbot Tutorial](https://docs.opensearch.org/3.0/tutorials/gen-ai/chatbots/build-chatbot/)
- [OpenSearch Assistant Toolkit](https://docs.opensearch.org/3.0/ml-commons-plugin/opensearch-assistant/)
- [Alert Insights](https://docs.opensearch.org/3.0/dashboards/dashboards-assistant/alert-insight/)
- [Data Summary](https://docs.opensearch.org/3.0/dashboards/dashboards-assistant/data-summary/)
- [Text to Visualization](https://docs.opensearch.org/3.0/dashboards/dashboards-assistant/text-to-visualization/)
- [dashboards-assistant Repository](https://github.com/opensearch-project/dashboards-assistant)

## Change History

- **v3.0.0** (2025-05-06): Major UI redesign, streaming output support, single button entry point, text-to-visualization enhancements with auto-aggregation, conversation auto-loading
- **v2.18.0** (2024-11-05): Added assistant capabilities for conditional UI rendering, new API to check agent config existence, renamed agentName to agentConfigName for clarity
- **v2.13** (2024): Initial introduction of OpenSearch Assistant for OpenSearch Dashboards
