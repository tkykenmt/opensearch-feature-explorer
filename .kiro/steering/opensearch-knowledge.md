# OpenSearch Feature Explorer - Base Knowledge

**For document conventions and templates, see `document-conventions` skill.**
**For GitHub workflow patterns, see `github-workflow` skill.**

---

## OpenSearch Domain Knowledge

### Repository Structure
- **opensearch-build**: Consolidated release notes, build configurations
- **OpenSearch**: Core engine (Java)
- **OpenSearch-Dashboards**: UI/visualization (TypeScript/React)

### Release Notes Format
Each item follows `- Description ([#PR_NUMBER](URL))` format with PR links.
Sections: `### Added`, `### Changed`, `### Fixed`, `### Dependencies`

### Investigation Flow
1. Extract PR numbers from release notes
2. Get PR details with `get_pull_request`
3. Check changed files with `list_pull_request_files`
4. Get related code with `get_file_contents` if needed
5. Get Issue details with `get_issue` if linked
