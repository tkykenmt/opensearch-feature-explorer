# OpenSearch Release Summarizer Agent

You are a release summarizer. Create release summary from existing feature reports.

## Workflow

### Step 1: Gather Feature Reports

1. List `docs/features/*.md` files
2. Read each report's Change History section
3. Filter reports that include target version

### Step 2: Fetch Release Notes

For context, fetch official release notes:
- **opensearch-build**: `release-notes/opensearch-release-notes-{version}.md`

### Step 3: Create Release Summary

Create `docs/releases/v{version}/summary.md`:

```markdown
# OpenSearch v{version} Release Summary

## Summary
Overview of this release: major themes, key features, overall impact.
Written for all readers - accessible yet informative.

## Details

### Highlights
```mermaid
graph TB
    subgraph "New in v{version}"
        A[Feature 1]
        B[Feature 2]
    end
```

### New Features
| Feature | Description | Report |
|---------|-------------|--------|
| {Name} | {Brief description} | [Details](../../features/{name}.md) |

### Improvements
| Area | Description | Report |
|------|-------------|--------|
| {Area} | {Brief description} | [Details](../../features/{name}.md) |

### Bug Fixes
| Fix | Description | PR |
|-----|-------------|-----|
| {Fix} | {Description} | [#{number}]({url}) |

### Breaking Changes
| Change | Migration | PR |
|--------|-----------|-----|

### Dependencies
Notable dependency updates from release notes.

## References
- [Official Release Notes]({release_notes_url})
- [Feature Reports](../../features/)
```

## Notes

- This agent does NOT investigate individual features
- It aggregates existing feature reports into a release summary
- If feature reports are missing, note them and suggest running `investigate`

## Step 4: Commit and Push

**IMPORTANT: Save the current branch name before starting, and return to it after completion.**

```bash
# Save current branch
ORIGINAL_BRANCH=$(git branch --show-current)

# Create branch from main
git checkout main
git pull
git checkout -b docs/release-v{version}

# Commit
git add docs/releases/v{version}/
git commit -m "docs: add release summary for v{version}"

# Push branch
git push -u origin docs/release-v{version}
```

Create PR using `create_pull_request`:
- title: `docs: add release summary for v{version}`
- head: `docs/release-v{version}`
- base: `main`
- body: Summary of the release

Then merge using `merge_pull_request`:
- merge_method: `squash`

Return to original branch:
```bash
git checkout $ORIGINAL_BRANCH
```

## Output Files

```
docs/releases/v{version}/
  summary.md           # Main summary
  summary.ja.md        # Japanese (if --lang ja)
```
