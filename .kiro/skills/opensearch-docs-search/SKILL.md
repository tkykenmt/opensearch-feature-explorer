---
name: opensearch-docs-search
description: Search OpenSearch documentation, blogs, and community forums. Use when the user asks about OpenSearch features, configuration, APIs, troubleshooting, k-NN, neural search, cluster settings, index mappings, query DSL, or any OpenSearch-related questions. Also use when investigating features and needing to find official documentation or blog posts.
---

# OpenSearch Documentation Search

Search and fetch OpenSearch docs, blogs, and forum content.

## Search

```bash
python scripts/search.py docs "k-NN"
python scripts/search.py blogs "performance" --limit 5
python scripts/search.py forum "cluster health"
```

Options: `-v/--version` (docs/blogs), `-l/--limit`, `-o/--offset` (docs/blogs)

## Fetch Page Content

```bash
python scripts/fetch.py "https://docs.opensearch.org/latest/vector-search/..."
python scripts/fetch.py "https://opensearch.org/blog/unveiling-opensearch-3-0/"
```

Returns page content as Markdown. Requires `trafilatura` package.

**Note**: `opensearch.org/docs/*` redirects to `docs.opensearch.org` via JavaScript. Use the `docs.opensearch.org` URL directly (search results already return the correct URL).

## Investigation Pattern

1. Search docs: `python scripts/search.py docs "{feature}" -v {version}`
2. Search blogs: `python scripts/search.py blogs "{feature}"`
3. Fetch full content: `python scripts/fetch.py "{url}"`
4. Save discovered URLs for References section
