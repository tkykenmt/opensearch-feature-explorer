#!/usr/bin/env python3
"""Fetch web page content as Markdown using trafilatura."""

import sys
import trafilatura

url = sys.argv[1] if len(sys.argv) > 1 else None
if not url:
    print("Usage: python fetch.py <URL>", file=sys.stderr)
    sys.exit(1)

html = trafilatura.fetch_url(url)
print(trafilatura.extract(html, output_format="markdown") or "" if html else "")
