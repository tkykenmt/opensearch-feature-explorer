# OpenSearch Feature Explorer - Base Knowledge

**For document conventions, templates, and rules, see DEVELOPMENT.md (Single Source of Truth).**

---

## OpenSearch Domain Knowledge

### Repository Structure
- **opensearch-build**: Consolidated release notes, build configurations
- **OpenSearch**: Core engine (Java)
- **OpenSearch-Dashboards**: UI/visualization (TypeScript/React)

### Release Notes Format
Each item follows `- Description ([#PR_NUMBER](URL))` format with PR links.
Sections: `### Added`, `### Changed`, `### Fixed`, `### Dependencies`

---

## GitHub MCP Tools Usage

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

---

## OpenSearch Docs MCP Tool

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

---

## Writing Guidelines

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

---

## Feature Report Update Rules

### Merge Strategy
When existing report exists:
1. Preserve existing structure
2. Integrate new information into appropriate sections
3. Update diagrams as needed
4. Append to Change History (newer at top)

### Release Dates Reference
Refer to https://opensearch.org/releases/ for official release dates.
