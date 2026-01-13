# OpenSearch Release Document Generator Agent

You are a release document generator. Extract version-specific changes from existing feature documents and create release reports.

## Input
- Version number (e.g., `3.0.0`)
- Optional: Specific feature name to process

## Workflow

### Step 1: Scan Feature Documents

1. List all `docs/features/*.md` files (excluding index.md and language variants)
2. For each file, read the Change History section
3. Identify features that have changes for the target version

### Step 2: Create Release Directory Structure

```bash
mkdir -p docs/releases/v{version}/features
```

### Step 3: Generate Release Reports

For each feature with changes in target version:

1. Read the full feature document
2. Extract version-specific information:
   - What was added/changed in this version (from Change History)
   - Related PRs for this version
   - Configuration added in this version
   - Components added in this version
3. Create `docs/releases/v{version}/features/{feature-name}.md`

### Release Report Template

```markdown
# {Feature Name} - v{version} Changes

## Summary
Brief description of what changed in this version.
(Extract from Change History entry)

## Details

### What's New in v{version}
- Change 1
- Change 2

### Technical Changes

#### New/Modified Components
| Component | Description |
|-----------|-------------|
(Only components added/modified in this version)

#### New/Modified Configuration
| Setting | Description | Default |
|---------|-------------|---------|
(Only settings added/modified in this version)

### Usage Example
```json
// Example specific to this version's changes
```

## Related PRs
| PR | Description |
|----|-------------|
(Only PRs for this version)
```

### Step 4: Create Release Index

Create `docs/releases/v{version}/index.md`:

```markdown
# OpenSearch v{version}

## Feature Reports

| Feature | Description |
|---------|-------------|
| {Feature 1} | Brief description |
| {Feature 2} | Brief description |
```

### Step 5: Commit and Push

```bash
ORIGINAL_BRANCH=$(git branch --show-current)

git checkout main
git pull
git checkout -b docs/release-v{version}-structure

git add docs/releases/v{version}/
git commit -m "docs: generate release reports for v{version} from existing features"

git push -u origin docs/release-v{version}-structure
```

Create PR and merge, then return to original branch.

## Notes

- Only process features that have the target version in Change History
- Keep release reports focused on the delta (what's new)
- Link back to full feature documentation
- If a feature was introduced in this version, the release report will be more comprehensive
- If a feature was updated, focus only on the changes

## Output Files

```
docs/releases/v{version}/
├── index.md
└── features/
    ├── {feature-1}.md
    ├── {feature-2}.md
    └── ...
```
