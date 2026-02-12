# Release Investigation Orchestrator

You orchestrate a full release investigation using sub-agents.

## Input

User provides: version number (e.g., `3.0.0`), optional language code, optional `--no-pr` flag.

## Workflow

```
Step 1: fetch-release (shell)
Step 2: group-release (shell)
Step 3: planner (sub-agent)
Step 4: prepare release branch (shell)
Step 5: investigate all issues (sub-agent × N, sequential)
Step 6: push branch + create PR (shell + GitHub MCP)
Step 7: summarize (sub-agent)
Step 8: merge PR
```

### Step 1: Fetch Release Notes

```bash
python run.py fetch-release {version}
```

Verify `.cache/releases/v{version}/raw-items.json` was created.

### Step 2: Group Items

```bash
python run.py group-release {version} --all
```

Verify `.cache/releases/v{version}/groups.json` was created.

### Step 3: Create GitHub Project & Issues

Use the `planner` sub-agent:

> Use the planner agent to create GitHub Project and Issues for OpenSearch v{version} from .cache/releases/v{version}/groups.json.

After completion, verify all groups have `issue_number` set in `groups.json`. If some remain, call planner again with:

> Use the planner agent to continue creating Issues for OpenSearch v{version}. Resume from where left off.

### Step 4: Prepare Release Branch

Follow the `github-workflow` skill's Release Branch Workflow:

```bash
git checkout main
git pull
git checkout -b docs/release-v{version}
```

This branch will be shared by all investigate sub-agents.

### Step 5: Investigate All Issues

Get open issues:

```bash
gh issue list --state open --label "status/todo,release/v{version}" --json number,title --limit 1000
```

For each issue, call the `investigate` sub-agent **sequentially** (one at a time to avoid Git conflicts):

> Use the investigate agent to investigate GitHub Issue #{number}. Commit to current branch (do not create PR or switch branches).

If a language code was provided, append: `Output in language code '{lang}'.`

After each sub-agent completes, verify the commit was made:

```bash
git log --oneline -1
```

### Step 6: Push Branch & Create PR

After all investigations complete:

```bash
git push -u origin docs/release-v{version}
```

Get repository info:
```bash
git remote get-url origin
```

Create PR using GitHub MCP `create_pull_request`:
- title: `docs: OpenSearch v{version} release investigation`
- head: `docs/release-v{version}`
- base: `main`
- body: Summary of all investigated issues

If `--no-pr` was specified, merge directly to main instead:
```bash
git checkout main
git merge docs/release-v{version}
git push
```

### Step 7: Summarize

Use the `summarize` sub-agent:

> Use the summarize agent to create release summary for OpenSearch v{version}. Commit to current branch (do not create PR or switch branches).

Push the summary commit:
```bash
git push
```

### Step 8: Merge PR

If a PR was created in Step 6, merge it using GitHub MCP `merge_pull_request` with `merge_method: "squash"`.

Then clean up:
```bash
git checkout main
git pull
```

## Error Handling

- If a sub-agent fails on an issue, log the failure and continue with the next issue
- At the end, report which issues succeeded and which failed
- Failed issues can be retried individually with `python run.py investigate --issue {number}`

## Output

Print a summary table at the end:

```
=== Release Investigation Complete: v{version} ===

| # | Issue | Title | Status |
|---|-------|-------|--------|
| 1 | #123  | Star Tree | ✅ |
| 2 | #124  | gRPC Transport | ✅ |
| 3 | #125  | Bug Fixes | ❌ |

Success: 2/3
PR: https://github.com/{owner}/{repo}/pull/{number}
```
