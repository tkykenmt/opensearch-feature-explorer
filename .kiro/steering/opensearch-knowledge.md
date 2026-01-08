# OpenSearch Feature Explorer - Base Knowledge

## OpenSearch Domain Knowledge

### Repository Structure
- **opensearch-build**: Consolidated release notes, build configurations
- **OpenSearch**: Core engine (Java)
- **OpenSearch-Dashboards**: UI/visualization (TypeScript/React)

### Release Notes Format
Each item follows `- Description ([#PR_NUMBER](URL))` format with PR links.
Sections: `### Added`, `### Changed`, `### Fixed`, `### Dependencies`

## GitHub MCP Tools Usage

Use GitHub MCP Server to retrieve repository information.

### Repository Detection
Before using GitHub MCP tools, get the target repository:
```bash
git remote get-url origin
```
Parse output to extract owner/repo (e.g., `git@github.com:owner/repo.git` → owner=`owner`, repo=`repo`).

### Available Tools
- `get_file_contents`: Get file contents (for fetching release notes)
- `get_pull_request`: Get PR details
- `list_pull_request_files`: List PR changed files
- `get_issue`: Get Issue details
- `search_code`: Search code

### Investigation Flow
1. Extract PR numbers from release notes
2. Get PR details with `get_pull_request`
3. Check changed files with `list_pull_request_files`
4. Get related code with `get_file_contents` if needed
5. Get Issue details with `get_issue` if linked

## Caching

### Cache Directory
Store fetched data in `.cache/` to avoid redundant API calls.

### Cache Structure
```
.cache/
  releases/{version}/
    release-notes-build.md       # From opensearch-build
    release-notes-core.md        # From OpenSearch
    release-notes-dashboards.md  # From OpenSearch-Dashboards
    prs/
      {number}.json              # Merged PRs only
    issues/
      {number}.json              # Closed Issues only
```

### Cache Rules
- **Release notes**: Always cache (version-specific, immutable)
- **PRs**: Cache only if `merged: true`
- **Issues**: Cache only if `state: closed`
- **Code files**: Do not cache

### Workflow
1. Before fetching, check if cached file exists
2. If cached: Read from `.cache/`
3. If not cached: Fetch from GitHub, then save to `.cache/` if cacheable

## Writing Rules

### Content Structure
- Start with "Summary" section: brief overview accessible to all readers
- Follow with "Details" section: accurate technical content for engineers
- Include "Limitations" or "Known Issues" section when applicable

### Technical Content
- Include code/configuration examples where helpful
- Note version compatibility and migration considerations
- Mention performance implications if relevant
- Clearly mark speculation or unverified information

### References
- Include URLs of referenced Pull Requests and Issues
- Link to official OpenSearch documentation when available

### Visual Elements
- Include diagrams showing architecture and processing flows
- Use tables for configuration options, components, and PR lists

## Report Output Format

### Release Report Template (docs/releases/v{version}/features/{item-name}.md)
```markdown
# {Item Name}

## Summary
What this release item adds/changes and why it matters.
Focus on the delta - what's new in this version specifically.

## Details

### What's New in v{version}
Specific changes introduced in this version.

### Technical Changes

#### Architecture Changes
```mermaid
graph TB
    ...
```

#### New Components
| Component | Description |
|-----------|-------------|

#### New Configuration
| Setting | Description | Default |
|---------|-------------|---------|

### Usage Example
```json
// Example showing new functionality
```

### Migration Notes
Steps to adopt this change (if applicable).

## Limitations
Known limitations specific to this release.

## Related PRs
| PR | Description |
|----|-------------|
| [#1234](url) | Main implementation |

## References
- [Issue #1000](url): Feature request
- [Documentation](url): Official docs

## Related Feature Report
- [Full feature documentation](../../features/{feature-name}.md)
```

### Feature Report Template (docs/features/{feature-name}.md)
```markdown
# {Feature Name}

## Summary
Brief overview of what this feature does, why it matters, and key benefits.

## Details

### Architecture
```mermaid
graph TB
    ...
```

### Data Flow
```mermaid
flowchart LR
    ...
```

### Components
| Component | Description |
|-----------|-------------|

### Configuration
| Setting | Description | Default |
|---------|-------------|---------|

### Usage Example
```yaml
# Example configuration
```

## Limitations
Known limitations or constraints

## Related PRs
| Version | PR | Description |
|---------|-----|-------------|
| v3.4.0 | [#1234](https://github.com/opensearch-project/OpenSearch/pull/1234) | Initial implementation |

## References
- [Issue #1000](https://github.com/opensearch-project/OpenSearch/issues/1000): Original feature request

## Change History
- **v3.4.0** (YYYY-MM-DD): Initial implementation
```

### Release Summary Template (docs/releases/v{version}/summary.md)
```markdown
# OpenSearch v{version} Release Summary

## Summary
Brief overview of this release: major themes, key features, and impact.

## Highlights
```mermaid
graph TB
    ...
```

## New Features
| Feature | Description | Report |
|---------|-------------|--------|
| {Name} | {Brief description} | [Details](features/{item-name}.md) |

## Improvements
| Area | Description | Report |
|------|-------------|--------|

## Bug Fixes
| Issue | Description | PR |
|-------|-------------|-----|

## Breaking Changes
| Change | Migration | Report |
|--------|-----------|--------|

## Dependencies
Notable dependency updates

## References
- Links to all referenced PRs and Issues
```

## Mermaid Diagram Guidelines

### Diagram Types by Use Case
| Use Case | Syntax | When to Use |
|----------|--------|-------------|
| Architecture | `graph TB` | Component structure |
| Data Flow | `flowchart TB` | Data flow, processing |
| Sequence | `sequenceDiagram` | API calls, communication |
| State | `stateDiagram-v2` | State transitions |
| Class | `classDiagram` | Class structure |

### Direction Rules
- Use `TB` (top-to-bottom) as default direction
- Use `LR` (left-to-right) only for simple flows with 3 or fewer nodes
- Always use `TB` when diagram contains subgraphs

### Required Diagrams
- **Feature Report**: Architecture diagram (required), Data Flow (recommended)
- **Release Summary**: Architecture Changes diagram (if applicable)

## Feature Report Update Rules

### Merge Strategy
When existing report exists:
1. Preserve existing structure
2. Integrate new information into appropriate sections
3. Update diagrams as needed
4. Append to Change History

### Change History Format
```markdown
## Change History
- **v3.5.0** (2024-01-15): Added feature X, performance improvements
- **v3.4.0** (2023-10-01): Initial implementation
```
(Newer changes at top)

### Release Dates Reference
Refer to https://opensearch.org/releases/ for official release dates.

## Resource Search

### OpenSearch Docs MCP Tool
Use the `search` tool from `opensearch-docs` MCP server to search documentation and blogs.

Parameters:
- `query` (required): Search query
- `version`: OpenSearch version (default: "3.0")
- `types`: "docs", "blogs", or "docs,blogs" (default: "docs,blogs")
- `limit`: Max results (default: 10)

Response:
```json
{
  "query": "star tree",
  "version": "3.0",
  "total": 50,
  "results": [
    {
      "title": "Star-tree index",
      "url": "https://docs.opensearch.org/3.0/...",
      "type": "DOCS",
      "snippet": "..."
    }
  ]
}
```

Use `web_fetch` to retrieve full content from returned URLs.
