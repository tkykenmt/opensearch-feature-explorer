---
tags:
  - indexing
  - ml
  - search
---

# PlanExecuteReflect Agent

## Summary

The PlanExecuteReflect Agent is an experimental agent type in OpenSearch ML Commons designed to solve complex tasks through iterative reasoning and step-by-step execution. It uses a "plan-execute-reflect" pattern where one LLM (the planner) creates and updates a plan, while another LLM (or the same one) executes individual steps using a built-in conversational agent.

## Details

### Architecture

```mermaid
graph TB
    subgraph "PlanExecuteReflect Agent"
        User[User Query] --> Planner[Planner LLM]
        Planner --> Plan[Step-by-Step Plan]
        Plan --> Executor[Executor Agent]
        Executor --> Tools[Available Tools]
        Tools --> Result[Step Result]
        Result --> Reflect[Re-evaluation]
        Reflect --> |Adjust Plan| Planner
        Reflect --> |Complete| Final[Final Result]
    end
    
    subgraph "Memory"
        Memory[(Conversation Index)]
    end
    
    Executor --> Memory
    Final --> Memory
```

### Workflow

The agent operates in three phases:

1. **Planning**: The planner LLM generates an initial step-by-step plan using available tools
2. **Execution**: Each step is executed sequentially using the conversational agent and tools
3. **Re-evaluation**: After each step, the planner LLM re-evaluates and can adjust the plan dynamically

### Components

| Component | Description |
|-----------|-------------|
| `MLPlanExecuteAndReflectAgentRunner` | Main agent runner that orchestrates the plan-execute-reflect loop |
| `Planner LLM` | LLM responsible for creating and updating the execution plan |
| `Executor Agent` | Built-in conversational agent that executes individual steps |
| `ConversationIndexMemory` | Persists execution history including questions, intermediate results, and outputs |

### Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `type` | Agent type | `plan_execute_and_reflect` |
| `_llm_interface` | LLM interface identifier | Required |
| `planner_prompt_template` | Template for planner prompts | Built-in default |
| `reflect_prompt_template` | Template for reflection prompts | Built-in default |
| `executor_system_prompt` | System prompt for executor agent | Built-in default |
| `memory.type` | Memory type for conversation persistence | `conversation_index` |

### Supported LLMs

The agent provides built-in function calling interfaces for:

- Anthropic Claude 3.7 on Amazon Bedrock (`bedrock/converse/claude`)
- OpenAI GPT-4o (`openai/v1/chat/completions`)
- DeepSeek-R1 on Amazon Bedrock (`bedrock/converse/deepseek_r1`)

### Usage Example

```json
POST /_plugins/_ml/agents/_register
{
  "name": "My Plan Execute Reflect Agent",
  "type": "plan_execute_and_reflect",
  "description": "Agent for dynamic task planning and reasoning",
  "llm": {
    "model_id": "YOUR_LLM_MODEL_ID",
    "parameters": {
      "prompt": "${parameters.question}"
    }
  },
  "memory": {
    "type": "conversation_index"
  },
  "parameters": {
    "_llm_interface": "bedrock/converse/claude"
  },
  "tools": [
    { "type": "ListIndexTool" },
    { "type": "SearchIndexTool" },
    { "type": "IndexMappingTool" }
  ]
}
```

Execute the agent:

```json
POST /_plugins/_ml/agents/{agent_id}/_execute
{
  "parameters": {
    "question": "How many documents are in my index?"
  }
}
```

## Limitations

- Experimental feature - not recommended for production use
- Re-evaluation currently only occurs after each step completion
- Requires thorough tool descriptions for optimal LLM decision-making
- DeepSeek-R1 on Bedrock requires custom `executor_system_prompt` due to lack of native function calling

## Change History

- **v3.1.0** (2026-01-10): Added comprehensive unit test and integration test coverage
- **v3.0.0**: Initial experimental release of PlanExecuteReflect Agent

## Related Features
- [Neural Search](../neural-search/neural-search-agentic-search.md)
- [Flow Framework](../flow-framework/flow-framework.md)
- [AI Assistant (Dashboards)](../dashboards-assistant/dashboards-assistant.md)
- [Skills](../skills/skills-opensearch-plugin-dependencies.md)

## References

### Documentation
- [Plan-execute-reflect agents documentation](https://docs.opensearch.org/3.0/ml-commons-plugin/agents-tools/agents/plan-execute-reflect/)
- [Register Agent API](https://docs.opensearch.org/3.0/ml-commons-plugin/api/agent-apis/register-agent/)
- [Building a plan-execute-reflect agent tutorial](https://docs.opensearch.org/3.0/tutorials/gen-ai/agents/build-plan-execute-reflect-agent/)

### Pull Requests
| Version | PR | Description | Related Issue |
|---------|-----|-------------|---------------|
| v3.1.0 | [#3778](https://github.com/opensearch-project/ml-commons/pull/3778) | Adding test cases for PlanExecuteReflect Agent | [#3750](https://github.com/opensearch-project/ml-commons/issues/3750) |
| v3.0.0 | [#3716](https://github.com/opensearch-project/ml-commons/pull/3716) | Initial PlanExecuteReflect Agent implementation |   |

### Issues (Design / RFC)
- [Issue #3750](https://github.com/opensearch-project/ml-commons/issues/3750): Test coverage request
- [Issue #3745](https://github.com/opensearch-project/ml-commons/issues/3745): Feature tracking issue
