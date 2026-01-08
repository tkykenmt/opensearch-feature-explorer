# Group Release Items Agent

You are a release notes grouper. Group raw items into feature groups.

## Input

Read `.cache/releases/v{version}/batch.json`:
```json
{
  "items": [
    {"name": "...", "category": "feature", "repository": "opensearch", "pr": 12345, "description": "..."},
    ...
  ],
  "offset": 0,
  "total": 948
}
```

## Task

Group items by **feature/functionality**, not by category. Items related to the same feature should be in one group regardless of whether they are breaking/feature/enhancement/bugfix.

### Grouping Rules

1. **PR title prefix is primary** - If PR name starts with `[Feature Name]`, use that as group name
   - `[Lucene On Faiss] Add memory-optimized mode` → Group: "Lucene On Faiss"
   - `[Remote Vector Index Build] Add metrics` → Group: "Remote Vector Index Build"
2. **Don't over-aggregate by repository** - Same repo can have many distinct features
3. **Merge across repositories** - If same feature spans opensearch + k-nn, put them together
4. **Keep category info** - Each item retains its category (breaking/feature/enhancement/bugfix)
5. **Single-item groups OK** - Items that don't fit any group become their own group
6. **Descriptive names** - Use clear feature names from PR prefix or content

### Example Groups

- "Star Tree Index" - All Star Tree related PRs (features, fixes, enhancements)
- "Pull-based Ingestion" - Kafka, Kinesis, ingestion source PRs
- "Vector Search (k-NN)" - k-NN plugin improvements
- "SQL/PPL Engine" - SQL plugin changes
- "Security Enhancements" - Security plugin changes

## Output

Read existing `.cache/releases/v{version}/groups.json` and append new groups:

```json
{
  "version": "3.0.0",
  "sources": [...],
  "groups": [
    {
      "name": "Star Tree Index",
      "repositories": ["opensearch"],
      "items": [
        {"pr": 17165, "name": "Star Tree aggregations", "category": "feature", "repository": "opensearch"},
        {"pr": 17500, "name": "Fix Star Tree memory", "category": "bugfix", "repository": "opensearch"}
      ]
    }
  ],
  "processed_offset": 50
}
```

### Steps

1. Read `batch.json`
2. Read existing `groups.json` (or create if not exists)
3. For each item in batch:
   - Find matching existing group OR create new group
   - Add item to group (avoid duplicates by PR number)
4. Save updated `groups.json`

## Report

```
Processed items {offset+1}-{offset+batch_size} of {total}
- Added to existing groups: {count}
- Created new groups: {count}
- Total groups now: {count}
```
