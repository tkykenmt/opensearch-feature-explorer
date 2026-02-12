#!/usr/bin/env python3
"""Fetch latest Kiro docs and save as raw markdown for diff/update review.

Usage: python3 scripts/fetch_docs.py [--diff]

Without --diff: fetches all docs and saves to references/raw/
With --diff:    fetches and shows which files have changed
"""

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = SKILL_DIR / "references" / "raw"
REFS_DIR = SKILL_DIR / "references"

# Map reference files to their source URLs
SOURCES = {}
for ref_file in REFS_DIR.glob("*.md"):
    with open(ref_file) as f:
        for line in f:
            m = re.match(r"^Source:\s*(https?://\S+)", line)
            if m:
                SOURCES[ref_file.stem] = m.group(1)
                break

# Additional URLs not in reference files
EXTRA_URLS = {
    "custom-agents-overview": "https://kiro.dev/docs/cli/custom-agents/",
    "creating": "https://kiro.dev/docs/cli/custom-agents/creating/",
    "context": "https://kiro.dev/docs/cli/chat/context/",
    "prompts": "https://kiro.dev/docs/cli/chat/manage-prompts/",
    "images": "https://kiro.dev/docs/cli/chat/images/",
    "subagents": "https://kiro.dev/docs/cli/chat/subagents/",
}


def fetch_url(url: str) -> str:
    """Fetch URL content using curl and return text."""
    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "30", url],
            capture_output=True, text=True, timeout=60
        )
        return result.stdout if result.returncode == 0 else ""
    except Exception as e:
        print(f"  Error fetching {url}: {e}", file=sys.stderr)
        return ""


def md5(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


def main():
    diff_mode = "--diff" in sys.argv
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    all_urls = {**SOURCES, **EXTRA_URLS}
    changed = []

    for name, url in sorted(all_urls.items()):
        print(f"Fetching {name}: {url}")
        content = fetch_url(url)
        if not content:
            print(f"  ⚠ Empty response, skipping")
            continue

        raw_file = RAW_DIR / f"{name}.html"
        old_hash = md5(raw_file.read_text()) if raw_file.exists() else ""
        new_hash = md5(content)

        if old_hash != new_hash:
            changed.append(name)
            if not diff_mode:
                raw_file.write_text(content)
                print(f"  ✅ Updated ({len(content)} bytes)")
            else:
                print(f"  🔄 Changed")
        else:
            print(f"  ✓ No changes")

    print(f"\n{'='*50}")
    if changed:
        print(f"📝 {len(changed)} source(s) changed: {', '.join(changed)}")
        if diff_mode:
            print("Run without --diff to save updates.")
        else:
            print("Raw files saved to references/raw/")
            print("Review changes and update reference files as needed.")
    else:
        print("✅ All sources up to date.")


if __name__ == "__main__":
    main()
