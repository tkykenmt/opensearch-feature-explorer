---
name: opensearch-docs-search
description: Search OpenSearch documentation, blogs, and community forums. Use when the user asks about OpenSearch features, configuration, APIs, troubleshooting, k-NN, neural search, cluster settings, index mappings, query DSL, or any OpenSearch-related questions. Also use when investigating features and needing to find official documentation or blog posts.
---

# OpenSearch Documentation Search

Search OpenSearch docs, blogs, and forum using the bundled script (Python 3.10+, no dependencies).

## Usage

```bash
python scripts/search.py docs "k-NN"
python scripts/search.py blogs "performance" --limit 5
python scripts/search.py forum "cluster health"
```

Options: `-v/--version` (docs/blogs), `-l/--limit`, `-o/--offset` (docs/blogs)

## Investigation Pattern

When investigating a feature:
1. Search docs first: `python scripts/search.py docs "{feature}" -v {version}`
2. Search blogs separately: `python scripts/search.py blogs "{feature}"`
3. Fetch full content of relevant results with `web_fetch`
4. Save discovered URLs for References section
