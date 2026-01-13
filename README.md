# OpenSearch Feature Explorer

A tool to analyze OpenSearch release notes and generate detailed feature/release reports.

## Overview

```mermaid
graph TB
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
| **fetch-release** | Fetch release notes → parse and save all items to `raw-items.json` |
| **group-release** | Group raw items into feature groups → save to `groups.json` |
| **review-groups** | Review and refine groups (split over-aggregated, merge related) |
| **planner** | Create GitHub Project and Issues from `groups.json` |
| **create-issues** | Create individual investigation Issues from tracking Issue |
| **investigate** | Deep investigation (4 modes: Issue, PR, Feature, Interactive Q&A) |
| **summarize** | Aggregate release reports into release summary |
| **generate-release-docs** | Generate release docs from existing feature documents |
| **refactor** | Batch structural changes to existing reports |
| **translate** | Translate reports to other languages |
| **dev** | Development and maintenance of this tool itself |

## Requirements

- Python 3.8+
- [Kiro CLI](https://kiro.dev/)
- [GitHub CLI](https://cli.github.com/) (`gh`) - authenticated via `gh auth login`
- Node.js (for GitHub MCP Server)

### GitHub Token Scopes

Run `gh auth login` with required scopes:

```bash
gh auth login -s read:org,repo,workflow,project
```

| Scope | Purpose |
|-------|---------|
| `repo` | Issue/PR operations |
| `project` | GitHub Projects (progress tracking) |
| `workflow` | GitHub Actions (MkDocs deployment) |
| `read:org` | Organization info |
| `gist` | (included by default) |

## Naming Conventions

| Resource | Pattern | Example |
|----------|---------|---------|
| GitHub Project | `v{version} Investigation` | `v3.0.0 Investigation` |
| Issue (group) | `[{category}] {group_name}` | `[feature] Star Tree Index` |
| Label (release) | `release/v{version}` | `release/v3.0.0` |
| Label (status) | `status/{status}` | `status/todo`, `status/done` |
| Cache directory | `.cache/releases/v{version}/` | `.cache/releases/v3.0.0/` |
| Data directory | `data/releases/v{version}/` | `data/releases/v3.0.0/` |
| Release report | `docs/releases/v{version}/features/{repo}/{item-name}.md` | `docs/releases/v3.0.0/features/opensearch/star-tree-index.md` |
| Feature report | `docs/features/{repo}/{feature-name}.md` | `docs/features/opensearch/star-tree-index.md` |

## Setup

```bash
git clone https://github.com/tkykenmt/opensearch-feature-explorer.git
cd opensearch-feature-explorer
pip install -r requirements.txt

# Authenticate GitHub CLI (required for GitHub MCP)
gh auth login
```

### GitHub Repository Settings

Enable the following in your repository settings (Settings → General):

- **Pull Requests**: Enable "Automatically delete head branches" to clean up feature branches after PR merge
- **Pages** (Settings → Pages): Set Source to "GitHub Actions" for automatic deployment

## Usage

### Use Case 1: Full Release Investigation

Complete workflow for investigating a new OpenSearch release.

```mermaid
flowchart TB
    A[release-investigate] --> B[(Release Reports)]
    A --> C[(Feature Reports)]
    A --> D[(Release Summary)]
```

```bash
python run.py release-investigate 3.0.0
```

<details>
<summary>Manual step-by-step execution</summary>

#### Step 1: Parse Release Notes

```mermaid
flowchart TB
    A[fetch-release] --> B[(raw-items.json)]
    B --> C[group-release]
    C --> D[(groups.json)]
```

```bash
python run.py fetch-release 3.0.0
python run.py group-release 3.0.0 --all
```

#### Step 2: Create GitHub Project & Issues

```mermaid
flowchart TB
    A[(groups.json)] --> B[planner]
    B --> C[(GitHub Project)]
    B --> D[(Issues)]
```

```bash
python run.py planner 3.0.0
```

#### Step 3: Investigate Each Issue

```mermaid
flowchart TB
    A[(Issue)] --> B[investigate]
    B --> C[(Release Report)]
    B --> D[(Feature Report)]
```

```bash
python run.py investigate --issue 124
# Or batch process all
python run.py batch-investigate --all
```

#### Step 4: Create Release Summary

```mermaid
flowchart TB
    A[(Release Reports)] --> B[summarize]
    B --> C[(Release Summary)]
```

```bash
python run.py summarize 3.0.0
```

</details>

### Use Case 2: Single Feature Investigation

Quick investigation of a specific feature without full release workflow.

```mermaid
flowchart TB
    A[PR Number] --> B[investigate]
    C[Feature Name] --> B
    B --> D[Feature Report]
```

```bash
# From a specific PR
python run.py investigate --pr 16233

# From feature name + PR
python run.py investigate --feature "Star Tree" --pr 16233

# Feature deep dive (searches all related PRs)
python run.py investigate --feature "Star Tree"
```

### Use Case 3: Interactive Exploration

Explore features interactively with Q&A.

```mermaid
flowchart TB
    A[investigate] --> B[Q&A Session]
    B --> C[Import URLs]
    C --> B
```

```bash
python run.py investigate
```

### Planner Options

```bash
# Ignore existing tracking Issue and create new one
python run.py planner 3.0.0 -i
python run.py planner 3.0.0 --ignore-existing
```

## Output Structure

```
docs/
├── features/                          # Cumulative feature documentation
│   ├── index.md
│   ├── opensearch/
│   │   ├── star-tree-index.md
│   │   └── star-tree-index.ja.md
│   ├── neural-search/
│   │   └── semantic-highlighting.md
│   └── k-nn/
│       └── explain-api.md
└── releases/
    └── v3.0.0/
        ├── index.md                   # Release index
        ├── summary.md                 # Release summary (from summarize)
        └── features/
            ├── opensearch/
            │   ├── star-tree-enhancements.md
            │   └── grpc-transport.md
            ├── neural-search/
            │   └── semantic-highlighting.md
            └── k-nn/
                └── explain-api.md
```

## Local Preview

```bash
mkdocs serve
# Open http://localhost:8000
```

## Disclosure

This project uses generative AI to create documentation. Generated content may contain inaccuracies. Always verify information against official OpenSearch documentation and source code.
