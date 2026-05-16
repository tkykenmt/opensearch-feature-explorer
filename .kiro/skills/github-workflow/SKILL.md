---
name: github-workflow
description: Common GitHub workflow patterns for this project. Use when creating branches, committing, pushing, creating PRs, merging, managing Issues (labels, comments, close), or detecting repository info. Covers the standard docs branch workflow used by investigate, summarize, refactor, and other agents.
---

# GitHub Workflow Patterns

All GitHub API operations use `gh` CLI via `execute_bash` / `shell`. No MCP server required.

## Repository Detection

Run FIRST before any GitHub API calls:
```bash
git remote get-url origin
```
Parse output: `git@github.com:owner/repo.git` → owner=`owner`, repo=`repo`.

## gh CLI Cheat Sheet

### Issues
```bash
# Get issue details
gh issue view {number} -R {owner}/{repo} --json title,body,labels,state,milestone

# List issues with filters
gh issue list -R {owner}/{repo} --state open --label "new-feature,update-feature" --sort created --order asc --limit 1 --json number,title,body,labels

# Create issue
gh issue create -R {owner}/{repo} --title "{title}" --body "{body}" --label "{label1},{label2}"

# Close issue with comment
gh issue comment {number} -R {owner}/{repo} --body "{comment}"
gh issue close {number} -R {owner}/{repo}

# Edit issue (add labels)
gh issue edit {number} -R {owner}/{repo} --add-label "{label}"
```

### Pull Requests
```bash
# Get PR details
gh pr view {number} -R {owner}/{repo} --json title,body,files,mergedAt,labels,milestone

# List PR changed files
gh pr view {number} -R {owner}/{repo} --json files --jq '.files[].path'

# Create PR
gh pr create -R {owner}/{repo} --title "{title}" --head {branch} --base main --body "{body}"

# Merge PR
gh pr merge {number} -R {owner}/{repo} --squash --delete-branch
```

### Search
```bash
# Search code
gh search code "{query}" -R {owner}/{repo} --json path,textMatches

# Search issues/PRs
gh search issues "{query}" -R {owner}/{repo} --json number,title,url
gh search prs "{query}" -R {owner}/{repo} --json number,title,url
```

### File Contents
```bash
# Fetch file from repo (specific branch)
gh api repos/{owner}/{repo}/contents/{path}?ref={branch} --jq '.content' | base64 -d

# Simpler: use git directly if repo is cloned
git show origin/main:{path}
```

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

# 4. Create PR and merge
gh pr create --title "{title}" --head {branch-name} --base main --body "{body}"
gh pr merge {branch-name} --squash --delete-branch

# 5. Return to original branch
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
gh pr create --title "docs: release v{version} reports" --head docs/release-v{version} --base main --body "{body}"
gh pr merge docs/release-v{version} --squash --delete-branch
```

## Issue Operations

### Labels
- Release: `release/v{version}`
- Status: `status/todo`, `status/done`
- Category: `new-feature`, `update-feature`, `enhancement`, `bug-fix`, `breaking-change`
- Repository: `repo/{repository}`

### Close with Comment
```bash
gh issue comment {number} -R {owner}/{repo} --body "{comment}"
gh issue close {number} -R {owner}/{repo}
```
