# Hooks Reference

Source: https://kiro.dev/docs/cli/hooks/

Hooks execute custom commands at specific points during agent lifecycle and tool execution.

## Hook Types

| Type | Trigger | Can Block? | Output Destination |
|------|---------|------------|-------------------|
| `agentSpawn` | Agent activated | No | Added to context |
| `userPromptSubmit` | User submits prompt | No | Added to context |
| `preToolUse` | Before tool execution | Yes (exit 2) | stderr to LLM |
| `postToolUse` | After tool execution | No | — |
| `stop` | Assistant finishes turn | No | — |

## Hook Event (STDIN JSON)

```json
{
  "hook_event_name": "preToolUse",
  "cwd": "/current/working/directory",
  "tool_name": "read",
  "tool_input": { ... },
  "tool_response": { ... }  // postToolUse only
}
```

`userPromptSubmit` also includes `"prompt": "user's input"`.

## Exit Codes

- **0**: Success. stdout captured.
- **2**: (preToolUse only) Block tool. stderr returned to LLM.
- **Other**: Warning shown to user.

## Matcher Patterns

- `"fs_write"` or `"write"` — Match write tool
- `"fs_read"` or `"read"` — Match read tool
- `"execute_bash"` or `"shell"` — Match shell
- `"use_aws"` or `"aws"` — Match AWS CLI tool
- `"@git"` — All tools from git MCP server
- `"@git/status"` — Specific MCP tool
- `"*"` — All tools (built-in and MCP)
- `"@builtin"` — All built-in tools only
- No matcher — Applies to all tools

Hook matchers support both canonical names (`fs_read`, `fs_write`, `execute_bash`, `use_aws`) and their aliases (`read`, `write`, `shell`, `aws`).

## Hook Type Details

### AgentSpawn

Runs when agent is activated. No tool context provided.

Exit: 0 = stdout added to context, other = stderr warning.

### UserPromptSubmit

Runs when user submits a prompt. Output added to conversation context.

Hook event includes `"prompt": "user's input prompt"`.

Exit: 0 = stdout added to context, other = stderr warning.

### PreToolUse

Runs before tool execution. Can validate and block tool usage.

Exit: 0 = allow, 2 = block (stderr to LLM), other = warning + allow.

### PostToolUse

Runs after tool execution. Hook event includes `tool_response`.

Exit: 0 = success, other = stderr warning (tool already ran).

### Stop

Runs when assistant finishes responding. Does not use matchers.

Exit: 0 = success, other = stderr warning.

### MCP Example

For MCP tools, the tool name includes the full namespaced format:

```json
{
  "hook_event_name": "preToolUse",
  "cwd": "/current/working/directory",
  "tool_name": "@postgres/query",
  "tool_input": { "sql": "SELECT * FROM orders LIMIT 10;" }
}
```

## Options

- `timeout_ms`: Default 30000 (30s)
- `cache_ttl_seconds`: 0 = no caching (default). AgentSpawn hooks are never cached.
- `max_output_size`: Limit output size in bytes.

## Use Cases

- **Security validation**: preToolUse to block dangerous commands
- **Audit logging**: pre/postToolUse to log tool usage
- **Auto-formatting**: postToolUse on fs_write to run formatters
- **Context gathering**: agentSpawn to inject git status, env info
- **Post-processing**: stop to run tests/linting after each turn
