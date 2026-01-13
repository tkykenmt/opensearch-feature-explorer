# OpenSearch Feature Explorer - Development Guide

Development guide and **Single Source of Truth** for project conventions.

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
│       └── opensearch-knowledge.md  # LLM context (references this doc)
├── data/                     # Persistent data
│   └── releases/v{version}/
│       └── groups.json
├── .cache/                   # Temporary cache (git-ignored)
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

### Agent Workflow
```
fetch-release → group-release → planner → create-issues → investigate → summarize
```

| Agent | Input | Output |
|-------|-------|--------|
| `fetch-release` | Version | `raw-items.json` |
| `group-release` | `raw-items.json` | `groups.json` |
| `planner` | `groups.json` | GitHub Project + Issues |
| `create-issues` | Tracking Issue | Individual Issues |
| `investigate` | Issue | Release Report + Feature Report |
| `summarize` | Release Reports | Release Summary |
| `translate` | Report | Translated Report |
| `refactor` | Reports | Refactored Reports |

### Agent Configuration
```json
{
  "name": "agent-name",
  "prompt": ".kiro/agents/prompts/agent-name.md",
  "mcpServers": {
    "opensearch-docs": { "command": "python", "args": ["mcp_server.py"] },
    "github": { "command": "bash", "args": ["-c", "GITHUB_PERSONAL_ACCESS_TOKEN=$(gh auth token) npx -y @modelcontextprotocol/server-github"] }
  }
}
```

---

## Document Conventions

### Directory Structure
```
docs/
├── features/{repo}/           # Cumulative feature documentation
│   ├── {repo}-{feature}.md
│   └── index.md
└── releases/v{version}/       # Version-specific documentation
    ├── features/{repo}/
    │   └── {item-name}.md
    ├── index.md
    └── summary.md
```

### File Naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature doc | `{repo}/{repo}-{feature}.md` | `k-nn/k-nn-explain-api.md` |
| Release doc | `releases/v{ver}/features/{repo}/{item}.md` | `releases/v3.0.0/features/k-nn/explain-api.md` |
| Index | `{dir}/index.md` | `features/k-nn/index.md` |

Rules:
- Lowercase, hyphen-separated
- Include repo prefix for searchability
- Avoid temporal suffixes (`-bugfixes.md`, `-enhancements.md`)

### Directory Naming
- Use OpenSearch repository names as-is
- Remove `-plugin` suffix for dashboards plugins
  - `alerting-dashboards-plugin/` → `alerting-dashboards/`

---

## Tag System

Each document has exactly **one tag**: the repository name derived from file path.

```yaml
---
tags:
  - {repo}
---
```

| Path | Tag |
|------|-----|
| `docs/features/opensearch/*.md` | `opensearch` |
| `docs/features/k-nn/*.md` | `k-nn` |
| `docs/releases/v3.0.0/features/neural-search/*.md` | `neural-search` |

No `domain/`, `component/`, or `topic/` prefixes.

---

## Link Rules

### Internal Links
**Do NOT use internal `.md` links** between documents.

```markdown
# Bad - creates maintenance burden
See [Star Tree Index](../opensearch/opensearch-star-tree-index.md)

# Good - plain text reference
See Star Tree Index documentation
```

Rationale: Internal links break when files are moved/renamed.

### External Links
External links (GitHub PRs, Issues, official docs) are allowed and encouraged.

```markdown
# Good
- [#1234](https://github.com/opensearch-project/OpenSearch/pull/1234)
- [Official Docs](https://opensearch.org/docs/latest/...)
```

---

## Report Templates

### Frontmatter (Required)
All reports must include YAML frontmatter with tags:

```yaml
---
tags:
  - {repo}
---
```

### Feature Report Structure
```markdown
---
tags:
  - {repo}
---
# {Feature Name}

## Summary
Brief overview accessible to all readers.

## Details

### Architecture
(Mermaid diagram)

### Components
| Component | Description |
|-----------|-------------|

### Configuration
| Setting | Description | Default |
|---------|-------------|---------|

### Usage Example

## Limitations

## Change History
- **v3.1.0** (2024-03-01): Added X
- **v3.0.0** (2024-01-15): Initial implementation

## References

### Documentation
### Pull Requests
| Version | PR | Description |
|---------|-----|-------------|
```

### Release Report Structure
```markdown
---
tags:
  - {repo}
---
# {Item Name}

## Summary
What changed in this version (delta focus).

## Details

### What's New in v{version}

### Technical Changes

## Limitations

## References

### Pull Requests
| PR | Description | Related Issue |
|----|-------------|---------------|
```

### Release Summary Structure
```markdown
# OpenSearch v{version} Release Summary

## Summary

## Highlights
(Mermaid diagram)

## New Features
| Feature | Description | Report |
|---------|-------------|--------|

## Improvements

## Bug Fixes

## Breaking Changes

## References
```

---

## Mermaid Diagrams

### Direction
- Default: `TB` (top-to-bottom)
- Use `LR` only for simple flows (≤3 nodes)
- Always `TB` when using subgraphs

### Types
| Use Case | Syntax |
|----------|--------|
| Architecture | `graph TB` |
| Data Flow | `flowchart TB` |
| Sequence | `sequenceDiagram` |
| State | `stateDiagram-v2` |

---

## Caching

### Structure
```
.cache/releases/v{version}/
├── raw-items.json    # Parsed release items
├── batch.json        # Current batch
├── groups.json       # Grouped items
├── prs/{number}.json # Merged PRs only
└── issues/{number}.json # Closed Issues only
```

### Rules
- PRs: Cache only if `merged: true`
- Issues: Cache only if `state: closed`
- Code files: Do not cache

---

## Code Conventions

### Python
- Python 3.8+ compatible
- `argparse` for CLI
- JSON for data serialization

### Prompts
- Markdown with clear sections
- Reference DEVELOPMENT.md for rules
- Mermaid for workflow diagrams

### Naming
- Agents: `lowercase-with-hyphens`
- Reports: `lowercase-with-hyphens.md`
- Data: `lowercase.json`

---

## Testing

```bash
# Test agent
kiro chat --agent {agent-name}

# Test full workflow
python run.py fetch-release 3.0.0
python run.py group-release 3.0.0 --all
python run.py planner 3.0.0

# Preview docs
mkdocs serve
```

---

## Making Changes

1. Update DEVELOPMENT.md first (SSoT)
2. Update steering/prompts to reference new rules
3. Test with appropriate agent
4. Commit with descriptive message
