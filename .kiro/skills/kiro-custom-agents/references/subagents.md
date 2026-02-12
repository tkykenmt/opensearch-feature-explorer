# Subagents Reference

Source: https://kiro.dev/docs/cli/chat/subagents/

Subagents are specialized agents that autonomously execute complex tasks with their own context and tool access.

## Capabilities

- Autonomous execution with own context
- Live progress tracking
- Parallel execution of multiple subagents
- Result aggregation back to main agent

## Tool Availability

Available: `read`, `write`, `shell`, MCP tools.

Not available: `web_search`, `web_fetch`, `introspect`, `thinking`, `todo_list`, `use_aws`, `grep`, `glob`.

If a custom agent config includes unavailable tools, those tools are simply skipped.

## Using Custom Agents as Subagents

```
> Use the backend agent to refactor the payment module
```

Reference agent by name. Subagent inherits tool access and settings from that agent's configuration.

## Configuring Subagent Access

### availableAgents

Restrict which agents can be spawned as subagents:

```json
{
  "toolsSettings": {
    "subagent": {
      "availableAgents": ["reviewer", "tester", "docs-*"]
    }
  }
}
```

### trustedAgents

Allow specific agents to run without permission prompts:

```json
{
  "toolsSettings": {
    "subagent": {
      "trustedAgents": ["reviewer", "tester", "analyzer"]
    }
  }
}
```

### Combined

```json
{
  "toolsSettings": {
    "subagent": {
      "availableAgents": ["reviewer", "tester", "analyzer", "docs-*"],
      "trustedAgents": ["reviewer", "tester"]
    }
  }
}
```

Both support glob patterns.

## Troubleshooting

| Issue | Solution |
|-------|---------|
| Subagent not starting | Verify task description is clear and actionable |
| Missing tool access | Check if tool is available in subagent runtime |
| Incomplete results | Provide more specific instructions or break into smaller tasks |
