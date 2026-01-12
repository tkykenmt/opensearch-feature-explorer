#!/usr/bin/env python3
"""Add Related Issue column to PR tables in markdown files."""

import json
import os
import re
import subprocess
from pathlib import Path

CACHE_DIR = Path(".cache/prs")
DOCS_DIR = Path("docs")

ISSUE_PATTERNS = [
    r'(?:resolves|fixes|closes|fix|close|resolve)\s+#(\d+)',
    r'(?:resolves|fixes|closes|fix|close|resolve)\s+https://github\.com/[^/]+/[^/]+/issues/(\d+)',
]

def get_pr_related_issue(owner: str, repo: str, pr_number: int) -> int | None:
    """Fetch PR and extract related issue."""
    cache_file = CACHE_DIR / f"{owner}_{repo}_{pr_number}.json"
    
    if cache_file.exists():
        with open(cache_file) as f:
            data = json.load(f)
            return data.get("related_issue")
    
    try:
        result = subprocess.run(
            ["gh", "api", f"/repos/{owner}/{repo}/pulls/{pr_number}"],
            capture_output=True, text=True, check=True
        )
        data = json.loads(result.stdout)
        
        if data.get("merged"):
            body = data.get("body") or ""
            related_issue = None
            for pattern in ISSUE_PATTERNS:
                match = re.search(pattern, body, re.IGNORECASE)
                if match:
                    related_issue = int(match.group(1))
                    break
            
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            with open(cache_file, "w") as f:
                json.dump({"number": pr_number, "owner": owner, "repo": repo, 
                          "merged": True, "related_issue": related_issue}, f, indent=2)
            return related_issue
    except subprocess.CalledProcessError:
        pass
    return None

def process_file(filepath: Path) -> tuple[bool, int, int]:
    """Process a markdown file and add Related Issue column to PR tables."""
    with open(filepath) as f:
        lines = f.readlines()
    
    modified = False
    prs_processed = 0
    issues_found = 0
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Detect PR table header (must have PR and Description columns, no Related Issue yet)
        if re.match(r'\|.*\|\s*PR\s*\|.*Description\s*\|', line) and "Related Issue" not in line:
            # Add Related Issue column to header
            new_header = line.rstrip() + " Related Issue |\n"
            new_lines.append(new_header)
            i += 1
            
            # Process separator line
            if i < len(lines) and re.match(r'\|[-:\s|]+\|', lines[i]):
                new_sep = lines[i].rstrip() + "---------------|\n"
                new_lines.append(new_sep)
                i += 1
            
            # Process data rows
            while i < len(lines) and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                row = lines[i]
                
                # Extract PR URL
                url_match = re.search(r'\[([^\]]+)\]\((https://github\.com/([^/]+)/([^/]+)/pull/(\d+))\)', row)
                related_cell = " "
                
                if url_match:
                    owner, repo, pr_num = url_match.group(3), url_match.group(4), int(url_match.group(5))
                    prs_processed += 1
                    
                    issue_num = get_pr_related_issue(owner, repo, pr_num)
                    if issue_num:
                        related_cell = f"[#{issue_num}](https://github.com/{owner}/{repo}/issues/{issue_num})"
                        issues_found += 1
                
                new_row = row.rstrip() + f" {related_cell} |\n"
                new_lines.append(new_row)
                modified = True
                i += 1
        else:
            new_lines.append(line)
            i += 1
    
    if modified:
        with open(filepath, "w") as f:
            f.writelines(new_lines)
    
    return modified, prs_processed, issues_found

def main():
    files_modified = 0
    total_prs = 0
    total_issues = 0
    
    md_files = list(DOCS_DIR.rglob("*.md"))
    print(f"Scanning {len(md_files)} files...")
    
    for md_file in md_files:
        modified, prs, issues = process_file(md_file)
        if modified:
            files_modified += 1
            total_prs += prs
            total_issues += issues
            print(f"✓ {md_file}: {prs} PRs, {issues} issues")
    
    print(f"\nDone: {files_modified} files, {total_prs} PRs, {total_issues} issues found")

if __name__ == "__main__":
    main()
