# Prompts Reference

Source: https://kiro.dev/docs/cli/chat/manage-prompts/

Reusable prompts for development workflows. Three types: local (workspace), global (user-wide), MCP (from servers).

## Commands

- `/prompts list` — List all available prompts (local, global, MCP)
- `/prompts create --name <name> [--content <content>]` — Create local prompt. Opens editor if no content provided.
- `/prompts edit <name>` — Edit existing prompt in default editor
- `/prompts details <name>` — View metadata, content, arguments, source

## Using Prompts

Invoke with `@` prefix in chat:

```
@code-review
@team-standup
```

## MCP Prompt Arguments

MCP prompts accept arguments; file-based prompts do not.

```
@server-name/prompt-name <required-arg> [optional-arg]
@dev-tools/analyze "performance issue" "detailed"
```

Use `/prompts details <name>` to discover available arguments.

## Storage & Priority

1. **Local** (highest): `.kiro/prompts/` — workspace-specific
2. **Global**: `~/.kiro/prompts/` — all projects
3. **MCP** (lowest): from configured MCP servers

Local overrides global, global overrides MCP for same-name prompts.
