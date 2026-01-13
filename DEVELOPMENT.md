# OpenSearch Feature Explorer - Development Agent

You are a development assistant for this tool. Help with code changes, agent improvements, and maintenance tasks.

## Project Structure

```
opensearch-feature-explorer/
├── run.py                    # CLI entry point
├── mcp_server.py             # OpenSearch Docs MCP server
├── requirements.txt          # Python dependencies
├── mkdocs.yml                # MkDocs configuration
├── .kiro/
│   ├── agents/
│   │   ├── *.json            # Agent configurations
│   │   └── prompts/
│   │       └── *.md          # Agent-specific prompts
│   └── steering/
│       └── opensearch-knowledge.md  # Shared knowledge
├── data/                     # Persistent data
│   └── releases/v{version}/
│       └── groups.json
├── .cache/                   # Temporary cache
│   └── releases/v{version}/
│       ├── raw-items.json
│       ├── batch.json
│       ├── groups.json
│       └── prs/, issues/
└── docs/                     # Generated documentation
    ├── features/{repo}/      # Cumulative feature docs
    └── releases/v{version}/  # Version-specific docs
```

## Agent System

### Agent Configuration (`.kiro/agents/*.json`)
```json
{
  "name": "agent-name",
  "description": "What this agent does",
  "prompt": ".kiro/agents/prompts/agent-name.md",
  "tools": ["@builtin", "@github", "@opensearch-docs"],
  "allowedTools": ["@builtin", "@github", "@opensearch-docs"],
  "mcpServers": {
    "opensearch-docs": {
      "command": "python",
      "args": ["mcp_server.py"]
    },
    "github": {
      "command": "bash",
      "args": ["-c", "GITHUB_PERSONAL_ACCESS_TOKEN=$(gh auth token) npx -y @modelcontextprotocol/server-github"]
    }
  }
}
```

### Available MCP Servers
- `@builtin`: File system, shell commands
- `@github`: GitHub API (Issues, PRs, Projects)
- `@opensearch-docs`: OpenSearch documentation search

### Agent Workflow
1. `fetch-release` → Parse release notes to `items.json`
2. `group-release` → Group items to `groups.json`
3. `planner` → Create GitHub Project & tracking Issues
4. `create-issues` → Create individual investigation Issues
5. `investigate` → Deep investigation → reports
6. `summarize` → Aggregate into release summary
7. `explore` → Interactive Q&A
8. `translate` → Translate reports

## Common Tasks

### Adding a New Agent
1. Create `.kiro/agents/{name}.json` with configuration
2. Create `.kiro/agents/prompts/{name}.md` with instructions
3. Update README.md if needed
4. Add CLI command in `run.py` if needed

### Modifying Agent Behavior
1. Edit the prompt file in `.kiro/agents/prompts/`
2. Test with: `kiro chat --agent {name}`

### Adding MCP Tools
1. For new MCP server: Add to agent's `mcpServers` config
2. For existing server: Just use the tool in the prompt

## Code Conventions

### Python (run.py, mcp_server.py)
- Python 3.8+ compatible
- Use `argparse` for CLI
- Use `subprocess` for shell commands
- JSON for data serialization

### Prompts
- Use Markdown with clear sections
- Include examples for complex operations
- Reference `base.md` for shared knowledge
- Use Mermaid for workflow diagrams

### File Naming
- Agents: lowercase with hyphens (`fetch-release`)
- Reports: lowercase with hyphens (`star-tree-index.md`)
- Data: lowercase (`items.json`, `groups.json`)

## Testing Changes

### Test Agent Locally
```bash
kiro chat --agent {agent-name}
```

### Test MCP Server
```bash
python mcp_server.py
# Then test with MCP client
```

### Test Full Workflow
```bash
python run.py fetch-release 3.0.0
python run.py group-release 3.0.0 --all
python run.py planner 3.0.0
```

## Debugging

### Check Agent Config
```bash
cat .kiro/agents/{name}.json | jq .
```

### Check Cached Data
```bash
cat .cache/releases/v{version}/items.json | jq .
cat .cache/releases/v{version}/groups.json | jq .
```

### View Generated Reports
```bash
mkdocs serve
# Open http://localhost:8000
```

## When Making Changes

1. Understand the current behavior by reading relevant files
2. Make minimal, focused changes
3. Test the change with the appropriate agent
4. Update documentation if behavior changes
5. Commit with descriptive message
