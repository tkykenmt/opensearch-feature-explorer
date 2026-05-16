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
2. Get PR details: `gh pr view {number} -R {owner}/{repo} --json title,body,files,labels`
3. Check changed files: `gh pr view {number} -R {owner}/{repo} --json files --jq '.files[].path'`
4. Get related code: `gh api repos/{owner}/{repo}/contents/{path} --jq '.content' | base64 -d`
5. Get Issue details: `gh issue view {number} -R {owner}/{repo} --json title,body,labels,comments`
