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
  releases/{version}/release-notes.md    # Release notes (immutable)
  prs/{number}.json                      # Merged PRs only
  issues/{number}.json                   # Closed Issues only
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
- **v3.4.0**: Initial implementation
```

### Release Report Template (docs/releases/v{version}/summary.md)
```markdown
# OpenSearch v{version} Release Summary

## Summary
Brief overview of this release: major themes, key features, and impact.

## Details

### Highlights
```mermaid
graph TB
    ...
```

### New Features
| Feature | Description | PR |
|---------|-------------|-----|

### Improvements
| Area | Description | PR |
|------|-------------|-----|

### Bug Fixes
| Issue | Description | PR |
|-------|-------------|-----|

### Breaking Changes
| Change | Migration | PR |
|--------|-----------|-----|

### Dependencies
Notable dependency updates

## References
- Links to all referenced PRs and Issues
```

## Mermaid Diagram Guidelines

### Diagram Types by Use Case
| Use Case | Syntax | When to Use |
|----------|--------|-------------|
| Architecture | `graph TB` or `graph LR` | Component structure |
| Data Flow | `flowchart LR` | Data flow, processing |
| Sequence | `sequenceDiagram` | API calls, communication |
| State | `stateDiagram-v2` | State transitions |
| Class | `classDiagram` | Class structure |

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
