---
name: github-workflow
description: Common GitHub workflow patterns for this project. Use when creating branches, committing, pushing, creating PRs, merging, managing Issues (labels, comments, close), or detecting repository info. Covers the standard docs branch workflow used by investigate, summarize, refactor, and other agents.
---

# GitHub Workflow Patterns

## Repository Detection

Run FIRST before any GitHub API calls:
```bash
git remote get-url origin
```
Parse output: `git@github.com:owner/repo.git` → owner=`owner`, repo=`repo`.

## Branch + PR + Merge Workflow

Standard pattern for docs changes:

```bash
# 1. Save current branch
ORIGINAL_BRANCH=$(git branch --show-current)

# 2. Create branch from main
git checkout main
git pull
git checkout -b {branch-name}

# 3. Stage and commit
git add {paths}
git commit -m "{message}"
git push -u origin {branch-name}
```

Then use GitHub tools:
1. `create_pull_request` — title, head={branch-name}, base=main
2. `merge_pull_request` — merge_method=squash

```bash
# 4. Return to original branch
git checkout $ORIGINAL_BRANCH
git pull origin $ORIGINAL_BRANCH
```

### Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature report | `docs/{item-name}-v{version}` | `docs/star-tree-index-v3.0.0` |
| Release investigation | `docs/release-v{version}` | `docs/release-v3.0.0` |
| Release summary | `docs/release-v{version}-summary` | `docs/release-v3.0.0-summary` |
| Release structure | `docs/release-v{version}-structure` | `docs/release-v3.0.0-structure` |

### Release Branch Workflow

Used by `release-investigate` agent. Single branch for all investigation work in a version:

```bash
# 1. Create shared branch
git checkout main && git pull
git checkout -b docs/release-v{version}

# 2. Sub-agents commit to this branch (no branch switching)
git add docs/ && git commit -m "docs: add {item-name} report for v{version}"

# 3. After all investigations, push and create single PR
git push -u origin docs/release-v{version}
# create_pull_request → merge_pull_request
```

## Issue Operations

### Labels
- Release: `release/v{version}`
- Status: `status/todo`, `status/done`
- Category: `new-feature`, `update-feature`, `enhancement`, `bug-fix`, `breaking-change`
- Repository: `repo/{repository}`

### Close with Comment
Post completion comment, then close with `update_issue` (state=closed).

## GitHub MCP Tools Reference

- `get_file_contents`: Fetch file from repo
- `get_pull_request`: PR details
- `list_pull_request_files`: PR changed files
- `get_issue` / `list_issues`: Issue operations
- `search_code`: Code search
- `create_pull_request` / `merge_pull_request`: PR lifecycle
- `create_issue` / `update_issue`: Issue lifecycle
- `add_labels_to_issue`: Label management
