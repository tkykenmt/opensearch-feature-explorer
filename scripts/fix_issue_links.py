#!/usr/bin/env python3
"""Fix GitHub Issue body links to prevent cross-repository 'referenced on' noise.

Converts bare #NUMBER, shorthand repo#NUMBER, and [text](URL) patterns
to backtick-quoted URL format: `https://github.com/opensearch-project/REPO/pull/NUMBER`

Usage:
    # Dry run (preview changes)
    python scripts/fix_issue_links.py

    # Fix a single issue (dry run)
    python scripts/fix_issue_links.py --issue 140

    # Fix a single issue (apply)
    python scripts/fix_issue_links.py --issue 140 --apply

    # Fix all issues (dry run)
    python scripts/fix_issue_links.py --all

    # Fix all issues (apply)
    python scripts/fix_issue_links.py --all --apply

    # Fix comments too
    python scripts/fix_issue_links.py --issue 140 --apply --comments
"""
import argparse
import json
import re
import subprocess
import sys

# Short name -> GitHub repo name mapping
REPO_MAP = {
    "opensearch": "OpenSearch",
    "dashboards": "OpenSearch-Dashboards",
    "opensearch-dashboards": "OpenSearch-Dashboards",
    "k-nn": "k-NN",
    "ml-commons": "ml-commons",
    "neural-search": "neural-search",
    "security": "security",
    "alerting": "alerting",
    "anomaly-detection": "anomaly-detection",
    "asynchronous-search": "asynchronous-search",
    "cross-cluster-replication": "cross-cluster-replication",
    "custom": "custom-codecs",
    "flow": "flow-framework",
    "geospatial": "geospatial",
    "index-management": "index-management",
    "job": "job-scheduler",
    "notifications": "notifications",
    "observability": "observability",
    "performance": "performance-analyzer",
    "query": "query-insights",
    "reporting": "reporting",
    "search": "search-processor",
    "skills": "skills",
    "sql": "sql",
    "common": "common-utils",
    "remote": "remote-vector-index-builder",
    "system": "OpenSearch",
    "user": "user-behavior-insights",
    "ml": "ml-commons",
    "k": "k-NN",
    "learning": "ml-commons",
}

OWNER = "opensearch-project"


def gh(*args):
    result = subprocess.run(["gh"] + list(args), capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  gh error: {result.stderr.strip()}", file=sys.stderr)
        return None
    return result.stdout.strip()


def get_repo_info():
    """Get owner/repo for this repository."""
    out = gh("repo", "view", "--json", "owner,name")
    if not out:
        return "tkykenmt", "opensearch-feature-explorer"
    data = json.loads(out)
    return data["owner"]["login"], data["name"]


def github_url(repo_short, pr_num):
    """Convert short repo name + PR number to full GitHub URL."""
    repo_name = REPO_MAP.get(repo_short, repo_short)
    return f"https://github.com/{OWNER}/{repo_name}/pull/{pr_num}"


def fix_body(body, issue_number=None):
    """Fix link formats in issue body. Returns (new_body, changes)."""
    changes = []
    new_body = body

    # Pattern 1: Table rows with | #NUMBER | ... | repository |
    # e.g. | #3412 | Title | breaking | dashboards |
    def fix_table_row(m):
        full = m.group(0)
        pr_num = m.group(1)
        repo_short = m.group(2).strip()
        url = github_url(repo_short, pr_num)
        replacement = full.replace(f"#{pr_num}", f"`{url}`")
        if replacement != full:
            changes.append(f"  table: #{pr_num} ({repo_short}) -> `{url}`")
        return replacement

    new_body = re.sub(
        r'\| #(\d+) \|.+\| ([\w-]+) \|$',
        fix_table_row,
        new_body,
        flags=re.MULTILINE,
    )

    # Pattern 2: Shorthand repo#NUMBER in text (e.g., "PRs: custom#228, dashboards#16366")
    def fix_shorthand(m):
        repo_short = m.group(1)
        pr_num = m.group(2)
        if repo_short.lower() in REPO_MAP:
            url = github_url(repo_short.lower(), pr_num)
            changes.append(f"  shorthand: {repo_short}#{pr_num} -> `{url}`")
            return f"`{url}`"
        return m.group(0)

    new_body = re.sub(r'(\w[\w-]*)#(\d+)', fix_shorthand, new_body)

    # Pattern 3: Markdown links [text](#NUMBER) or [#NUMBER](URL) or [`URL`](URL)
    def fix_md_link(m):
        text = m.group(1)
        url = m.group(2)
        if "github.com/opensearch-project/" in url:
            changes.append(f"  md-link: [{text}]({url}) -> `{url}`")
            return f"`{url}`"
        return m.group(0)

    new_body = re.sub(r'\[([^\]]*)\]\((https://github\.com/opensearch-project/[^)]+)\)', fix_md_link, new_body)

    # Pattern 4: Remaining bare #NUMBER that reference external PRs/issues
    # Skip self-references (Parent: #122 etc.) - these reference our own repo
    # We can only fix these if we can determine the repo from context
    # For now, leave them as-is since we can't determine the target repo

    return new_body, changes


def get_all_issues(owner, repo):
    """Get all issues (not PRs) with their numbers."""
    out = gh("issue", "list", "-R", f"{owner}/{repo}",
             "--state", "all", "--limit", "5000",
             "--json", "number,title,state")
    if not out:
        return []
    return json.loads(out)


def process_issue(owner, repo, number, apply=False, fix_comments=False):
    """Process a single issue."""
    out = gh("issue", "view", str(number), "-R", f"{owner}/{repo}",
             "--json", "number,title,body,state,comments")
    if not out:
        return False

    data = json.loads(out)
    body = data["body"]
    title = data["title"]

    print(f"\n{'='*60}")
    print(f"Issue #{number}: {title} ({data['state']})")
    print(f"{'='*60}")

    new_body, changes = fix_body(body, number)

    if not changes:
        print("  No changes needed in body.")
    else:
        print(f"  Body changes ({len(changes)}):")
        for c in changes:
            print(f"    {c}")
        if apply:
            gh("issue", "edit", str(number), "-R", f"{owner}/{repo}",
               "--body", new_body)
            print("  ✅ Body updated.")

    # Fix comments
    if fix_comments and data.get("comments"):
        for i, comment in enumerate(data["comments"]):
            cbody = comment.get("body", "")
            new_cbody, cchanges = fix_body(cbody)
            if cchanges:
                print(f"  Comment #{i} changes ({len(cchanges)}):")
                for c in cchanges:
                    print(f"    {c}")
                if apply:
                    comment_url = comment.get("url", "")
                    if comment_url:
                        cid_match = re.search(r'issuecomment-(\d+)', comment_url)
                        if cid_match:
                            cid = cid_match.group(1)
                            gh("api", f"repos/{owner}/{repo}/issues/comments/{cid}",
                               "-X", "PATCH", "-f", f"body={new_cbody}")
                            print(f"  ✅ Comment #{i} updated.")

    return bool(changes)


def main():
    parser = argparse.ArgumentParser(description="Fix issue link formats")
    parser.add_argument("--issue", type=int, help="Fix a single issue")
    parser.add_argument("--all", action="store_true", help="Fix all issues")
    parser.add_argument("--apply", action="store_true", help="Apply changes (default: dry run)")
    parser.add_argument("--comments", action="store_true", help="Also fix comments")
    args = parser.parse_args()

    if not args.issue and not args.all:
        parser.print_help()
        return

    owner, repo = get_repo_info()
    print(f"Repository: {owner}/{repo}")
    print(f"Mode: {'APPLY' if args.apply else 'DRY RUN'}")

    if args.issue:
        process_issue(owner, repo, args.issue, args.apply, args.comments)
    elif args.all:
        issues = get_all_issues(owner, repo)
        print(f"Total issues: {len(issues)}")
        changed = 0
        for issue in issues:
            if process_issue(owner, repo, issue["number"], args.apply, args.comments):
                changed += 1
        print(f"\n{'='*60}")
        print(f"Summary: {changed}/{len(issues)} issues need changes")


if __name__ == "__main__":
    main()
