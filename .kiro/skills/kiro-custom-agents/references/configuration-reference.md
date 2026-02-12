# Agent Configuration Reference

Source: https://kiro.dev/docs/cli/custom-agents/configuration-reference/

## File Locations

- Local (project-specific): `.kiro/agents/<name>.json`
- Global (user-wide): `~/.kiro/agents/<name>.json`
- Local agents take precedence over global agents with the same name.

## All Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | No | Agent name (derived from filename if omitted) |
| `description` | No | Human-readable description |
| `prompt` | No | System prompt. Inline string or `file://` URI |
| `mcpServers` | No | MCP server definitions |
| `tools` | No | Available tools list |
| `toolAliases` | No | Tool name remapping |
| `allowedTools` | No | Tools that skip permission prompts |
| `toolsSettings` | No | Per-tool configuration |
| `resources` | No | Files, skills, or knowledge bases |
| `hooks` | No | Commands at lifecycle trigger points |
| `includeMcpJson` | No | Include MCP servers from mcp.json files |
| `model` | No | Model ID (e.g. `claude-sonnet-4`) |
| `keyboardShortcut` | No | Shortcut to switch to agent (e.g. `ctrl+a`) |
| `welcomeMessage` | No | Message shown when switching to agent |

## prompt

Supports inline text or `file://` URI:

```json
{ "prompt": "You are an expert AWS specialist" }
{ "prompt": "file://./prompts/my-prompt.md" }
```

Path resolution:
- Relative paths resolve relative to the agent config file's directory
- `"file://./prompt.md"` → same directory as agent config
- `"file://../shared/prompt.md"` → parent directory
- Absolute paths used as-is: `"file:///home/user/prompts/agent.md"`

## mcpServers

```json
{
  "mcpServers": {
    "server-name": {
      "command": "command-to-run",
      "args": ["arg1"],
      "env": { "KEY": "value" },
      "timeout": 120000
    }
  }
}
```

Fields: `command` (required), `args` (optional), `env` (optional), `timeout` (optional, default 120000ms).

Remote MCP servers use `type` and `url` instead of `command`:

```json
{
  "mcpServers": {
    "remote": {
      "type": "http",
      "url": "https://api.example.com/mcp"
    }
  }
}
```

## tools

```json
{
  "tools": [
    "read", "write", "shell", "aws",
    "@git",
    "@server/specific_tool",
    "*",
    "@builtin"
  ]
}
```

- `*` = all tools (built-in + MCP)
- `@builtin` = all built-in tools
- `@server_name` = all tools from that MCP server
- `@server_name/tool_name` = specific MCP tool

## toolAliases

Remap tool names to resolve naming collisions or create intuitive names:

```json
{
  "toolAliases": {
    "@github-mcp/get_issues": "github_issues",
    "@gitlab-mcp/get_issues": "gitlab_issues",
    "@aws-cloud-formation/deploy_stack_with_parameters": "deploy_cf"
  }
}
```

## allowedTools

Supports exact matches and glob wildcards (`*`, `?`):

```json
{
  "allowedTools": [
    "read",
    "@git/git_status",
    "@server/read_*",
    "@fetch",
    "@builtin"
  ]
}
```

Patterns:
- Exact: `"read"`, `"@server_name/tool_name"`, `"@server_name"`
- Prefix wildcard: `"@server/read_*"` → matches `read_file`, `read_config`
- Suffix wildcard: `"@server/*_get"` → matches `issue_get`, `data_get`
- Server pattern: `"@git-*/*"` → any tool from servers matching `git-*`
- Native tool prefix: `@builtin` = all built-in tools
- Single char: `?` matches exactly one character

Rules: `*` matches any sequence (including none), `?` matches exactly one char, exact matches take precedence, case-sensitive.

Does NOT support `"*"` for allowing all tools.

## toolsSettings

```json
{
  "toolsSettings": {
    "write": { "allowedPaths": ["src/**", "*.md"] },
    "shell": {
      "allowedCommands": ["git status"],
      "deniedCommands": ["git push .*"],
      "autoAllowReadonly": true
    },
    "aws": { "allowedServices": ["s3", "lambda"] },
    "@git/git_status": { "git_user": "$GIT_USER" }
  }
}
```

Note: Specifications that configure allowable patterns will be overridden if the tool is also included in `allowedTools`.

## resources

Three types via URI schemes:

```json
{
  "resources": [
    "file://README.md",
    "file://docs/**/*.md",
    "skill://.kiro/skills/**/SKILL.md",
    {
      "type": "knowledgeBase",
      "source": "file://./docs",
      "name": "ProjectDocs",
      "description": "Project documentation",
      "indexType": "best",
      "autoUpdate": true
    }
  ]
}
```

- `file://` — Loaded into context at startup
- `skill://` — Metadata at startup, full content on demand
- `knowledgeBase` — Indexed searchable content

Knowledge base fields: `type` (required, `"knowledgeBase"`), `source` (required, `file://` path), `name` (required), `description` (optional), `indexType` (`"best"` default or `"fast"`), `autoUpdate` (default `false`).

## hooks

```json
{
  "hooks": {
    "agentSpawn": [{ "command": "git status" }],
    "userPromptSubmit": [{ "command": "ls -la" }],
    "preToolUse": [{ "matcher": "execute_bash", "command": "audit-script" }],
    "postToolUse": [{ "matcher": "fs_write", "command": "cargo fmt --all" }],
    "stop": [{ "command": "npm test" }]
  }
}
```

Hook fields: `command` (required), `matcher` (optional, for pre/postToolUse), `timeout_ms`, `cache_ttl_seconds`, `max_output_size`.

Matchers use canonical tool names: `fs_read`, `fs_write`, `execute_bash`, `use_aws`. Also support aliases: `read`, `write`, `shell`, `aws`. MCP tools: `@server/tool`.

Exit codes:
- 0: Success (stdout captured)
- 2: (preToolUse only) Block tool execution, stderr returned to LLM
- Other: Warning shown to user

## includeMcpJson

When `true`, merges MCP servers from workspace and user-level mcp.json files into the agent.

## keyboardShortcut

Format: `[modifier+]key`. Modifiers: `ctrl`, `shift`. Keys: `a-z`, `0-9`.

Toggle behavior: pressing shortcut switches to this agent; pressing again switches back to previous agent. Conflicting shortcuts are disabled with a warning.

## Best Practices

- Start restrictive: begin with minimal tool access and expand as needed
- Name clearly: use descriptive names indicating the agent's purpose
- Document usage: add clear descriptions
- Version control: store agent configs in your project repository
- Test thoroughly: verify tool permissions before sharing
- Use local agents for project-specific configs, global agents for general-purpose workflows
- Review `allowedTools` carefully; use specific patterns over wildcards
- Configure `toolsSettings` for sensitive operations

## Complete Example

```json
{
  "name": "aws-rust-agent",
  "description": "Specialized agent for AWS and Rust development",
  "prompt": "file://./prompts/aws-rust-expert.md",
  "mcpServers": {
    "fetch": { "command": "fetch-server", "args": [] },
    "git": { "command": "git-mcp", "args": [] }
  },
  "tools": ["read", "write", "shell", "aws", "@git", "@fetch/fetch_url"],
  "toolAliases": {
    "@git/git_status": "status",
    "@fetch/fetch_url": "get"
  },
  "allowedTools": ["read", "@git/git_status"],
  "toolsSettings": {
    "write": { "allowedPaths": ["src/**", "tests/**", "Cargo.toml"] },
    "aws": { "allowedServices": ["s3", "lambda"], "autoAllowReadonly": true }
  },
  "resources": ["file://README.md", "file://docs/**/*.md"],
  "hooks": {
    "agentSpawn": [{ "command": "git status" }],
    "postToolUse": [{ "matcher": "fs_write", "command": "cargo fmt --all" }]
  },
  "model": "claude-sonnet-4",
  "keyboardShortcut": "ctrl+shift+r",
  "welcomeMessage": "Ready to help with AWS and Rust development!"
}
```
