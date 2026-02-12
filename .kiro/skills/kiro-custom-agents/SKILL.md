---
name: kiro-custom-agents
description: Create and configure Kiro CLI custom agents (JSON config files). Use when user asks to "create a kiro agent", "make a custom agent", "configure agent tools", "set up MCP servers in an agent", "add hooks to an agent", "troubleshoot agent config", or any task involving kiro-cli agent JSON configuration, tool permissions, resources, hooks, steering, MCP integration, or code intelligence setup.
---

# Kiro Custom Agents

## Overview

Guide for creating and configuring Kiro CLI custom agents — JSON configuration files that customize Kiro's behavior for specific workflows.

## Quick Start

Create an agent interactively in a Kiro CLI session:

```
/agent generate
```

Or via CLI:

```bash
kiro-cli agent create --name my-agent
```

Or manually create a JSON file:
- Global: `~/.kiro/agents/<name>.json`
- Local (project): `.kiro/agents/<name>.json`

Minimal agent:

```json
{
  "name": "my-agent",
  "description": "A custom agent for my workflow",
  "tools": ["read", "write"],
  "allowedTools": ["read"],
  "resources": ["file://README.md"],
  "prompt": "You are a helpful coding assistant"
}
```

## Workflow

1. Clarify the agent's purpose and target workflow
2. Determine which tools are needed (`tools`) and which to pre-approve (`allowedTools`)
3. Identify MCP servers if external tools are needed
4. Choose resources to load (files, skills, knowledge bases)
5. Add hooks for dynamic context or validation
6. Configure tool restrictions via `toolsSettings`
7. Write the JSON config file
8. Test: `/agent list` → `/agent swap <name>` → `/tools` → test workflows

## Key Concepts

**tools**: What the agent CAN use. `"*"` = all, `"@builtin"` = built-in only, `"@server"` = all from MCP server.

**allowedTools**: What runs WITHOUT permission prompts. Supports glob patterns (`@server/read_*`, `@builtin`). Does NOT support `"*"`.

**toolAliases**: Remap tool names to resolve naming collisions or create intuitive names.

**resources**: Context loaded at startup. `file://` = immediate, `skill://` = on-demand, `knowledgeBase` = indexed search.

**hooks**: Commands at lifecycle points. `agentSpawn`, `userPromptSubmit`, `preToolUse` (can block), `postToolUse`, `stop`.

**steering**: NOT auto-included in custom agents. Add explicitly: `"resources": ["file://.kiro/steering/**/*.md"]`

## Updating This Skill

Reference files have `Source: <URL>` headers linking to official Kiro docs. To check for updates:

```bash
python3 scripts/fetch_docs.py --diff   # Check which sources changed
python3 scripts/fetch_docs.py          # Fetch and save raw HTML to references/raw/
```

After fetching, compare `references/raw/*.html` against existing `references/*.md` files and update the summaries as needed. Each reference file is a curated summary — not a raw copy — so review changes before updating.

## References

- **Full config schema**: See [references/configuration-reference.md](references/configuration-reference.md) for all fields, patterns, and best practices
- **Working examples**: See [references/examples.md](references/examples.md) for AWS, dev workflow, code review, project-specific, and remote MCP agents
- **Hooks**: See [references/hooks.md](references/hooks.md) for hook types, matchers, exit codes, MCP examples, and use cases
- **MCP setup**: See [references/mcp.md](references/mcp.md) for MCP server configuration (CLI, mcp.json, agent config, remote)
- **Steering**: See [references/steering.md](references/steering.md) for steering file scope, team steering, custom files, and integration with agents
- **Code intelligence**: See [references/code-intelligence.md](references/code-intelligence.md) for LSP setup, pattern search/rewrite, `/code` commands, and language server usage
- **Context management**: See [references/context.md](references/context.md) for agent resources, session context, knowledge bases, and compaction
- **Subagents**: See [references/subagents.md](references/subagents.md) for subagent tool availability, `availableAgents`/`trustedAgents` config, and usage
- **Prompts**: See [references/prompts.md](references/prompts.md) for `/prompts` commands, MCP prompt arguments, and storage priority
- **Images**: See [references/images.md](references/images.md) for image input methods, supported formats, and use cases
- **Troubleshooting**: See [references/troubleshooting.md](references/troubleshooting.md) for common issues and testing checklist
