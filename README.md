# OpenSearch Feature Explorer

A tool to analyze OpenSearch release notes and generate detailed feature/release reports.

## Overview

```mermaid
graph LR
    subgraph Input
        RN[Release Notes]
        PR[Pull Requests]
        Issue[Issues]
        Docs[Docs/Blogs]
    end
    subgraph "Kiro CLI + MCP"
        Agent[Agents]
        MCP[OpenSearch Docs MCP]
    end
    subgraph Output
        FR[Feature Reports]
        RR[Release Reports]
        GH[GitHub Issues]
    end
    RN --> Agent
    PR --> Agent
    Issue --> Agent
    Docs --> MCP --> Agent
    Agent --> FR
    Agent --> RR
    Agent --> GH
```

## Agents

| Agent | Description |
|-------|-------------|
| **planner** | Analyze release notes → create GitHub Issues for investigation |
| **investigate** | Deep investigation of a single feature |
| **explore** | Interactive Q&A + URL import |
| **summarize** | Create release summary from feature reports |
| **translate** | Translate reports to other languages |

## Requirements

- Python 3.8+
- [Kiro CLI](https://kiro.dev/)
- [GitHub CLI](https://cli.github.com/) (`gh`) - authenticated via `gh auth login`
- Node.js (for GitHub MCP Server)

## Setup

```bash
git clone https://github.com/tkykenmt/opensearch-feature-explorer.git
cd opensearch-feature-explorer
pip install -r requirements.txt

# Authenticate GitHub CLI (required for GitHub MCP)
gh auth login
```

### MCP Server Configuration

Add to your Kiro CLI MCP config (`~/.kiro/settings.json`):

```json
{
  "mcpServers": {
    "opensearch-docs": {
      "command": "python",
      "args": ["/path/to/opensearch-feature-explorer/mcp_server.py"]
    }
  }
}
```

## Usage

### Workflow

```bash
# 1. Plan release investigation (creates GitHub Issues)
python run.py planner 3.0.0

# 2. Investigate each feature (from GitHub Issue)
python run.py investigate --issue 123

# 3. Or investigate directly
python run.py investigate "Star Tree" --pr 16233

# 4. Create release summary
python run.py summarize 3.0.0

# 5. Translate if needed
python run.py translate --feature "Star Tree" --to ja
```

### Interactive Exploration

```bash
python run.py explore "Segment Replication" --lang ja
```

## Output Structure

```
docs/
├── features/
│   ├── star-tree-index.md
│   └── star-tree-index.ja.md
└── releases/
    └── v3.0.0/
        └── summary.md
```

## Local Preview

```bash
mkdocs serve
# Open http://localhost:8000
```

## License

MIT
