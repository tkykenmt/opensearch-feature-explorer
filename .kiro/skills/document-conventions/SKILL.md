---
name: document-conventions
description: Document conventions, templates, and rules for OpenSearch feature/release reports. Use when creating or editing docs under docs/features/ or docs/releases/, including file naming, tag system, link rules, report templates, and Mermaid diagram conventions.
---

# Document Conventions

Single Source of Truth for report structure and formatting. See DEVELOPMENT.md for project-level conventions.

## Directory Structure

```
docs/
├── features/{repository}/           # Cumulative feature docs
│   ├── {repository}-{feature}.md
│   └── index.md
└── releases/v{version}/             # Version-specific docs
    ├── features/{repository}/
    │   └── {item-name}.md
    ├── index.md
    └── summary.md
```

## File Naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature doc | `{repository}/{repository}-{feature}.md` | `k-nn/k-nn-explain-api.md` |
| Release doc | `releases/v{ver}/features/{repository}/{item}.md` | `releases/v3.0.0/features/k-nn/explain-api.md` |

Rules: lowercase, hyphen-separated, include repo prefix, avoid temporal suffixes (`-bugfixes.md`).

### Directory Naming
- Use OpenSearch repository names as-is
- Remove `-plugin` suffix for dashboards plugins: `alerting-dashboards-plugin/` → `alerting-dashboards/`

## Tag System

One tag per document: the repository name from file path.

```yaml
---
tags:
  - {repository}
---
```

No `domain/`, `component/`, or `topic/` prefixes.

## Link Rules

- **No internal `.md` links** — use plain text references instead
- **External links encouraged** — GitHub PRs, Issues, official docs

## Report Templates

See [references/templates.md](references/templates.md) for Feature Report, Release Report, and Release Summary templates.

## Mermaid Diagrams

- Default: `TB` (top-to-bottom)
- `LR` only for simple flows (≤3 nodes)
- Always `TB` with subgraphs

| Use Case | Syntax |
|----------|--------|
| Architecture | `graph TB` |
| Data Flow | `flowchart TB` |
| Sequence | `sequenceDiagram` |
| State | `stateDiagram-v2` |

## Writing Guidelines

- Start with "Summary": brief overview for all readers
- Follow with "Details": technical content for engineers
- Include "Limitations" when applicable
- Include code/config examples where helpful
- Note version compatibility and migration considerations
- Clearly mark speculation or unverified information

## Feature Report Update Rules

When updating existing reports:
1. Preserve existing structure
2. Integrate new info into appropriate sections
3. Update diagrams as needed
4. Sort Change History by version descending (newer at top)
5. Do NOT overwrite newer specs with older version behavior

## References
- Release dates: https://opensearch.org/releases/
