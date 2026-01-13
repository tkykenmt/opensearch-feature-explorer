# Refactor Agent

Transform report files structurally without changing content.

## Modes

### File Mode
Transform single file structurally.
```bash
python run.py refactor docs/features/k-nn/vector-search-k-nn.md
```

### Issue Mode
Read Issue for transformation rules, process target files.
```bash
python run.py refactor --issue 1942
```

## Processing Flow

1. **Identify targets**: Parse file path or Issue body for target files
2. **Determine transformation**: Simple (sed/grep) or LLM-based
3. **Create plan**: Post plan as Issue comment (Issue mode only)
4. **Process files**: Transform each file, commit changes
5. **Update progress**: Update Issue comment with status

## Issue Comment Format

When processing an Issue, post a plan comment:

```markdown
## Refactor Plan
**Target**: {count} files matching `{pattern}`

### Files
- [ ] path/to/file1.md
- [ ] path/to/file2.md
...

## Progress (0/{count})
| File | Status | Notes |
|------|--------|-------|
```

Update progress after each file:
- `✓ Done` - Successfully transformed
- `⏭ Skipped` - No changes needed
- `✗ Failed` - Error occurred

## Transformation Types

### Simple Replacement (no LLM)
Use sed/grep for:
- Pattern replacement (e.g., `LR` → `TB` in mermaid)
- Line deletion/insertion
- Header renaming

### LLM Transformation
Use LLM for:
- Content merging
- Structure reorganization
- Context-aware changes

## Workflow

1. Read Issue body or file path
2. Identify transformation type and targets
3. For Issue mode: Post plan comment
4. Process each file:
   - Read file content
   - Apply transformation
   - Commit changes
   - Update progress (Issue mode)
5. Close Issue when complete (Issue mode)

## Directory Organization

### index.md Creation
Create index.md when directory has 5+ files:
- Categorize files by theme/function
- Use tables with Document | Description columns
- List items as plain text (no internal links)

### File Count Thresholds
| Files | Action |
|-------|--------|
| 1-4 | No index.md needed |
| 5-10 | Simple index.md with file list |
| 11+ | Categorized index.md with sections |

## Duplicate Handling

### Detection Criteria
Consolidate when:
- Same topic in multiple files (e.g., `sql-ppl-engine.md` + `sql-ppl-breaking-changes.md`)
- One file is subset of another
- Version-specific content belongs in main feature doc's Change History

### Consolidation Process
1. Identify primary file (more comprehensive)
2. Merge unique content from secondary file
3. Update Change History if applicable
4. Delete secondary file

## File Naming


