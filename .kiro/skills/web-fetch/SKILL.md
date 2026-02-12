---
name: web-fetch
description: Fetch web page content as Markdown using trafilatura. Use when sub-agents or agents need to read web page content but don't have access to the web_fetch tool. Works via shell with a Python one-liner.
---

# Web Fetch (trafilatura)

Fetch web page content as Markdown text. Replacement for `web_fetch` tool in contexts where it's unavailable (e.g., sub-agents).

## Usage

```bash
python -c "import trafilatura; print(trafilatura.extract(trafilatura.fetch_url('URL'), output_format='markdown') or '')"
```

## Notes

- Returns empty string if extraction fails
- Automatically removes navigation, footers, sidebars
- Requires `trafilatura` package (in `requirements.txt`)
